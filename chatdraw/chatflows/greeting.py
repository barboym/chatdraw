from typing import List
from chatdraw.chatflows.chat_system import AtomicMessage, ChatHandler, ChatMessage, ChatResponse, ProjectHandler

class GreetingProject(ProjectHandler):
    """Handles initial conversation flow"""
    
    def __init__(self, available_projects: List[str]):
        self.available_projects = available_projects
        
    def handle_message(self,message: ChatMessage) -> ChatResponse:
        return {
            "start":self._start,
            "chooseproject":self._choose_project,
        }[message.context](message.message.content)
    
    def _start(self, message:str) -> ChatResponse:
        return ChatResponse(
            response=f"Hey there! Welcome to my chat. What would you like to do? Options are: {','.join(self.available_projects)}",
            next_context="chooseproject")

    def _choose_project(self, message:str) -> ChatResponse:
        return ChatResponse(response=f"Ok! Let do {message}",next_context="start." + message + "_start")


if __name__=="__main__":
    ch = ChatHandler()
    ch.register_project("greeting",GreetingProject(available_projects=["a"]))
    ch.register_project("a",GreetingProject(available_projects=[]))
    print(ch.process_message(ChatMessage(message='5',context="greeting_start")))
    print(ch.process_message(ChatMessage(message="a",context="greeting_chooseproject")))
    