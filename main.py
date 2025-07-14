from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
from bpm import fetch_bpm

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_csv(file: UploadFile):
    df = pd.read_csv(file.file)
    df['BPM'] = df['Track name'].apply(fetch_bpm)
    output_path = "/tmp/output.csv"
    df.to_csv(output_path, index=False)
    return FileResponse(output_path, filename="library_with_bpm.csv")


@app.get("/")
def root():
    return {"message": "Stream-to-BPM backend is running."}
