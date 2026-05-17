---
name: deploy-firecracker-sandbox
description: Provision or configure AWS Firecracker-based agent sandboxes. Use when wiring infra/sandbox, EC2 bare metal, or Nitro Enclaves for agent code execution.
---

# Deploy Firecracker agent sandbox

## When to use

- Implementing `infra/sandbox/firecracker_runner.py` against real AWS hosts
- Replacing the local socket stub with production microVM isolation
- Hardening multi-tenant agent code execution

## Instructions

1. Read current AWS docs via MCP `search_documentation` for Firecracker on EC2 bare metal.
2. Never route agent-generated code through standard Docker — use microVM isolation per blueprint.
3. Scope IAM roles per tenant; agents authenticate with PoP tokens, not human OAuth.
4. Expose runner socket or API behind private VPC endpoints only.
5. Log every execution with `tenant_id`, workflow id, and idempotency key.

## References

- [AWS MCP Server](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/mcp-server.html)
- Project runner: `infra/sandbox/firecracker_runner.py`
