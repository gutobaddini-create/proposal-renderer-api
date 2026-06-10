# JSON Sanitizer Spec

## Objetivo

Corrigir automaticamente pequenos problemas recorrentes no JSON gerado pelo GPT antes de enviar ao renderizador.

## Sanitizações obrigatórias

### 1. E-mail markdown

Converter:

```text
[advlobobaddini.erica@gmail.com](mailto:advlobobaddini.erica@gmail.com)
```

para:

```text
advlobobaddini.erica@gmail.com
```

### 2. Qualquer link markdown de e-mail

Converter padrões como:

```text
[email@dominio.com](mailto:email@dominio.com)
```

para:

```text
email@dominio.com
```

### 3. Remover `mailto:`

Se algum campo contiver:

```text
mailto:email@dominio.com
```

converter para:

```text
email@dominio.com
```

### 4. Aplicar recursivamente

A sanitização deve percorrer todo o JSON, inclusive:

- provider.email;
- layoutPlan;
- footer;
- acceptance;
- qualquer string aninhada.

## Exemplo de função

```python
import re

def sanitize_string(value: str) -> str:
    value = re.sub(r"\[([^\]]+@[^\]]+)\]\(mailto:[^)]+\)", r"\1", value)
    value = re.sub(r"mailto:([\w.%-]+@[\w.-]+\.[A-Za-z]{2,})", r"\1", value)
    return value

def sanitize_json(obj):
    if isinstance(obj, dict):
        return {k: sanitize_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_json(v) for v in obj]
    if isinstance(obj, str):
        return sanitize_string(obj)
    return obj
```