import pytest
from sqlalchemy import select
from datetime import datetime
from typing import Dict, Any
from chatdraw.db import Sketch, get_db_session

def test_sketch_insert_and_query():
    with get_db_session() as session:
        session.begin()
        try:
            concept = "unit_test_concept"
            model_json: Dict[str, Any] = {"shapes": ["circle", "square"]}
            model_name = "test_model"
            sketch = Sketch(
                concept=concept,
                model_json=model_json,
                model_name=model_name
            )
            session.add(sketch)
            session.flush()
            fetched_sketch = session.execute(
                select(Sketch).where(Sketch.concept == concept)
            ).scalar_one()
            assert fetched_sketch.concept == concept
            assert fetched_sketch.model_json == model_json
            assert fetched_sketch.model_name == model_name
            assert isinstance(fetched_sketch.create_time, datetime)
        finally:
            session.rollback()

def test_sketch_unique_concept_constraint():
    with get_db_session() as session:
        session.begin()
        try:
            concept = "unique_concept"
            model_json = {"a": 1}
            model_name = "model"
            sketch1 = Sketch(concept=concept, model_json=model_json, model_name=model_name)
            session.add(sketch1)
            session.flush()
            sketch2 = Sketch(concept=concept, model_json=model_json, model_name=model_name)
            session.add(sketch2)
            with pytest.raises(Exception):
                session.flush()
        finally:
            session.rollback()