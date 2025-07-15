from typing import Dict
from typing import Dict, Any, Optional, Union, List
from abc import ABC, abstractmethod
from pydantic import BaseModel
from pydantic import BaseModel, Field
import json
import unittest
from unittest.mock import MagicMock

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
    """Dispatcher that routes messages to appropriate project handlers"""
    def __init__(self):
        self.projects: Dict[str, ProjectHandler] = {}
    
        # Register default handler
        self.register_project("default", DefaultProjectHandler())

    def register_project(self, project_name: str, handler: ProjectHandler):
        """Register any project handler"""
        self.projects[project_name] = handler
    
    def process_message(self, message: ChatMessage) -> ChatResponse:
        """Route to current project handler"""
        #TODO: change the string scheme with dict scheme
        context_list = message.context.split(".") 
        current_project, current_state = context_list[-1].split("_")
        """Route to current project handler based on context"""
        # Extract current project and state from context
        current_project = message.context.get("current_project", "default")
        current_state = message.context.get("current_state", "start")
        project_context = message.context.get("project_data", {})






        # Get project handler or use default if not found
        project = self.projects.get(current_project, self.projects["default"])

        # Create a new message with project-specific context
        project_message = ChatMessage(
            content=message.content,
            context=project_context
        )
     
        # Get response from project handler
        project_response = project.handle_message(project_message)













        # Check for project transition
        next_project = project_response.next_context.get("transition_to")
        if next_project:
            # Create a new context for the next project
            next_context = {
                "current_project": next_project,
                "current_state": "start",
                "project_data": {},
                "history": message.context.get("history", []) + [{
                    "project": current_project,
                    "state": current_state,
                    "data": project_context
                }]
            }

            # Process the transition
            transition_message = ChatMessage(
                content=TextContent(text=""),  # Empty message for transition
                context=next_context
            )
            next_response = self.process_message(transition_message)

            # Combine responses
            combined_content = []
            if isinstance(project_response.content, list):
                combined_content.extend(project_response.content)
            else:
                combined_content.append(project_response.content)

            if isinstance(next_response.content, list):
                combined_content.extend(next_response.content)
            else:
                combined_content.append(next_response.content)

            return ChatResponse(


                content=combined_content,
                next_context=next_response.next_context
            )

        # No transition, update context with project response
        return ChatResponse(


            content=project_response.content,
            next_context={
                "current_project": current_project,
                "current_state": project_response.next_context.get("state", current_state),
                "project_data": project_response.next_context,
                "history": message.context.get("history", [])
            }
        )
     
# Tests for the chat system
class TestChatSystem(unittest.TestCase):
    def test_text_message_handling(self):
        chat_handler = ChatHandler()
        test_handler = MagicMock()
        test_handler.handle_message.return_value = ChatResponse(
            content=TextContent(text="Test response"),
            next_context={"state": "next_state"}
        )
        chat_handler.register_project("test_project", test_handler)

        message = ChatMessage(
            content=TextContent(text="Hello"),
            context={"current_project": "test_project", "current_state": "start"}
        )

        response = chat_handler.process_message(message)
        self.assertEqual(response.content.text, "Test response")
        self.assertEqual(response.next_context["current_state"], "next_state")

    def test_image_message_handling(self):
        chat_handler = ChatHandler()
        test_handler = MagicMock()
        test_handler.handle_message.return_value = ChatResponse(
            content=TextContent(text="Image received"),
            next_context={"state": "image_received"}
        )
        chat_handler.register_project("test_project", test_handler)

        message = ChatMessage(
            content=ImageContent(url="http://example.com/image.jpg"),
            context={"current_project": "test_project", "current_state": "start"}
        )

        response = chat_handler.process_message(message)
        self.assertEqual(response.content.text, "Image received")
        self.assertEqual(response.next_context["current_state"], "image_received")

    def test_project_transition(self):
        chat_handler = ChatHandler()

        # First project handler
        first_handler = MagicMock()
        first_handler.handle_message.return_value = ChatResponse(
            content=TextContent(text="Transitioning..."),
            next_context={"transition_to": "second_project"}
        )

        # Second project handler
        second_handler = MagicMock()
        second_handler.handle_message.return_value = ChatResponse(
            content=TextContent(text="In second project"),
            next_context={"state": "second_start"}
        )

        chat_handler.register_project("first_project", first_handler)
        chat_handler.register_project("second_project", second_handler)

        message = ChatMessage(
            content=TextContent(text="Start transition"),
            context={"current_project": "first_project", "current_state": "start"}
        )

        response = chat_handler.process_message(message)
        self.assertEqual(response.next_context["current_project"], "second_project")
        self.assertEqual(response.next_context["current_state"], "second_start")

if __name__=="__main__":
    message = ChatMessage(
        content=TextContent(text="hey there"),
        context={"current_project": "default", "current_state": "start"}
    )
    print(ChatHandler().process_message(message))

if __name__=="__main__":
    print(ChatHandler().process_message(ChatMessage(message="hey there",context="some_start")))