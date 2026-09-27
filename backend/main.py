import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from hindsight_client import Hindsight


# ============================================================
# Configuration
# ============================================================

load_dotenv()

HINDSIGHT_API_URL = os.getenv("HINDSIGHT_API_URL")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID")

if not HINDSIGHT_API_URL:
    raise RuntimeError("HINDSIGHT_API_URL is missing from .env")

if not HINDSIGHT_API_KEY:
    raise RuntimeError("HINDSIGHT_API_KEY is missing from .env")

if not HINDSIGHT_BANK_ID:
    raise RuntimeError("HINDSIGHT_BANK_ID is missing from .env")


# ============================================================
# Hindsight Client
# ============================================================

hindsight = Hindsight(
    base_url=HINDSIGHT_API_URL,
    api_key=HINDSIGHT_API_KEY,
)


# ============================================================
# FastAPI App
# ============================================================

app = FastAPI(
    title="OpsMemory",
    description="AI Incident Response Agent powered by Hindsight",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"status": "online", "service": "OpsMemory"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request Models
# ============================================================

class IncidentRequest(BaseModel):
    incident: str


class ResolveRequest(BaseModel):
    incident: str
    resolution: str


# ============================================================
# Health Check
# ============================================================

@app.get("/api/health")
async def health():
    return {
        "status": "online",
        "service": "OpsMemory",
        "memory": "Hindsight",
        "bank_id": HINDSIGHT_BANK_ID,
    }


# ============================================================
# Analyze Incident
# ============================================================

@app.post("/api/analyze")
async def analyze_incident(request: IncidentRequest):

    incident = request.incident.strip()

    if not incident:
        raise HTTPException(
            status_code=400,
            detail="Incident description cannot be empty."
        )

    try:

        # ----------------------------------------------------
        # STEP 1: Recall previous incidents
        # ----------------------------------------------------

        memory_response = await hindsight.arecall(
            bank_id=HINDSIGHT_BANK_ID,
            query=incident,
            max_tokens=3000,
        )

        memories = []

        for result in memory_response.results:
            if result.text:
                memories.append(result.text)


        # ----------------------------------------------------
        # STEP 2: Ask Hindsight to reason over memory
        # ----------------------------------------------------

        reflection_query = f"""
You are an experienced production incident response engineer.

A new production incident has occurred:

{incident}

Use the relevant historical incidents stored in your memory bank
to help analyze this incident.

Provide:

1. Likely root cause
2. Recommended investigation steps
3. Recommended resolution
4. Relevant previous incident(s)
5. What was learned from those previous incidents

Important:
- Clearly distinguish historical evidence from your inference.
- Do not invent incident history.
- If there is insufficient historical evidence, say so.
- Prefer previously successful resolutions when they are relevant.
"""

        reflection = await hindsight.areflect(
            bank_id=HINDSIGHT_BANK_ID,
            query=reflection_query,
            budget="mid",
            max_tokens=2500,
            include_facts=True,
        )


        # ----------------------------------------------------
        # STEP 3: Return memory + reasoning to frontend
        # ----------------------------------------------------

        return {
            "status": "success",
            "incident": incident,
            "memories_found": len(memories),
            "memories": memories,
            "analysis": reflection.text,
        }

    except Exception as error:

        print(f"ANALYZE ERROR: {error}")

        raise HTTPException(
            status_code=500,
            detail="Unable to analyze the incident using Hindsight."
        )


# ============================================================
# Resolve + Learn
# ============================================================

@app.post("/api/resolve")
async def resolve_incident(request: ResolveRequest):

    incident = request.incident.strip()
    resolution = request.resolution.strip()

    if not incident:
        raise HTTPException(
            status_code=400,
            detail="Incident description cannot be empty."
        )

    if not resolution:
        raise HTTPException(
            status_code=400,
            detail="Resolution cannot be empty."
        )

    try:

        # ----------------------------------------------------
        # Store the new incident + successful resolution
        # ----------------------------------------------------

        memory_content = f"""
Production Incident

Incident:
{incident}

Resolution:
{resolution}

Outcome:
The incident was resolved using the resolution described above.

Learning:
This incident and its successful resolution should be considered
when handling similar production incidents in the future.
"""

        await hindsight.aretain(
            bank_id=HINDSIGHT_BANK_ID,
            content=memory_content,
            context="production incident and successful resolution",
        )

        return {
            "status": "success",
            "message": "Incident resolution stored in Hindsight.",
            "learned": True,
        }

    except Exception as error:

        print(f"RESOLVE ERROR: {error}")

        raise HTTPException(
            status_code=500,
            detail="Unable to store the incident in Hindsight."
        )