from typing import List
from pydantic import BaseModel, Field
from llama_index.llms.anthropic import Anthropic
from llama_index.core import PromptTemplate
from chatdraw.sketches.svg_parsing import SUPPORTED_ELEMENTS, element_to_path, parse_svg_steps, strip_svg_fence

prompt_svg = PromptTemplate(template=(
    'generate an svg file depicting a {concept}. '
    'The svg should be black and white. '
    'Make sure there are comments explaining what the elements represent. '
    'No preambles. Output an svg string only. '
))

class SingleStroke(BaseModel):
    path: str = Field(description="The d attribute of a <path/> element")
    id: str = Field(description="A short descriptive identifier for the stroke, explaining which part of the sketch it corresponds to")

class Step(BaseModel):
    thinking: str = Field(description="Which part in the plan is being implemented")
    strokes: List[SingleStroke] = Field(description="Stokes that generate this part of the sketch")

class TutorialOutput(BaseModel):
    model_name: str
    concept: str
    svg_raw: str
    steps: List[Step] = Field(description="List of sketching steps")


model_name='claude-sonnet-4-20250514'

llm = Anthropic(
    model=model_name, 
    max_tokens=3000,
    temperature=0,
)


def generate_tutorial(concept:str) -> TutorialOutput:
    svg_str = llm.predict(prompt_svg,concept=concept)
    svg_str = strip_svg_fence(svg_str)
    steps = parse_svg_steps(svg_str)
    for step in steps:
        comment = step.pop("comment")
        elements = step.pop('elements')
        elements_supported = filter(
            lambda x:x.tag.split("}")[-1] in SUPPORTED_ELEMENTS,elements)
        elements_path = map(
            lambda x:{
                "path":element_to_path(x).get('d'),
                "id":comment
            },elements_supported
        )
        step["strokes"]=list(elements_path)
        step["thinking"] = comment
    tutorial_dict = {
        "model_name":llm.model,
        "concept":concept,
        "svg_raw":svg_str,
        "steps":steps
    }
    tutorial = TutorialOutput.model_validate(tutorial_dict)
    return tutorial