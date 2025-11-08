#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Forge Communication Hub v3
──────────────────────────────────────────────
Bi-directional messaging + agent registration
──────────────────────────────────────────────
"""
import os, json, threading, time
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BUS_PATH = os.path.join(ROOT, "forge_comm_bus.json")
LOCK = threading.Lock()

def _init_bus():
    if not os.path.exists(BUS_PATH):
        json.dump({"agents": {}, "messages": []}, open(BUS_PATH, "w"))
_init_bus()

def _load_bus(): return json.load(open(BUS_PATH))
def _save_bus(data): 
    with LOCK: json.dump(data, open(BUS_PATH, "w"), indent=2)

def register_agent(name):
    data = _load_bus()
    data["agents"][name] = {"last_seen": datetime.now().isoformat()}
    _save_bus(data)

def post(sender, recipient, text, priority="normal"):
    data = _load_bus()
    msg = {
        "time": datetime.now().isoformat(),
        "from": sender, "to": recipient,
        "text": text, "priority": priority,
        "status": "queued"
    }
    data["messages"].append(msg)
    _save_bus(data)

def fetch(name):
    data = _load_bus()
    inbox = [m for m in data["messages"] if m["to"].lower() == name.lower() and m["status"]=="queued"]
    for m in inbox: m["status"]="delivered"
    _save_bus(data)
    return inbox

def reply(name, msg, text):
    data=_load_bus()
    for m in data["messages"]:
        if m["time"]==msg["time"]:
            m["status"]="replied"
            m["response"]={"from":name,"text":text,"time":datetime.now().isoformat()}
    _save_bus(data)

def listen(name, handler, interval=4):
    def loop():
        register_agent(name)
        print(f"[{name}] Listening for messages…")
        while True:
            time.sleep(interval)
            for msg in fetch(name):
                handler(msg)
    threading.Thread(target=loop,daemon=True).start()