"""Dex CRM MCP Server - Access contacts, notes, and reminders via MCP."""

import os
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from .client import DexClient


# Initialize server
server = Server("dex-mcp-server")

# Global client instance (initialized on first use)
_client: DexClient | None = None


def get_client() -> DexClient:
    """Get or create the Dex client."""
    global _client
    if _client is None:
        api_key = os.environ.get("DEX_API_KEY")
        if not api_key:
            raise ValueError(
                "DEX_API_KEY environment variable is required. "
                "Get your API key from https://getdex.com/appv3/settings/api"
            )
        _client = DexClient(api_key)
    return _client


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available Dex CRM tools."""
    return [
        # Contacts
        Tool(
            name="dex_list_contacts",
            description="List all contacts from Dex CRM with pagination. Returns contact details including name, email, phone, job title, and social profiles.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of contacts to return (default: 10, max: 100)",
                        "default": 10,
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Number of contacts to skip for pagination (default: 0)",
                        "default": 0,
                    },
                },
            },
        ),
        Tool(
            name="dex_get_contact",
            description="Get detailed information about a specific contact by their ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {
                        "type": "string",
                        "description": "The UUID of the contact to retrieve",
                    },
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="dex_search_contacts",
            description="Search for contacts by email address.",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Email address to search for",
                    },
                },
                "required": ["email"],
            },
        ),
        Tool(
            name="dex_create_contact",
            description="Create a new contact in Dex CRM.",
            inputSchema={
                "type": "object",
                "properties": {
                    "first_name": {
                        "type": "string",
                        "description": "Contact's first name",
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Contact's last name",
                    },
                    "email": {
                        "type": "string",
                        "description": "Contact's email address",
                    },
                    "phone": {
                        "type": "string",
                        "description": "Contact's phone number",
                    },
                    "phone_label": {
                        "type": "string",
                        "description": "Label for phone number (e.g., 'Work', 'Mobile')",
                        "default": "Work",
                    },
                    "job_title": {
                        "type": "string",
                        "description": "Contact's job title",
                    },
                    "description": {
                        "type": "string",
                        "description": "Notes about the contact",
                    },
                    "linkedin": {
                        "type": "string",
                        "description": "LinkedIn username",
                    },
                    "twitter": {
                        "type": "string",
                        "description": "Twitter handle",
                    },
                    "instagram": {
                        "type": "string",
                        "description": "Instagram username",
                    },
                    "website": {
                        "type": "string",
                        "description": "Personal website URL",
                    },
                },
                "required": ["first_name", "last_name"],
            },
        ),
        Tool(
            name="dex_update_contact",
            description="Update an existing contact's information.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {
                        "type": "string",
                        "description": "The UUID of the contact to update",
                    },
                    "first_name": {
                        "type": "string",
                        "description": "New first name",
                    },
                    "last_name": {
                        "type": "string",
                        "description": "New last name",
                    },
                    "job_title": {
                        "type": "string",
                        "description": "New job title",
                    },
                    "description": {
                        "type": "string",
                        "description": "New description/notes",
                    },
                    "linkedin": {
                        "type": "string",
                        "description": "New LinkedIn username",
                    },
                    "twitter": {
                        "type": "string",
                        "description": "New Twitter handle",
                    },
                    "instagram": {
                        "type": "string",
                        "description": "New Instagram username",
                    },
                    "website": {
                        "type": "string",
                        "description": "New website URL",
                    },
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="dex_delete_contact",
            description="Delete a contact from Dex CRM.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {
                        "type": "string",
                        "description": "The UUID of the contact to delete",
                    },
                },
                "required": ["contact_id"],
            },
        ),
        # Notes
        Tool(
            name="dex_list_notes",
            description="List all notes from Dex CRM with pagination. Notes are timeline items that can be associated with contacts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of notes to return (default: 10)",
                        "default": 10,
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Number of notes to skip for pagination (default: 0)",
                        "default": 0,
                    },
                },
            },
        ),
        Tool(
            name="dex_get_notes_for_contact",
            description="Get all notes associated with a specific contact.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {
                        "type": "string",
                        "description": "The UUID of the contact to get notes for",
                    },
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="dex_create_note",
            description="Create a new note and associate it with one or more contacts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "note": {
                        "type": "string",
                        "description": "The note content",
                    },
                    "contact_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of contact UUIDs to associate with this note",
                    },
                    "event_time": {
                        "type": "string",
                        "description": "ISO 8601 timestamp for the note (defaults to now)",
                    },
                },
                "required": ["note", "contact_ids"],
            },
        ),
        Tool(
            name="dex_update_note",
            description="Update the content of an existing note.",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "The UUID of the note to update",
                    },
                    "note": {
                        "type": "string",
                        "description": "New note content",
                    },
                },
                "required": ["note_id", "note"],
            },
        ),
        Tool(
            name="dex_delete_note",
            description="Delete a note from Dex CRM.",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {
                        "type": "string",
                        "description": "The UUID of the note to delete",
                    },
                },
                "required": ["note_id"],
            },
        ),
        # Reminders
        Tool(
            name="dex_list_reminders",
            description="List all reminders from Dex CRM with pagination. Reminders can be associated with contacts and have due dates.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of reminders to return (default: 10)",
                        "default": 10,
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Number of reminders to skip for pagination (default: 0)",
                        "default": 0,
                    },
                },
            },
        ),
        Tool(
            name="dex_create_reminder",
            description="Create a new reminder, optionally associated with contacts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Reminder title",
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Due date in YYYY-MM-DD format",
                    },
                    "contact_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of contact UUIDs to associate with this reminder",
                    },
                    "text": {
                        "type": "string",
                        "description": "Additional reminder details",
                    },
                },
                "required": ["title", "due_date"],
            },
        ),
        Tool(
            name="dex_update_reminder",
            description="Update an existing reminder.",
            inputSchema={
                "type": "object",
                "properties": {
                    "reminder_id": {
                        "type": "string",
                        "description": "The UUID of the reminder to update",
                    },
                    "title": {
                        "type": "string",
                        "description": "New title",
                    },
                    "text": {
                        "type": "string",
                        "description": "New description text",
                    },
                    "due_date": {
                        "type": "string",
                        "description": "New due date in YYYY-MM-DD format",
                    },
                    "is_complete": {
                        "type": "boolean",
                        "description": "Mark as complete or incomplete",
                    },
                },
                "required": ["reminder_id"],
            },
        ),
        Tool(
            name="dex_complete_reminder",
            description="Mark a reminder as complete.",
            inputSchema={
                "type": "object",
                "properties": {
                    "reminder_id": {
                        "type": "string",
                        "description": "The UUID of the reminder to complete",
                    },
                },
                "required": ["reminder_id"],
            },
        ),
        Tool(
            name="dex_delete_reminder",
            description="Delete a reminder from Dex CRM.",
            inputSchema={
                "type": "object",
                "properties": {
                    "reminder_id": {
                        "type": "string",
                        "description": "The UUID of the reminder to delete",
                    },
                },
                "required": ["reminder_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    client = get_client()

    try:
        # Contacts
        if name == "dex_list_contacts":
            result = await client.list_contacts(
                limit=arguments.get("limit", 10),
                offset=arguments.get("offset", 0),
            )
        elif name == "dex_get_contact":
            result = await client.get_contact(arguments["contact_id"])
        elif name == "dex_search_contacts":
            result = await client.search_contacts_by_email(arguments["email"])
        elif name == "dex_create_contact":
            result = await client.create_contact(
                first_name=arguments["first_name"],
                last_name=arguments["last_name"],
                email=arguments.get("email"),
                phone=arguments.get("phone"),
                phone_label=arguments.get("phone_label", "Work"),
                job_title=arguments.get("job_title"),
                description=arguments.get("description"),
                linkedin=arguments.get("linkedin"),
                twitter=arguments.get("twitter"),
                instagram=arguments.get("instagram"),
                website=arguments.get("website"),
            )
        elif name == "dex_update_contact":
            contact_id = arguments.pop("contact_id")
            result = await client.update_contact(contact_id, **arguments)
        elif name == "dex_delete_contact":
            result = await client.delete_contact(arguments["contact_id"])

        # Notes
        elif name == "dex_list_notes":
            result = await client.list_notes(
                limit=arguments.get("limit", 10),
                offset=arguments.get("offset", 0),
            )
        elif name == "dex_get_notes_for_contact":
            result = await client.get_notes_for_contact(arguments["contact_id"])
        elif name == "dex_create_note":
            result = await client.create_note(
                note=arguments["note"],
                contact_ids=arguments["contact_ids"],
                event_time=arguments.get("event_time"),
            )
        elif name == "dex_update_note":
            result = await client.update_note(
                note_id=arguments["note_id"],
                note=arguments["note"],
            )
        elif name == "dex_delete_note":
            result = await client.delete_note(arguments["note_id"])

        # Reminders
        elif name == "dex_list_reminders":
            result = await client.list_reminders(
                limit=arguments.get("limit", 10),
                offset=arguments.get("offset", 0),
            )
        elif name == "dex_create_reminder":
            result = await client.create_reminder(
                title=arguments["title"],
                due_date=arguments["due_date"],
                contact_ids=arguments.get("contact_ids"),
                text=arguments.get("text"),
            )
        elif name == "dex_update_reminder":
            result = await client.update_reminder(
                reminder_id=arguments["reminder_id"],
                title=arguments.get("title"),
                text=arguments.get("text"),
                due_date=arguments.get("due_date"),
                is_complete=arguments.get("is_complete"),
            )
        elif name == "dex_complete_reminder":
            result = await client.complete_reminder(arguments["reminder_id"])
        elif name == "dex_delete_reminder":
            result = await client.delete_reminder(arguments["reminder_id"])

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def run_server():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    """Main entry point."""
    import asyncio
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
