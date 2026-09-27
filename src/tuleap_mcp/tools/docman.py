from typing import Any, Dict, List, Optional
from ..client import TuleapClient

_MOVABLE_ITEM_ROUTES = {
    "folder": "docman_folders",
    "file": "docman_files",
    "link": "docman_links",
    "embedded_file": "docman_embedded_files",
    "empty_document": "docman_empty_documents",
}

_ITEM_ROUTES = {
    **_MOVABLE_ITEM_ROUTES,
    "other_type": "docman_other_type_documents",
}


def _item_route(item_type: str) -> str:
    try:
        return _ITEM_ROUTES[item_type]
    except KeyError:
        raise ValueError(
            f"Unknown item_type '{item_type}'. Expected one of: {', '.join(_ITEM_ROUTES)}"
        )


async def get_docman_service(client: TuleapClient, project_id: int) -> Dict[str, Any]:
    """Get a project's Document Manager service info, including its root folder (root_item.id),
    the entry point for browsing the document tree."""
    return await client.get(f"/projects/{project_id}/docman_service")


async def get_docman_project_metadata(
    client: TuleapClient, project_id: int, limit: int = 10, offset: int = 0
) -> List[Dict[str, Any]]:
    """List the custom metadata fields defined for a project's Document Manager."""
    params = {"limit": limit, "offset": offset}
    return await client.get(f"/projects/{project_id}/docman_metadata", params=params)


async def get_docman_item(
    client: TuleapClient, item_id: int, with_size: bool = False
) -> Dict[str, Any]:
    """Get a document manager item (folder, file, link, embedded file, empty document...).
    with_size (folders only) also returns the folder's total size in bytes."""
    params = {"with_size": with_size}
    return await client.get(f"/docman_items/{item_id}", params=params)


async def get_docman_folder_content(
    client: TuleapClient, folder_id: int, limit: int = 50, offset: int = 0
) -> List[Dict[str, Any]]:
    """List the direct children of a document manager folder."""
    params = {"limit": limit, "offset": offset}
    return await client.get(f"/docman_items/{folder_id}/docman_items", params=params)


async def get_docman_item_parents(
    client: TuleapClient, item_id: int, limit: int = 50, offset: int = 0
) -> List[Dict[str, Any]]:
    """Get the parent folders of a document manager item, ordered from root to direct parent."""
    params = {"limit": limit, "offset": offset}
    return await client.get(f"/docman_items/{item_id}/parents", params=params)


async def get_docman_item_logs(
    client: TuleapClient, item_id: int, limit: int = 50, offset: int = 0
) -> List[Dict[str, Any]]:
    """Get the audit log (creation, updates, moves...) of a document manager item."""
    params = {"limit": limit, "offset": offset}
    return await client.get(f"/docman_items/{item_id}/logs", params=params)


