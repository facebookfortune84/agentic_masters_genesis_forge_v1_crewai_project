#!/usr/bin/env python
from reactive_agent_base import ReactiveAgent
import psutil, os

class DiagnosticsAgent(ReactiveAgent):
    def respond(self,text):
        if "status" in text or "health" in text:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            return f"System health → CPU: {cpu}% | Memory: {mem}%"
        return "Specify 'status' or 'health' check."

if __name__=="__main__":
    DiagnosticsAgent("diagnostics_forger")
    import time; 
    while True: time.sleep(30)
