# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI tool rules repository that provides configuration and documentation for AI development tools, specifically focused on:
- Qdrant vector database setup and management
- Kilo Code configuration for AI-assisted development
- Claude Code usage guidelines and best practices

## Key Components

### Qdrant Vector Database
- **Configuration**: `qdrant-docker-compose.yaml` - Docker Compose setup for Qdrant
- **Startup**: Use `docker compose -f qdrant-docker-compose.yaml up -d` to start the service
- **Port**: Qdrant runs on port 6333
- **Storage**: Persistent volume `qdrant_storage` for data persistence

### Kilo Code Configuration
- **Location**: `.kilocode/` directory contains rules and workflows
- **Rules**: Design documentation standards in `.kilocode/rules/design_documentation_standards.md`
- **Workflows**:
  - `gen-doc.md` - Generate design documentation based on code analysis
  - `init.md` - Initialize project context documentation

### Documentation Standards
- **Design Documents**: Follow SMART, SOLID, and KISS principles
- **Format**: Markdown with Mermaid diagrams for visualizations
- **Structure**: Organized in `/docs/{two-digit-number}_{topic}/` directories
- **Context**: Project context stored in `/docs/.context/`

## Common Commands

### Qdrant Management
```bash
# Start Qdrant service
docker compose -f qdrant-docker-compose.yaml up -d

# Stop Qdrant service
docker compose -f qdrant-docker-compose.yaml down

# Check service status
docker compose -f qdrant-docker-compose.yaml ps
```

### Kilo Code Setup
```bash
# Create symlink for Kilo Code configuration (macOS)
ln -s /Users/xuyulu/workspace/code/01_AI/ai-rule-commands/.kilocode /Users/xuyulu/.kilocode
```

### Documentation Workflows
- Use Kilo Code workflows for generating design documentation
- Follow the established documentation structure and standards
- Context documentation should be maintained in `/docs/.context/`

## Architecture Notes

- This is primarily a configuration and documentation repository
- No traditional application code or build processes
- Focus on AI development toolchain setup and best practices
- Docker-based infrastructure for vector database
- Markdown-based documentation with structured workflows

## Development Guidelines

- Follow the design documentation standards when creating new docs
- Use the established Kilo Code workflows for documentation generation
- Maintain consistency with existing configuration patterns
- Ensure Docker services are properly managed and documented