from fastapi import (
    FastAPI, 
    Path, 
    Query, 
    Depends, 
    HTTPException,
    UploadFile,
    File,
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from pydantic import BaseModel, Field

# database
from db import models
from db.database import engine, SessionLocal
from sqlalchemy.orm import Session

from Bio import SeqIO
from predict import predict_seq

# temporary file
from tempfile import NamedTemporaryFile

## Start API
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    try: 
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Inference(BaseModel):
    fasta_id: str = Field(min_length=1)
    filename: str = Field(min_length=1)
    prediction: str = Field(min_length=1)
    confidence: float = Field()


# request
@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Inference).all()


# post
@app.post("/predict")
async def predict_model(file: UploadFile = File(...), db: Session = Depends(get_db)):

    # temporary file
    contents = await file.read()
    file_copy = NamedTemporaryFile('wb', delete=False)
    with file_copy as f: 
        f.write(contents)
    
    record = SeqIO.parse(file_copy.name, "fasta")
    fasta = next(record)
    prediction, confidence = predict_seq(str(fasta.seq))
    file_copy.close()

    inference_model = models.Inference()
    inference_model.fasta_id = str(fasta.id)
    inference_model.filename = file.filename
    inference_model.confidence = confidence
    inference_model.prediction = prediction

    db.add(inference_model)
    db.commit()
    
    json_response = inference_model.to_dict()
    

    return JSONResponse(
        content = json_response# {"prediction": "Exito"}
    )

# post


# delete


# save fasta