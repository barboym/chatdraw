from chatdraw.chatflows.chat_system import AtomicMessage, ChatHandler, ChatMessage, ChatResponse, ProjectHandler
from chatdraw.sketches.drawing_score import get_drawing_score
from chatdraw.sketches.tutorial_creator_sketchagent import load_tutorial
from chatdraw.sketches.svg_utils import render_tutorial_to_pil, svg_to_points
from chatdraw.utils import encode_image_to_string


class DrawingProject(ProjectHandler):
    """Handles initial conversation flow"""
    
    def handle_message(self,message: ChatMessage) -> ChatResponse:
        if message.context=="start":
            return self._start(message)
        elif message.context=="chooseconcept":
            return self._chooseconcept(message)
        elif message.context=="end":
            return self._end(message)
        return self._draw_step(message)
    
    def _start(self, message: ChatMessage) -> ChatResponse:
        return ChatResponse(
            response=f"What would you like to draw?",
            next_context="chooseconcept")

    def _chooseconcept(self, message: ChatMessage) -> ChatResponse:
        concept=message.message.content
        response =  self._draw_step(
            ChatMessage(message=AtomicMessage(content="",mtype="text"),context=f"{concept},1")
            )
        return ChatResponse(
            response=[f"What a good choice. Lets draw a {concept}."] + response.response,
            next_context=response.next_context)

    def _end(self, message: ChatMessage) -> ChatResponse:
        response = []
        response.append(f"Thats it. Thank you for drawing with me.")
        return ChatResponse(response=response, next_context="")

    def _draw_step(self, message: ChatMessage) -> ChatResponse:
        concept, step = message.context.split(",")
        step = int(step)
        sorted_strokes, curr_stroke_id, image_txt, smooth_strokes = self._get_strokes(concept, step)

        response = []
        if step>1 and message.message.mtype=="image":
            user_points = svg_to_points(message.message.content)
            score = get_drawing_score(user_points,smooth_strokes[:-1])
            response.append(
                f"Your drawing score is: {score}"
            )
        response += [
            f"Please draw the {curr_stroke_id}. Like in the next example:",
            AtomicMessage(content=image_txt, mtype="image")
        ]

        next_context = f"{concept},{step+1}" if step < len(sorted_strokes) else ""
        if not next_context:
            next_context = "end"

        return ChatResponse(response=response, next_context=next_context)

    def _get_strokes(self, concept, step):
        tutorial = load_tutorial(concept)
        strokes = tutorial["answer"]["strokes"]
        smooth_strokes = [stroke["smoothed_vector"] for stroke in strokes[:step]]
        curr_stroke_name = strokes[step-1]['id']
        image = render_tutorial_to_pil(smooth_strokes,last_step_highlighted=True)
        image_txt = encode_image_to_string(image)
        return strokes,curr_stroke_name,image_txt, smooth_strokes


if __name__=="__main__":
    ch = ChatHandler()
    ch.register_project("greeting",DrawingProject())
    context="greeting_start"
    while context!="":
        response = ch.process_message(ChatMessage(message="monkey",context=context))
        print(response)
        context=response.next_context

    