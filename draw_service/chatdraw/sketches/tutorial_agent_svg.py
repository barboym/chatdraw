from typing import List
from pydantic import BaseModel, Field
from llama_index.llms.anthropic import Anthropic
from llama_index.core import PromptTemplate
from draw_service.chatdraw.sketches.svg_parsing import element_to_path, parse_svg_steps, strip_svg_fence
from draw_service.chatdraw.sketches.tutorial_agent_svg_chain import Step

prompt_svg = PromptTemplate(template=(
    'generate an svg file depicting a {concept}. '
    'Make sure there are comments explaining what the elements represent. '
    'No preambles. Output an svg string. '
))

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
        step["strokes"]=list(
            map(
                lambda x:{
                    "path":element_to_path(x).get('d'),
                    "id":comment
                },step.pop('elements')
            )
        )
        step["thinking"] = comment
    tutorial_dict = {
        "model_name":llm.model,
        "concept":concept,
        "svg_raw":svg_str,
        "steps":steps
    }
    tutorial = TutorialOutput.model_validate(tutorial_dict)
    return tutorial