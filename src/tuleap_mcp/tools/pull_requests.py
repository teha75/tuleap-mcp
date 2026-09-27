import json
from typing import Any, Dict, List, Optional
from ..client import TuleapClient


def _build_pull_requests_query(
    status: Optional[str] = None,
    authors: Optional[List[int]] = None,
    labels: Optional[List[int]] = None,
    search: Optional[List[str]] = None,
    target_branches: Optional[List[str]] = None,
    reviewers: Optional[List[int]] = None,
    related_to: Optional[int] = None,
) -> str:
    """Build the JSON `query` string used to filter pull requests."""
    query: Dict[str, Any] = {}
    if status:
        query["status"] = status
    if authors:
        query["authors"] = [{"id": user_id} for user_id in authors]
    if labels:
        query["labels"] = [{"id": label_id} for label_id in labels]
    if search:
        query["search"] = [{"keyword": keyword} for keyword in search]
    if target_branches:
        query["target_branches"] = [{"name": name} for name in target_branches]
    if reviewers:
        query["reviewers"] = [{"id": user_id} for user_id in reviewers]
    if related_to:
        query["related_to"] = [{"id": related_to}]
    return json.dumps(query) if query else ""


async def list_pull_requests(
    client: TuleapClient,
    repository_id: int,
    status: Optional[str] = None,
    authors: Optional[List[int]] = None,
    labels: Optional[List[int]] = None,
    search: Optional[List[str]] = None,
    target_branches: Optional[List[str]] = None,
    reviewers: Optional[List[int]] = None,
    related_to: Optional[int] = None,
    order: str = "desc",
    limit: int = 50,
    offset: int = 0,
) -> Dict[str, Any]:
    """List pull requests of a git repository, with optional filters."""
    params = {
        "query": _build_pull_requests_query(
            status, authors, labels, search, target_branches, reviewers, related_to
        ),
        "order": order,
        "limit": limit,
        "offset": offset,
    }
    return await client.get(f"/git/{repository_id}/pull_requests", params=params)


async def get_pull_request_authors(
    client: TuleapClient, repository_id: int, limit: int = 50, offset: int = 0
) -> List[Dict[str, Any]]:
    """List the authors of pull requests in a git repository."""
    params = {"limit": limit, "offset": offset}
    return await client.get(
        f"/git/{repository_id}/pull_requests_authors", params=params
    )


async def get_repository_pull_request_reviewers(
    client: TuleapClient, repository_id: int, limit: int = 50, offset: int = 0
) -> List[Dict[str, Any]]:
    """List the reviewers of pull requests in a git repository."""
    params = {"limit": limit, "offset": offset}
    return await client.get(
        f"/git/{repository_id}/pull_requests_reviewers", params=params
    )


async def get_pull_request(
    client: TuleapClient, pull_request_id: int
) -> Dict[str, Any]:
    """Get details of a specific pull request."""
    return await client.get(f"/pull_requests/{pull_request_id}")


async def create_pull_request(
    client: TuleapClient,
    repository_id: int,
    repository_dest_id: int,
    branch_src: str,
    branch_dest: str,
) -> Dict[str, Any]:
    """Create a new pull request between two branches (which may live in two different, but related, repositories)."""
    payload = {
        "repository_id": repository_id,
        "repository_dest_id": repository_dest_id,
        "branch_src": branch_src,
        "branch_dest": branch_dest,
    }
    return await client.post("/pull_requests", json=payload)


async def update_pull_request(
    client: TuleapClient,
    pull_request_id: int,
    status: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    description_format: Optional[str] = None,
) -> Dict[str, Any]:
    """Update a pull request. Use `status` ("merge", "abandon" or "review") to change its
    state, or `title`/`description` to edit its metadata. These two usages are mutually
    exclusive: when `status` is provided, title/description are ignored by the API."""
    payload: Dict[str, Any] = {}
    if status is not None:
        payload["status"] = status
    else:
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if description_format is not None:
            payload["description_format"] = description_format
    return await client.patch(f"/pull_requests/{pull_request_id}", json=payload)


async def get_pull_request_commits(
    client: TuleapClient, pull_request_id: int, limit: int = 50, offset: int = 0
) -> List[Dict[str, Any]]:
    """List the commits of a pull request."""
    params = {"limit": limit, "offset": offset}
    return await client.get(f"/pull_requests/{pull_request_id}/commits", params=params)


async def get_pull_request_files(
    client: TuleapClient, pull_request_id: int
) -> List[Dict[str, Any]]:
    """List the files impacted by a pull request."""
    return await client.get(f"/pull_requests/{pull_request_id}/files")


