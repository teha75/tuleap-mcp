import pytest
from unittest.mock import AsyncMock
from tuleap_mcp.tools import docman
from tuleap_mcp.client import TuleapClient


@pytest.mark.asyncio
async def test_get_docman_service():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"root_item": {"id": 10}}

    result = await docman.get_docman_service(client_mock, project_id=1)

    client_mock.get.assert_called_once_with("/projects/1/docman_service")
    assert result == {"root_item": {"id": 10}}


@pytest.mark.asyncio
async def test_get_docman_project_metadata():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = [{"short_name": "field_3"}]

    result = await docman.get_docman_project_metadata(client_mock, project_id=1)

    client_mock.get.assert_called_once_with(
        "/projects/1/docman_metadata", params={"limit": 10, "offset": 0}
    )
    assert result == [{"short_name": "field_3"}]


@pytest.mark.asyncio
async def test_get_docman_item():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"id": 10, "type": "folder"}

    result = await docman.get_docman_item(client_mock, item_id=10, with_size=True)

    client_mock.get.assert_called_once_with(
        "/docman_items/10", params={"with_size": True}
    )
    assert result == {"id": 10, "type": "folder"}


@pytest.mark.asyncio
async def test_get_docman_folder_content():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = [{"id": 11, "type": "file"}]

    result = await docman.get_docman_folder_content(client_mock, folder_id=10)

    client_mock.get.assert_called_once_with(
        "/docman_items/10/docman_items", params={"limit": 50, "offset": 0}
    )
    assert result == [{"id": 11, "type": "file"}]


@pytest.mark.asyncio
async def test_get_docman_item_parents():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = [{"id": 10, "type": "folder"}]

    result = await docman.get_docman_item_parents(client_mock, item_id=11)

    client_mock.get.assert_called_once_with(
        "/docman_items/11/parents", params={"limit": 50, "offset": 0}
    )
    assert result == [{"id": 10, "type": "folder"}]


@pytest.mark.asyncio
async def test_get_docman_item_logs():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = [{"who": "jdoe", "what": "Item creation"}]

    result = await docman.get_docman_item_logs(client_mock, item_id=11)

    client_mock.get.assert_called_once_with(
        "/docman_items/11/logs", params={"limit": 50, "offset": 0}
    )
    assert result == [{"who": "jdoe", "what": "Item creation"}]


@pytest.mark.asyncio
async def test_search_docman_items_minimal():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = []

    result = await docman.search_docman_items(client_mock, folder_id=10)

    client_mock.post.assert_called_once_with(
        "/docman_search/10", json={"limit": 50, "offset": 0}
    )
    assert result == []


@pytest.mark.asyncio
async def test_search_docman_items_with_filters():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = [{"id": 11, "title": "Lorem ipsum"}]

    result = await docman.search_docman_items(
        client_mock,
        folder_id=10,
        global_search="lorem*",
        properties=[{"name": "type", "value": "folder"}],
        sort=[{"name": "title", "order": "asc"}],
    )

    client_mock.post.assert_called_once_with(
        "/docman_search/10",
        json={
            "limit": 50,
            "offset": 0,
            "global_search": "lorem*",
            "properties": [{"name": "type", "value": "folder"}],
            "sort": [{"name": "title", "order": "asc"}],
        },
    )
    assert result == [{"id": 11, "title": "Lorem ipsum"}]


@pytest.mark.asyncio
async def test_create_docman_folder():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = {"id": 20, "uri": "docman_items/20"}

    result = await docman.create_docman_folder(
        client_mock, parent_folder_id=10, title="Specs", description="Design docs"
    )

    client_mock.post.assert_called_once_with(
        "/docman_folders/10/folders",
        json={"title": "Specs", "description": "Design docs"},
    )
    assert result == {"id": 20, "uri": "docman_items/20"}


@pytest.mark.asyncio
async def test_create_docman_empty_document():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = {"id": 21}

    result = await docman.create_docman_empty_document(
        client_mock, parent_folder_id=10, title="Placeholder"
    )

    client_mock.post.assert_called_once_with(
        "/docman_folders/10/empties", json={"title": "Placeholder"}
    )
    assert result == {"id": 21}


