from fastapi import FastAPI, HTTPException, Header
from typing import Optional
import os
import json

app = FastAPI()
API_KEY = os.environ.get("allowed_key", "examplekey_")
def check_for_files():
    if not os.path.exists("whitelist.json"):
        with open("whitelist.json", "w") as f:
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

@app.get("/whitelist/user/get/{user_id}")
async def get_whitelisted_user(user_id: int, authorization: Optional[str] = Header(None)):
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

@app.get("/whitelist/server/get/{guild_id}")
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

