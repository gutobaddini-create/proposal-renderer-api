# Contrato da API — Renderizador de Propostas

## Base URL local

```text
http://localhost:8000
```

## Endpoint de saúde

```http
GET /health
```

### Resposta esperada

```json
{
  "status": "ok",
  "service": "proposal-renderer-api",
  "version": "0.1.0"
}
```

---

## Endpoint principal

```http
POST /generate-proposal
```

## Objetivo

Receber JSON estruturado de proposta e gerar arquivos.

## Entrada

O corpo da requisição deve seguir o padrão:

```json
{
  "schema_version": "proposal_renderer_v1",
  "document_type": "proposta_juridica",
  "metadata": {},
  "output": {
    "generatePdf": true,
    "generateVisualDocx": true,
    "generateEditableDocx": true
  },
  "provider": {},
  "client": {},
  "layoutPreferences": {},
  "proposal": {},
  "layoutPlan": [],
  "pendingFields": []
}
```

## Saída

```json
{
  "status": "success",
  "proposalId": "generated-id",
  "message": "Proposta gerada com sucesso.",
  "files": {
    "pdf": "/output/generated-id/proposta.pdf",
    "visualDocx": "/output/generated-id/proposta_visual.docx",
    "editableDocx": "/output/generated-id/proposta_editavel.docx"
  },
  "warnings": []
}
```

## Saída com erro

```json
{
  "status": "error",
  "message": "Descrição clara do erro.",
  "warnings": [],
  "details": {}
}
```

---

## Sanitização obrigatória

Antes de renderizar, a API deve substituir automaticamente:

```text
[advlobobaddini.erica@gmail.com](mailto:advlobobaddini.erica@gmail.com)
```

por:

```text
advlobobaddini.erica@gmail.com
```

Também deve remover qualquer `mailto:` encontrado em campos de e-mail.

## Campos críticos

A API deve validar:

- `provider.name`
- `provider.email`
- `client.name`
- `proposal.title`
- `proposal.investment.amountText`
- `proposal.term.duration`
- `layoutPlan`

Se campos críticos estiverem ausentes, deve retornar erro claro.

## Campos pendentes

Campos com `[informar]` são permitidos. Eles não devem bloquear a geração, mas podem gerar `warnings`.