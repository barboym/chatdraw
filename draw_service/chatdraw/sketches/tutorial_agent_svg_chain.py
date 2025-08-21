from typing import List
from pydantic import BaseModel, Field
from llama_index.llms.anthropic import Anthropic
from llama_index.core import PromptTemplate

prompt_svg_free = PromptTemplate(template=(
    'generate an svg file depicting a {concept}. '
    'No preambles. Output an svg string. '
))

model_name='claude-sonnet-4-20250514'
# model_name="anthropic.claude-sonnet-4-20250514-v1:0"
# model_name="claude-3-7-sonnet-20250219"
llm = Anthropic(
    model=model_name, 
    max_tokens=3000,
    temperature=0,
)

prompt_svg_convert = PromptTemplate(template=(
    'convert the following svg string so that its colorless and all its elements are <path/> elements '
    'line, cicle, eclipse, rect and other elements should be converted to path. '
    'They should have any filling and color attributes ommited. '
    'Then they should be converted to path elements one by one so that all shapes and the overall picture remains similar. '
    'No preambles. Output an svg string. \n'
    '{svg} '
))


prompt_tutorial = PromptTemplate(template=(
    'create a tutorial for drawing a simple sketch of a <concept>{concept}</concept>. '
    'consider the following svg string as an example to what the end goal of the tutorial should like: '
    '{svg} '
))

class SingleStroke(BaseModel):
    path: str = Field(description="The d attribute of a <path/> element")
    id: str = Field(description="A short descriptive identifier for the stroke, explaining which part of the sketch it corresponds to")

class Step(BaseModel):
    thinking: str = Field(description="Which part in the plan is being implemented")
    strokes: List[SingleStroke] = Field(description="Stokes that generate this part of the sketch")

class TutorialOutput(BaseModel):
    plan: str = Field(description="""Think before you provide each step. 
First, think through what parts of the concept you want to sketch and the sketching order.
Then, think about where the parts should be located on the grid.
Finally, provide your response, step by step, using your analysis.""")
    steps: List[Step] = Field(description="List of sketching steps")

class Tutorial(TutorialOutput):
    model_name: str
    concept: str
    svg_raw: str
    svg_sketch: str
    
llm_tutorial = llm.as_structured_llm(TutorialOutput)


def generate_tutorial(concept:str) -> dict:
    response_svg = llm.predict(prompt_svg_free,concept=concept)
    response_svg_bw = llm.predict(prompt_svg_convert,svg=response_svg)
    # changing stroke fill, color and width
    response_svg_bw_parsed = "\n".join(
        [
            response_svg_bw.split("\n")[0][:-1]+ ' fill="none" stroke="black" stroke-width="1"' + ">"
        ]+response_svg_bw.split("\n")[1:]
    )
    response_tutorial = llm_tutorial.predict(prompt_tutorial,concept=concept,svg=response_svg_bw_parsed)
    tutorial_output = TutorialOutput.model_validate_json(response_tutorial)
    
    tutorial = Tutorial(
        **tutorial_output.model_dump(),
        concept=concept,
        model_name=model_name,
        svg_raw=response_svg,
        svg_sketch=response_svg_bw_parsed
    )

    return tutorial.model_dump()


