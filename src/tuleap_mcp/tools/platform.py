from typing import Any, Dict, List, Optional
from ..client import TuleapClient


async def get_platform_banner(client: TuleapClient) -> Dict[str, Any]:
    """Get the platform-wide banner message, if any is set."""
    return await client.get("/banner")


async def set_platform_banner(
    client: TuleapClient,
    message: str,
    importance: str = "standard",
    expiration_date: Optional[str] = None,
) -> None:
    """Set the platform-wide banner (site admin only). `importance` is "standard", "warning"
    or "critical". `expiration_date` is an optional ISO-8601 date; omit for no expiration."""
    payload: Dict[str, Any] = {"message": message, "importance": importance}
    if expiration_date is not None:
        payload["expiration_date"] = expiration_date
    return await client.put("/banner", json=payload)


async def delete_platform_banner(client: TuleapClient) -> None:
    """Delete the platform-wide banner (site admin only)."""
    return await client.delete("/banner")


async def get_project_banner(client: TuleapClient, project_id: int) -> Dict[str, Any]:
    """Get a project's banner message, if any is set."""
    return await client.get(f"/projects/{project_id}/banner")


async def set_project_banner(
    client: TuleapClient, project_id: int, message: str
) -> None:
    """Set a project's banner message (requires project admin rights)."""
    payload = {"message": message, "importance": "standard"}
    return await client.put(f"/projects/{project_id}/banner", json=payload)


async def delete_project_banner(client: TuleapClient, project_id: int) -> None:
    """Delete a project's banner message."""
    return await client.delete(f"/projects/{project_id}/banner")


async def get_system_events(
    client: TuleapClient,
    status: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    """List platform system events (site admin only). `status` filters by "new", "running",
    "done", "warning" or "error" - use status="error" to see failed background jobs."""
    params: Dict[str, Any] = {"limit": limit, "offset": offset}
    if status is not None:
        params["status"] = status
    return await client.get("/system_event", params=params)
