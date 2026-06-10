from __future__ import annotations

import re
from typing import Any


LABEL_TRANSLATIONS = {
    "acceptance": "Aceite",
    "acceptance text": "Texto de aceite",
    "acceptance_text": "Texto de aceite",
    "acceptancetext": "Texto de aceite",
    "client": "Contratante",
    "client name": "Nome do contratante",
    "client_name": "Nome do contratante",
    "clientname": "Nome do contratante",
    "contractor": "Contratante",
    "customer": "Contratante",
    "provider": "Proponente",
    "provider name": "Nome do proponente",
    "provider_name": "Nome do proponente",
    "providername": "Nome do proponente",
    "responsibility": "Responsabilidade",
    "responsibilities": "Responsabilidades",
    "responsible": "Responsável",
    "scope": "Escopo",
    "object": "Objeto",
    "objective": "Objetivo",
    "conditions": "Condições",
    "investment": "Investimento",
    "term": "Prazo",
    "deadline": "Prazo",
    "duration": "Duração",
    "price": "Investimento",
    "amount": "Valor",
    "contact": "Contato",
    "email": "E-mail",
    "phone": "Telefone",
    "address": "Endereço",
    "signature": "Assinatura",
    "signatures": "Assinaturas",
    "proposal": "Proposta",
}


PHRASE_TRANSLATIONS = {
    "Acceptance Text": "Texto de aceite",
    "Acceptance": "Aceite",
    "Client": "Contratante",
    "Provider": "Proponente",
    "Responsibility": "Responsabilidade",
    "Responsibilities": "Responsabilidades",
}


def _split_identifier(value: str) -> str:
    value = re.sub(r"[_\-]+", " ", value)
    value = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def translate_label(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    normalized = _split_identifier(text)
    key = normalized.lower()
    return LABEL_TRANSLATIONS.get(key, normalized)


def translate_known_phrases(value: Any) -> str:
    text = str(value or "")
    for source, target in PHRASE_TRANSLATIONS.items():
        text = text.replace(source, target)
    return text
