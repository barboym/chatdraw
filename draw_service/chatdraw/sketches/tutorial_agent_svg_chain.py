from typing import List
from pydantic import BaseModel, Field
from llama_index.llms.anthropic import Anthropic
from llama_index.core import PromptTemplate
from llama_index.core.program import LLMTextCompletionProgram

prompt_svg_free = PromptTemplate(template=(
    'generate an svg file depicting a {concept}. '
    'No preambles. Output an svg string. '
))

model_name='claude-sonnet-4-20250514'
# model_name="anthropic.claude-sonnet-4-20250514-v1:0"
# model_name="claude-3-7-sonnet-20250219"
# model_name="claude-3-5-haiku-latest"
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
    '{svg} \n'
    '<examples>\n{examples}\n<examples'
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
program_tutorial = LLMTextCompletionProgram.from_defaults(
    prompt=prompt_tutorial,
    output_cls=TutorialOutput,
    llm=llm,
)

def generate_tutorial(concept:str) -> dict:
    response_svg = llm.predict(prompt_svg_free,concept=concept)
    response_svg_bw = llm.predict(prompt_svg_convert,svg=response_svg)
    # changing stroke fill, color and width
    response_svg_bw_parsed = "\n".join(
        [
            response_svg_bw.split("\n")[0][:-1]+ ' fill="none" stroke="black" stroke-width="1"' + ">"
        ]+response_svg_bw.split("\n")[1:]
    )
    
    response_tutorial = llm_tutorial.predict(
        prompt_tutorial,
        concept=concept,
        svg=response_svg_bw_parsed,
        examples="{\"plan\": \"Looking at the squirrel sketch, I can identify the main components and their drawing order:\\n\\n1. Start with the large bushy tail on the left side - this is the most distinctive feature\\n2. Draw the oval body in the center\\n3. Add the circular head above the body\\n4. Draw the pointed ears on top of the head\\n5. Add facial features - eyes, nose\\n6. Draw the front paws/arms\\n7. Add the back legs/paws\\n8. Finally, add a small acorn that the squirrel is holding\\n\\nFor positioning on a 300x300 grid:\\n- Tail: Left side, vertically elongated from y=100 to y=260\\n- Body: Center, oval shape around x=150, y=200\\n- Head: Above body, circular around x=150, y=130\\n- Ears: Top of head around y=90-120\\n- Eyes: On the head around y=125\\n- Nose: Below eyes around y=140\\n- Front paws: On sides of body around y=180\\n- Back paws: Bottom of body around y=240\\n- Acorn: Small detail near front paw\\n\\nThis creates a classic side-view squirrel pose with the characteristic bushy tail.\", \"steps\": [{\"thinking\": \"Starting with the most distinctive feature - the large bushy tail on the left side\", \"strokes\": [{\"path\": \"M 80 100 C 119 100 125 140 125 180 C 125 220 119 260 80 260 C 41 260 35 220 35 180 C 35 140 41 100 80 100 Z\", \"id\": \"tail_outer\"}, {\"path\": \"M 75 110 C 110 110 115 142.5 115 175 C 115 207.5 110 240 75 240 C 40 240 35 207.5 35 175 C 35 142.5 40 110 75 110 Z\", \"id\": \"tail_inner\"}]}, {\"thinking\": \"Drawing the main body as an oval shape in the center\", \"strokes\": [{\"path\": \"M 110 200 C 110 169.6 126.9 145 150 145 C 173.1 145 190 169.6 190 200 C 190 230.4 173.1 255 150 255 C 126.9 255 110 230.4 110 200 Z\", \"id\": \"body_outer\"}, {\"path\": \"M 120 200 C 120 175.1 132.4 155 150 155 C 167.6 155 180 175.1 180 200 C 180 224.9 167.6 245 150 245 C 132.4 245 120 224.9 120 200 Z\", \"id\": \"body_inner\"}]}, {\"thinking\": \"Adding the circular head above the body\", \"strokes\": [{\"path\": \"M 115 130 C 115 110.7 130.7 95 150 95 C 169.3 95 185 110.7 185 130 C 185 149.3 169.3 165 150 165 C 130.7 165 115 149.3 115 130 Z\", \"id\": \"head_outer\"}, {\"path\": \"M 125 130 C 125 116.2 136.2 105 150 105 C 163.8 105 175 116.2 175 130 C 175 143.8 163.8 155 150 155 C 136.2 155 125 143.8 125 130 Z\", \"id\": \"head_inner\"}]}, {\"thinking\": \"Drawing the pointed ears on top of the head\", \"strokes\": [{\"path\": \"M 127 105 C 127 96.7 130.7 90 135 90 C 139.3 90 143 96.7 143 105 C 143 113.3 139.3 120 135 120 C 130.7 120 127 113.3 127 105 Z\", \"id\": \"left_ear_outer\"}, {\"path\": \"M 157 105 C 157 96.7 160.7 90 165 90 C 169.3 90 173 96.7 173 105 C 173 113.3 169.3 120 165 120 C 160.7 120 157 113.3 157 105 Z\", \"id\": \"right_ear_outer\"}, {\"path\": \"M 130 108 C 130 101.4 132.2 98 135 98 C 137.8 98 140 101.4 140 108 C 140 114.6 137.8 118 135 118 C 132.2 118 130 114.6 130 108 Z\", \"id\": \"left_ear_inner\"}, {\"path\": \"M 160 108 C 160 101.4 162.2 98 165 98 C 167.8 98 170 101.4 170 108 C 170 114.6 167.8 118 165 118 C 162.2 118 160 114.6 160 108 Z\", \"id\": \"right_ear_inner\"}]}, {\"thinking\": \"Adding the facial features - eyes and nose\", \"strokes\": [{\"path\": \"M 134 125 C 134 121.7 136.7 119 140 119 C 143.3 119 146 121.7 146 125 C 146 128.3 143.3 131 140 131 C 136.7 131 134 128.3 134 125 Z\", \"id\": \"left_eye_outer\"}, {\"path\": \"M 154 125 C 154 121.7 156.7 119 160 119 C 163.3 119 166 121.7 166 125 C 166 128.3 163.3 131 160 131 C 156.7 131 154 128.3 154 125 Z\", \"id\": \"right_eye_outer\"}, {\"path\": \"M 140 123 C 140 121.9 140.9 121 142 121 C 143.1 121 144 121.9 144 123 C 144 124.1 143.1 125 142 125 C 140.9 125 140 124.1 140 123 Z\", \"id\": \"left_eye_pupil\"}, {\"path\": \"M 160 123 C 160 121.9 160.9 121 162 121 C 163.1 121 164 121.9 164 123 C 164 124.1 163.1 125 162 125 C 160.9 125 160 124.1 160 123 Z\", \"id\": \"right_eye_pupil\"}, {\"path\": \"M 147 140 C 147 139.1 148.3 138 150 138 C 151.7 138 153 139.1 153 140 C 153 140.9 151.7 142 150 142 C 148.3 142 147 140.9 147 140 Z\", \"id\": \"nose\"}]}, {\"thinking\": \"Drawing the front paws on either side of the body\", \"strokes\": [{\"path\": \"M 122 180 C 122 171.7 125.6 165 130 165 C 134.4 165 138 171.7 138 180 C 138 188.3 134.4 195 130 195 C 125.6 195 122 188.3 122 180 Z\", \"id\": \"left_front_paw\"}, {\"path\": \"M 162 180 C 162 171.7 165.6 165 170 165 C 174.4 165 178 171.7 178 180 C 178 188.3 174.4 195 170 195 C 165.6 195 162 188.3 162 180 Z\", \"id\": \"right_front_paw\"}]}, {\"thinking\": \"Adding the back legs/paws at the bottom\", \"strokes\": [{\"path\": \"M 123 240 C 123 230.1 128.4 222 135 222 C 141.6 222 147 230.1 147 240 C 147 249.9 141.6 258 135 258 C 128.4 258 123 249.9 123 240 Z\", \"id\": \"left_back_paw\"}, {\"path\": \"M 153 240 C 153 230.1 158.4 222 165 222 C 171.6 222 177 230.1 177 240 C 177 249.9 171.6 258 165 258 C 158.4 258 153 249.9 153 240 Z\", \"id\": \"right_back_paw\"}]}, {\"thinking\": \"Finally, adding a small acorn that the squirrel is holding\", \"strokes\": [{\"path\": \"M 114 170 C 114 165.6 116.7 162 120 162 C 123.3 162 126 165.6 126 170 C 126 174.4 123.3 178 120 178 C 116.7 178 114 174.4 114 170 Z\", \"id\": \"acorn_body\"}, {\"path\": \"M 116 165 C 116 163.3 117.8 162 120 162 C 122.2 162 124 163.3 124 165 C 124 166.7 122.2 168 120 168 C 117.8 168 116 166.7 116 165 Z\", \"id\": \"acorn_cap\"}]}], \"model_name\": \"claude-sonnet-4-20250514\", \"concept\": \"squirrel\", \"svg_raw\": \"<svg width=\\\"300\\\" height=\\\"300\\\" viewBox=\\\"0 0 300 300\\\" xmlns=\\\"http://www.w3.org/2000/svg\\\">\\n  <!-- Tail -->\\n  <ellipse cx=\\\"80\\\" cy=\\\"180\\\" rx=\\\"45\\\" ry=\\\"80\\\" fill=\\\"#8B4513\\\" transform=\\\"rotate(-30 80 180)\\\"/>\\n  <ellipse cx=\\\"75\\\" cy=\\\"175\\\" rx=\\\"35\\\" ry=\\\"65\\\" fill=\\\"#D2691E\\\" transform=\\\"rotate(-30 75 175)\\\"/>\\n  \\n  <!-- Body -->\\n  <ellipse cx=\\\"150\\\" cy=\\\"200\\\" rx=\\\"40\\\" ry=\\\"55\\\" fill=\\\"#8B4513\\\"/>\\n  <ellipse cx=\\\"150\\\" cy=\\\"200\\\" rx=\\\"30\\\" ry=\\\"45\\\" fill=\\\"#D2691E\\\"/>\\n  \\n  <!-- Head -->\\n  <circle cx=\\\"150\\\" cy=\\\"130\\\" r=\\\"35\\\" fill=\\\"#8B4513\\\"/>\\n  <circle cx=\\\"150\\\" cy=\\\"130\\\" r=\\\"25\\\" fill=\\\"#D2691E\\\"/>\\n  \\n  <!-- Ears -->\\n  <ellipse cx=\\\"135\\\" cy=\\\"105\\\" rx=\\\"8\\\" ry=\\\"15\\\" fill=\\\"#8B4513\\\"/>\\n  <ellipse cx=\\\"165\\\" cy=\\\"105\\\" rx=\\\"8\\\" ry=\\\"15\\\" fill=\\\"#8B4513\\\"/>\\n  <ellipse cx=\\\"135\\\" cy=\\\"108\\\" rx=\\\"5\\\" ry=\\\"10\\\" fill=\\\"#D2691E\\\"/>\\n  <ellipse cx=\\\"165\\\" cy=\\\"108\\\" rx=\\\"5\\\" ry=\\\"10\\\" fill=\\\"#D2691E\\\"/>\\n  \\n  <!-- Eyes -->\\n  <circle cx=\\\"140\\\" cy=\\\"125\\\" r=\\\"6\\\" fill=\\\"#000\\\"/>\\n  <circle cx=\\\"160\\\" cy=\\\"125\\\" r=\\\"6\\\" fill=\\\"#000\\\"/>\\n  <circle cx=\\\"142\\\" cy=\\\"123\\\" r=\\\"2\\\" fill=\\\"#FFF\\\"/>\\n  <circle cx=\\\"162\\\" cy=\\\"123\\\" r=\\\"2\\\" fill=\\\"#FFF\\\"/>\\n  \\n  <!-- Nose -->\\n  <ellipse cx=\\\"150\\\" cy=\\\"140\\\" rx=\\\"3\\\" ry=\\\"2\\\" fill=\\\"#000\\\"/>\\n  \\n  <!-- Front paws -->\\n  <ellipse cx=\\\"130\\\" cy=\\\"180\\\" rx=\\\"8\\\" ry=\\\"15\\\" fill=\\\"#8B4513\\\"/>\\n  <ellipse cx=\\\"170\\\" cy=\\\"180\\\" rx=\\\"8\\\" ry=\\\"15\\\" fill=\\\"#8B4513\\\"/>\\n  \\n  <!-- Back paws -->\\n  <ellipse cx=\\\"135\\\" cy=\\\"240\\\" rx=\\\"12\\\" ry=\\\"18\\\" fill=\\\"#8B4513\\\"/>\\n  <ellipse cx=\\\"165\\\" cy=\\\"240\\\" rx=\\\"12\\\" ry=\\\"18\\\" fill=\\\"#8B4513\\\"/>\\n  \\n  <!-- Acorn -->\\n  <ellipse cx=\\\"120\\\" cy=\\\"170\\\" rx=\\\"6\\\" ry=\\\"8\\\" fill=\\\"#8B4513\\\"/>\\n  <ellipse cx=\\\"120\\\" cy=\\\"165\\\" rx=\\\"4\\\" ry=\\\"3\\\" fill=\\\"#228B22\\\"/>\\n</svg>\", \"svg_sketch\": \"<svg width=\\\"300\\\" height=\\\"300\\\" viewBox=\\\"0 0 300 300\\\" xmlns=\\\"http://www.w3.org/2000/svg\\\" fill=\\\"none\\\" stroke=\\\"black\\\" stroke-width=\\\"1\\\">\\n  <!-- Tail -->\\n  <path d=\\\"M 80 100 C 119 100 125 140 125 180 C 125 220 119 260 80 260 C 41 260 35 220 35 180 C 35 140 41 100 80 100 Z\\\"/>\\n  <path d=\\\"M 75 110 C 110 110 115 142.5 115 175 C 115 207.5 110 240 75 240 C 40 240 35 207.5 35 175 C 35 142.5 40 110 75 110 Z\\\"/>\\n  \\n  <!-- Body -->\\n  <path d=\\\"M 110 200 C 110 169.6 126.9 145 150 145 C 173.1 145 190 169.6 190 200 C 190 230.4 173.1 255 150 255 C 126.9 255 110 230.4 110 200 Z\\\"/>\\n  <path d=\\\"M 120 200 C 120 175.1 132.4 155 150 155 C 167.6 155 180 175.1 180 200 C 180 224.9 167.6 245 150 245 C 132.4 245 120 224.9 120 200 Z\\\"/>\\n  \\n  <!-- Head -->\\n  <path d=\\\"M 115 130 C 115 110.7 130.7 95 150 95 C 169.3 95 185 110.7 185 130 C 185 149.3 169.3 165 150 165 C 130.7 165 115 149.3 115 130 Z\\\"/>\\n  <path d=\\\"M 125 130 C 125 116.2 136.2 105 150 105 C 163.8 105 175 116.2 175 130 C 175 143.8 163.8 155 150 155 C 136.2 155 125 143.8 125 130 Z\\\"/>\\n  \\n  <!-- Ears -->\\n  <path d=\\\"M 127 105 C 127 96.7 130.7 90 135 90 C 139.3 90 143 96.7 143 105 C 143 113.3 139.3 120 135 120 C 130.7 120 127 113.3 127 105 Z\\\"/>\\n  <path d=\\\"M 157 105 C 157 96.7 160.7 90 165 90 C 169.3 90 173 96.7 173 105 C 173 113.3 169.3 120 165 120 C 160.7 120 157 113.3 157 105 Z\\\"/>\\n  <path d=\\\"M 130 108 C 130 101.4 132.2 98 135 98 C 137.8 98 140 101.4 140 108 C 140 114.6 137.8 118 135 118 C 132.2 118 130 114.6 130 108 Z\\\"/>\\n  <path d=\\\"M 160 108 C 160 101.4 162.2 98 165 98 C 167.8 98 170 101.4 170 108 C 170 114.6 167.8 118 165 118 C 162.2 118 160 114.6 160 108 Z\\\"/>\\n  \\n  <!-- Eyes -->\\n  <path d=\\\"M 134 125 C 134 121.7 136.7 119 140 119 C 143.3 119 146 121.7 146 125 C 146 128.3 143.3 131 140 131 C 136.7 131 134 128.3 134 125 Z\\\"/>\\n  <path d=\\\"M 154 125 C 154 121.7 156.7 119 160 119 C 163.3 119 166 121.7 166 125 C 166 128.3 163.3 131 160 131 C 156.7 131 154 128.3 154 125 Z\\\"/>\\n  <path d=\\\"M 140 123 C 140 121.9 140.9 121 142 121 C 143.1 121 144 121.9 144 123 C 144 124.1 143.1 125 142 125 C 140.9 125 140 124.1 140 123 Z\\\"/>\\n  <path d=\\\"M 160 123 C 160 121.9 160.9 121 162 121 C 163.1 121 164 121.9 164 123 C 164 124.1 163.1 125 162 125 C 160.9 125 160 124.1 160 123 Z\\\"/>\\n  \\n  <!-- Nose -->\\n  <path d=\\\"M 147 140 C 147 139.1 148.3 138 150 138 C 151.7 138 153 139.1 153 140 C 153 140.9 151.7 142 150 142 C 148.3 142 147 140.9 147 140 Z\\\"/>\\n  \\n  <!-- Front paws -->\\n  <path d=\\\"M 122 180 C 122 171.7 125.6 165 130 165 C 134.4 165 138 171.7 138 180 C 138 188.3 134.4 195 130 195 C 125.6 195 122 188.3 122 180 Z\\\"/>\\n  <path d=\\\"M 162 180 C 162 171.7 165.6 165 170 165 C 174.4 165 178 171.7 178 180 C 178 188.3 174.4 195 170 195 C 165.6 195 162 188.3 162 180 Z\\\"/>\\n  \\n  <!-- Back paws -->\\n  <path d=\\\"M 123 240 C 123 230.1 128.4 222 135 222 C 141.6 222 147 230.1 147 240 C 147 249.9 141.6 258 135 258 C 128.4 258 123 249.9 123 240 Z\\\"/>\\n  <path d=\\\"M 153 240 C 153 230.1 158.4 222 165 222 C 171.6 222 177 230.1 177 240 C 177 249.9 171.6 258 165 258 C 158.4 258 153 249.9 153 240 Z\\\"/>\\n  \\n  <!-- Acorn -->\\n  <path d=\\\"M 114 170 C 114 165.6 116.7 162 120 162 C 123.3 162 126 165.6 126 170 C 126 174.4 123.3 178 120 178 C 116.7 178 114 174.4 114 170 Z\\\"/>\\n  <path d=\\\"M 116 165 C 116 163.3 117.8 162 120 162 C 122.2 162 124 163.3 124 165 C 124 166.7 122.2 168 120 168 C 117.8 168 116 166.7 116 165 Z\\\"/>\\n</svg>\"}"
    )
    tutorial_output = TutorialOutput.model_validate_json(response_tutorial)
    
    tutorial = Tutorial(
        **tutorial_output.model_dump(),
        concept=concept,
        model_name=model_name,
        svg_raw=response_svg,
        svg_sketch=response_svg_bw_parsed
    )

    return tutorial.model_dump()


