from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
import uvicorn

app = FastAPI()

# Set up the templates directory
templates = Jinja2Templates(directory="templates")

# MongoDB setup
client = MongoClient('mongodb://root:origez12@localhost:27017/')

# Access the admin database to verify the connection
try:
    db = client.admin
    server_status = db.command("serverStatus")
    print("MongoDB server status:", server_status)
except Exception as e:
    print("Unable to connect to the MongoDB server:", e)
    raise HTTPException(status_code=500, detail="Unable to connect to the MongoDB server")

# Example: Accessing a specific database and collection
mydb = client["mydatabase"]
mycollection = mydb["mycollection"]

@app.get("/", response_class=HTMLResponse)
async def get_input(request: Request):
    # Fetch all player documents from the collection
    players = list(mycollection.find({}, {"_id": 0, "name": 1}))
    return templates.TemplateResponse("home.html", {"request": request, "players": players})

@app.get("/input", response_class=HTMLResponse)
async def get_input(request: Request):
    return templates.TemplateResponse("testinput.html", {"request": request})

@app.post("/input", response_class=HTMLResponse)
async def add_player(request: Request, name: str = Form(...)):
    # Insert the player name into the MongoDB collection
    try:
        result = mycollection.insert_one({"name": name})
        print(f"Inserted document id: {result.inserted_id}")
        message = f"Player {name} added successfully!"
    except Exception as e:
        print(f"Failed to insert document: {e}")
        raise HTTPException(status_code=500, detail="Failed to add player to the database")

    # Return the input.html template with a success message
    return templates.TemplateResponse("testinput.html", {"request": request, "message": message})
@app.post("/delete_alice", response_class=HTMLResponse)
async def delete_alice(request: Request):
    # Delete all documents with the name "Alice"
    try:
        result = mycollection.delete_many({"name": "Alice"})
        print(f"Deleted {result.deleted_count} documents")
        message = f"Deleted {result.deleted_count} 'Alice' entries successfully!"
    except Exception as e:
        print(f"Failed to delete documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete 'Alice' entries from the database")
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