async def search_docman_items(
    client: TuleapClient,
    folder_id: int,
    global_search: Optional[str] = None,
    properties: Optional[List[Dict[str, Any]]] = None,
    sort: Optional[List[Dict[str, Any]]] = None,
    limit: int = 50,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    """Search paginated items recursively under a folder (use the project's root_item id from
    get_docman_service to search the whole document tree). `global_search` matches all text
    properties (supports "lorem", "lorem*", "*lorem", "*lorem*"). `properties` is a list of
    {"name": ..., "value": ...} (or "value_date": {"date": "2022-01-30", "operator": "<|>|="})
    filters on fields like "type", "title", "status", "owner", "field_XXX" (custom metadata).
    `sort` is a list of {"name": ..., "order": "asc"|"desc"}."""
    payload: Dict[str, Any] = {"limit": limit, "offset": offset}
    if global_search is not None:
        payload["global_search"] = global_search
    if properties:
        payload["properties"] = properties
    if sort:
        payload["sort"] = sort
    return await client.post(f"/docman_search/{folder_id}", json=payload)


async def create_docman_folder(
    client: TuleapClient,
    parent_folder_id: int,
    title: str,
    description: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new subfolder. `status` may be "none" (default), "draft", "approved" or
    "rejected", if the project's document approval workflow is enabled."""
    payload: Dict[str, Any] = {"title": title}
    if description is not None:
        payload["description"] = description
    if status is not None:
        payload["status"] = status
    return await client.post(
        f"/docman_folders/{parent_folder_id}/folders", json=payload
    )


async def create_docman_empty_document(
    client: TuleapClient,
    parent_folder_id: int,
    title: str,
    description: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new empty document placeholder in a folder."""
    payload: Dict[str, Any] = {"title": title}
    if description is not None:
        payload["description"] = description
    if status is not None:
        payload["status"] = status
    return await client.post(
        f"/docman_folders/{parent_folder_id}/empties", json=payload
    )


async def create_docman_link(
    client: TuleapClient,
    parent_folder_id: int,
    title: str,
    link_url: str,
    description: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new link document pointing to an external URL."""
    payload: Dict[str, Any] = {
        "title": title,
        "link_properties": {"link_url": link_url},
    }
    if description is not None:
        payload["description"] = description
    if status is not None:
        payload["status"] = status
    return await client.post(f"/docman_folders/{parent_folder_id}/links", json=payload)


async def create_docman_embedded_file(
    client: TuleapClient,
    parent_folder_id: int,
    title: str,
    content: str = "",
    description: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new embedded file (HTML content stored directly in Tuleap, not uploaded)."""
    payload: Dict[str, Any] = {
        "title": title,
        "embedded_properties": {"content": content},
    }
    if description is not None:
        payload["description"] = description
    if status is not None:
        payload["status"] = status
    return await client.post(
        f"/docman_folders/{parent_folder_id}/embedded_files", json=payload
    )


async def create_docman_other_type_document(
    client: TuleapClient,
    parent_folder_id: int,
    title: str,
    type: str,
    description: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new document of a custom "other" type (as configured by project admins)."""
    payload: Dict[str, Any] = {"title": title, "type": type}
    if description is not None:
        payload["description"] = description
    if status is not None:
        payload["status"] = status
    return await client.post(f"/docman_folders/{parent_folder_id}/others", json=payload)


async def create_docman_file(
    client: TuleapClient,
    parent_folder_id: int,
    title: str,
    file_name: str,
    file_size: int,
    description: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    """Declare a new file document. This only creates the file's metadata; the returned
    file_properties.upload_href must then be used to upload the actual file content
    separately via the tus.io resumable upload protocol (https://tus.io) - not a plain
    JSON call, so it is not handled by this tool."""
    payload: Dict[str, Any] = {
        "title": title,
        "file_properties": {"file_name": file_name, "file_size": file_size},
    }
    if description is not None:
        payload["description"] = description
    if status is not None:
        payload["status"] = status
    return await client.post(f"/docman_folders/{parent_folder_id}/files", json=payload)


async def move_docman_item(
    client: TuleapClient, item_type: str, item_id: int, destination_folder_id: int
) -> None:
    """Move a document manager item to a different parent folder. item_type is one of:
    folder, file, link, embedded_file, empty_document (not supported for other_type items)."""
    if item_type not in _MOVABLE_ITEM_ROUTES:
        raise ValueError(
            f"Unknown or non-movable item_type '{item_type}'. Expected one of: "
            f"{', '.join(_MOVABLE_ITEM_ROUTES)}"
        )
    route = _MOVABLE_ITEM_ROUTES[item_type]
    payload = {"move": {"destination_folder_id": destination_folder_id}}
    return await client.patch(f"/{route}/{item_id}", json=payload)


async def delete_docman_item(
    client: TuleapClient, item_type: str, item_id: int
) -> None:
    """Delete a document manager item. item_type is one of: folder, file, link,
    embedded_file, empty_document, other_type."""
    route = _item_route(item_type)
    return await client.delete(f"/{route}/{item_id}")


async def rename_docman_item(
    client: TuleapClient,
    item_type: str,
    item_id: int,
    title: str,
    owner_id: int,
    description: Optional[str] = None,
    status: Optional[str] = None,
    obsolescence_date: Optional[str] = None,
) -> None:
    """Update the title/description/owner/status of a non-folder document manager item
    (file, link, embedded_file, empty_document, other_type - use update_docman_folder for
    folders). This is a full replace of the item's properties: owner_id is required by the
    API - pass the item's current owner id (from get_docman_item) to leave it unchanged."""
    if item_type == "folder":
        raise ValueError("Use update_docman_folder for folders.")
    route = _item_route(item_type)
    payload: Dict[str, Any] = {"title": title, "owner_id": owner_id}
    if description is not None:
        payload["description"] = description
    if status is not None:
        payload["status"] = status
    if obsolescence_date is not None:
        payload["obsolescence_date"] = obsolescence_date
    return await client.put(f"/{route}/{item_id}/metadata", json=payload)


async def update_docman_folder(
    client: TuleapClient,
    folder_id: int,
    title: str,
    description: Optional[str] = None,
    status_value: str = "none",
    status_recursion: str = "none",
) -> None:
    """Update the title/description/status of a folder. This is a full replace of the
    folder's properties. status_recursion applies status_value to "none" (this folder only),
    "folders" (subfolders too) or "all_items" (subfolders and documents)."""
    payload: Dict[str, Any] = {
        "title": title,
        "status": {"value": status_value, "recursion": status_recursion},
    }
    if description is not None:
        payload["description"] = description
    return await client.put(f"/docman_folders/{folder_id}/metadata", json=payload)
