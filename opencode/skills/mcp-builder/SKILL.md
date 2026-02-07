---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
license: Complete terms in LICENSE.txt
---

# MCP Server Development Guide

Create MCP servers that enable LLMs to interact with external services through well-designed tools.

---

## Quick Start

Building an MCP server involves four phases:

1. **Research & Plan** - Understand API and design your tools. See [design_principles.md](reference/design_principles.md)
2. **Implement** - Build server with proper schemas and annotations. See [node_mcp_server.md](reference/node_mcp_server.md) or [python_mcp_server.md](reference/python_mcp_server.md)
3. **Test** - Verify functionality with MCP Inspector
4. **Evaluate** - Create evaluation questions. See [evaluation.md](reference/evaluation.md)

---

## Workflow Overview

```
Research → Implementation → Testing → Evaluation
```

**Phase 1: Research & Planning**
- Study service API (endpoints, auth, data models)
- Choose language: TypeScript (recommended) or Python
- Plan tool coverage: read operations first, then write operations
- Design input/output schemas with proper validation

**Phase 2: Implementation**
- Set up project structure (see language-specific guides)
- Implement core infrastructure (API client, error handling)
- Register tools with Zod/Pydantic schemas
- Add tool annotations (readOnlyHint, destructiveHint, etc.)

**Phase 3: Testing**
- Run `npm run build` (TypeScript) or `python -m py_compile` (Python)
- Test with MCP Inspector: `npx @modelcontextprotocol/inspector`
- Verify all tools work with valid/invalid inputs
- Check error messages are actionable

**Phase 4: Evaluation**
- Create 10 complex, realistic, read-only evaluation questions
- Verify answers are stable and verifiable
- Run evaluation using provided scripts

---

## Language Selection

### TypeScript (Recommended)

**Use when:**
- You need high-quality type safety and tooling
- Deploying as remote HTTP server
- Integrating with TypeScript ecosystems

**Resources:**
- [⚡ TypeScript Guide](reference/node_mcp_server.md) - Implementation patterns
- [📋 Best Practices](reference/mcp_best_practices.md) - Naming, pagination, response formats
- Fetch SDK: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`

### Python

**Use when:**
- Rapid prototyping or simple integrations
- Local development with minimal setup
- Integrating with Python ecosystems

**Resources:**
- [🐍 Python Guide](reference/python_mcp_server.md) - Implementation patterns
- [📋 Best Practices](reference/mcp_best_practices.md) - Naming, pagination, response formats
- Fetch SDK: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`

---

## Reference Files

Load these resources during development:

### Core Design
- [design_principles.md](reference/design_principles.md) - Core MCP design patterns (API coverage, naming, error handling)

### Language-Specific
- [node_mcp_server.md](reference/node_mcp_server.md) - TypeScript project setup, Zod patterns, complete examples
- [python_mcp_server.md](reference/python_mcp_server.md) - Python/FastMCP setup, Pydantic patterns, complete examples

### Best Practices
- [mcp_best_practices.md](reference/mcp_best_practices.md) - Server naming, tool naming, pagination, security

### Examples & Evaluation
- [examples.md](reference/examples.md) - Complete working examples (GitHub, Weather, File System)
- [evaluation.md](reference/evaluation.md) - Creating and running evaluations

### Protocol Documentation
Fetch MCP spec pages:
```
https://modelcontextprotocol.io/sitemap.xml
https://modelcontextprotocol.io/specification/draft.md
```

---

## Examples

### Example: Simple Tool (TypeScript)

**Input**: User wants to search GitHub repositories

```typescript
server.registerTool(
  "github_search_repos",
  {
    title: "Search GitHub Repositories",
    description: "Search for repositories matching criteria",
    inputSchema: {
      query: z.string().describe("Search query"),
      limit: z.number().min(1).max(100).default(10).describe("Number of results")
    },
    annotations: { readOnlyHint: true, idempotentHint: true }
  },
  async ({ query, limit }) => {
    const repos = await searchGitHub(query, limit);
    return {
      content: [{ type: "text", text: formatResults(repos) }],
      structuredContent: { repos }
    };
  }
);
```

### Example: Simple Tool (Python)

**Input**: User wants to get weather information

```python
@mcp.tool(
    name="get_weather",
    annotations={"readOnlyHint": True, "idempotentHint": True}
)
async def get_weather(location: str, units: str = "metric") -> str:
    weather = await client.get_current_weather(location, units)
    return f"## Weather for {weather['name']}\nTemperature: {weather['main']['temp']}°"
```

**For more complete examples**, see [examples.md](reference/examples.md).

---

## Key Principles

1. **API Coverage First**: Prioritize comprehensive API endpoints over workflow tools
2. **Clear Naming**: Use `service_action_resource` pattern with service prefix
3. **Proper Annotations**: Add readOnlyHint, destructiveHint, idempotentHint to all tools
4. **Actionable Errors**: Guide agents with specific next steps in error messages
5. **Structured Output**: Return both text (human-readable) and structuredContent (machine-readable)
6. **Pagination**: Always support limit/offset with pagination metadata

---

## See Also

- [examples.md](reference/examples.md) - Complete working examples with detailed explanations
- [design_principles.md](reference/design_principles.md) - Deep dive into MCP design philosophy
- [mcp_best_practices.md](reference/mcp_best_practices.md) - Comprehensive best practices reference
