from __future__ import annotations

import os
import secrets

from fastapi import Header, HTTPException


def verify_api_key(x_api_key: str = Header(default="", alias="X-API-Key")) -> None:
    expected_api_key = os.getenv("PROPOSAL_RENDERER_API_KEY", "")
    if not expected_api_key:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "PROPOSAL_RENDERER_API_KEY não configurada.",
                "warnings": [],
                "details": {},
            },
        )
    if not x_api_key or not secrets.compare_digest(x_api_key, expected_api_key):
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "message": "API key inválida ou ausente.",
                "warnings": [],
                "details": {},
            },
        )
