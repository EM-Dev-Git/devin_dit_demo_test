from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, transcript, minutes, graph
from modules.database import engine, Base
from modules.logger import setup_logging
import os
from dotenv import load_dotenv

load_dotenv()

setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Transcript Minutes API",
    description="API for generating meeting minutes from transcripts using OpenAI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(transcript.router, prefix="/transcript", tags=["transcript"])
app.include_router(minutes.router, prefix="/minutes", tags=["minutes"])
app.include_router(graph.router, prefix="/graph", tags=["microsoft-graph"])

@app.get("/")
async def root():
    return {"message": "Transcript Minutes API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )
