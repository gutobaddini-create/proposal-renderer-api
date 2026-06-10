from __future__ import annotations

from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from uuid import uuid4


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"


def build_proposal_id(metadata: dict | None = None) -> str:
    metadata = metadata or {}
    raw_id = metadata.get("proposalId") or metadata.get("proposal_id") or metadata.get("id")
    if raw_id:
        return str(raw_id).strip().replace("/", "-").replace("\\", "-")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"proposal_{timestamp}_{uuid4().hex[:8]}"


def prepare_output_dir(proposal_id: str) -> Path:
    path = OUTPUT_DIR / proposal_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def public_output_url(path: Path, base_url: str) -> str:
    relative_path = path.relative_to(OUTPUT_DIR).as_posix()
    encoded_path = "/".join(quote(part) for part in relative_path.split("/"))
    return f"{base_url.rstrip('/')}/{encoded_path}"
