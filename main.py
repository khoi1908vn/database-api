"""
The server exposes four endpoints:

/whitelist/user/check/{user_id} - GET endpoint that takes a user ID and returns a JSON object with a boolean flag indicating if the user is whitelisted.

/whitelist/user/get - GET endpoint that returns a JSON object with a list of all whitelisted beta users.

/whitelist/server/check/{guild_id} - GET endpoint that takes a server ID and returns a JSON object with a boolean flag indicating if the server is whitelisted.

/whitelist/server/get - GET endpoint that returns a JSON object with a list of all whitelisted servers.

The server also provides two PUT endpoints to modify the whitelist data:

/whitelist/user/modify/{user_id} - PUT endpoint that takes a user ID and a boolean status flag indicating if the user should be added or removed from the whitelist.

/whitelist/server/modify/{guild_id} - PUT endpoint that takes a server ID and a boolean status flag indicating if the server should be added or removed from the whitelist.

All endpoints require an authorization header with an API key to ensure that only authorized users can access the server. If the authorization header is not present or contains an incorrect API key, the server returns a 401 Unauthorized error.
"""

from fastapi import FastAPI, HTTPException, Header
from typing import Optional
import os
import json

app = FastAPI()
API_KEY = os.environ.get("allowed_key", "examplekey_")
def check_for_files():
    if not os.path.exists("whitelist.json"):
        with open("whitelist.json", "w+") as f:
            data = {"whitelisted_beta_users": [], "whitelisted_servers": []}
            json.dump(data, f)

def get_whitelist():
    check_for_files()
    with open("whitelist.json", "r") as f:
        data = json.load(f)
    return data

def modify_whitelist(newdata: dict):
    check_for_files()
    with open("whitelist.json", "w") as f:
        json.dump(newdata, f)

@app.get("/")
async def root():
    return {"root": "This is the root of the API."}

@app.get("/whitelist/user/check/{user_id}")
async def check_wl_user(user_id: int, authorization: Optional[str] = Header(None)):
    if authorization != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    whitelist = get_whitelist()
    success = True
    try:
        whitelisted = user_id in whitelist["whitelisted_beta_users"]
        response = {"success": success, "whitelisted": whitelisted}
    except Exception as e:
        success = False
        response = {"success": success}
    return response

@app.get("/whitelist/user/get")
async def get_wl_user(authorization: Optional[str] = Header(None)):
    if authorization != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    whitelist = get_whitelist()
    return {"success": True, "whitelisted_beta_users": whitelist["whitelisted_beta_users"]}

@app.get("/whitelist/server/check/{guild_id}")
async def get_whitelisted_server(guild_id: int, authorization: Optional[str] = Header(None)):
    if authorization != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    whitelist = get_whitelist()
    success = True
    try:
        whitelisted = guild_id in whitelist["whitelisted_servers"]
        response = {"success": success, "whitelisted": whitelisted}
    except Exception as e:
        success = False
        response = {"success": success}
    return response

@app.get("/whitelist/server/get")
async def get_wl_server(authorization: Optional[str] = Header(None)):
    if authorization != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    whitelist = get_whitelist()
    return {"success": True, "whitelisted_beta_users": whitelist["whitelisted_servers"]}

@app.put("/whitelist/user/modify/{user_id}")
async def modify_whitelisted_user(user_id: int, status: bool, authorization: Optional[str] = Header(None)):
    if authorization != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    whitelist = get_whitelist()
    success = True
    try:
        if status:
            if user_id not in whitelist["whitelisted_beta_users"]:
                whitelist["whitelisted_beta_users"].append(user_id)
        else:
            if user_id in whitelist["whitelisted_beta_users"]:
                whitelist["whitelisted_beta_users"].remove(user_id)
        modify_whitelist(whitelist)
    except Exception as e:
        success = False
    return {"success": success}

@app.put("/whitelist/server/modify/{guild_id}")
async def modify_whitelisted_server(guild_id: int, status: bool, authorization: Optional[str] = Header(None)):
    if authorization != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    whitelist = get_whitelist()
    success = True
    try:
        if status:
            if guild_id not in whitelist["whitelisted_servers"]:
                whitelist["whitelisted_servers"].append(guild_id)
        else:
            if guild_id in whitelist["whitelisted_servers"]:
                whitelist["whitelisted_servers"].remove(guild_id)
        modify_whitelist(whitelist)
    except Exception as e:
        success = False
    return {"success": success}

