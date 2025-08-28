from typing import Annotated, List

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

import itertools
from chatdraw.sketches.tutorial_creator_sketchagent import load_tutorial, normalize_concept_string
from chatdraw.sketches.svg_utils import render_tutorial_to_pil
from chatdraw.utils import encode_image_to_string


class Message(TypedDict):
    mtype: str
    content: str

class State(TypedDict):
    context: str 
    messages: Annotated[List[Message], add_messages]

def router(state: State):
    if state.context in ["greeting","chooseconcept","farewell"]: return state.context
    return "draw"
    
def greeting(state: State):
    return {"messages": [{"content":"""Welcome to Chatdraw. 
I am a drawing tutorial bot for drawing simple sketches. 
What would you like to learn to draw today?""","mtype":"text"}],"context":"chooseconcept"}

def chooseconcept(state: State):
    if state.messages[0]["mtype"]=="image":
        return {
            "messages":[
                {
                    "content":"You need to write a concept you would like to draw. Try writing a noun that comes to your mind.",
                    "mtype":"text"
                }
            ],
            "context":"chooseconcept"
        }


    concept=state.messages[0].content
    concept = normalize_concept_string(concept)
    # response =  self._draw_step(
    #     ChatMessage(message=AtomicMessage(content="",mtype="text"),context=f"{concept},1")
    #     )
    return {"messages":[{"content":f"What a good choice. Lets draw a {concept}.","mtype":"text"}],"context":"draw"}

def draw(state: State):
    concept, step = state.context.split(",")
    step = int(step)
    tutorial = load_tutorial(concept)["steps"]
    
    response = []
    # if step>1 and message.message.mtype=="image":
    #     user_points = svg_to_points(message.message.content)
    #     score = get_drawing_score(user_points,smooth_strokes[:-1])
    #     response.append(
    #         f"Your drawing score is: {score}"
    #     )
    if step==1:
        strokes = itertools.chain(*[step["strokes"] for step in tutorial])
        smooth_strokes = [el["smoothed_vector_scaled"] for el in strokes]
        image_full = render_tutorial_to_pil(smooth_strokes)
        image_full_txt = encode_image_to_string(image_full)
        response += [
            {"content":f"The full image will look like that:","mtype":"text"},
            {"content":image_full_txt, "mtype":"image"} 
        ]
    
    response.append(tutorial[step-1]["thinking"])
    strokes = itertools.chain(*[step["strokes"] for step in tutorial[:step]])
    smooth_strokes = [el["smoothed_vector_scaled"] for el in strokes]   
    smooth_strokes_highlight = [el["smoothed_vector_scaled"] for el in tutorial[step-1]["strokes"]]     
    image = render_tutorial_to_pil(smooth_strokes,highlighted_strokes=smooth_strokes_highlight)
    image_txt = encode_image_to_string(image)
    response += [
        {"content":image_txt, "mtype":"image"}
    ]

    next_context = f"{concept},{step+1}" if step < len(tutorial) else ""
    if not next_context:
        next_context = "end"

    return {"messages":response,"context":next_context}

def farewell(state: State):
    return {"messages": ["Thats it. Thank you for drawing with me."],"context":"greeting"}

routes_dict = {"greeting":"greeting","chooseconcept":"chooseconcept","farewell":"farewell","draw":"draw"}
    
chatflow_builder = StateGraph(State)
chatflow_builder.add_conditional_edges(START,router,routes_dict)
chatflow_builder.add_node("greeting",greeting)
chatflow_builder.add_node("chooseconcept",chooseconcept)
chatflow_builder.add_node("farewell",farewell)
chatflow_builder.add_node("draw",draw)
chatflow_graph = chatflow_builder.compile()