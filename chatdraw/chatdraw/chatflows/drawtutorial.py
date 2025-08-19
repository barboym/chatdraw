import itertools
from chatdraw.chatflows.chat_system import AtomicMessage, ChatHandler, ChatMessage, ChatResponse, ProjectHandler
from chatdraw.sketches.tutorial_creator_sketchagent import load_tutorial, normalize_concept_string
from chatdraw.sketches.svg_utils import render_tutorial_to_pil
from chatdraw.chatdraw.utils import encode_image_to_string


class DrawingProject(ProjectHandler):
    """Handles initial conversation flow"""
    
    def handle_message(self,message: ChatMessage) -> ChatResponse:
        if message.context=="start":
            return self._start()
        elif message.context=="chooseconcept":
            return self._chooseconcept(message)
        elif message.context=="end":
            return self._end(message)
        return self._draw_step(message)
    
    def _start(self) -> ChatResponse:
        return ChatResponse(
            response=f"""Welcome to Chatdraw. 
I am a drawing tutorial bot for drawing simple sketches. 
What would you like to learn to draw today?""",
            next_context="chooseconcept")

    def _chooseconcept(self, message: ChatMessage) -> ChatResponse:
        if message.message.mtype=="image":
            return ChatResponse(
                response = [
                    AtomicMessage(
                        content="You need to write a concept you would like to draw. Try writing a noun that comes to your mind.",
                        mtype="text"
                        )   
                ],
                next_context="chooseconcept"
            )
        
        
        concept=message.message.content
        concept = normalize_concept_string(concept)
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
        tutorial = load_tutorial(concept)

        response = []
        # if step>1 and message.message.mtype=="image":
        #     user_points = svg_to_points(message.message.content)
        #     score = get_drawing_score(user_points,smooth_strokes[:-1])
        #     response.append(
        #         f"Your drawing score is: {score}"
        #     )
        if step==1:
            strokes = itertools.chain(*[step["strokes"] for step in tutorial])
            smooth_strokes = [el["smoothed_vector"] for el in strokes]
            image_full = render_tutorial_to_pil(smooth_strokes)
            image_full_txt = encode_image_to_string(image_full)
            response += [
                f"The full image will look like that:",
                AtomicMessage(content=image_full_txt, mtype="image") 
            ]
        response.append(tutorial[step-1]["thinking"])
        strokes = itertools.chain(*[step["strokes"] for step in tutorial[:step]])
        smooth_strokes = [el["smoothed_vector"] for el in strokes]   
        smooth_strokes_highlight = [el["smoothed_vector"] for el in tutorial[step-1]["strokes"]]     
        image = render_tutorial_to_pil(smooth_strokes,highlighted_strokes=smooth_strokes_highlight)
        image_txt = encode_image_to_string(image)
        response += [
            AtomicMessage(content=image_txt, mtype="image")
        ]

        next_context = f"{concept},{step+1}" if step < len(tutorial) else ""
        if not next_context:
            next_context = "end"

        return ChatResponse(response=response, next_context=next_context)


if __name__=="__main__":
    ch = ChatHandler("")
    ch.register_project("greeting",DrawingProject())
    context="greeting_start"
    while context!="":
        response = ch.process_message(ChatMessage(message="monkey",context=context))
        print(response)
        context=response.next_context

    