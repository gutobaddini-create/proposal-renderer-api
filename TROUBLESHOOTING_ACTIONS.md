# Troubleshooting — GPT Actions e API Renderizadora

## Erro: GPT não consegue chamar a Action

Verifique:

- a URL no schema OpenAPI;
- se a API está pública;
- se usa HTTPS;
- se o endpoint existe;
- se o schema foi salvo sem erros.

## Erro: 401 Unauthorized

Verifique:

- se a API exige `X-API-Key`;
- se o GPT está enviando a chave;
- se o nome do header está exatamente `X-API-Key`;
- se a chave no GPT é igual à variável `PROPOSAL_RENDERER_API_KEY`.

## Erro: 400 Bad Request

Verifique:

- JSON inválido;
- campos obrigatórios ausentes;
- schema rígido demais;
- problema em `proposal`, `client` ou `provider`.

## Erro: 500 Internal Server Error

Verifique os logs da API.

Causas comuns:

- pasta `output/` sem permissão;
- biblioteca ausente;
- erro no ReportLab;
- erro no python-docx;
- caracteres especiais não tratados;
- caminho de arquivo inválido.

## GPT passa e-mail com mailto

A API deve corrigir com o sanitizador.

Verifique se o sanitizador percorre o JSON inteiro, inclusive:

- `provider.email`;
- `layoutPlan`;
- `footer`;
- `acceptance`;
- strings dentro de listas.

## GPT não chama a Action

Reforce nas instruções do GPT:

```text
Após o usuário confirmar os dados e pedir geração dos arquivos finais, gere o JSON e chame obrigatoriamente a Action generateProposal.
```

## Links retornam 404

Verifique:

- se os arquivos foram salvos;
- se a API está servindo arquivos estáticos;
- se `OUTPUT_BASE_URL` está correto;
- se a rota `/files/...` existe.

## PDF gera, mas Word visual não

No MVP, aceite PDF + Word editável primeiro.

Depois implemente PDF → imagens → DOCX visual.
