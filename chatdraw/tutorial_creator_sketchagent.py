import json
import re
import xmltodict
import subprocess
import pathlib
import anthropic
from prompts import sketch_first_prompt, system_prompt, gt_example

def get_sketch(
    concept = 'caterpillar',
    model = 'claude-3-5-sonnet-20240620',
    sketch_first_prompt=sketch_first_prompt, 
    system_prompt=system_prompt, 
    gt_example=gt_example,
):
    return anthropic.Anthropic().messages.create(**{
        'model':model,
        'max_tokens':3000,
        'system': system_prompt.replace('{res}',str(50)),
        'messages':[{
            "role":"user",
            "content":sketch_first_prompt.replace('{concept}',concept).replace('{gt_sketches_str}',gt_example)
        }],
        'temperature':0,
        'top_k':1,
        'stop_sequences':['</answer>'],
    })

def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses 

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    match = re.search(f'<{tag}>(.*?)</{tag}>', text, re.DOTALL)
    return f'<{tag}>{match.group(1)}</{tag}>' if match else ""

def load_tutorial(concept):
    path = f"/home/mos/exercises/chatprojects/SketchAgent/results/test/{concept}/experiment_log.json"
    if not pathlib.Path(path).exists(): # creating the sketch is costly
        subprocess.run(
            ["/home/mos/miniconda3/envs/sketch_agent/bin/python", 
             "/home/mos/exercises/chatprojects/SketchAgent/gen_sketch.py", 
             "--concept_to_draw", 
             concept, 
             "--path2save",
             path,
            ])
    with open(path) as f:
        txt_response = json.load(f)[2]["content"][0]["text"]

    answer = extract_xml(txt_response+"</answer>","answer")
    answer_dict = xmltodict.parse(answer)
    concept = answer_dict["answer"]["concept"]
    strokes = answer_dict["answer"]["strokes"]
    # tvalues = answer_dict["answer"][""]
    tutorial = [{
        "name": el['id'],
        "points":el["points"],
        "t_values":el["t_values"]
    } for el in strokes.values()]
    return tutorial


if __name__ == "__main__":
    # Example usage
    tutorial = load_tutorial("giraffe")
