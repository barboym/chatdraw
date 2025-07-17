from typing import Dict, List
from abc import ABC, abstractmethod
from pydantic import BaseModel


class AtomicMessage(BaseModel):
    content: str
    mtype: str # either text or image


class ChatMessage(BaseModel):
    """Stateless message containing all context needed for processing"""
    message: str | AtomicMessage
    context: str  # All state lives here in the form of project1_state1.project2_state1

    def __init__(self, **kwargs):
        if isinstance(kwargs["message"],str):
            kwargs["message"] = AtomicMessage(content=kwargs["message"],mtype="text")
        super().__init__(**kwargs)

assert ChatMessage(message="a",context="a").message.content=="a"

class ChatResponse(BaseModel):
    """Response from the chat system"""
    response: str | AtomicMessage | List[AtomicMessage|str]
    next_context: str

    def __init__(self, **kwargs):
        if isinstance(kwargs["response"],AtomicMessage):
            kwargs["response"] = [kwargs["response"]]
        elif isinstance(kwargs["response"],str):
            kwargs["response"] = [AtomicMessage(content=kwargs["response"],mtype="text")]
        elif isinstance(kwargs["response"],list):
            for i in range(len(kwargs["response"])):
                if isinstance(kwargs["response"][i],str):                    
                    kwargs["response"][i] = AtomicMessage(content=kwargs["response"][i],mtype="text")
        super().__init__(**kwargs)
        
assert isinstance(ChatResponse(response="",next_context="").response,list)


class ProjectHandler(ABC):
    """Base class for all handlers including greeting"""
    
    @abstractmethod
    def handle_message(self, message: ChatMessage) -> ChatResponse:
        """Handle message processing"""
        pass


class DefaultProjectHandler(ProjectHandler):
    """Base class for all handlers including greeting"""
    
    def handle_message(self, message: ChatMessage) -> ChatResponse:
        """Handle message processing"""
        return ChatResponse(
            response="I can tell you want to talk. Say something.",
            next_context=message.context,
        )
    


class ChatHandler:
    """Simple dispatcher - just routes to the current project"""
    def __init__(self):
        self.projects: Dict[str, ProjectHandler] = {}

    def register_project(self, project_name: str, handler: ProjectHandler):
        """Register any project handler"""
        self.projects[project_name] = handler
    
    def process_message(self, message: ChatMessage) -> ChatResponse:
        """Route to current project handler"""
        #TODO: change the string scheme with dict scheme
        context_list = message.context.split(".") 
        current_project, current_state = context_list[-1].split("_")

        project = self.projects[current_project]
        project_response = project.handle_message(
            ChatMessage(
                message=message.message,
                context=current_state,
            )
        )

        # in case project ends the context is empty 
        projects_next_context = ""
        # if a project continues the response is non empty
        if project_response.next_context!="":
            projects_next_context = current_project + "_" + project_response.next_context
        # if the project dives into another project, we process a different message
        if "." in projects_next_context:
            next_respose = self.process_message(
                ChatMessage(
                    message="",
                    context=".".join(context_list[:-1] + [projects_next_context]),
                )
            )
            return ChatResponse(
                response=project_response.response + next_respose.response,
                next_context=next_respose.next_context,
            )
        return ChatResponse(
            response=project_response.response,
            next_context=".".join(context_list[:-1] + [projects_next_context]),
        )
     
     
if __name__=="__main__":
    ch = ChatHandler()
    ch.register_project("default",DefaultProjectHandler())
    print(ch.process_message(ChatMessage(message="hey there",context="default_start")))