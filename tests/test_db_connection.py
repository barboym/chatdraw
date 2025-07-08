

from chatdraw.utils import get_db_connection
import json

def test_connection_works():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT sketch_id FROM sketch WHERE concept = 'giraffe'")
    result = cur.fetchone()

def test_insert_query():
    conn = get_db_connection()
    cur = conn.cursor()
    conn.autocommit = False  # start transaction
    try:
       
        model_json = {'q':['a','b']}
        cur.execute("""
            INSERT INTO sketch (concept, model_json, model_name)
            VALUES (%s, %s, %s)
        """, ('test', json.dumps(model_json), 'model_test'))

        cur.execute("SELECT model_json FROM sketch WHERE concept='test'")
        model_json_fetch = cur.fetchone()
        assert str((model_json,))==str(model_json_fetch)  # check what would be inserted

          # undo insert
        # print("Rolled back successfully.")

    finally:
        conn.rollback()
        cur.close()
        conn.close()

if __name__=="__main__":

    test_insert_query()