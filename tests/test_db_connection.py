import pytest
from sqlalchemy import select

from chatdraw.db import Sketch, get_db_session


def test_connection_works():
    with get_db_session() as session:
        _ = session.execute(select(Sketch.sketch_id).limit(1)).first()


def test_insert_query():
    with get_db_session() as session:
        session.begin()
        concept = 'test'
        model_json = {'q':['a','b']}
        try:
            sketch = Sketch(concept=concept, model_json=model_json, model_name='model_test')
            session.add(sketch)
            session.flush()
            fetched = session.execute(select(Sketch.model_json).where(Sketch.concept==concept)).scalar_one()
            assert model_json == fetched
        finally:
            session.rollback()

if __name__=="__main__":
    test_connection_works()
    test_insert_query()