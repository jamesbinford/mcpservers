# Dex CRM MCP Server

An MCP (Model Context Protocol) server that provides access to your Dex CRM data, including contacts, notes, and reminders.

## Features

- **Contacts**: List, search, create, update, and delete contacts
- **Notes**: List, create, update, and delete notes associated with contacts
- **Reminders**: List, create, update, complete, and delete reminders

## Setup

### 1. Get your Dex API Key

1. Log into your Dex account at https://getdex.com
2. Go to Settings > API: https://getdex.com/appv3/settings/api
3. Copy your API key

### 2. Install the server

```bash
cd dex-mcp-server
pip install -e .
```

### 3. Configure Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "dex": {
      "command": "dex-mcp-server",
      "env": {
        "DEX_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Or if using uv:

```json
{
  "mcpServers": {
    "dex": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/dex-mcp-server", "dex-mcp-server"],
      "env": {
        "DEX_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Available Tools

### Contacts

| Tool | Description |
|------|-------------|
| `dex_list_contacts` | List all contacts with pagination |
| `dex_get_contact` | Get a specific contact by ID |
| `dex_search_contacts` | Search contacts by email |
| `dex_create_contact` | Create a new contact |
| `dex_update_contact` | Update an existing contact |
| `dex_delete_contact` | Delete a contact |

### Notes

| Tool | Description |
|------|-------------|
| `dex_list_notes` | List all notes with pagination |
| `dex_get_notes_for_contact` | Get notes for a specific contact |
| `dex_create_note` | Create a note linked to contacts |
| `dex_update_note` | Update a note's content |
| `dex_delete_note` | Delete a note |

### Reminders

| Tool | Description |
|------|-------------|
| `dex_list_reminders` | List all reminders with pagination |
| `dex_create_reminder` | Create a reminder with due date |
| `dex_update_reminder` | Update a reminder |
| `dex_complete_reminder` | Mark a reminder as complete |
| `dex_delete_reminder` | Delete a reminder |

## Example Usage

Once configured, you can ask Claude things like:

- "Show me my Dex contacts"
- "Find the contact with email john@example.com"
- "Create a reminder to follow up with Jane next Monday"
- "What notes do I have for contact ID xyz?"
- "Add a note to my meeting with Bob: discussed Q4 goals"

## API Reference

This server uses the [Dex User API](https://getdex.com/docs/integrationsandfeatures/api). See the full API documentation for more details on available fields and response formats.
