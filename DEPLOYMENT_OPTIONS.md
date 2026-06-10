# Opções de Deploy para a API FastAPI

## Objetivo

Publicar a API renderizadora em uma URL HTTPS acessível pelo GPT.

## Opção recomendada para MVP: Render ou Railway

Para MVP, prefira uma plataforma simples de deploy de aplicações web Python, sem precisar configurar servidor manualmente.

### Opção A — Render

Vantagens:

- deploy simples por GitHub;
- suporte a Web Service;
- HTTPS automático;
- bom para MVP;
- fácil de configurar variável de ambiente.

Configuração típica:

```text
Build command:
pip install -r requirements.txt

Start command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Variáveis de ambiente:

```text
PROPOSAL_RENDERER_API_KEY=sua_chave_segura
OUTPUT_BASE_URL=https://seu-servico.onrender.com/files
```

### Opção B — Railway

Vantagens:

- deploy rápido;
- integração com GitHub;
- HTTPS automático;
- variáveis de ambiente simples.

Start command:

```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Opção C — VPS própria

Vantagens:

- mais controle;
- melhor para produção madura;
- permite domínio próprio e storage próprio.

Desvantagens:

- exige configuração de servidor;
- precisa configurar Nginx, SSL, firewall, logs e updates.

### Opção D — Docker

Boa para padronizar deploy.

Pode ser usada em Render, Railway, VPS, Fly.io ou outro ambiente.

## Recomendação

Para começar, use:

```text
Render ou Railway
```

Depois que o MVP estiver validado, avalie migrar para VPS, Docker ou infraestrutura própria.

## Cuidados

- Nunca deixe a API sem autenticação.
- Não exponha arquivos sensíveis publicamente sem controle.
- Use nomes de arquivos não previsíveis.
- Não registre no log dados pessoais completos.
- Configure limpeza periódica dos arquivos gerados.
