
from abc import abstractmethod
import json
from typing import List
from pydantic import BaseModel, Field
from llama_index.llms.anthropic import Anthropic
from llama_index.core.llms import ChatMessage

from chatdraw.sketches.svg_utils import DEFAULT_RES


class SingleStroke(BaseModel):
    points: str = Field(description="A list of x-y coordinates defining the curve. These points define the path the stroke follows")
    id: str = Field(description="A short descriptive identifier for the stroke, explaining which part of the sketch it corresponds to")

class Step(BaseModel):
    thinking: str = Field(description="Which part in the plan is being implemented")
    strokes: List[SingleStroke] = Field(description="Stokes that generate this part of the sketch")

class LLMOutput(BaseModel):
    concept: str = Field(description="The concept depicted in the sketch")
    plan: str = Field(description="""Think before you provide the steps. 
First, think through what parts of the concept you want to sketch and the sketching order.
Then, think about where the parts should be located on the grid.
Finally, provide your response, step by step, using your analysis.""")
    steps: List[Step] = Field(description="List of sketching steps")




HOUSE_EXAMPLE = LLMOutput(
    concept="house",
    plan="""The house has the following components which will be drawn step by step: 
1. A general structure of the building. 
2. Finer properties of the structure and smaller sections. 
3. details like doors, windows, fenses etc. """,
    steps = [
        Step(
            thinking="Start by drawing the front of the house",
            strokes=[
                SingleStroke(id="house base front rectangle",points="x13y27 x24y27 x24y27 x24y11 x24y11 x13y11 x13y11 x13y27"),
                SingleStroke(id="roof front triangle",points="x13y27 x18y37 x18y37 x24y27"),
            ]
        ),
        Step(
            thinking="Add the house's right section",
            strokes=[
                SingleStroke(id="house base right section",points="x24y27 x36y28 x36y28 x36y21 x36y21 x36y12 x36y12 x24y11"),
                SingleStroke(id="roof right section",points="x18y37 x30y38 x30y38 x36y28"),
            ]
        ),
        Step(
            thinking="Add details to it, like windows and a door",
            strokes=[
                SingleStroke(id="left window square",points="x26y25 x29y25 x29y25 x29y21 x29y21 x26y21 x26y21 x26y25"),
                SingleStroke(id="right window square",points="x31y25 x34y25 x34y25 x34y21 x34y21 x31y21 x31y21 x31y25"),
                SingleStroke(id="front door",points="x17y11 x17y18 x17y18 x21y18 x21y18 x21y11 x21y11 x17y11"),
            ]
        ),
    ]
)

sketch_prompt = f"""Your goal is to produce a visually appealing sketch of a {{concept}}.
You need to provide x-y coordinates that construct a recognizable sketch of the concept.
To draw a visually appealing sketch of the given object or concept, break down complex drawings into manageable steps. 
Begin with the most important part of the object, then observe your progress and add additional elements as needed. 
Continuously refine your sketch by starting with a basic structure and gradually adding complexity. Think step-by-step.

Here are a few examples: 
{HOUSE_EXAMPLE.model_dump_json()} 
"""

system_prompt="""You are an expert artist specializing in drawing sketches that are visually appealing, expressive, and professional.
You will be provided with a blank grid. Your task is to specify where to place strokes on the grid to create a visually appealing sketch of the given textual concept.
The grid uses numbers (1 to {res}) along the bottom (x axis) and numbers (1 to {res}) along the left edge (y axis) to reference specific locations within the grid. 
Each cell is uniquely identified by a combination of the corresponding x axis numbers and y axis number. The bottom-left cell is 'x1y1', the cell to its right is 'x2y1'.
You can draw on this grid by specifying where to draw strokes. You can draw multiple strokes to depict the whole object, where different strokes compose different parts of the object. 
To draw a stroke on the grid, you need to specify the following:
Starting Point: Specify the starting point by giving the grid location.
Ending Point: Specify the ending point in the same way.
Intermediate Points: Specify intermediate points that the stroke should pass through. List these in the order the stroke should follow, using the same grid location format.
By default all strokes are smooth. To make a sharp angle withing a stroke, repeat the intermediate point once for the angle location.   
Stroke Examples:
A smooth convex curve that starts at x8y6 and ends at x8y11: 'x8y6 x6y7 x6y10 x8y11'. 
To close this curve into an ellipse shape, you can add another curve 'x8y11 x11y10 x11y7 x8y6'. 
A large circle that starts at x25y44: 'x25y44  x32y41 x35y35 x31y29 x25y27 x19y29 x15y35 x18y41 x25y44'. 
To draw non-smooth shapes (with corners) like triangles or rectangles, you need to specify the corner points twice. 
For example, to draw an upside-down "V" shape that starts at x13y27, ends at x24y27, with a pick (corner) at x18y37: 'x13y27 x18y37 x18y37 x24y27'. 
To draw a triangle with corners at x10y29, x15y33, and x9y35, start with drawing a "V" shape that starts at x10y29, ends at x9y35, with a pick (corner) at x15y33, and then close it with a straight line from x15y33 to x10y29: 'x10y29 x15y33 x15y33 x9y35 x9y35 x10y29'. 
To draw a rectangle with four corners at x13y27, x24y27, x24y11, x13y11: 'x13y27 x24y27 x24y27 x24y11 x24y11 x13y11 x13y11 x13y27'. 
To draw a small square with four corners at x26y25, x29y25, x29y21, x26y21: 'x26y25 x29y25 x29y25 x29y21 x29y21 x26y21 x26y21 x26y25'.
To draw a single dot at x15y31 do a single point strock: 'x15y31'. 
To draw a straight linear line that starts at x18y31 and ends at x35y14 use: 'x18y31 x35y14'. 
If you want to draw a big and long stroke, split it into multiple small curves that connect to each other."""




class TutorialAgentBase:

    @abstractmethod
    def create_tutorial(self, concept: str) -> dict:
        pass

class TutorialAgent(TutorialAgentBase):
    def create_tutorial(self, concept:str) -> dict:
        model_name='claude-sonnet-4-20250514'
        llm = Anthropic(
            model=model_name, 
            max_tokens=3000,
            temperature=0,
        ).as_structured_llm(LLMOutput)
        messages = [
            ChatMessage(role="system", content=system_prompt.replace("{res}",str(DEFAULT_RES))),
            ChatMessage(role="user", content=sketch_prompt.replace("{concept}",concept)),
        ]
        # parsing response into the structure used up till now
        chat_response = llm.chat(messages,top_k=1,)
        tutorial_dict = json.loads(chat_response.message.blocks[0].text) # type: ignore
        tutorial_dict["model_name"] = model_name
        return tutorial_dict