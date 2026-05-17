"""PII masking gateway — lightweight NER with cryptographic token replacement."""

import hashlib
import re
import secrets
from dataclasses import dataclass

from cryptography.fernet import Fernet

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"\+?\d[\d\s\-().]{7,}\d")


@dataclass
class PiiGateway:
    """Tokenize PII before LLM exposure; store reversible mapping in CRM."""

    _fernet: Fernet

    @classmethod
    def from_key(cls, key: bytes | None = None) -> "PiiGateway":
        if key is None:
            key = Fernet.generate_key()
        return cls(_fernet=Fernet(key))

    def _token(self, tenant_id: str, value: str) -> str:
        digest = hashlib.sha256(f"{tenant_id}:{value}".encode()).hexdigest()[:16]
        return f"PII_{digest}_{secrets.token_hex(4)}"

    def mask_text(self, tenant_id: str, text: str) -> tuple[str, dict[str, str]]:
        mappings: dict[str, str] = {}

        def replace(pattern: re.Pattern[str], label: str, s: str) -> str:
            def sub(m: re.Match[str]) -> str:
                raw = m.group(0)
                tok = self._token(tenant_id, raw)
                mappings[tok] = self._fernet.encrypt(raw.encode()).decode()
                return tok

            return pattern.sub(sub, s)

        masked = replace(EMAIL_RE, "email", text)
        masked = replace(PHONE_RE, "phone", masked)
        return masked, mappings

    def detokenize(self, token: str, ciphertext: str) -> str:
        return self._fernet.decrypt(ciphertext.encode()).decode()
