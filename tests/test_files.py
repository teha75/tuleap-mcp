import pytest
from unittest.mock import AsyncMock
from tuleap_mcp.tools.files import (
    get_git_repositories,
    get_artifact_file_chunk,
    list_temporary_files,
    get_temporary_file_chunk,
    create_temporary_file,
    append_temporary_file_chunk,
    delete_temporary_file,
)


@pytest.mark.asyncio
async def test_get_git_repositories():
    mock_client = AsyncMock()
    mock_client.get.return_value = [{"id": 10, "name": "backend"}]

    result = await get_git_repositories(mock_client, project_id=1)

    mock_client.get.assert_called_once_with("/projects/1/git")
    assert result == [{"id": 10, "name": "backend"}]


@pytest.mark.asyncio
async def test_get_artifact_file_chunk():
    mock_client = AsyncMock()
    mock_client.get.return_value = {"data": "aGVsbG8="}

    result = await get_artifact_file_chunk(mock_client, file_id=7)

    mock_client.get.assert_called_once_with(
        "/artifact_files/7", params={"offset": 0, "limit": 1048576}
    )
    assert result == {"data": "aGVsbG8="}


@pytest.mark.asyncio
async def test_list_temporary_files():
    mock_client = AsyncMock()
    mock_client.get.return_value = [{"id": 1, "name": "diagram.png"}]

    result = await list_temporary_files(mock_client)

    mock_client.get.assert_called_once_with(
        "/artifact_temporary_files", params={"limit": 10, "offset": 0}
    )
    assert result == [{"id": 1, "name": "diagram.png"}]


@pytest.mark.asyncio
async def test_get_temporary_file_chunk():
    mock_client = AsyncMock()
    mock_client.get.return_value = {"data": "aGVsbG8="}

    result = await get_temporary_file_chunk(mock_client, file_id=1)

    mock_client.get.assert_called_once_with(
        "/artifact_temporary_files/1", params={"offset": 0, "limit": 1048576}
    )
    assert result == {"data": "aGVsbG8="}


@pytest.mark.asyncio
async def test_create_temporary_file():
    mock_client = AsyncMock()
    mock_client.post.return_value = {"id": 1, "name": "diagram.png"}

    result = await create_temporary_file(
        mock_client,
        name="diagram.png",
        mimetype="image/png",
        content_base64="aGVsbG8=",
        description="A diagram",
    )

    mock_client.post.assert_called_once_with(
        "/artifact_temporary_files",
        json={
            "name": "diagram.png",
            "mimetype": "image/png",
            "content": "aGVsbG8=",
            "description": "A diagram",
        },
    )
    assert result == {"id": 1, "name": "diagram.png"}


@pytest.mark.asyncio
async def test_append_temporary_file_chunk():
    mock_client = AsyncMock()
    mock_client.put.return_value = {"id": 1, "size": 2048}

    result = await append_temporary_file_chunk(
        mock_client, file_id=1, content_base64="d29ybGQ=", offset=2
    )

    mock_client.put.assert_called_once_with(
        "/artifact_temporary_files/1",
        json={"content": "d29ybGQ=", "offset": 2},
    )
    assert result == {"id": 1, "size": 2048}


@pytest.mark.asyncio
async def test_delete_temporary_file():
    mock_client = AsyncMock()
    mock_client.delete.return_value = None

    await delete_temporary_file(mock_client, file_id=1)

    mock_client.delete.assert_called_once_with("/artifact_temporary_files/1")
