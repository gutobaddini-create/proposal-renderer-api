# Proposal Renderer API

API FastAPI para receber um JSON estruturado de proposta jurídica e gerar arquivos em PDF, Word visual e Word editável.

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
- `proposta_visual.docx`, com as páginas do PDF renderizadas como imagens A4

## Deploy

Para Render, o repositório inclui `render.yaml`. No painel do Render:

1. Clique em `New`.
2. Escolha `Blueprint`.
3. Conecte o repositório `gutobaddini-create/proposal-renderer-api`.
4. Confirme o arquivo `render.yaml`.
5. Preencha as variáveis solicitadas:

```text
PROPOSAL_RENDERER_API_KEY=sua_chave_segura
OUTPUT_BASE_URL=https://proposal-renderer-api.onrender.com/files
```

O serviço usa `/render-health` como health check público do Render. Os endpoints usados pela Action continuam protegidos por `X-API-Key`.

Para configuração manual no Render ou Railway, use:

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

O schema já está configurado para `https://proposal-renderer-api.onrender.com`.

## Logo do escritório

Para usar o logo real do escritório no PDF e no Word editável, salve o arquivo em:

```text
assets/logo.png
```

Se esse arquivo não existir, a API usa automaticamente um monograma temporário gerado em tempo de execução.

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
