# MCP Server Examples

Complete working examples of MCP servers demonstrating best practices.

---

## Example 1: GitHub MCP Server (TypeScript)

A complete GitHub integration MCP server showing:
- Server initialization with Streamable HTTP transport
- Multiple tools (search, create_issue, list_repos)
- Pagination support
- Error handling with actionable messages
- Tool annotations

### Project Structure

```
github-mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts          # Main server entry point
│   ├── client.ts         # GitHub API client
│   └── tools/
│       ├── search.ts     # Search repositories
│       ├── issues.ts     # Create and list issues
│       └── repos.ts      # List repositories
└── README.md
```

### Main Server (src/index.ts)

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express from "express";
import { registerGitHubTools } from "./tools/index.js";
import { createGitHubClient } from "./client.js";

const server = new McpServer({
  name: "github-mcp-server",
  version: "1.0.0"
});

const app = express();
const port = process.env.PORT || 3000;

// Create GitHub client with authentication
const githubClient = createGitHubClient({
  token: process.env.GITHUB_TOKEN!
});

// Register all GitHub tools
registerGitHubTools(server, githubClient);

// Create transport
const transport = new StreamableHTTPServerTransport({
  path: "/mcp"
});

// Start server
app.use("/mcp", transport.createRequestHandler());

app.listen(port, () => {
  console.log(`GitHub MCP Server running on port ${port}`);
});

await server.connect(transport);
```

### Search Tool (src/tools/search.ts)

```typescript
import { z } from "zod";
import { Octokit } from "@octokit/rest";

export interface GitHubToolsContext {
  server: McpServer;
  client: Octokit;
}

export function registerSearchTool({ server, client }: GitHubToolsContext) {
  server.registerTool(
    "github_search_repos",
    {
      title: "Search GitHub Repositories",
      description: "Search for GitHub repositories matching criteria. Returns repositories with owner, name, description, language, stars, and forks.",
      inputSchema: {
        query: z.string()
          .describe("Search query (e.g., 'language:typescript stars:>100')"),
        limit: z.number()
          .min(1)
          .max(100)
          .default(10)
          .describe("Number of results to return (1-100)"),
        page: z.number()
          .min(1)
          .default(1)
          .describe("Page number for pagination")
      },
      annotations: {
        readOnlyHint: true,
        idempotentHint: true
      }
    },
    async ({ query, limit, page }) => {
      try {
        const response = await client.rest.search.repos({
          q: query,
          per_page: limit,
          page: page
        });

        const repos = response.data.items.map(repo => ({
          id: repo.id,
          name: repo.name,
          fullName: repo.full_name,
          description: repo.description,
          language: repo.language,
          stars: repo.stargazers_count,
          forks: repo.forks_count,
          url: repo.html_url
        }));

        return {
          content: [{
            type: "text",
            text: formatMarkdownResponse(repos)
          }],
          structuredContent: {
            total: response.data.total_count,
            count: repos.length,
            page: page,
            items: repos
          }
        };
      } catch (error: any) {
        return {
          isError: true,
          content: [{
            type: "text",
            text: `GitHub API error: ${error.message}. Try a more specific query or use limit=5.`
          }]
        };
      }
    }
  );
}

function formatMarkdownResponse(repos: any[]): string {
  if (repos.length === 0) return "No repositories found.";

  const lines = [
    `Found ${repos.length} repositories:\n`,
    ...repos.map(repo =>
      `**${repo.fullName}** - ${repo.description || 'No description'}\n` +
      `  - Language: ${repo.language || 'N/A'} | Stars: ${repo.stars} | Forks: ${repo.forks}\n` +
      `  - URL: ${repo.url}\n`
    )
  ];

  return lines.join('\n');
}
```

### Create Issue Tool (src/tools/issues.ts)

```typescript
import { z } from "zod";

