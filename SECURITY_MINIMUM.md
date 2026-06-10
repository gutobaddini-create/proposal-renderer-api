# Segurança Mínima da API Renderizadora

## Objetivo

Evitar que a API pública de geração de propostas fique aberta para qualquer pessoa.

## 1. API Key obrigatória

Toda chamada à API deve exigir:

```http
X-API-Key: SUA_CHAVE_SEGURA
```

## 2. Variável de ambiente

A chave deve ficar em variável de ambiente:

```text
PROPOSAL_RENDERER_API_KEY=sua_chave_segura
```

Nunca colocar a chave diretamente no código.

## 3. Validação no FastAPI

Exemplo conceitual:

```python
import os
from fastapi import Header, HTTPException

API_KEY = os.getenv("PROPOSAL_RENDERER_API_KEY")

def verify_api_key(x_api_key: str = Header(default="")):
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida ou ausente.")
```

## 4. Arquivos gerados

Evite nomes previsíveis simples.

Prefira:

```text
proposal_20260610_ab12cd34
```

em vez de:

```text
proposta_1
```

## 5. Dados sensíveis

Não grave logs completos com:

- CPF;
- CNPJ;
- dados pessoais;
- documentos internos;
- conteúdo integral da proposta.

Logar apenas:

```text
proposalId
status
timestamp
erro técnico resumido
```

## 6. Limpeza de arquivos

Implementar futuramente limpeza de arquivos antigos.

Exemplo:

```text
apagar arquivos com mais de 7 ou 30 dias
```

## 7. Produção

Para produção real, avaliar:

- autenticação por usuário;
- links assinados;
- storage privado;
- criptografia;
- logs de auditoria;
- termos de uso;
- política de privacidade.
