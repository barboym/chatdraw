from typing import Dict
from chatdraw.chat_system import ChatHandler, ChatMessage, ChatResponse, ProjectHandler


class GreetingProject(ProjectHandler):
    """Handles initial conversation flow"""
    
    def __init__(self, available_projects: Dict[str,ProjectHandler]):
        self.available_projects = available_projects
        
    def handle_message(self,message: ChatMessage) -> ChatResponse:
        return {
            "start":self._start,
            "chooseproject":self._choose_project,
        }[message.context](message.message)
    
    def _start(self, message:str) -> ChatResponse:
        return ChatResponse(
            response=f"Hey there! Welcome to my chat. What would you like to do? Options are: {','.join(self.available_projects)}",
            next_context="chooseproject")

    def _choose_project(self, message:str) -> ChatResponse:
        return ChatResponse(response=f"Ok! Let do {message}",next_context="start." + message + "_start")


if __name__=="__main__":
    ch = ChatHandler()
    ch.register_project("greeting",GreetingProject(available_projects={"a":GreetingProject({})}))
    print(ch.process_message(ChatMessage(message="Hi",context="greeting_start")))
    print(ch.process_message(ChatMessage(message="a",context="greeting_chooseproject")))
    