"""
Utility per logging sicuro e troncamento dei payload JSON.

Fornisce funzioni per serializzare oggetti in JSON in modo robusto
e per registrare payload lunghi evitando flooding dei log.
"""
import json
import logging
from typing import Any, Optional
import os


def safe_serialize(obj: Any, ensure_ascii: bool = False, indent: int | None = None) -> str:
    """Serializza un oggetto in JSON in modo robusto. Se la serializzazione fallisce,
    prova a rappresentare l'oggetto con repr()."""
    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent, default=str)
    except Exception:
        try:
            return json.dumps(str(obj), ensure_ascii=ensure_ascii)
        except Exception:
            return repr(obj)


def truncate(text: str, max_chars: Optional[int] = 1000) -> str:
    """Tronca una stringa preservando l'inizio e la fine se molto lunga."""
    if text is None:
        return ""
    if max_chars is None:
        return text
    if len(text) <= max_chars:
        return text
    head = text[: max_chars // 2]
    tail = text[- (max_chars // 2) :]
    return f"{head}...[TRUNCATED:{len(text)} chars]...{tail}"


def log_truncated(logger: logging.Logger, level: int, label: str, obj: Any, max_chars: int = 1000) -> None:
    """Serializza un oggetto e lo registra troncato.

    - logger: istanza di logging.Logger
    - level: livello di logging (es. logging.DEBUG)
    - label: etichetta descrittiva
    - obj: oggetto da serializzare
    - max_chars: lunghezza massima da loggare
    """
    # Honor environment switch to allow full payload logging for debugging
    env_full = os.getenv('LOG_FULL_PAYLOADS', '').lower() in ('1', 'true', 'yes', 'on')
    try:
        serialized = safe_serialize(obj, ensure_ascii=False)
    except Exception:
        serialized = repr(obj)

    effective_max = None if env_full else max_chars
    text = truncate(serialized, max_chars=effective_max)
    logger.log(level, f"{label}: {text}")


def section_to_string(value: Any) -> str:
    """Normalize a section value to a string suitable for DeterminaContent.

    - If it's already a string, return it.
    - If it's a dict and contains 'contenuto', return that (or its stringified form).
    - If it's a dict or list otherwise, return a truncated JSON representation.
    """
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        if 'contenuto' in value and isinstance(value['contenuto'], str):
            return value['contenuto']
        # if contenuto exists but is not str, stringify
        if 'contenuto' in value:
            return safe_serialize(value['contenuto'])
        return safe_serialize(value)
    if isinstance(value, list):
        # join strings or serialize elements
        parts = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and 'contenuto' in item and isinstance(item['contenuto'], str):
                parts.append(item['contenuto'])
            else:
                parts.append(safe_serialize(item))
        return "\n".join(parts)
    return safe_serialize(value)


def allegati_to_list(allegati: Any) -> list:
    """Normalize allegati to a list of strings (names).

    - If it's already a list of strings, return it.
    - If it's a list of dicts with 'nome', extract names.
    - Else stringify elements.
    """
    if allegati is None:
        return []
    if isinstance(allegati, list):
        out = []
        for item in allegati:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict) and 'nome' in item and isinstance(item['nome'], str):
                out.append(item['nome'])
            else:
                out.append(safe_serialize(item))
        return out
    # single item
    if isinstance(allegati, str):
        return [allegati]
    if isinstance(allegati, dict) and 'nome' in allegati and isinstance(allegati['nome'], str):
        return [allegati['nome']]
    return [safe_serialize(allegati)]
