from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pymongo import MongoClient, errors
import uvicorn

app = FastAPI()

# Set up the templates directory
templates = Jinja2Templates(directory="templates")

# MongoDB setup
client = MongoClient('mongodb://root:origez12@mongodb:27017/', serverSelectionTimeoutMS=5000)

# Access the admin database to verify the connection
try:
    db = client.admin
    server_status = db.command("serverStatus")
    print("MongoDB server status:", server_status)
except errors.ServerSelectionTimeoutError as err:
    print("Unable to connect to the MongoDB server:", err)
    raise HTTPException(status_code=500, detail="Unable to connect to the MongoDB server")

# Example: Accessing a specific database and collection
mydb = client["mydatabase"]
mycollection = mydb["mycollection"]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Fetch all player documents from the collection
    players = list(mycollection.find({}, {"_id": 0, "name": 1, "wins": 1}))
    return templates.TemplateResponse("player_management.html", {"request": request, "players": players})

@app.post("/add_player", response_class=HTMLResponse)
async def add_player(request: Request, name: str = Form(...), wins: int = Form(...)):
    # Insert the player name and wins into the MongoDB collection
    try:
        result = mycollection.insert_one({"name": name, "wins": wins})
        print(f"Inserted document id: {result.inserted_id}")
        message = f"Player {name} with {wins} wins added successfully!"
    except Exception as e:
        print(f"Failed to insert document: {e}")
        raise HTTPException(status_code=500, detail="Failed to add player to the database")

    # Fetch all player documents from the collection
    players = list(mycollection.find({}, {"_id": 0, "name": 1, "wins": 1}))
    return templates.TemplateResponse("player_management.html", {"request": request, "message": message, "players": players})

@app.post("/delete_player", response_class=HTMLResponse)
async def delete_player(request: Request, name: str = Form(...)):
    # Delete the specific player document with the given name
    try:
        result = mycollection.delete_one({"name": name})
        if result.deleted_count == 1:
            delete_message = f"Player {name} deleted successfully!"
        else:
            delete_message = f"No player named {name} found."
        print(delete_message)
    except Exception as e:
        print(f"Failed to delete document: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete player from the database")

    # Fetch all player documents from the collection
    players = list(mycollection.find({}, {"_id": 0, "name": 1, "wins": 1}))
    return templates.TemplateResponse("player_management.html", {"request": request, "delete_message": delete_message, "players": players})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
