# Configuração da Action no GPT — Passo a Passo

## 1. Publicar a API

Antes de configurar a Action, publique a API e confirme:

```text
https://SUA-API.com/health
```

A resposta deve ser:

```json
{
  "status": "ok",
  "service": "proposal-renderer-api",
  "version": "0.1.0"
}
```

## 2. Atualizar o OpenAPI Schema

Abra o arquivo:

```text
OPENAPI_SCHEMA_ACTION_COM_API_KEY.yaml
```

Substitua:

```text
https://SEU-DOMINIO-DA-API.com
```

pela URL real da API.

Exemplo:

```text
https://gerador-propostas-api.onrender.com
```

## 3. Abrir editor do GPT

No ChatGPT:

```text
GPTs
↓
Seu GPT Gerador de Propostas Jurídicas
↓
Editar
↓
Configure / Configurar
↓
Actions / Ações
```

## 4. Criar nova Action

Clique em:

```text
Create new action
```

ou:

```text
Criar nova ação
```

## 5. Colar o schema

Cole o conteúdo de:

```text
OPENAPI_SCHEMA_ACTION_COM_API_KEY.yaml
```

no campo de schema OpenAPI.

## 6. Configurar autenticação

Escolha autenticação por API Key.

Configuração sugerida:

```text
Auth type: API Key
Header name: X-API-Key
API key: sua_chave_segura
```

A chave deve ser a mesma configurada na API como variável de ambiente:

```text
PROPOSAL_RENDERER_API_KEY=sua_chave_segura
```

## 7. Salvar

Salve a Action.

## 8. Testar dentro do editor

Faça um teste com:

```text
Verifique se a API renderizadora está ativa.
```

O GPT deve chamar `healthCheck`.

Depois teste:

```text
Gere uma proposta de teste usando o JSON da Bovmeat e chame a Action generateProposal.
```

## 9. Resultado esperado

O GPT deve responder com os links retornados pela API:

```text
PDF: ...
Word visual: ...
Word editável: ...
```

## 10. Se der erro

Verifique:

- URL da API;
- HTTPS;
- schema OpenAPI;
- nome do header `X-API-Key`;
- chave configurada no GPT;
- chave configurada na API;
- logs da API;
- se o endpoint `/generate-proposal` aceita o JSON enviado.
