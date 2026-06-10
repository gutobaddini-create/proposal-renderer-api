# FASE 3 — Action/API do Renderizador de Propostas

## Objetivo

Criar a primeira versão da API externa que será chamada pelo GPT personalizado por meio de uma Action.

Essa API será responsável por receber o JSON estruturado da proposta e gerar:

1. PDF visual da proposta;
2. Word visual de alta fidelidade;
3. Word editável simplificado.

Nesta fase, o GPT deixa de ser apenas um agente conversacional e passa a acionar uma ferramenta externa.

---

## Fluxo esperado

```text
Advogado conversa com o GPT
↓
GPT coleta dados e gera resumo
↓
Usuário confirma
↓
GPT gera JSON final
↓
GPT chama Action generateProposal
↓
API recebe JSON
↓
API corrige/sanitiza campos problemáticos, como e-mails em markdown
↓
API gera PDF, DOCX visual e DOCX editável
↓
API retorna links ou arquivos
↓
GPT entrega os links ao usuário
```

---

## Decisão técnica recomendada

Backend inicial:

```text
Python
FastAPI
Pydantic
ReportLab
python-docx
pypdfium2
Pillow
Uvicorn
```

## Por que FastAPI?

FastAPI é simples para criar endpoints REST, gera documentação OpenAPI automaticamente e facilita validações com Pydantic.

## Por que manter o renderizador fora do GPT?

Porque o GPT deve ser o cérebro editorial, não o motor visual. O renderizador precisa ser previsível, testável e controlado por código.

---

## Escopo da Fase 3

Nesta fase, criar:

1. endpoint `/health`;
2. endpoint `/generate-proposal`;
3. validação do JSON recebido;
4. sanitização automática de e-mails;
5. geração inicial de PDF simples ou placeholder visual;
6. geração inicial de Word editável simples;
7. retorno de links/paths dos arquivos gerados;
8. schema OpenAPI para configurar a Action no GPT;
9. documentação de teste local.

---

## Fora do escopo por enquanto

Não implementar ainda:

- login de usuários;
- painel web;
- banco de dados completo;
- pagamento;
- storage em nuvem;
- assinatura digital;
- envio automático por e-mail;
- múltiplos escritórios;
- filas assíncronas complexas.

Essas funções ficam para fases posteriores.

---

## Critério de aceite

A fase será considerada concluída quando:

- a API rodar localmente;
- `/health` responder `ok`;
- `/generate-proposal` aceitar um JSON de proposta;
- a API sanitizar `mailto:` e e-mails em markdown;
- a API gerar pelo menos um PDF funcional;
- a API gerar pelo menos um DOCX editável simples;
- a API retornar uma resposta JSON com status e caminhos/links dos arquivos;
- o schema OpenAPI estiver pronto para colar na Action do GPT.