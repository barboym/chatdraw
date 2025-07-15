from chatdraw.chatflows.chat_system import ChatHandler, ChatMessage, ChatResponse, ProjectHandler
from chatdraw.sketches.tutorial_creator_sketchagent import load_tutorial
from chatdraw.sketches.svg_utils import render_tutorial_to_pil
from chatdraw.utils import encode_image_to_string


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
        step = int(step)
        tutorial = load_tutorial(concept)
        strokes = sorted(tutorial["answer"]["strokes"].items(),key=lambda x:int(x[0][1:]))
        curr_stroke = strokes[step-1]
        image = render_tutorial_to_pil([el[1]["smoothed_vector"] for el in strokes[:step]])
        image_txt = encode_image_to_string(image)
        response=f"Please draw {curr_stroke[1]['id']}. example: \n <img src={image_txt}>\n"
        if len(strokes)>step:
            next_context = concept+","+str(step+1)
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

    