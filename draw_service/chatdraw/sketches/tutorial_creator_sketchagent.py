import json
import re
from typing import Dict, List
from chatdraw.sketches.svg_utils import add_smooth_vectors_to_tutorial
from chatdraw.sketches.tutorial_agent_svg_examples import TutorialAgentSVGExmaples
from chatdraw.db import get_db_session, Sketch
from dotenv import load_dotenv


load_dotenv()

DEFAULT_TUTORIAL_LIST = (
    "giraffe",
    "monkey",
    "banana",
    "speaker",
    "superman",
    "pen-pineapple-apple-pen",
)


def add_concept_to_db(concept) -> Dict:
    with get_db_session() as session:
        existing = session.query(Sketch).filter(Sketch.concept == concept).first()
        if existing is not None:
            print(f"The {concept} concept is already available")
            return existing.model_json
        answer_dict = TutorialAgentSVGExmaples().create_tutorial(concept)
        sketch = Sketch(concept=concept, model_json=json.dumps(answer_dict), model_name=answer_dict["model_name"])
        session.add(sketch)
        session.commit()
        print(f"Added the {concept} to the db")
        return answer_dict

def normalize_concept_string(s: str) -> str:
    """
    Normalizes a string by:
    - Lowercasing
    - Removing special characters (keeps alphanumerics and spaces)
    - Removing articles ('a', 'an', 'the')
    - Removing extra whitespace
    - Stripping leading/trailing spaces

    Args:
        s (str): Input string

    Returns:
        str: Normalized string
    """
    # Lowercase
    s = s.lower()
    # Remove special characters (keep alphanumerics and spaces)
    s = re.sub(r'[^a-z0-9\s]', '', s)
    # Remove articles from the start, even if there are multiple
    s = re.sub(r'^((a|an|the)\s+)+', '', s)
    # Remove extra whitespace
    s = re.sub(r'\s+', ' ', s)
    # Strip leading/trailing spaces
    s = s.strip()
    return s
        

def load_tutorial(concept:str) -> List[dict]:
    """
    General method for fetching tutorials
    """
    concept = normalize_concept_string(concept)
    # First, try to fetch from db
    with get_db_session() as session:
        row = session.query(Sketch.model_json).filter(Sketch.concept == concept).first()
    if row:
        answer_dict = json.loads(row[0])
    else:
        answer_dict = add_concept_to_db(concept)
    tutorial = answer_dict["steps"]
    add_smooth_vectors_to_tutorial(tutorial)
    return tutorial



if __name__ == "__main__":
    print(load_tutorial("giraffe"))