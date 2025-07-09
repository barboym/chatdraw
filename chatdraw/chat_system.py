from typing import Dict, Any
from abc import ABC, abstractmethod
from pydantic import BaseModel

class ChatMessage(BaseModel):
    """Stateless message containing all context needed for processing"""
    message: str
    context: str  # All state lives here in the form of project1_state1.project2_state1
    
class ChatResponse(BaseModel):
    """Response from the chat system"""
    response: str
    next_context: str


class ProjectHandler(ABC):
    """Base class for all handlers including greeting"""
    
    @abstractmethod
    def _get_dialogue(self) -> Dict[str,Any]:
        pass 

    def handle_message(self, message: ChatMessage) -> ChatResponse:
        """Handle message processing"""
        context = message.context
        message_txt = message.message.strip()
        
        next_context,response = self._get_dialogue()[context](message_txt)
        return ChatResponse(
            response=response,
            next_context=next_context
        )


class DefaultProjectHandler(ProjectHandler):
    """Base class for all handlers including greeting"""
    
    def _get_dialogue(self) -> Dict[str,Any]:
        """Handle message processing"""
        return {
            "start":lambda message_txt:ChatResponse(
                response="I can tell you want to talk. Say something.",
                next_context=message_txt,
            )
        }


class ChatHandler:
    """Simple dispatcher - just routes to the current project"""
    
    def __init__(self):
        self.projects: Dict[str, ProjectHandler] = {
            "default":DefaultProjectHandler()
        }
    
    def register_project(self, project_name: str, handler: ProjectHandler):
        """Register any project handler"""
        self.projects[project_name] = handler
    
    def process_message(self, message: ChatMessage) -> ChatResponse:
        """Route to current project handler"""
        context_list = message.context.split(".")
        current_project, current_state = context_list[-1].split("_")

        project = self.projects.get(current_project,self.projects["default"])
        project_response = project.handle_message(
            ChatMessage(
                message=message.message,
                context=current_state,
            )
        )

        projects_next_context = ""
        if project_response.next_context!="":
            projects_next_context = current_project + "_" + project_response.next_context
        return ChatResponse(
            response=project_response.response,
            next_context=".".join(context_list + [projects_next_context]),
        )
     

if __name__=="__main__":
    print(ChatHandler().process_message(ChatMessage(message="hey there",context="start")))