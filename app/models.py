from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class OutputOptions(BaseModel):
    model_config = ConfigDict(extra="allow")

    generatePdf: bool = True
    generateVisualDocx: bool = False
    generateEditableDocx: bool = True


class Provider(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str = Field(min_length=1)
    email: str = Field(min_length=1)


class Client(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str = Field(min_length=1)
    email: str | None = None


class Investment(BaseModel):
    model_config = ConfigDict(extra="allow")

    amountText: str


class Term(BaseModel):
    model_config = ConfigDict(extra="allow")

    duration: str


class ProposalDetails(BaseModel):
    model_config = ConfigDict(extra="allow")

    title: str = Field(min_length=1)
    investment: Investment
    term: Term


class ProposalRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    schema_version: str = "proposal_renderer_v1"
    document_type: str = "proposta_juridica"
    metadata: dict[str, Any] = Field(default_factory=dict)
    output: OutputOptions = Field(default_factory=OutputOptions)
    provider: Provider
    client: Client
    layoutPreferences: dict[str, Any] = Field(default_factory=dict)
    proposal: ProposalDetails
    layoutPlan: list[dict[str, Any]]
    pendingFields: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_layout_plan(self) -> "ProposalRequest":
        if not self.layoutPlan:
            raise ValueError("layoutPlan deve conter pelo menos uma seção.")
        return self


class GeneratedFiles(BaseModel):
    pdf: str | None = None
    visualDocx: str | None = None
    editableDocx: str | None = None


class GenerateProposalResponse(BaseModel):
    status: Literal["success"]
    proposalId: str
    message: str
    files: GeneratedFiles
    warnings: list[str] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    status: Literal["error"]
    message: str
    warnings: list[str] = Field(default_factory=list)
    details: dict[str, Any] = Field(default_factory=dict)
