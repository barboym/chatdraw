import json
import re
import xmltodict

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

def load_tutorial(path):
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
    return concept, tutorial


if __name__ == "__main__":
    # Example usage
    import subprocess
    import pathlib
    concept = "giraffe"
    log_path = f"/home/mos/exercises/SketchAgent/results/test/{concept}/experiment_log.json"
    if not pathlib.Path(log_path).exists(): # creating the sketch is costly
        subprocess.run(["/home/mos/miniconda3/envs/sketch_agent/bin/python", "/home/mos/exercises/SketchAgent/gen_sketch.py", "--concept_to_draw", concept])
    concept, tutorial = load_tutorial(log_path)