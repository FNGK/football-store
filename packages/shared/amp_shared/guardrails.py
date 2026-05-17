"""Minimum Viable Budget (MVG) guardrails and circuit breakers."""

from dataclasses import dataclass, field
from enum import Enum
from time import monotonic


class AgentMode(str, Enum):
    NORMAL = "normal"
    SAFE = "safe"


@dataclass
class BudgetGuardrails:
    max_input_tokens: int = 100_000
    max_output_tokens: int = 50_000
    max_tool_calls: int = 50
    max_wall_clock_seconds: float = 600.0
    reserved_tokens_per_step: int = 4_000

    tokens_in: int = 0
    tokens_out: int = 0
    tool_calls: int = 0
    started_at: float = field(default_factory=monotonic)
    mode: AgentMode = AgentMode.NORMAL

    def reserve_step(self) -> None:
        if self.mode == AgentMode.SAFE:
            raise RuntimeError("Agent in Safe Mode — writes blocked")
        remaining = self.max_output_tokens - self.tokens_out
        if remaining < self.reserved_tokens_per_step:
            self.trip_circuit("Insufficient token budget for step reservation")

    def record_tokens(self, inp: int, out: int) -> None:
        self.tokens_in += inp
        self.tokens_out += out
        if self.tokens_in > self.max_input_tokens or self.tokens_out > self.max_output_tokens:
            self.trip_circuit("Token budget exceeded")

    def record_tool_call(self) -> None:
        self.tool_calls += 1
        if self.tool_calls > self.max_tool_calls:
            self.trip_circuit("Behavioral cap: max tool calls exceeded")
        elapsed = monotonic() - self.started_at
        if elapsed > self.max_wall_clock_seconds:
            self.trip_circuit("Wall-clock limit exceeded")

    def trip_circuit(self, reason: str) -> None:
        self.mode = AgentMode.SAFE
        raise RuntimeError(f"Circuit breaker tripped: {reason}")
