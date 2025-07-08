import json
import re
import xmltodict
import pathlib
import anthropic
from chatdraw.utils import get_db_connection
from prompts import sketch_first_prompt, system_prompt, gt_example
import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_sketch_using_anthropic_llm(
    concept,
    model = 'claude-sonnet-4-20250514',
    sketch_first_prompt=sketch_first_prompt, 
    system_prompt=system_prompt, 
    gt_example=gt_example,
    res=50,
):
    return anthropic.Anthropic().messages.create(**{
        'model':model,
        'max_tokens':3000,
        'system': system_prompt.replace('{res}',str(res)),
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

def add_concept_to_db(concept):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        model_response = get_sketch_using_anthropic_llm(concept)
        txt_response = model_response.content[0].text
        answer = extract_xml(txt_response+"</answer>", "answer")
        answer_dict = xmltodict.parse(answer)
        model_name = model_response.model
        cur.execute("""
            SELECT concept FROM sketch WHERE concept=%s
        """, (concept,))
        if cur.fetchone() is not None: 
            print("This concept is already available")
            return 
        cur.execute("""
            INSERT INTO sketch (concept, model_json, model_name)
            VALUES (%s, %s, %s)
        """, (concept, json.dumps(answer_dict), model_name))
        return answer_dict
    finally:
        cur.close()
        conn.close()

    
def load_tutorial(concept):
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
    return answer_dict


if __name__ == "__main__":
    # Example usage
    tutorial = load_tutorial("giraffe")
    print(tutorial)
