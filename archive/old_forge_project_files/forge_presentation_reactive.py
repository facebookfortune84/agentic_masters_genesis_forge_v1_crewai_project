#!/usr/bin/env python
from reactive_agent_base import ReactiveAgent
from forge_comm_hub_v3 import post
import subprocess

class ForgePresenter(ReactiveAgent):
    def respond(self,text):
        if "present" in text or "launch" in text:
            subprocess.Popen(["python","forge_project/forge_presentation_neural.py"])
            return "Presentation launched."
        return "Ready for next cue."

if __name__=="__main__":
    ForgePresenter("forge_presentation_neural")
    import time; 
    while True: time.sleep(30)
