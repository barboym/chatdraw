from chatdraw.chatflows.greeting import GreetingProject
from chatdraw.chatflows.chat_system import ChatMessage, ChatResponse

def test_start_context_response():
    project = GreetingProject(available_projects=["ProjectA", "ProjectB"])
    msg = ChatMessage(message="Hello", context="ProjectA_start")
    response = project.handle_message(msg)
    assert isinstance(response, ChatResponse)
    assert "Welcome to my chat" in response.response[0].content
    assert "ProjectA,ProjectB" in response.response[0].content
    assert response.next_context == "chooseproject"

def test_choose_project_context_response():
    project = GreetingProject(available_projects=["ProjectA"])
    msg = ChatMessage(message="ProjectA", context="chooseproject")
    response = project.handle_message(msg)
    assert isinstance(response, ChatResponse)
    assert "Let do ProjectA" in response.response[0].content
    assert response.next_context == "start.ProjectA_start"

def test_handle_message_invalid_context():
    project = GreetingProject(available_projects=["ProjectA"])
    msg = ChatMessage(message="Test", context="invalidcontext")
    try:
        project.handle_message(msg)
        assert False, "Expected KeyError for invalid context"
    except KeyError:
        pass

def test_greeting_project_init_available_projects():
    projects = ["X", "Y"]
    project = GreetingProject(available_projects=projects)
    assert project.available_projects == projects