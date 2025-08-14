import json
import re
from typing import Dict, List
from chatdraw.sketches.svg_utils import add_smooth_vectors_to_tutorial, parse_point_string_to_vector
from chatdraw.sketches.tutorial_agent_base import Step, TutorialAgent
from chatdraw.utils import get_db_connection

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
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # try to fetch an existing sketch
        cur.execute("""
            SELECT concept FROM sketch WHERE concept=%s LIMIT 1
        """, (concept,))
        answer_dict_curr = cur.fetchone()
        if answer_dict_curr is not None: 
            print(f"The {concept} concept is already available")
            return answer_dict_curr[0]
        # create new sketch
        answer_dict = TutorialAgent().create_tutorial(concept)
        # add it to the db
        cur.execute("""
            INSERT INTO sketch (concept, model_json, model_name)
            VALUES (%s, %s, %s)
        """, (concept, json.dumps(answer_dict), answer_dict["model_name"]))
        conn.commit()
        print(f"Added the {concept} to the db")
        return answer_dict
    finally:
        cur.close()
        conn.close()

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
    # First, try to fetch from postgres db
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT model_json FROM sketch WHERE concept = %s", (concept,))
        result = cur.fetchone()
        if result:
            # Found in database
            answer_dict = result[0]
        else:
            answer_dict = add_concept_to_db(concept)
    finally:
        cur.close()
        conn.close()
    tutorial = answer_dict["steps"]
    add_smooth_vectors_to_tutorial(tutorial)
    return tutorial



if __name__ == "__main__":
    print(load_tutorial("giraffe"))