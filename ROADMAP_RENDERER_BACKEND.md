# Roadmap — Backend Renderizador de Propostas

## Fase 0 — Estrutura do projeto

- [ ] Criar repositório/pasta do backend
- [ ] Criar ambiente virtual Python
- [ ] Criar `requirements.txt`
- [ ] Criar `app/main.py`
- [ ] Criar estrutura de pastas
- [ ] Criar endpoint `/health`
- [ ] Rodar API localmente

## Fase 1 — Modelos e validação

- [ ] Criar modelos Pydantic
- [ ] Validar campos obrigatórios
- [ ] Permitir campos pendentes com `[informar]`
- [ ] Criar função de sanitização de strings
- [ ] Remover markdown de e-mails
- [ ] Remover `mailto:`
- [ ] Criar testes do sanitizador

## Fase 2 — Geração de PDF

- [ ] Criar gerador PDF inicial com ReportLab
- [ ] Criar capa simples
- [ ] Criar páginas a partir de `layoutPlan`
- [ ] Criar página de investimento/prazo/condições
- [ ] Criar página de aceite
- [ ] Salvar PDF em `/output/{proposalId}/proposta.pdf`

## Fase 3 — Word editável

- [ ] Criar DOCX textual com python-docx
- [ ] Inserir título, cliente, objeto, escopo, entregáveis, investimento e aceite
- [ ] Salvar em `/output/{proposalId}/proposta_editavel.docx`

## Fase 4 — Word visual

- [ ] Renderizar PDF em imagens
- [ ] Criar DOCX A4
- [ ] Inserir cada página como imagem
- [ ] Salvar em `/output/{proposalId}/proposta_visual.docx`

## Fase 5 — Endpoint final

- [ ] Criar endpoint `/generate-proposal`
- [ ] Receber JSON
- [ ] Validar JSON
- [ ] Sanitizar dados
- [ ] Gerar arquivos conforme `output`
- [ ] Retornar paths/links
- [ ] Testar com JSON da Bovmeat

## Fase 6 — Action do GPT

- [ ] Publicar API em URL acessível por HTTPS
- [ ] Ajustar `OPENAPI_SCHEMA_ACTION.yaml` com domínio real
- [ ] Colar schema na Action do GPT
- [ ] Testar chamada pelo GPT
- [ ] Ajustar autenticação se necessário

## Fase 7 — Segurança e produção

- [ ] Adicionar chave de API
- [ ] Adicionar limite de tamanho do JSON
- [ ] Adicionar logs
- [ ] Adicionar limpeza de arquivos antigos
- [ ] Adicionar armazenamento persistente ou storage externo