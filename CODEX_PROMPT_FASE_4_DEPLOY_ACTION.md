# Prompt para Codex — Fase 4 Deploy e Action

Você está trabalhando no projeto da API Renderizadora de Propostas Jurídicas.

Objetivo desta fase:
Preparar a API para publicação em ambiente HTTPS e integração com GPT Action.

Leia:

- `FASE_4_PUBLICACAO_CONFIGURACAO_ACTION.md`
- `DEPLOYMENT_OPTIONS.md`
- `GPT_ACTION_SETUP_PASSO_A_PASSO.md`
- `OPENAPI_SCHEMA_ACTION_COM_API_KEY.yaml`
- `SECURITY_MINIMUM.md`
- `TESTE_PONTA_A_PONTA.md`
- `TROUBLESHOOTING_ACTIONS.md`

## Tarefas

1. Adicionar autenticação simples por API Key no header `X-API-Key`.
2. Ler a chave da variável de ambiente `PROPOSAL_RENDERER_API_KEY`.
3. Proteger os endpoints `/health` e `/generate-proposal`, salvo se for decidido deixar `/health` público.
4. Criar/ajustar `requirements.txt`.
5. Criar `Dockerfile`, se útil para deploy.
6. Criar arquivo de exemplo `.env.example`.
7. Ajustar geração de URLs públicas dos arquivos.
8. Criar endpoint estático ou mecanismo para servir arquivos gerados, se ainda não existir.
9. Atualizar README com instruções de deploy.
10. Garantir que o schema OpenAPI da Action use `X-API-Key`.
11. Testar chamada local simulando header `X-API-Key`.

## Variáveis de ambiente esperadas

```text
PROPOSAL_RENDERER_API_KEY=
OUTPUT_BASE_URL=
```

## Critérios de aceite

A fase estará concluída quando:

- a API recusar chamadas sem `X-API-Key`;
- a API aceitar chamadas com `X-API-Key` correta;
- `/generate-proposal` continuar gerando arquivos;
- a resposta retornar URLs ou paths acessíveis;
- o OpenAPI schema estiver pronto para colar no GPT;
- houver instrução clara de deploy em README.
