import pytest
from unittest.mock import AsyncMock
from tuleap_mcp.tools import kanban
from tuleap_mcp.client import TuleapClient


@pytest.mark.asyncio
async def test_get_kanban():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"id": 1, "label": "Bugs Kanban"}

    result = await kanban.get_kanban(client_mock, kanban_id=1)

    client_mock.get.assert_called_once_with("/kanban/1")
    assert result == {"id": 1, "label": "Bugs Kanban"}


@pytest.mark.asyncio
async def test_update_kanban_label():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.patch.return_value = None

    await kanban.update_kanban(client_mock, kanban_id=1, label="New label")

    client_mock.patch.assert_called_once_with("/kanban/1", json={"label": "New label"})


@pytest.mark.asyncio
async def test_update_kanban_collapse_column():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.patch.return_value = None

    await kanban.update_kanban(
        client_mock, kanban_id=1, collapse_column_id=42, collapse_column_value=True
    )

    client_mock.patch.assert_called_once_with(
        "/kanban/1",
        json={"collapse_column": {"column_id": 42, "value": True}},
    )


@pytest.mark.asyncio
async def test_delete_kanban():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.delete.return_value = None

    await kanban.delete_kanban(client_mock, kanban_id=1)

    client_mock.delete.assert_called_once_with("/kanban/1")


@pytest.mark.asyncio
async def test_get_kanban_backlog():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"total_size": 0, "items": []}

    result = await kanban.get_kanban_backlog(client_mock, kanban_id=1)

    client_mock.get.assert_called_once_with(
        "/kanban/1/backlog", params={"query": "", "limit": 10, "offset": 0}
    )
    assert result == {"total_size": 0, "items": []}


@pytest.mark.asyncio
async def test_get_kanban_backlog_with_report():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"total_size": 0, "items": []}

    await kanban.get_kanban_backlog(client_mock, kanban_id=1, tracker_report_id=41)

    client_mock.get.assert_called_once_with(
        "/kanban/1/backlog",
        params={"query": '{"tracker_report_id": 41}', "limit": 10, "offset": 0},
    )


@pytest.mark.asyncio
async def test_update_kanban_backlog_add_and_order():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.patch.return_value = None

    await kanban.update_kanban_backlog(
        client_mock,
        kanban_id=1,
        add_ids=[100, 101],
        order_ids=[100],
        order_direction="before",
        order_compared_to=99,
    )

    client_mock.patch.assert_called_once_with(
        "/kanban/1/backlog",
        json={
            "add": {"ids": [100, 101]},
            "order": {"ids": [100], "direction": "before", "compared_to": 99},
        },
    )


@pytest.mark.asyncio
async def test_get_kanban_archive():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"total_size": 0, "items": []}

    result = await kanban.get_kanban_archive(client_mock, kanban_id=1)

    client_mock.get.assert_called_once_with(
        "/kanban/1/archive", params={"query": "", "limit": 10, "offset": 0}
    )
    assert result == {"total_size": 0, "items": []}


@pytest.mark.asyncio
async def test_update_kanban_archive():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.patch.return_value = None

    await kanban.update_kanban_archive(client_mock, kanban_id=1, add_ids=[100])

    client_mock.patch.assert_called_once_with(
        "/kanban/1/archive", json={"add": {"ids": [100]}}
    )


@pytest.mark.asyncio
async def test_get_kanban_column_items():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"total_size": 0, "items": []}

    result = await kanban.get_kanban_column_items(client_mock, kanban_id=1, column_id=5)

    client_mock.get.assert_called_once_with(
        "/kanban/1/items",
        params={"column_id": 5, "query": "", "limit": 10, "offset": 0},
    )
    assert result == {"total_size": 0, "items": []}


@pytest.mark.asyncio
async def test_update_kanban_column_items():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.patch.return_value = None

    await kanban.update_kanban_column_items(
        client_mock, kanban_id=1, column_id=5, add_ids=[100]
    )

    client_mock.patch.assert_called_once_with(
        "/kanban/1/items",
        params={"column_id": 5},
        json={"add": {"ids": [100]}},
    )


@pytest.mark.asyncio
async def test_create_kanban_column():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = {"id": 9, "label": "Review"}

    result = await kanban.create_kanban_column(client_mock, kanban_id=1, label="Review")

    client_mock.post.assert_called_once_with(
        "/kanban/1/columns", json={"label": "Review"}
    )
    assert result == {"id": 9, "label": "Review"}


@pytest.mark.asyncio
async def test_reorder_kanban_columns():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.put.return_value = None

    await kanban.reorder_kanban_columns(client_mock, kanban_id=1, column_ids=[3, 1, 2])

    client_mock.put.assert_called_once_with("/kanban/1/columns", json=[3, 1, 2])


@pytest.mark.asyncio
async def test_update_kanban_column():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.patch.return_value = None

    await kanban.update_kanban_column(
        client_mock, column_id=9, kanban_id=1, label="Done", wip_limit=3
    )

    client_mock.patch.assert_called_once_with(
        "/kanban_columns/9",
        params={"kanban_id": 1},
        json={"label": "Done", "wip_limit": 3},
    )


@pytest.mark.asyncio
async def test_delete_kanban_column():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.delete.return_value = None

    await kanban.delete_kanban_column(client_mock, column_id=9, kanban_id=1)

    client_mock.delete.assert_called_once_with(
        "/kanban_columns/9", params={"kanban_id": 1}
    )


@pytest.mark.asyncio
async def test_create_kanban_item():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = {"id": 200, "label": "New card"}

    result = await kanban.create_kanban_item(
        client_mock, kanban_id=1, label="New card", column_id=5
    )

    client_mock.post.assert_called_once_with(
        "/kanban_items",
        json={"kanban_id": 1, "label": "New card", "column_id": 5},
    )
    assert result == {"id": 200, "label": "New card"}


@pytest.mark.asyncio
async def test_get_kanban_item():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"id": 200, "label": "New card"}

    result = await kanban.get_kanban_item(client_mock, item_id=200)

    client_mock.get.assert_called_once_with("/kanban_items/200")
    assert result == {"id": 200, "label": "New card"}
