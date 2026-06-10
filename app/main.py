from __future__ import annotations

from typing import Any

import os

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError

from app.file_manager import OUTPUT_DIR, build_proposal_id, prepare_output_dir, public_output_url
from app.generators.editable_docx_generator import generate_editable_docx
from app.generators.pdf_generator import generate_pdf
from app.generators.visual_docx_generator import generate_visual_docx_placeholder
from app.models import ErrorResponse, GenerateProposalResponse, GeneratedFiles, ProposalRequest
from app.security import verify_api_key
from app.sanitizer import collect_warnings, sanitize_proposal_json


app = FastAPI(title="Proposal Renderer API", version="0.1.0")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/files", StaticFiles(directory=OUTPUT_DIR), name="files")


def get_files_base_url(request: Request) -> str:
    configured_base_url = os.getenv("OUTPUT_BASE_URL", "").strip()
    if configured_base_url:
        return configured_base_url
    return str(request.base_url).rstrip("/") + "/files"


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail if isinstance(exc.detail, dict) else {"message": str(exc.detail)}
    return JSONResponse(status_code=exc.status_code, content=detail)


@app.get("/health", dependencies=[Depends(verify_api_key)])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "proposal-renderer-api", "version": "0.1.0"}


@app.get("/render-health")
def render_health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/generate-proposal",
    response_model=GenerateProposalResponse,
    dependencies=[Depends(verify_api_key)],
)
async def generate_proposal(request: Request) -> GenerateProposalResponse:
    raw_payload: dict[str, Any] = await request.json()
    sanitized_payload = sanitize_proposal_json(raw_payload)

    try:
        proposal_request = ProposalRequest.model_validate(sanitized_payload)
    except ValidationError as exc:
        error = ErrorResponse(
            status="error",
            message="JSON inválido ou campos obrigatórios ausentes.",
            details={"errors": exc.errors()},
        )
        raise HTTPException(status_code=400, detail=error.model_dump())

    proposal_data = proposal_request.model_dump(mode="json")
    warnings = collect_warnings(proposal_data)
    proposal_id = build_proposal_id(proposal_data.get("metadata"))
    output_dir = prepare_output_dir(proposal_id)
    files_base_url = get_files_base_url(request)

    files = GeneratedFiles()
    if proposal_request.output.generatePdf:
        files.pdf = public_output_url(generate_pdf(proposal_data, output_dir), files_base_url)
    if proposal_request.output.generateEditableDocx:
        files.editableDocx = public_output_url(generate_editable_docx(proposal_data, output_dir), files_base_url)
    if proposal_request.output.generateVisualDocx:
        files.visualDocx = public_output_url(
            generate_visual_docx_placeholder(proposal_data, output_dir),
            files_base_url,
        )

    return GenerateProposalResponse(
        status="success",
        proposalId=proposal_id,
        message="Proposta gerada com sucesso.",
        files=files,
        warnings=warnings,
    )
