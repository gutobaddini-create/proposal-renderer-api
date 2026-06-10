# FASE 4 — Publicação da API e Configuração da Action no GPT

## Objetivo

Publicar a API renderizadora em uma URL HTTPS e conectar essa API ao GPT personalizado por meio de uma Action.

Ao final desta fase, o GPT deverá conseguir:

1. receber o pedido do advogado;
2. montar o resumo de validação;
3. gerar o JSON final;
4. chamar a Action `generateProposal`;
5. enviar o JSON para a API;
6. receber os links dos arquivos gerados;
7. entregar ao usuário os links do PDF, Word visual e Word editável.

## Fluxo final esperado

```text
Usuário → GPT → JSON → Action → API Renderizadora → Arquivos → GPT → Usuário
```

## Pré-requisitos

Antes de começar esta fase, confirme:

- [ ] A API roda localmente.
- [ ] `GET /health` retorna `ok`.
- [ ] `POST /generate-proposal` aceita o JSON da Bovmeat.
- [ ] A API sanitiza e-mail com `mailto:`.
- [ ] A API gera pelo menos PDF e DOCX editável.
- [ ] A API retorna JSON com caminhos dos arquivos.
- [ ] O schema OpenAPI local está sem erros graves.

## Decisão importante

A API deve estar disponível em HTTPS.

Exemplos:

```text
https://proposal-renderer-api.seudominio.com
https://gerador-propostas-api.onrender.com
https://nome-do-projeto.up.railway.app
```

Não use `localhost` na Action final do GPT, porque o GPT precisa acessar a API pela internet.

## Segurança mínima

A API deve exigir uma chave simples, enviada no header:

```http
X-API-Key: SUA_CHAVE_SEGURA
```

A Action do GPT deve ser configurada para enviar essa chave.

## Resultado esperado

Ao concluir a Fase 4:

- a API estará publicada;
- o schema OpenAPI estará atualizado com a URL real;
- o GPT terá uma Action chamada `generateProposal`;
- o GPT conseguirá chamar a API;
- o usuário receberá links dos arquivos gerados.