async def get_pull_request_file_diff(
    client: TuleapClient, pull_request_id: int, path: str
) -> Dict[str, Any]:
    """Get the unified diff of a single file in a pull request."""
    return await client.get(
        f"/pull_requests/{pull_request_id}/file_diff", params={"path": path}
    )


async def get_pull_request_timeline(
    client: TuleapClient, pull_request_id: int, limit: int = 10, offset: int = 0
) -> Dict[str, Any]:
    """Get the timeline (comments, inline comments, status/reviewer changes) of a pull request."""
    params = {"limit": limit, "offset": offset}
    return await client.get(f"/pull_requests/{pull_request_id}/timeline", params=params)


async def get_pull_request_comments(
    client: TuleapClient,
    pull_request_id: int,
    limit: int = 10,
    offset: int = 0,
    order: str = "asc",
) -> List[Dict[str, Any]]:
    """List the general (non-inline) comments of a pull request."""
    params = {"limit": limit, "offset": offset, "order": order}
    return await client.get(f"/pull_requests/{pull_request_id}/comments", params=params)


async def add_pull_request_comment(
    client: TuleapClient,
    pull_request_id: int,
    content: str,
    format: Optional[str] = None,
    parent_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Post a new general comment on a pull request. `format` may be "text" or "commonmark"."""
    payload: Dict[str, Any] = {"content": content}
    if format is not None:
        payload["format"] = format
    if parent_id is not None:
        payload["parent_id"] = parent_id
    return await client.post(f"/pull_requests/{pull_request_id}/comments", json=payload)


async def update_pull_request_comment(
    client: TuleapClient, comment_id: int, content: str
) -> Dict[str, Any]:
    """Update the content of an existing general pull request comment."""
    return await client.patch(
        f"/pull_request_comments/{comment_id}", json={"content": content}
    )


async def add_pull_request_inline_comment(
    client: TuleapClient,
    pull_request_id: int,
    content: str,
    file_path: str,
    unidiff_offset: int,
    position: str,
    format: Optional[str] = None,
    parent_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Post a new inline comment on a pull request file. `position` must be "left" or "right"."""
    payload: Dict[str, Any] = {
        "content": content,
        "file_path": file_path,
        "unidiff_offset": unidiff_offset,
        "position": position,
    }
    if format is not None:
        payload["format"] = format
    if parent_id is not None:
        payload["parent_id"] = parent_id
    return await client.post(
        f"/pull_requests/{pull_request_id}/inline-comments", json=payload
    )


async def update_pull_request_inline_comment(
    client: TuleapClient, comment_id: int, content: str
) -> Dict[str, Any]:
    """Update the content of an existing inline pull request comment."""
    return await client.patch(
        f"/pull_request_inline_comments/{comment_id}", json={"content": content}
    )


async def reply_to_inline_comment(
    client: TuleapClient, comment_id: int, content: str, format: str = "commonmark"
) -> Dict[str, Any]:
    """Reply to an existing inline comment. `format` must be "text" or "commonmark"."""
    return await client.post(
        f"/pull_request_inline_comments/{comment_id}/reply",
        json={"content": content, "format": format},
    )


async def get_pull_request_labels(
    client: TuleapClient, pull_request_id: int, limit: int = 50, offset: int = 0
) -> Dict[str, Any]:
    """List the labels attached to a pull request."""
    params = {"limit": limit, "offset": offset}
    return await client.get(f"/pull_requests/{pull_request_id}/labels", params=params)


async def update_pull_request_labels(
    client: TuleapClient,
    pull_request_id: int,
    add: Optional[List[Dict[str, Any]]] = None,
    remove: Optional[List[Dict[str, Any]]] = None,
) -> None:
    """Add or remove labels on a pull request. `add`/`remove` are lists of dicts, e.g.
    [{"id": 1}] to reference an existing project label, or [{"label": "Emergency Fix"}]
    to create (or reuse) a label by name."""
    payload: Dict[str, Any] = {}
    if add:
        payload["add"] = add
    if remove:
        payload["remove"] = remove
    return await client.patch(f"/pull_requests/{pull_request_id}/labels", json=payload)


async def get_pull_request_reviewers(
    client: TuleapClient, pull_request_id: int
) -> Dict[str, Any]:
    """List the reviewers of a pull request."""
    return await client.get(f"/pull_requests/{pull_request_id}/reviewers")


async def set_pull_request_reviewers(
    client: TuleapClient, pull_request_id: int, users: List[Dict[str, Any]]
) -> None:
    """Set (replace) the reviewers of a pull request. `users` is a list of dicts
    referencing users, e.g. [{"id": 102}] or [{"username": "jdoe"}]."""
    return await client.put(
        f"/pull_requests/{pull_request_id}/reviewers", json={"users": users}
    )
