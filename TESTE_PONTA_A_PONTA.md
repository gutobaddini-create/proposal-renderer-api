# Teste Ponta a Ponta — GPT + Action + API

## Objetivo

Validar se o GPT consegue chamar a Action e gerar arquivos reais.

## 1. Testar API publicada

Acesse no navegador:

```text
https://SUA-API.com/health
```

Se `/health` exigir API key, teste via Postman, Insomnia ou curl.

## 2. Testar com curl

```bash
curl -X POST https://SUA-API.com/generate-proposal \
  -H "Content-Type: application/json" \
  -H "X-API-Key: SUA_CHAVE_SEGURA" \
  -d @sample_data/bovmeat.json
```

Resposta esperada:

```json
{
  "status": "success",
  "proposalId": "...",
  "files": {
    "pdf": "...",
    "visualDocx": "...",
    "editableDocx": "..."
  },
  "warnings": []
}
```

## 3. Configurar GPT Action

No GPT, configure a Action usando:

```text
OPENAPI_SCHEMA_ACTION_COM_API_KEY.yaml
```

## 4. Teste de saúde pelo GPT

No GPT, escreva:

```text
Verifique se a API renderizadora está ativa.
```

Resultado esperado:

```text
O GPT chama healthCheck e informa que a API está ativa.
```

## 5. Teste de geração pelo GPT

No GPT, escreva:

```text
Use o JSON aprovado da proposta da Bovmeat e chame a Action para gerar PDF, Word visual e Word editável.
```

Resultado esperado:

```text
O GPT chama generateProposal e retorna os links dos arquivos.
```

## 6. Conferir arquivos

Baixe e abra:

- PDF;
- Word visual;
- Word editável.

Verifique:

- arquivo abre;
- cliente correto;
- investimento correto;
- prazo correto;
- e-mail sem `mailto:`;
- layout sem campos quebrados graves.

## 7. Resultado aprovado

A fase é aprovada quando o GPT entregar os links dos arquivos gerados pela API.