@pytest.mark.asyncio
async def test_create_docman_link():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = {"id": 22}

    result = await docman.create_docman_link(
        client_mock,
        parent_folder_id=10,
        title="Wiki page",
        link_url="https://example.com",
    )

    client_mock.post.assert_called_once_with(
        "/docman_folders/10/links",
        json={
            "title": "Wiki page",
            "link_properties": {"link_url": "https://example.com"},
        },
    )
    assert result == {"id": 22}


@pytest.mark.asyncio
async def test_create_docman_embedded_file():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = {"id": 23}

    result = await docman.create_docman_embedded_file(
        client_mock, parent_folder_id=10, title="Notes", content="<p>Hello</p>"
    )

    client_mock.post.assert_called_once_with(
        "/docman_folders/10/embedded_files",
        json={"title": "Notes", "embedded_properties": {"content": "<p>Hello</p>"}},
    )
    assert result == {"id": 23}


@pytest.mark.asyncio
async def test_create_docman_other_type_document():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = {"id": 24}

    result = await docman.create_docman_other_type_document(
        client_mock, parent_folder_id=10, title="Contract", type="pdf_link"
    )

    client_mock.post.assert_called_once_with(
        "/docman_folders/10/others",
        json={"title": "Contract", "type": "pdf_link"},
    )
    assert result == {"id": 24}


@pytest.mark.asyncio
async def test_create_docman_file():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = {
        "id": 25,
        "file_properties": {"upload_href": "https://example.com/upload/25"},
    }

    result = await docman.create_docman_file(
        client_mock,
        parent_folder_id=10,
        title="Report",
        file_name="report.pdf",
        file_size=1024,
    )

    client_mock.post.assert_called_once_with(
        "/docman_folders/10/files",
        json={
            "title": "Report",
            "file_properties": {"file_name": "report.pdf", "file_size": 1024},
        },
    )
    assert result["file_properties"]["upload_href"] == "https://example.com/upload/25"


@pytest.mark.asyncio
async def test_move_docman_item():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.patch.return_value = None

    await docman.move_docman_item(
        client_mock, item_type="file", item_id=25, destination_folder_id=30
    )

    client_mock.patch.assert_called_once_with(
        "/docman_files/25", json={"move": {"destination_folder_id": 30}}
    )


@pytest.mark.asyncio
async def test_move_docman_item_rejects_other_type():
    client_mock = AsyncMock(spec=TuleapClient)

    with pytest.raises(ValueError):
        await docman.move_docman_item(
            client_mock, item_type="other_type", item_id=25, destination_folder_id=30
        )


@pytest.mark.asyncio
async def test_delete_docman_item():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.delete.return_value = None

    await docman.delete_docman_item(client_mock, item_type="link", item_id=22)

    client_mock.delete.assert_called_once_with("/docman_links/22")


@pytest.mark.asyncio
async def test_delete_docman_item_unknown_type():
    client_mock = AsyncMock(spec=TuleapClient)

    with pytest.raises(ValueError):
        await docman.delete_docman_item(client_mock, item_type="wiki", item_id=22)


@pytest.mark.asyncio
async def test_rename_docman_item():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.put.return_value = None

    await docman.rename_docman_item(
        client_mock,
        item_type="file",
        item_id=25,
        title="New title",
        owner_id=102,
        description="New desc",
    )

    client_mock.put.assert_called_once_with(
        "/docman_files/25/metadata",
        json={"title": "New title", "owner_id": 102, "description": "New desc"},
    )


@pytest.mark.asyncio
async def test_rename_docman_item_rejects_folder():
    client_mock = AsyncMock(spec=TuleapClient)

    with pytest.raises(ValueError):
        await docman.rename_docman_item(
            client_mock, item_type="folder", item_id=10, title="x", owner_id=102
        )


@pytest.mark.asyncio
async def test_update_docman_folder():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.put.return_value = None

    await docman.update_docman_folder(
        client_mock, folder_id=10, title="Specs", description="Design docs"
    )

    client_mock.put.assert_called_once_with(
        "/docman_folders/10/metadata",
        json={
            "title": "Specs",
            "status": {"value": "none", "recursion": "none"},
            "description": "Design docs",
        },
    )
