# Proposal Renderer API

API FastAPI para receber um JSON estruturado de proposta jurídica e gerar arquivos em PDF e Word editável.

## Variáveis de ambiente

Crie as variáveis abaixo antes de rodar a API:

```powershell
$env:PROPOSAL_RENDERER_API_KEY="troque_por_uma_chave_segura"
$env:OUTPUT_BASE_URL="http://localhost:8000/files"
```

Em produção, use a URL HTTPS pública:

```text
OUTPUT_BASE_URL=https://seu-servico.onrender.com/files
```

## Como rodar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A API sobe em:

```text
http://localhost:8000
```

## Health check

Todos os endpoints da API exigem o header `X-API-Key`.

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/health" `
  -Headers @{ "X-API-Key" = $env:PROPOSAL_RENDERER_API_KEY }
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "proposal-renderer-api",
  "version": "0.1.0"
}
```

## Gerar proposta Bovmeat

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://localhost:8000/generate-proposal" `
  -Headers @{ "X-API-Key" = $env:PROPOSAL_RENDERER_API_KEY } `
  -ContentType "application/json" `
  -InFile "sample_data/bovmeat.json"
```

Os arquivos são salvos em:

```text
output/{proposalId}/
```

E servidos publicamente pela API em:

```text
http://localhost:8000/files/{proposalId}/{arquivo}
```

Nesta versão, a API gera:

- `proposta.pdf`
- `proposta_editavel.docx`
- `proposta_visual.docx`, como placeholder se `generateVisualDocx` vier habilitado

## Deploy

Para Render ou Railway, configure:

```text
Build command: pip install -r requirements.txt
Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Variáveis de ambiente:

```text
PROPOSAL_RENDERER_API_KEY=sua_chave_segura
OUTPUT_BASE_URL=https://sua-api-publica.com/files
```

Também há um `Dockerfile` para plataformas que aceitam deploy via container.

## GPT Action

Use o arquivo:

```text
OPENAPI_SCHEMA_ACTION_COM_API_KEY.yaml
```

No editor de Actions do GPT, configure autenticação por API Key:

```text
Auth type: API Key
Header name: X-API-Key
API key: mesma chave de PROPOSAL_RENDERER_API_KEY
```

Substitua `https://SEU-DOMINIO-DA-API.com` pela URL HTTPS real da API.

## Sanitização obrigatória

Antes de gerar qualquer arquivo, a API percorre todo o JSON e converte links de e-mail em markdown, como:

```text
[advlobobaddini.erica@gmail.com](mailto:advlobobaddini.erica@gmail.com)
```

para:

```text
advlobobaddini.erica@gmail.com
```

Também remove qualquer prefixo `mailto:` encontrado em strings aninhadas.
