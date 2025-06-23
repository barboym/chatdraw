
# prompt_tutorial_template="""
# You are a painting instructor for students. 
# Assume your students are using a simple mspaint-like image editor. 
# They want to learn how to draw a basic black sketch of {{objective}}. 
# To be more practical, you need to create a 3-5 steps tutorial. 
# Each step need to have a JSON formatted description with a: 
# title, 2 sentence instruction, 5 sentence extended instruction, 
# and a few general tips. You are always starting from an empty white 
# 500x500 pixel image with light grey 100px grid. 
# Each steps should have a corresponding image example that adds a 
# little bit of complexity to the image of the previous step. 
# Write the tutorial without preambles.
# """

PROMPT_TUTORIAL_CREATION_TEMPLATE = ["""
You are a painting instructor for students.
Assume your students are using a simple mspaint-like image editor.
They want to learn how to draw a basic black sketch of <item>{{objective}}</item>.
To be more practical, you need to create a 4 steps tutorial.
Each step need to have a JSON formatted description with a title, 2 sentence instruction, 5 sentence extended instruction, and a few general tips.
Write the tutorial without preambles.
""","""
generate an image for each step.
Each image should be 500x500px with a white background, contain the example sketch and nothing else.
Each image should have few easy additional strokes relative to the previous step and image.
The images should be generated together in a 2x2 grid with the steps ordered from left to right and from up to bottom.
""","""
Correct the JSON tutorial to better fit the generated images. Write without preambles. 
"""]

from openai import OpenAI

def create_tutorial_for_item_sketching(item,tutorial_template=PROMPT_TUTORIAL_CREATION_TEMPLATE,verbose=False):
    """
    Probably Ill end up using the SketchAgent instead and just iterate on the strocks with the ids. 
    """
    client = OpenAI()
    history = []
    for prompt in tutorial_template:
        prompt = prompt.replace("{{objective}}",item)
        history += [
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = client.responses.create(
            model= "gpt-image-1" if prompt.startswith("generate an image") else "gpt-4o-mini",
            input=history,
            store=False,
        )
        if verbose:
            print(response.output_text)

        # Add the response to the conversation
        history += [{"role": el.role, "content": el.content} for el in response.output]
    return history


# print(second_response.output_text)
#     response = client.responses.create(
#         model="gpt-4o-mini",
#         input=[
#             {"role": "user", "content": "knock knock."},
#             {"role": "assistant", "content": "Who's there?"},
#             {"role": "user", "content": "Orange."},
#         ],
#     )