export function registerCreateIssueTool({ server, client }: GitHubToolsContext) {
  server.registerTool(
    "github_create_issue",
    {
      title: "Create GitHub Issue",
      description: "Create a new issue in a GitHub repository. Requires owner and repository name.",
      inputSchema: {
        owner: z.string().describe("Repository owner (username or organization)"),
        repo: z.string().describe("Repository name"),
        title: z.string().describe("Issue title"),
        body: z.string().optional().describe("Issue body/description"),
        labels: z.array(z.string()).optional().describe("Array of label names")
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: true,
        idempotentHint: false
      }
    },
    async ({ owner, repo, title, body, labels }) => {
      try {
        const response = await client.rest.issues.create({
          owner,
          repo,
          title,
          body,
          labels
        });

        const issue = response.data;

        return {
          content: [{
            type: "text",
            text: `Created issue #${issue.number}: ${issue.title}\n` +
                  `URL: ${issue.html_url}\n` +
                  `State: ${issue.state}\n`
          }],
          structuredContent: {
            number: issue.number,
            title: issue.title,
            url: issue.html_url,
            state: issue.state,
            labels: issue.labels.map((l: any) => l.name)
          }
        };
      } catch (error: any) {
        return {
          isError: true,
          content: [{
            type: "text",
            text: `Failed to create issue: ${error.message}. Verify owner and repo are correct.`
          }]
        };
      }
    }
  );
}
```

---

## Example 2: Weather MCP Server (Python)

A simple weather API integration showing:
- FastMCP framework
- API client integration
- JSON and Markdown response formats
- Location parameter with validation

### Project Structure

```
weather_mcp/
├── pyproject.toml
├── weather_mcp/
│   ├── __init__.py
│   ├── server.py      # Main server
│   └── client.py      # Weather API client
└── README.md
```

### Main Server (weather_mcp/server.py)

```python
from mcp.server.fastmcp import FastMCP
from .client import WeatherClient
import os

mcp = FastMCP("weather_mcp")

# Initialize weather client
weather_api_key = os.getenv("WEATHER_API_KEY")
client = WeatherClient(api_key=weather_api_key)

@mcp.tool(
    name="get_weather",
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True
    }
)
async def get_weather(location: str, units: str = "metric") -> str:
    """Get current weather for a location.

    Args:
        location: City name or coordinates (e.g., "New York" or "40.7128,-74.0060")
        units: Temperature units - 'metric' (Celsius) or 'imperial' (Fahrenheit)

    Returns:
        Weather information in markdown format
    """
    try:
        weather = await client.get_current_weather(location, units)

        # Markdown response
        markdown = f"""## Weather for {weather['name']}

**Temperature**: {weather['main']['temp']}°
**Feels Like**: {weather['main']['feels_like']}°
**Humidity**: {weather['main']['humidity']}%
**Description**: {weather['weather'][0]['description'].capitalize()}

---

"""
        return markdown

    except Exception as e:
        return f"Error fetching weather: {str(e)}. Check the location name and try again."

@mcp.tool(
    name="get_forecast",
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True
    }
)
async def get_forecast(location: str, days: int = 3) -> str:
    """Get weather forecast for a location.

    Args:
        location: City name
        days: Number of days to forecast (1-5)

    Returns:
        5-day weather forecast
    """
    if days < 1 or days > 5:
        return "Error: days must be between 1 and 5"

    try:
        forecast = await client.get_forecast(location, days)

        lines = [f"## {days}-Day Forecast for {location}\n"]

        for day in forecast['list'][:days]:
            date = day['dt_txt'].split(' ')[0]
            temp = day['main']['temp']
            desc = day['weather'][0]['description']
            lines.append(f"### {date}\n- Temperature: {temp}°\n- {desc.capitalize()}\n")

        return "\n".join(lines)

    except Exception as e:
        return f"Error fetching forecast: {str(e)}. Verify the city name."

if __name__ == "__main__":
    mcp.run()
```

### Weather Client (weather_mcp/client.py)

```python
import httpx
from typing import Dict, Any

class WeatherClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    async def get_current_weather(self, location: str, units: str = "metric") -> Dict[str, Any]:
        """Fetch current weather from OpenWeatherMap API."""
        params = {
            "q": location,
            "appid": self.api_key,
            "units": units
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/weather", params=params)
            response.raise_for_status()
            return response.json()

    async def get_forecast(self, location: str, days: int) -> Dict[str, Any]:
        """Fetch 5-day weather forecast."""
        params = {
            "q": location,
            "appid": self.api_key,
            "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/forecast", params=params)
            response.raise_for_status()
            return response.json()
```

---

## Example 3: File System MCP Server (Python)

A file system access MCP server showing:
- Read/write operations
- Path validation (security)
- File metadata handling
- Binary file support

```python
from mcp.server.fastmcp import FastMCP
import os
import base64
from pathlib import Path
from typing import Optional

mcp = FastMCP("filesystem_mcp")

# Security: Restrict to allowed directories
ALLOWED_BASE_DIRS = os.getenv("ALLOWED_DIRS", "").split(":")

def validate_path(path_str: str) -> Path:
    """Validate and resolve path, ensuring it's within allowed directories."""
    path = Path(path_str).resolve()

    # Check if path is within allowed directories
    if not any(
        str(path).startswith(str(Path(base_dir).resolve()))
        for base_dir in ALLOWED_BASE_DIRS
    ):
        raise ValueError(f"Access denied: path not within allowed directories")

    # Prevent directory traversal
    if ".." in path_str or path_str.startswith("/"):
        raise ValueError(f"Access denied: invalid path")

    return path

@mcp.tool(
    name="read_file",
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True
    }
)
async def read_file(path: str, encoding: str = "utf-8") -> str:
    """Read a text file.

    Args:
        path: Relative path to file
        encoding: File encoding (default: utf-8)

    Returns:
        File contents as text
    """
    try:
        file_path = validate_path(path)
        return file_path.read_text(encoding=encoding)
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool(
    name="write_file",
    annotations={
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False
    }
)
async def write_file(path: str, content: str, encoding: str = "utf-8") -> str:
    """Write content to a text file.

    Args:
        path: Relative path to file
        content: Content to write
        encoding: File encoding (default: utf-8)

    Returns:
        Success message
    """
    try:
        file_path = validate_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding=encoding)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@mcp.tool(
    name="list_files",
    annotations={
        "readOnlyHint": True,
        "idempotentHint": True
    }
)
async def list_files(path: str = ".") -> str:
    """List files and directories in a path.

    Args:
        path: Relative path to directory (default: current directory)

    Returns:
        Directory listing in markdown format
    """
    try:
        dir_path = validate_path(path)

        if not dir_path.is_dir():
            return f"Error: {path} is not a directory"

        lines = [f"# Directory: {path}\n\n"]

        for item in sorted(dir_path.iterdir()):
            icon = "📁" if item.is_dir() else "📄"
            size = f" ({item.stat().st_size} bytes)" if item.is_file() else ""
            lines.append(f"{icon} {item.name}{size}")

        return "\n".join(lines)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

---

## Key Patterns from Examples

### 1. Error Handling
Always provide actionable error messages:
```typescript
return {
  isError: true,
  content: [{
    type: "text",
    text: `Error: ${error.message}. Try using limit=5 to reduce results.`
  }]
};
```

### 2. Pagination
Always support pagination with metadata:
```typescript
return {
  structuredContent: {
    total: response.data.total_count,
    count: repos.length,
    page: page,
    has_more: count < total
  }
};
```

### 3. Annotations
Provide annotations for all tools:
```typescript
annotations: {
  readOnlyHint: true,      // For read operations
  destructiveHint: true,   // For write/delete operations
  idempotentHint: true,    // For operations that can be repeated safely
  openWorldHint: true      // For operations accessing external resources
}
```

### 4. Structured Content
Return both text and structured data:
```typescript
return {
  content: [{ type: "text", text: markdownFormat(data) }],
  structuredContent: data  // Raw JSON for programmatic use
};
```
