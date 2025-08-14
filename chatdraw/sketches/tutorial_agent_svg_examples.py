
import json
from typing import List
from pydantic import BaseModel, Field
from llama_index.llms.anthropic import Anthropic
from llama_index.core.llms import ChatMessage

from chatdraw.sketches.svg_utils import DEFAULT_RES
from chatdraw.sketches.tutorial_agent_base import HOUSE_EXAMPLE, Step, TutorialAgentBase

"""
The class creates a better tutorial because it starts with creating three SVGs 
of the concept and then basing of the tutorial on the SVGs
"""


class LLMOutputExtended(BaseModel):
    concept: str = Field(description="The concept depicted in the sketch")
    svgs: List[str] = Field(description="svgs depicting the concept")
    plan: str = Field(description="""Think before you provide the steps. 
First, think through what parts of the concept you want to sketch and the sketching order.
Then, think about where the parts should be located on the grid.
Finally, provide your response, step by step, using your analysis.""")
    steps: List[Step] = Field(description="List of sketching steps")


svg1="""<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <polygon points="100,20 30,80 170,80" fill="none" stroke="black" stroke-width="2"/>
  <rect x="50" y="80" width="100" height="90" fill="none" stroke="black" stroke-width="2"/>
  <rect x="90" y="120" width="20" height="50" fill="none" stroke="black" stroke-width="2"/>
</svg>"""

svg2="""<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <polygon points="100,30 40,90 160,90" fill="none" stroke="black" stroke-width="2"/>
  <rect x="55" y="90" width="90" height="80" fill="none" stroke="black" stroke-width="2"/>
  <rect x="75" y="120" width="20" height="50" fill="none" stroke="black" stroke-width="2"/>
  <rect x="115" y="110" width="20" height="20" fill="none" stroke="black" stroke-width="2"/>
  <line x1="115" y1="120" x2="135" y2="120" stroke="black" stroke-width="2"/>
  <line x1="125" y1="110" x2="125" y2="130" stroke="black" stroke-width="2"/>
</svg>"""

svg3="""<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <polygon points="100,20 30,80 170,80" fill="none" stroke="black" stroke-width="2"/>
  <rect x="50" y="80" width="100" height="100" fill="none" stroke="black" stroke-width="2"/>
  <line x1="50" y1="130" x2="150" y2="130" stroke="black" stroke-width="2"/>
  <rect x="90" y="150" width="20" height="30" fill="none" stroke="black" stroke-width="2"/>
  <rect x="60" y="95" width="20" height="20" fill="none" stroke="black" stroke-width="2"/>
  <rect x="120" y="95" width="20" height="20" fill="none" stroke="black" stroke-width="2"/>
</svg>"""

HOUSE_EXAMPLE_EXTENDED = LLMOutputExtended(svgs = [svg1,svg2,svg3],**HOUSE_EXAMPLE.model_dump())
   
user_prompt=f"""Your goal is to produce a step by step tutorial for drawing a concept based on its svgs.
The tutorial need to be separated into simple and manageable steps, each containing up to a few strokes. 
First write down three separate svg files depicting the concept. Should be colorless. Should have different styles. Only output the svgs.    
Then based of the svg example plan how to create a tutorial for drawing down the concept. 
Continuously refine the tutorial by starting with a basic structure and gradually adding complexity. 
Think step-by-step both on the level of the tutorial and the scope of each step.

examples: 
<exmple>
{HOUSE_EXAMPLE_EXTENDED.model_dump_json()}
</example>
"""

system_prompt="""You are an expert artist specializing in drawing sketches that are visually appealing, expressive, and professional.
You will be provided an SVG of some concept. Your task is to specify simple steps to draw the concept depicted in the SVG. 
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


class TutorialAgentSVGExmaples(TutorialAgentBase):

    def create_tutorial(self, concept:str) -> dict:
        model_name='claude-sonnet-4-20250514'
        llm = Anthropic(
            model=model_name, 
            max_tokens=3000,
            temperature=0,
        ).as_structured_llm(LLMOutputExtended)
        messages = [
            ChatMessage(role="system", content=system_prompt.replace("{res}",str(DEFAULT_RES))),
            ChatMessage(role="user", content=user_prompt),
            ChatMessage(role="system", content=f"{{\"concept\":\"{concept}\",")
        ]
        chat_response = llm.chat(messages,top_k=1,)
        tutorial_dict = json.loads(chat_response.message.blocks[0].text) # type: ignore
        tutorial_dict["model_name"] = model_name
        answer_dict = {"answer":tutorial_dict}
        return answer_dict