from chatdraw.chatflows.chat_system import ChatHandler, ChatMessage, ChatResponse, ProjectHandler
from chatdraw.sketches.tutorial_creator_sketchagent import load_tutorial


class DrawingProject(ProjectHandler):
    """Handles initial conversation flow"""
    
    def handle_message(self,message: ChatMessage) -> ChatResponse:
        if message.context=="start":
            return self._start(message)
        elif message.context=="chooseconcept":
            return self._chooseconcept(message)
        concept, step = message.context.split(",")
        return self._draw_step(concept, step)
    
    def _start(self, message: ChatMessage) -> ChatResponse:
        return ChatResponse(
            response=f"What would you like to draw?",
            next_context="chooseconcept")

    def _chooseconcept(self, message: ChatMessage) -> ChatResponse:
        concept=message.message
        response =  self._draw_step(concept,'1')
        return ChatResponse(
            response=f"What a good choice. Lets draw a {concept}.\n" + response.response,
            next_context=response.next_context)

    def _draw_step(self, concept, step) -> ChatResponse:
        tutorial = load_tutorial(concept)
        strokes = tutorial["answer"]["strokes"]
        curr_stroke = strokes[f"s{step}"]
        response=f"Please draw {curr_stroke['id']}. "
        next_step = str(int(step)+1)
        if f"s{next_step}" in strokes:
            next_context = concept+","+next_step
        else: 
            next_context = ""
            response+= f"\nThats it. Thank you for drawing a {concept} with me."
        return ChatResponse(response=response,next_context=next_context)


if __name__=="__main__":
    ch = ChatHandler()
    ch.register_project("greeting",DrawingProject())
    context="greeting_start"
    while context!="":
        response = ch.process_message(ChatMessage(message="monkey",context=context))
        print(response)
        context=response.next_context
    