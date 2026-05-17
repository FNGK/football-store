---
name: ask-docs
description: Query up-to-date CrewAI documentation via MCP or llms.txt. Use before changing crew APIs, MCP integration, or deploy commands.
---

# Ask CrewAI docs

## Tools

1. **crewai-docs** MCP — `search_crew_ai` and `query_docs_filesystem_crew_ai`
2. **llms.txt** — `https://docs.crewai.com/llms.txt`

## Workflow

1. Search for the feature (e.g. "MCPServerHTTP", "Process.parallel").
2. Read full pages with `head`/`cat` on `.mdx` paths from search results.
3. Apply changes to `packages/agents/` only after confirming current API.
