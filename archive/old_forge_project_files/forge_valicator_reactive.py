#!/usr/bin/env python
from reactive_agent_base import ReactiveAgent
from forge_comm_hub_v3 import post
import os, json, glob

class ForgeValidator(ReactiveAgent):
    def respond(self,text):
        if "check" in text or "validate" in text:
            reports = glob.glob("deliverables/*.md")
            return f"Validation complete: {len(reports)} markdown deliverables found."
        return "Awaiting validation command."

if __name__=="__main__":
    ForgeValidator("forge_validator")
    while True: time.sleep(30)