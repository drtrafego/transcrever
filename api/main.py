from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
from datetime import datetime
import os
import uuid
import shutil

try:
    from services.audio import extract_mp3_from_video
    from services.whisper_engine import transcribe_audio_file
except ImportError:
    from .services.audio import extract_mp3_from_video
    from .services.whisper_engine import transcribe_audio_file

BASE_DIR = Path(__file__).parent.parent
VIDEOS_DIR = BASE_DIR / "videos"
TRANSCRICAO_DIR = BASE_DIR / "transcrição"

VIDEOS_DIR.mkdir(exist_ok=True)
TRANSCRICAO_DIR.mkdir(exist_ok=True)

JOBS: dict = {}

ALLOWED_EXTENSIONS = {".mp4", ".m4a", ".ogg", ".wav", ".mp3", ".webm"}

app = FastAPI(
    title="Video Transcription API",
    description="API Gratuita Local para Conversao MP4/Transcricoes Turbo"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://transcrever.casaldotrafego.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranscribeRequest(BaseModel):
    video_path: str
    language: Optional[str] = "pt"


class JobsRequest(BaseModel):
    files: list[str]
    language: str = "pt"


@app.get("/")
def home():
    return {
        "message": "API de Transcricao Local Operacional!",
        "doc_url": "Acesse http://127.0.0.1:8000/docs para ver e testar o painel interativo Swagger."
    }


@app.post("/transcribe")
def transcribe_video(req: TranscribeRequest):
    video_path = req.video_path

    if not os.path.exists(video_path):
        raise HTTPException(
            status_code=404,
            detail=f"O arquivo de video inserido nao foi encontrado: {video_path}"
        )

    mp3_tmp_path = None
    try:
        mp3_tmp_path = extract_mp3_from_video(video_path)
        text_result = transcribe_audio_file(mp3_tmp_path, language=req.language)

        return {
            "status": "success",
            "video": os.path.basename(video_path),
            "text": text_result,
            "language": req.language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if mp3_tmp_path and os.path.exists(mp3_tmp_path):
            os.remove(mp3_tmp_path)


@app.get("/videos")
def list_videos():
    files = []
    for f in VIDEOS_DIR.iterdir():
        if f.is_file() and f.suffix.lower() in ALLOWED_EXTENSIONS:
            files.append({
                "name": f.name,
                "size": f.stat().st_size,
                "extension": f.suffix.lower(),
            })
    return files


@app.post("/videos/upload")
async def upload_video(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Extensao nao suportada: {ext}")

    dest = VIDEOS_DIR / file.filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "size": dest.stat().st_size}


def _run_job(job_id: str, filename: str, language: str):
    JOBS[job_id]["status"] = "processing"
    mp3_tmp_path = None
    try:
        video_path = VIDEOS_DIR / filename
        mp3_tmp_path = extract_mp3_from_video(str(video_path))
        text_result = transcribe_audio_file(mp3_tmp_path, language=language)

        date_str = datetime.now().strftime("%Y-%m-%d")
        output_dir = TRANSCRICAO_DIR / date_str
        output_dir.mkdir(parents=True, exist_ok=True)

        stem = Path(filename).stem
        output_file = output_dir / f"{stem}.txt"
        output_file.write_text(text_result, encoding="utf-8")

        JOBS[job_id]["status"] = "done"
        JOBS[job_id]["output_path"] = str(output_file.relative_to(BASE_DIR))
    except Exception as e:
        JOBS[job_id]["status"] = "error"
        JOBS[job_id]["error"] = str(e)
    finally:
        if mp3_tmp_path and os.path.exists(mp3_tmp_path):
            os.remove(mp3_tmp_path)


@app.post("/jobs")
def create_jobs(req: JobsRequest, background_tasks: BackgroundTasks):
    created = []
    for filename in req.files:
        video_path = VIDEOS_DIR / filename
        if not video_path.exists():
            raise HTTPException(status_code=404, detail=f"Arquivo nao encontrado: {filename}")

        job_id = str(uuid.uuid4())
        JOBS[job_id] = {
            "job_id": job_id,
            "filename": filename,
            "status": "pending",
            "output_path": None,
            "error": None,
        }
        background_tasks.add_task(_run_job, job_id, filename, req.language)
        created.append({"job_id": job_id, "filename": filename})

    return {"jobs": created}


@app.get("/jobs")
def list_jobs():
    return list(JOBS.values())


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job nao encontrado")
    return job


@app.get("/transcricoes")
def list_transcricoes():
    result = []
    if not TRANSCRICAO_DIR.exists():
        return result

    for date_dir in sorted(TRANSCRICAO_DIR.iterdir(), reverse=True):
        if not date_dir.is_dir():
            continue
        files = []
        for f in sorted(date_dir.iterdir()):
            if f.is_file() and f.suffix == ".txt":
                files.append({
                    "name": f.name,
                    "size": f.stat().st_size,
                    "path": f"{date_dir.name}/{f.name}",
                })
        if files:
            result.append({"date": date_dir.name, "files": files})

    return result


@app.get("/transcricoes/{date}/{filename}")
def download_transcricao(date: str, filename: str):
    file_path = TRANSCRICAO_DIR / date / filename
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Arquivo nao encontrado")

    return FileResponse(
        path=str(file_path),
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
