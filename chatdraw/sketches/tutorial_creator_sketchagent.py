import itertools
import json
import re
from typing import Dict
from chatdraw.sketches.svg_utils import DEFAULT_RES, add_smooth_vectors_to_tutorial, add_vectors_to_tutorial
from chatdraw.sketches.tutorial_structure import HOUSE_EXAMPLE
from chatdraw.utils import get_db_connection
from chatdraw.sketches.tutorial_structure import LLMOutput
from llama_index.llms.anthropic import Anthropic
from llama_index.core.llms import ChatMessage
from chatdraw.sketches.prompts import sketch_prompt, system_prompt

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
        model_name='claude-sonnet-4-20250514'
        llm = Anthropic(
            model=model_name, 
            max_tokens=3000,
            temperature=0,
        ).as_structured_llm(LLMOutput)
        messages = [
            ChatMessage(role="system", content=system_prompt.replace("{res}",str(DEFAULT_RES))),
            ChatMessage(role="user", content=sketch_prompt.replace("{concept}",concept).replace("{gt_sketches_str}",HOUSE_EXAMPLE.model_dump_json())),
        ]
        # parsing response into the structure used up till now
        chat_response = llm.chat(messages,top_k=1,)
        tutorial_dict = json.loads(chat_response.message.blocks[0].text)
        tutorial_dict["strokes"]=list(itertools.chain(*[el["strokes"] for el in tutorial_dict["steps"]]))
        answer_dict = {"answer":tutorial_dict}
        # add it to the db
        cur.execute("""
            INSERT INTO sketch (concept, model_json, model_name)
            VALUES (%s, %s, %s)
        """, (concept, json.dumps(answer_dict), model_name))
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
    
def load_tutorial(concept:str) -> Dict:
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
    add_vectors_to_tutorial(answer_dict)
    add_smooth_vectors_to_tutorial(answer_dict)
    return answer_dict



if __name__ == "__main__":
    print(load_tutorial("giraffe"))