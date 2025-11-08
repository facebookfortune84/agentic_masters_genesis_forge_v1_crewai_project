#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
💎 Forge Communication Hub
─────────────────────────────────────────────
Acts as a shared message bus for all Forge agents.
Messages are JSON-logged and retrieved by listening agents.
─────────────────────────────────────────────
"""

import os, json, time
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BUS_FILE = os.path.join(ROOT, "forge_comm_bus.json")

def post_message(agent, recipient, message):
    os.makedirs(os.path.dirname(BUS_FILE), exist_ok=True)
    if not os.path.exists(BUS_FILE):
        json.dump([], open(BUS_FILE, "w"))

    data = json.load(open(BUS_FILE))
    entry = {
        "timestamp": datetime.now().isoformat(),
        "from": agent,
        "to": recipient,
        "message": message,
        "status": "pending"
    }
    data.append(entry)
    json.dump(data, open(BUS_FILE, "w"), indent=2)

def fetch_messages(agent):
    """Retrieve new messages for a given agent."""
    if not os.path.exists(BUS_FILE):
        return []
    data = json.load(open(BUS_FILE))
    new = [msg for msg in data if msg["to"].lower() == agent.lower() and msg["status"] == "pending"]
    for msg in new:
        msg["status"] = "delivered"
    json.dump(data, open(BUS_FILE, "w"), indent=2)
    return new

def reply_to_message(original, response):
    """Attach a response to a message."""
    data = json.load(open(BUS_FILE))
    for msg in data:
        if msg["timestamp"] == original["timestamp"]:
            msg["status"] = "replied"
            msg["response"] = response
    json.dump(data, open(BUS_FILE, "w"), indent=2)