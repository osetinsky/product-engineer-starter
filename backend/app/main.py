from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from . import models, schemas, database

import logging
import json

logging.basicConfig(level=logging.INFO)

app = FastAPI()

MAX_CASES_PER_INDEX_REQUEST = 3

# load the mock json templates for interpolation
def load_response_templates():
    templates = {}
    for i in range(1, 4):
        with open(f"assets/response-{i}.json", "r") as file:
            templates[i] = json.load(file)
    return templates

# load templates once at startup
RESPONSE_TEMPLATES = load_response_templates()

# select the appropriate response template based on elapsed time
def select_response_template(elapsed):
    if elapsed < 10:
        return RESPONSE_TEMPLATES[1].copy()
    elif elapsed < 30:
        return RESPONSE_TEMPLATES[2].copy()
    return RESPONSE_TEMPLATES[3].copy()

# note: we should make allowed fields explicit for security purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/cases/", response_model=dict)
def create_case(db: Session = Depends(database.get_db)):
    db_case = models.Case()
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return {"case_id": db_case.id}

@app.get("/cases/{case_id}", response_model=schemas.Case)
def get_case(case_id: str, db: Session = Depends(database.get_db)):
    db_case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    
    now = datetime.now(timezone.utc)
    elapsed = (now - db_case.created_at).total_seconds()

    logging.info(f"now: {now}")
    logging.info(f"Elapsed time for case {case_id}: {elapsed} seconds")

    response = select_response_template(elapsed)

    response["case_id"] = db_case.id
    response["created_at"] = db_case.created_at.isoformat()

    schemas.Case(**response)  # Validate the response against the schema
    
    return response

@app.get("/cases/", response_model=List[schemas.Case])
def get_cases(db: Session = Depends(database.get_db)):
    # NOTE: we're limiting to only 3 cases based on the value of the MAX_CASES_PER_INDEX_REQUEST constant
    # provide pagination params that we can pass to the query as needed to retrieve and respond with additional
    # records beyond the first three in reverse chronological order of created_at
    db_cases = db.query(models.Case).order_by(desc(models.Case.created_at)).limit(MAX_CASES_PER_INDEX_REQUEST).all()
    now = datetime.now(timezone.utc)
    responses = []

    for db_case in db_cases:
        elapsed = (now - db_case.created_at).total_seconds()
        response = select_response_template(elapsed)

        response["case_id"] = db_case.id
        response["created_at"] = db_case.created_at.isoformat()

        try:
            validated_response = schemas.Case(**response)
            responses.append(validated_response)
        except Exception as e:
            logging.error(f"Error validating response for case {db_case.id}: {str(e)}")
            continue

    return responses
