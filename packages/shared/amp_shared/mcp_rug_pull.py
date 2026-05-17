"""MCP tool schema rug-pull detection."""

import hashlib
import json
from dataclasses import dataclass, field


@dataclass
class SchemaRegistry:
    """Stores known-good tool schema hashes per server/tool."""

    _hashes: dict[str, str] = field(default_factory=dict)

    def _key(self, server: str, tool: str) -> str:
        return f"{server}:{tool}"

    @staticmethod
    def hash_schema(schema: dict) -> str:
        canonical = json.dumps(schema, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode()).hexdigest()

    def register(self, server: str, tool: str, schema: dict) -> str:
        digest = self.hash_schema(schema)
        self._hashes[self._key(server, tool)] = digest
        return digest

    def verify(self, server: str, tool: str, schema: dict) -> bool:
        key = self._key(server, tool)
        digest = self.hash_schema(schema)
        known = self._hashes.get(key)
        if known is None:
            self._hashes[key] = digest
            return True
        return known == digest

    def block_on_drift(self, server: str, tool: str, schema: dict) -> None:
        if not self.verify(server, tool, schema):
            raise RuntimeError(
                f"MCP rug-pull detected for {server}/{tool}: schema hash drift"
            )


global_schema_registry = SchemaRegistry()
