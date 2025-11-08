import os, time
from colorama import Fore, Style, init
from forge_comm_hub_v3 import post, reply, listen

init(autoreset=True)

class ReactiveAgent:
    def __init__(self, name):
        self.name = name
        listen(name, self.on_message)

    def log(self,msg,color=Fore.CYAN):
        print(color+f"[{self.name}] {msg}"+Style.RESET_ALL)

    def on_message(self, msg):
        self.log(f"📩 {msg['from']} says: {msg['text']}")
        response = self.respond(msg['text'])
        reply(self.name,msg,response)
        self.log(f"💬 Replied: {response}",Fore.GREEN)

    def respond(self,text): raise NotImplementedError
