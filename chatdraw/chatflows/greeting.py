from enum import Enum
from typing import Any, Dict, List
from chatdraw.chat_system import ChatMessage, ChatResponse, ProjectHandler


class GreetingProjectStates(Enum):
    START = "start"
    NAME_COLLECT = "namecollect"
    CHOOSE_PROJECT = "chooseproject"


class GreetingProject(ProjectHandler):
    """Handles initial conversation flow"""
    
    def __init__(self, available_projects: List[str]):
        self.available_projects = available_projects
        
    def get_dialogue(self) -> Dict[str,Any]:
        return {
            "start":self._start,
            "namecollect":self._name_collect,
            "chooseproject":self._choose_project,
        }
    
    def _start(self, message:ChatMessage) -> ChatResponse:
        return ChatResponse(response="",next_context="")

    def _name_collect(self, message:ChatMessage) -> ChatResponse:
        return ChatResponse(response="",next_context="")


    def _choose_project(self, message:ChatMessage) -> ChatResponse:
        return ChatResponse(response="",next_context="")


    