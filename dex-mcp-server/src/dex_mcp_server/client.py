"""Dex CRM API client."""

import httpx
from typing import Any


class DexClient:
    """Client for interacting with the Dex CRM API."""

    BASE_URL = "https://api.getdex.com/api/rest"

    def __init__(self, api_key: str):
        """Initialize the Dex client with an API key.

        Args:
            api_key: Your Dex API key from https://getdex.com/appv3/settings/api
        """
        self.api_key = api_key
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Content-Type": "application/json",
                "x-hasura-dex-api-key": api_key,
            },
            timeout=30.0,
        )

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an API request."""
        response = await self._client.request(method, path, params=params, json=json)
        response.raise_for_status()
        return response.json()

    # -------------------------------------------------------------------------
    # Contacts
    # -------------------------------------------------------------------------

    async def list_contacts(
        self, limit: int = 10, offset: int = 0
    ) -> dict[str, Any]:
        """Fetch all contacts with pagination.

        Args:
            limit: Maximum number of contacts to return (default: 10)
            offset: Number of contacts to skip (default: 0)

        Returns:
            Dictionary with 'contacts' list and 'pagination' info
        """
        return await self._request(
            "GET", "/contacts", params={"limit": limit, "offset": offset}
        )

    async def get_contact(self, contact_id: str) -> dict[str, Any]:
        """Fetch a specific contact by ID.

        Args:
            contact_id: The UUID of the contact

        Returns:
            Contact details
        """
        return await self._request("GET", f"/contacts/{contact_id}")

    async def search_contacts_by_email(self, email: str) -> dict[str, Any]:
        """Search for contacts by email address.

        Args:
            email: Email address to search for

        Returns:
            Matching contacts
        """
        return await self._request(
            "GET", "/search/contacts", params={"email": email}
        )

    async def create_contact(
        self,
        first_name: str,
        last_name: str,
        email: str | None = None,
        phone: str | None = None,
        phone_label: str = "Work",
        job_title: str | None = None,
        description: str | None = None,
        linkedin: str | None = None,
        twitter: str | None = None,
        instagram: str | None = None,
        website: str | None = None,
    ) -> dict[str, Any]:
        """Create a new contact.

        Args:
            first_name: Contact's first name
            last_name: Contact's last name
            email: Contact's email address
            phone: Contact's phone number
            phone_label: Label for phone (e.g., "Work", "Mobile")
            job_title: Contact's job title
            description: Notes about the contact
            linkedin: LinkedIn username
            twitter: Twitter handle
            instagram: Instagram username
            website: Personal website URL

        Returns:
            Created contact details
        """
        contact_data: dict[str, Any] = {
            "first_name": first_name,
            "last_name": last_name,
            "job_title": job_title,
            "description": description,
            "linkedin": linkedin,
            "twitter": twitter,
            "instagram": instagram,
            "website": website,
        }

        if email:
            contact_data["contact_emails"] = {"data": {"email": email}}

        if phone:
            contact_data["contact_phone_numbers"] = {
                "data": {"phone_number": phone, "label": phone_label}
            }

        return await self._request("POST", "/contacts", json={"contact": contact_data})

    async def update_contact(
        self, contact_id: str, **fields: Any
    ) -> dict[str, Any]:
        """Update an existing contact.

        Args:
            contact_id: The UUID of the contact to update
            **fields: Fields to update (first_name, last_name, job_title, etc.)

        Returns:
            Updated contact details
        """
        return await self._request(
            "PUT", f"/contacts/{contact_id}", json={"contact": fields}
        )

    async def delete_contact(self, contact_id: str) -> dict[str, Any]:
        """Delete a contact.

        Args:
            contact_id: The UUID of the contact to delete

        Returns:
            Deletion confirmation
        """
        return await self._request("DELETE", f"/contacts/{contact_id}")

    # -------------------------------------------------------------------------
    # Notes (Timeline Items)
    # -------------------------------------------------------------------------

    async def list_notes(
        self, limit: int = 10, offset: int = 0
    ) -> dict[str, Any]:
        """Fetch all notes with pagination.

        Args:
            limit: Maximum number of notes to return (default: 10)
            offset: Number of notes to skip (default: 0)

        Returns:
            Dictionary with 'timeline_items' list and 'pagination' info
        """
        return await self._request(
            "GET", "/timeline_items", params={"limit": limit, "offset": offset}
        )

    async def get_notes_for_contact(self, contact_id: str) -> dict[str, Any]:
        """Fetch all notes for a specific contact.

        Args:
            contact_id: The UUID of the contact

        Returns:
            Notes associated with the contact
        """
        return await self._request("GET", f"/timeline_items/contacts/{contact_id}")

    async def create_note(
        self,
        note: str,
        contact_ids: list[str],
        event_time: str | None = None,
    ) -> dict[str, Any]:
        """Create a new note.

        Args:
            note: The note content
            contact_ids: List of contact UUIDs to associate with this note
            event_time: ISO 8601 timestamp (defaults to now if not provided)

        Returns:
            Created note details
        """
        from datetime import datetime, timezone

        if event_time is None:
            event_time = datetime.now(timezone.utc).isoformat()

        timeline_event = {
            "note": note,
            "event_time": event_time,
            "meeting_type": "note",
            "timeline_items_contacts": {
                "data": [{"contact_id": cid} for cid in contact_ids]
            },
        }

        return await self._request(
            "POST", "/timeline_items", json={"timeline_event": timeline_event}
        )

    async def update_note(
        self, note_id: str, note: str
    ) -> dict[str, Any]:
        """Update an existing note.

        Args:
            note_id: The UUID of the note to update
            note: New note content

        Returns:
            Updated note details
        """
        return await self._request(
            "PUT", f"/timeline_items/{note_id}", json={"timeline_event": {"note": note}}
        )

    async def delete_note(self, note_id: str) -> dict[str, Any]:
        """Delete a note.

        Args:
            note_id: The UUID of the note to delete

        Returns:
            Deletion confirmation
        """
        return await self._request("DELETE", f"/timeline_items/{note_id}")

    # -------------------------------------------------------------------------
    # Reminders
    # -------------------------------------------------------------------------

    async def list_reminders(
        self, limit: int = 10, offset: int = 0
    ) -> dict[str, Any]:
        """Fetch all reminders with pagination.

        Args:
            limit: Maximum number of reminders to return (default: 10)
            offset: Number of reminders to skip (default: 0)

        Returns:
            Dictionary with 'reminders' list and total count
        """
        return await self._request(
            "GET", "/reminders", params={"limit": limit, "offset": offset}
        )

    async def create_reminder(
        self,
        title: str,
        due_date: str,
        contact_ids: list[str] | None = None,
        text: str | None = None,
        is_complete: bool = False,
    ) -> dict[str, Any]:
        """Create a new reminder.

        Args:
            title: Reminder title
            due_date: Due date in YYYY-MM-DD format
            contact_ids: List of contact UUIDs to associate with this reminder
            text: Additional reminder details
            is_complete: Whether the reminder is already complete

        Returns:
            Created reminder details
        """
        reminder_data: dict[str, Any] = {
            "title": title,
            "text": text,
            "is_complete": is_complete,
            "due_at_date": due_date,
        }

        if contact_ids:
            reminder_data["reminders_contacts"] = {
                "data": [{"contact_id": cid} for cid in contact_ids]
            }

        return await self._request(
            "POST", "/reminders", json={"reminder": reminder_data}
        )

    async def update_reminder(
        self,
        reminder_id: str,
        title: str | None = None,
        text: str | None = None,
        due_date: str | None = None,
        is_complete: bool | None = None,
    ) -> dict[str, Any]:
        """Update an existing reminder.

        Args:
            reminder_id: The UUID of the reminder to update
            title: New title (optional)
            text: New text (optional)
            due_date: New due date in YYYY-MM-DD format (optional)
            is_complete: New completion status (optional)

        Returns:
            Updated reminder details
        """
        reminder_data: dict[str, Any] = {}
        if title is not None:
            reminder_data["title"] = title
        if text is not None:
            reminder_data["text"] = text
        if due_date is not None:
            reminder_data["due_at_date"] = due_date
        if is_complete is not None:
            reminder_data["is_complete"] = is_complete

        return await self._request(
            "PUT", f"/reminders/{reminder_id}", json={"reminder": reminder_data}
        )

    async def delete_reminder(self, reminder_id: str) -> dict[str, Any]:
        """Delete a reminder.

        Args:
            reminder_id: The UUID of the reminder to delete

        Returns:
            Deletion confirmation
        """
        return await self._request("DELETE", f"/reminders/{reminder_id}")

    async def complete_reminder(self, reminder_id: str) -> dict[str, Any]:
        """Mark a reminder as complete.

        Args:
            reminder_id: The UUID of the reminder

        Returns:
            Updated reminder details
        """
        return await self.update_reminder(reminder_id, is_complete=True)
