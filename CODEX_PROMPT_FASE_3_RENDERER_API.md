# Prompt para Codex — Fase 3 Renderizador API

Você está trabalhando no projeto **Renderizador de Propostas Jurídicas**.

Objetivo:
Criar uma API em Python/FastAPI que receba um JSON estruturado de proposta jurídica e gere arquivos de saída.

Leia os arquivos:

- `FASE_3_ACTION_API_RENDERIZADOR.md`
- `API_CONTRACT.md`
- `ROADMAP_RENDERER_BACKEND.md`
- `OPENAPI_SCHEMA_ACTION.yaml`

## Stack obrigatória

Use:

- Python 3.12+
- FastAPI
- Uvicorn
- Pydantic
- ReportLab
- python-docx
- Pillow
- pypdfium2, se necessário para Word visual

## Tarefa inicial

Implemente somente a primeira versão funcional da API.

Crie:

1. Estrutura de projeto.
2. `requirements.txt`.
3. `app/main.py`.
4. Endpoint `GET /health`.
5. Endpoint `POST /generate-proposal`.
6. Modelos Pydantic básicos.
7. Função `sanitize_proposal_json`.
8. Sanitização obrigatória de e-mails markdown e `mailto:`.
9. Geração de PDF simples usando ReportLab.
10. Geração de Word editável simples usando python-docx.
11. Retorno JSON com paths dos arquivos gerados.
12. Pasta `output/`.
13. Teste com JSON de exemplo da Bovmeat.

## Regra crítica

Antes de gerar qualquer arquivo, a API deve substituir qualquer ocorrência de:

`[advlobobaddini.erica@gmail.com](mailto:advlobobaddini.erica@gmail.com)`

por:

`advlobobaddini.erica@gmail.com`

Também deve remover qualquer `mailto:` presente em campos de e-mail.

## Estrutura sugerida

```text
proposal-renderer-api/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── sanitizer.py
│   ├── file_manager.py
│   └── generators/
│       ├── pdf_generator.py
│       ├── editable_docx_generator.py
│       └── visual_docx_generator.py
├── sample_data/
│   └── bovmeat.json
├── output/
├── tests/
├── requirements.txt
└── README.md
```

## Critérios de aceite

A tarefa só estará concluída quando:

- `uvicorn app.main:app --reload` iniciar a API;
- `GET /health` retornar status ok;
- `POST /generate-proposal` aceitar o JSON da Bovmeat;
- a API gerar pelo menos PDF e Word editável;
- os arquivos forem salvos em `output/{proposalId}/`;
- a resposta trouxer os caminhos dos arquivos;
- o e-mail não aparecer com `mailto:` em nenhum conteúdo processado;
- o README explicar como rodar e testar.