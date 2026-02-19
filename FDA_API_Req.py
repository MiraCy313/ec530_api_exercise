# Requirement
#   requests --- used for url api requests
#   FastAPPI --- used for defined local api services
#   uvicorn  --- used for enabling localhast requests
#   random   --- used for random numbers

import requests
from fastapi import FastAPI
import uvicorn
import random

#test
url = "https://api.fda.gov/drug/event.json?limit=1"

#response = requests.get(url)
#print(response.json())

# test fastAPI
app = FastAPI()

users = {}


@app.get("/")
def hello():
    return {"msg": "Test for a new API!"}

@app.get("/user/create")
def create_user(username: str):
    for user_info in users.values():
        if user_info["username"] == username:
            return {409}
    
    user_id = random.randint(1000, 9999)
    users[user_id] = {
        "username": username,
        "notes": []
    }
    return {"msg": "new user created!", "username": username, "user_id": user_id}

@app.get("/admin/reset")
def reset_all(pswd: str):
    if pswd == "020219":
        users = {}
        return {"msg": "All information is cleared!!!"}

@app.get("/admin/listall")
def list_all(pswd: str):
    if pswd == "020219":
        result = []
        for ids, infos in users.items():
            result.append({
                "user_id": ids,
                "username": infos["username"]
            })
        return {
            "total": len(users),
            "result": results
        }

@app.get("/user/add_note")
def add_note(username: str, note: str):
    for user_id, user_info in users.items():
        if user_info["username"] == username:
            users[user_id]["notes"].append(note)
            return {"msg": "Notes added!"}

@app.get("/user/read_note")
def read_note(username:str):
    for user_id, user_info in users.items():
        if user_info["username"] == username:
            return {
                "username": username,
                "notes": users[user_id]["notes"]
            }

@app.get("/user/find_name")
def find_user(user_id: int):
    if user_id in users:
        return {
            "user_id": user_id,
            "username": users[user_id]["username"]
        } 

@app.get("/user/get_disclaimer")
def get_disc(username: str):
    for user_id, user_info in users.items():
        if user_info["username"] == username:
            url = "https://api.fda.gov/drug/event.json?limit=1"
            response = requests.get(url)
            data = response.json()
            disclaimer = data["meta"]["disclaimer"]
            users[user_id]["notes"].append(disclaimer)
            return {"msg": "Disclaimer already stored as a note!"}

