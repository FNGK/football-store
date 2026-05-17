"""
AWS Firecracker microVM runner interface.

Agent-generated code MUST execute here — never in standard Docker containers.
"""

import json
import socket
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FirecrackerRunner:
    socket_path: Path

    def execute(self, tenant_id: str, code: str, language: str = "python") -> dict:
        """Submit code to Firecracker via host socket (stub for local dev)."""
        payload = {
            "tenant_id": tenant_id,
            "language": language,
            "code": code,
        }
        if not self.socket_path.exists():
            return {
                "status": "simulated",
                "stdout": f"[firecracker-stub] Would execute {language} for {tenant_id}",
                "stderr": "",
            }
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.connect(str(self.socket_path))
                sock.sendall(json.dumps(payload).encode())
                data = sock.recv(65536)
                return json.loads(data.decode())
        except OSError as exc:
            return {"status": "error", "stdout": "", "stderr": str(exc)}
