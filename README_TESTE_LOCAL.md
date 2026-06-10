# Teste Local da API Renderizadora

## 1. Criar ambiente

```bash
python -m venv .venv
```

## 2. Ativar ambiente

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## 4. Rodar API

```bash
uvicorn app.main:app --reload
```

## 5. Testar saúde

Acesse:

```text
http://localhost:8000/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "proposal-renderer-api",
  "version": "0.1.0"
}
```

## 6. Testar geração

Usando curl:

```bash
curl -X POST http://localhost:8000/generate-proposal ^
  -H "Content-Type: application/json" ^
  -d @sample_data/bovmeat.json
```

No PowerShell:

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://localhost:8000/generate-proposal" `
  -ContentType "application/json" `
  -InFile "sample_data/bovmeat.json"
```

## 7. Resultado esperado

A API deve criar:

```text
output/{proposalId}/proposta.pdf
output/{proposalId}/proposta_editavel.docx
output/{proposalId}/proposta_visual.docx
```

No MVP, o Word visual pode ser deixado como pendente se a renderização PDF→imagem ainda não estiver implementada.