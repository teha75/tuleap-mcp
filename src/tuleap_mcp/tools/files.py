from typing import List, Dict, Any, Optional
from ..client import TuleapClient


async def get_git_repositories(
    client: TuleapClient, project_id: int
) -> List[Dict[str, Any]]:
    """List Git repositories in a project."""
    return await client.get(f"/projects/{project_id}/git")


async def get_artifact_file_chunk(
    client: TuleapClient, file_id: int, offset: int = 0, limit: int = 1048576
) -> Dict[str, Any]:
    """Get a (base64-encoded) chunk of a file already attached to an artifact."""
    params = {"offset": offset, "limit": limit}
    return await client.get(f"/artifact_files/{file_id}", params=params)


async def list_temporary_files(
    client: TuleapClient, limit: int = 10, offset: int = 0
) -> List[Dict[str, Any]]:
    """List the current user's temporary files (uploaded but not yet attached to an artifact)."""
    params = {"limit": limit, "offset": offset}
    return await client.get("/artifact_temporary_files", params=params)


async def get_temporary_file_chunk(
    client: TuleapClient, file_id: int, offset: int = 0, limit: int = 1048576
) -> Dict[str, Any]:
    """Get a (base64-encoded) chunk of one of the current user's temporary files."""
    params = {"offset": offset, "limit": limit}
    return await client.get(f"/artifact_temporary_files/{file_id}", params=params)


async def create_temporary_file(
    client: TuleapClient,
    name: str,
    mimetype: str,
    content_base64: str,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a temporary file from its first (base64-encoded) chunk. Max 1MB per chunk;
    use append_temporary_file_chunk for larger files. Attach the resulting file id to an
    artifact via update_artifact's `values` on a File field."""
    payload: Dict[str, Any] = {
        "name": name,
        "mimetype": mimetype,
        "content": content_base64,
    }
    if description is not None:
        payload["description"] = description
    return await client.post("/artifact_temporary_files", json=payload)


async def append_temporary_file_chunk(
    client: TuleapClient, file_id: int, content_base64: str, offset: int
) -> Dict[str, Any]:
    """Append a (base64-encoded) chunk to an existing temporary file. `offset` is the
    1-based index of this chunk (the first chunk from create_temporary_file is offset 1,
    so the next one is 2, etc.)."""
    return await client.put(
        f"/artifact_temporary_files/{file_id}",
        json={"content": content_base64, "offset": offset},
    )


async def delete_temporary_file(client: TuleapClient, file_id: int) -> None:
    """Delete one of the current user's temporary files."""
    return await client.delete(f"/artifact_temporary_files/{file_id}")
