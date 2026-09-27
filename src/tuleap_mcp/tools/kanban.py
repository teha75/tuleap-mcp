import json
from typing import Any, Dict, List, Optional
from ..client import TuleapClient


def _build_report_query(tracker_report_id: Optional[int]) -> str:
    return (
        json.dumps({"tracker_report_id": tracker_report_id})
        if tracker_report_id
        else ""
    )


def _build_order(
    order_ids: Optional[List[int]],
    order_direction: Optional[str],
    order_compared_to: Optional[int],
) -> Optional[Dict[str, Any]]:
    if not order_ids:
        return None
    return {
        "ids": order_ids,
        "direction": order_direction,
        "compared_to": order_compared_to,
    }


async def get_kanban(client: TuleapClient, kanban_id: int) -> Dict[str, Any]:
    """Get the definition of a kanban board (columns, backlog/archive info)."""
    return await client.get(f"/kanban/{kanban_id}")


async def update_kanban(
    client: TuleapClient,
    kanban_id: int,
    label: Optional[str] = None,
    is_promoted: Optional[bool] = None,
    collapse_backlog: Optional[bool] = None,
    collapse_archive: Optional[bool] = None,
    collapse_column_id: Optional[int] = None,
    collapse_column_value: Optional[bool] = None,
) -> None:
    """Update a kanban's label/promotion, or collapse/expand its backlog, archive or a column
    (saved as the current user's preference)."""
    payload: Dict[str, Any] = {}
    if label is not None:
        payload["label"] = label
    if is_promoted is not None:
        payload["is_promoted"] = is_promoted
    if collapse_backlog is not None:
        payload["collapse_backlog"] = collapse_backlog
    if collapse_archive is not None:
        payload["collapse_archive"] = collapse_archive
    if collapse_column_id is not None:
        payload["collapse_column"] = {
            "column_id": collapse_column_id,
            "value": collapse_column_value,
        }
    return await client.patch(f"/kanban/{kanban_id}", json=payload)


async def delete_kanban(client: TuleapClient, kanban_id: int) -> None:
    """Delete a kanban board."""
    return await client.delete(f"/kanban/{kanban_id}")


async def get_kanban_backlog(
    client: TuleapClient,
    kanban_id: int,
    tracker_report_id: Optional[int] = None,
    limit: int = 10,
    offset: int = 0,
) -> Dict[str, Any]:
    """Get the items in a kanban's backlog column, optionally filtered by a tracker report."""
    params = {
        "query": _build_report_query(tracker_report_id),
        "limit": limit,
        "offset": offset,
    }
    return await client.get(f"/kanban/{kanban_id}/backlog", params=params)


async def update_kanban_backlog(
    client: TuleapClient,
    kanban_id: int,
    add_ids: Optional[List[int]] = None,
    order_ids: Optional[List[int]] = None,
    order_direction: Optional[str] = None,
    order_compared_to: Optional[int] = None,
) -> None:
    """Add items to a kanban's backlog column and/or reorder items within it. `order_direction`
    is "before" or "after" `order_compared_to` (an item id already in the backlog)."""
    payload: Dict[str, Any] = {}
    if add_ids:
        payload["add"] = {"ids": add_ids}
    order = _build_order(order_ids, order_direction, order_compared_to)
    if order:
        payload["order"] = order
    return await client.patch(f"/kanban/{kanban_id}/backlog", json=payload)


async def get_kanban_archive(
    client: TuleapClient,
    kanban_id: int,
    tracker_report_id: Optional[int] = None,
    limit: int = 10,
    offset: int = 0,
) -> Dict[str, Any]:
    """Get the archived (closed) items of a kanban, optionally filtered by a tracker report."""
    params = {
        "query": _build_report_query(tracker_report_id),
        "limit": limit,
        "offset": offset,
    }
    return await client.get(f"/kanban/{kanban_id}/archive", params=params)


async def update_kanban_archive(
    client: TuleapClient,
    kanban_id: int,
    add_ids: Optional[List[int]] = None,
    order_ids: Optional[List[int]] = None,
    order_direction: Optional[str] = None,
    order_compared_to: Optional[int] = None,
) -> None:
    """Move items into a kanban's archive and/or reorder items within it."""
    payload: Dict[str, Any] = {}
    if add_ids:
        payload["add"] = {"ids": add_ids}
    order = _build_order(order_ids, order_direction, order_compared_to)
    if order:
        payload["order"] = order
    return await client.patch(f"/kanban/{kanban_id}/archive", json=payload)


async def get_kanban_column_items(
    client: TuleapClient,
    kanban_id: int,
    column_id: int,
    tracker_report_id: Optional[int] = None,
    limit: int = 10,
    offset: int = 0,
) -> Dict[str, Any]:
    """Get the items in a given column of a kanban, optionally filtered by a tracker report."""
    params = {
        "column_id": column_id,
        "query": _build_report_query(tracker_report_id),
        "limit": limit,
        "offset": offset,
    }
    return await client.get(f"/kanban/{kanban_id}/items", params=params)


async def update_kanban_column_items(
    client: TuleapClient,
    kanban_id: int,
    column_id: int,
    add_ids: Optional[List[int]] = None,
    order_ids: Optional[List[int]] = None,
    order_direction: Optional[str] = None,
    order_compared_to: Optional[int] = None,
) -> None:
    """Move items into a kanban column (e.g. drag a card to a new column) and/or reorder items
    within it."""
    payload: Dict[str, Any] = {}
    if add_ids:
        payload["add"] = {"ids": add_ids}
    order = _build_order(order_ids, order_direction, order_compared_to)
    if order:
        payload["order"] = order
    return await client.patch(
        f"/kanban/{kanban_id}/items", params={"column_id": column_id}, json=payload
    )


async def create_kanban_column(
    client: TuleapClient, kanban_id: int, label: str
) -> Dict[str, Any]:
    """Add a new column to a kanban board."""
    return await client.post(f"/kanban/{kanban_id}/columns", json={"label": label})


async def reorder_kanban_columns(
    client: TuleapClient, kanban_id: int, column_ids: List[int]
) -> None:
    """Reorder a kanban's columns. `column_ids` is the full list of column ids in their new order."""
    return await client.put(f"/kanban/{kanban_id}/columns", json=column_ids)


async def update_kanban_column(
    client: TuleapClient,
    column_id: int,
    kanban_id: int,
    label: Optional[str] = None,
    wip_limit: Optional[int] = None,
) -> None:
    """Rename a kanban column and/or set its WIP limit."""
    payload: Dict[str, Any] = {}
    if label is not None:
        payload["label"] = label
    if wip_limit is not None:
        payload["wip_limit"] = wip_limit
    return await client.patch(
        f"/kanban_columns/{column_id}", params={"kanban_id": kanban_id}, json=payload
    )


async def delete_kanban_column(
    client: TuleapClient, column_id: int, kanban_id: int
) -> None:
    """Delete a column from a kanban board."""
    return await client.delete(
        f"/kanban_columns/{column_id}", params={"kanban_id": kanban_id}
    )


async def create_kanban_item(
    client: TuleapClient, kanban_id: int, label: str, column_id: int = 0
) -> Dict[str, Any]:
    """Create a new kanban item (artifact) in a kanban board, in a given column (0 = backlog)."""
    payload = {"kanban_id": kanban_id, "label": label, "column_id": column_id}
    return await client.post("/kanban_items", json=payload)


async def get_kanban_item(client: TuleapClient, item_id: int) -> Dict[str, Any]:
    """Get details of a kanban item."""
    return await client.get(f"/kanban_items/{item_id}")
