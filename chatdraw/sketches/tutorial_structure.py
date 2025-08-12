from pydantic import BaseModel, Field
from typing import List

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

