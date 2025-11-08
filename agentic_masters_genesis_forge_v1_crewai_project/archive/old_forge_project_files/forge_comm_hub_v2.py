#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Forge Communication Hub v2
──────────────────────────────────────────────
Bidirectional agent messaging system.
Adds live event loop and real-time delivery callbacks.
──────────────────────────────────────────────
"""

import os, json, time, threading
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BUS_FILE = os.path.join(ROOT, "forge_comm_bus.json")
LOCK = threading.Lock()

def _load_bus():
    if not os.path.exists(BUS_FILE):
        json.dump([], open(BUS_FILE, "w"))
    return json.load(open(BUS_FILE))

def _save_bus(data):
    with LOCK:
        json.dump(data, open(BUS_FILE, "w"), indent=2)

def post_message(sender, recipient, message, priority="normal"):
    data = _load_bus()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "from": sender,
        "to": recipient,
        "message": message,
        "priority": priority,
        "status": "queued"
    }
    data.append(entry)
    _save_bus(data)
    return entry

def fetch_messages(agent):
    """Fetch pending messages for this agent."""
    data = _load_bus()
    new = [m for m in data if m["to"].lower() == agent.lower() and m["status"] == "queued"]
    for m in new:
        m["status"] = "delivered"
    _save_bus(data)
    return new

def reply_message(agent, original, response):
    """Mark message replied and attach response."""
    data = _load_bus()
    for m in data:
        if m["timestamp"] == original["timestamp"]:
            m["status"] = "replied"
            m["response"] = {"from": agent, "text": response, "timestamp": datetime.now().isoformat()}
    _save_bus(data)

def start_listener(agent_name, callback, poll_interval=5):
    """Continuously poll for new messages for this agent."""
    def loop():
        print(f"[{agent_name}] Listening for messages...")
        while True:
            time.sleep(poll_interval)
            messages = fetch_messages(agent_name)
            for m in messages:
                callback(m)
    t = threading.Thread(target=loop, daemon=True)
    t.start()