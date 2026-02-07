# MCP Design Principles

Core design principles for building high-quality MCP servers.

---

## API Coverage vs. Workflow Tools

Balance comprehensive API endpoint coverage with specialized workflow tools.

**Workflow tools** are more convenient for specific tasks and reduce the number of tool calls an agent needs to make.

**Comprehensive API coverage** gives agents flexibility to compose operations. Performance varies by client—some clients benefit from code execution that combines basic tools, while others work better with higher-level workflows.

**When uncertain**: Prioritize comprehensive API coverage over workflow tools. Agents can compose operations themselves.

---

## Tool Naming and Discoverability

Clear, descriptive tool names help agents find the right tools quickly.

### Naming Conventions

1. Use snake_case format: `service_action_resource`
2. Include service prefix: `github_create_issue` (not just `create_issue`)
3. Be action-oriented: Start with verbs (get, list, search, create, update, delete)
4. Be specific: Avoid generic names that could conflict with other servers

### Examples

- ✅ `slack_send_message`, `github_list_repos`, `jira_create_issue`
- ❌ `send_message`, `list_repos`, `create_issue`

---

## Context Management

Agents benefit from concise tool descriptions and the ability to filter/paginate results.

### Tool Descriptions

- Narrow and unambiguous descriptions of functionality
- Descriptions must precisely match actual behavior
- Include parameter constraints and examples in descriptions

### Result Filtering

- Use `limit` and `offset` parameters for pagination
- Default to 20-50 items per page
- Return pagination metadata: `has_more`, `next_offset`, `total_count`

### Format Options

Support both JSON and Markdown response formats:
- JSON for programmatic processing
- Markdown for human readability

---

## Actionable Error Messages

Error messages should guide agents toward solutions with specific suggestions.

### Good Error Message

```
Error: API rate limit exceeded. Retry after 60 seconds or use limit=10 to reduce request size.
```

### Bad Error Message

```
Error: Rate limit exceeded.
```

### Error Handling Pattern

```typescript
try {
  const result = await apiCall(params);
  return { content: [{ type: "text", text: formatResult(result) }] };
} catch (error) {
  return {
    isError: true,
    content: [{
      type: "text",
      text: `Error: ${error.message}. Try using limit=${Math.floor(params.limit / 2)} to reduce results.`
    }]
  };
}
```

---

## MCP Protocol Documentation

Study the MCP specification to understand the protocol architecture.

### Key Resources

**Start with the sitemap** to find relevant pages:
```
https://modelcontextprotocol.io/sitemap.xml
```

**Fetch specific pages** with `.md` suffix for markdown format:
```
https://modelcontextprotocol.io/specification/draft.md
https://modelcontextprotocol.io/specification/server.md
https://modelcontextprotocol.io/specification/types/tools.md
```

### Key Pages to Review

1. **Specification overview and architecture** - Understanding the protocol
2. **Transport mechanisms** - streamable HTTP, stdio
3. **Tool definitions** - Input/output schemas, annotations
4. **Resource definitions** - File system access, data resources
5. **Prompt definitions** - Template prompts for agents

---

## Framework Documentation

### Recommended Stack

- **Language**: TypeScript (high-quality SDK support, static typing, good compatibility)
- **Transport**: Streamable HTTP for remote servers, stdio for local servers

### TypeScript SDK

Use WebFetch to load the latest documentation:
```
https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md

See [node_mcp_server.md](./node_mcp_server.md) for implementation patterns.
```

### Python SDK

Use WebFetch to load the latest documentation:
```
https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md

See [python_mcp_server.md](./python_mcp_server.md) for implementation patterns.
```

---

## Implementation Planning

### Understand the API

Review the service's API documentation to identify:
- Key endpoints and their purposes
- Authentication requirements (API keys, OAuth, etc.)
- Data models and response formats
- Rate limits and pagination

### Tool Selection

1. List all endpoints you want to implement
2. Start with the most common operations (read, list, search)
3. Add write operations (create, update, delete) with appropriate annotations
4. Consider workflow tools for common multi-step operations

### Prioritization

- **First**: Read-only operations (list, get, search)
- **Second**: Write operations with idempotent annotations
- **Third**: Workflow tools for complex use cases

### Input Schema Design

- Use Zod (TypeScript) or Pydantic (Python)
- Include constraints (min, max, pattern, enum)
- Add examples in field descriptions
- Make parameters optional with sensible defaults

### Output Schema Design

- Define `outputSchema` for structured data
- Helps clients understand and process tool outputs
- Use JSON schema compatible with Zod/Pydantic
- Include both `content` and `structuredContent` in responses

### Tool Annotations

Provide annotations to help clients understand tool behavior:

| Annotation | Type | Default | Description |
|-----------|------|---------|-------------|
| `readOnlyHint` | boolean | false | Tool does not modify its environment |
| `destructiveHint` | boolean | true | Tool may perform destructive updates |
| `idempotentHint` | boolean | false | Repeated calls with same args have no additional effect |
| `openWorldHint` | boolean | true | Tool interacts with external entities |

---

## See Also

- [mcp_best_practices.md](./mcp_best_practices.md) - Complete best practices
- [node_mcp_server.md](./node_mcp_server.md) - TypeScript implementation guide
- [python_mcp_server.md](./python_mcp_server.md) - Python implementation guide
