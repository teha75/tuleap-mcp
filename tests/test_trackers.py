import pytest
from unittest.mock import AsyncMock
from tuleap_mcp.tools.trackers import (
    get_artifact_details,
    search_artifacts,
    update_artifact,
    get_tracker,
    get_tracker_reports,
    get_tracker_artifacts,
    get_tracker_parent_artifacts,
    update_tracker_workflow,
    get_tracker_report,
    get_tracker_report_artifacts,
)
from tuleap_mcp.client import TuleapClient


@pytest.mark.asyncio
async def test_get_artifact_details():
    mock_client = AsyncMock()
    mock_client.get.return_value = {"id": 100, "title": "Bug"}

    result = await get_artifact_details(mock_client, artifact_id=100)

    mock_client.get.assert_called_once_with("/artifacts/100")
    assert result == {"id": 100, "title": "Bug"}


@pytest.mark.asyncio
async def test_search_artifacts():
    mock_client = AsyncMock()
    mock_client.get.return_value = [{"id": 100}]

    result = await search_artifacts(mock_client, tracker_id=5, query="auth")

    mock_client.get.assert_called_once_with(
        "/artifacts", params={"tracker_id": 5, "query": "auth"}
    )
    assert result == [{"id": 100}]


@pytest.mark.asyncio
async def test_update_artifact():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.put.return_value = {"id": 123, "status": "updated"}

    values = [{"field_id": 1, "value": "New Title"}]
    comment = "Doing some work"

    result = await update_artifact(client_mock, 123, values, comment)

    client_mock.put.assert_called_once_with(
        "/artifacts/123", json={"values": values, "comment": {"body": comment, "format": "text"}}
    )
    assert result == {"id": 123, "status": "updated"}


@pytest.mark.asyncio
async def test_get_tracker():
    mock_client = AsyncMock()
    mock_client.get.return_value = {"id": 5, "label": "Bugs"}

    result = await get_tracker(mock_client, tracker_id=5)

    mock_client.get.assert_called_once_with("/trackers/5")
    assert result == {"id": 5, "label": "Bugs"}


@pytest.mark.asyncio
async def test_get_tracker_reports():
    mock_client = AsyncMock()
    mock_client.get.return_value = [{"id": 1, "label": "Default"}]

    result = await get_tracker_reports(mock_client, tracker_id=5)

    mock_client.get.assert_called_once_with(
        "/trackers/5/tracker_reports", params={"limit": 10, "offset": 0}
    )
    assert result == [{"id": 1, "label": "Default"}]


@pytest.mark.asyncio
async def test_get_tracker_artifacts_no_filters():
    mock_client = AsyncMock()
    mock_client.get.return_value = [{"id": 100}]

    result = await get_tracker_artifacts(mock_client, tracker_id=5)

    mock_client.get.assert_called_once_with(
        "/trackers/5/artifacts",
        params={
            "values": "",
            "limit": 100,
            "offset": 0,
            "query": "",
            "expert_query": "",
            "order": "asc",
        },
    )
    assert result == [{"id": 100}]


@pytest.mark.asyncio
async def test_get_tracker_artifacts_with_query():
    mock_client = AsyncMock()
    mock_client.get.return_value = [{"id": 100}]

    result = await get_tracker_artifacts(
        mock_client, tracker_id=5, values="all", query={"title": "bug"}
    )

    mock_client.get.assert_called_once_with(
        "/trackers/5/artifacts",
        params={
            "values": "all",
            "limit": 100,
            "offset": 0,
            "query": '{"title": "bug"}',
            "expert_query": "",
            "order": "asc",
        },
    )
    assert result == [{"id": 100}]


@pytest.mark.asyncio
async def test_get_tracker_parent_artifacts():
    mock_client = AsyncMock()
    mock_client.get.return_value = [{"id": 42}]

    result = await get_tracker_parent_artifacts(mock_client, tracker_id=5)

    mock_client.get.assert_called_once_with(
        "/trackers/5/parent_artifacts", params={"limit": 100, "offset": 0}
    )
    assert result == [{"id": 42}]


@pytest.mark.asyncio
async def test_update_tracker_workflow():
    mock_client = AsyncMock()
    mock_client.patch.return_value = {"id": 5}

    workflow = {"set_transitions_rules": {"field_id": 1234}}
    result = await update_tracker_workflow(mock_client, tracker_id=5, workflow=workflow)

    mock_client.patch.assert_called_once_with(
        "/trackers/5", json={"workflow": workflow}
    )
    assert result == {"id": 5}


@pytest.mark.asyncio
async def test_get_tracker_report():
    mock_client = AsyncMock()
    mock_client.get.return_value = {"id": 9, "label": "Open bugs"}

    result = await get_tracker_report(mock_client, report_id=9)

    mock_client.get.assert_called_once_with(
        "/tracker_reports/9", params={"with_unsaved_changes": False}
    )
    assert result == {"id": 9, "label": "Open bugs"}


@pytest.mark.asyncio
async def test_get_tracker_report_artifacts():
    mock_client = AsyncMock()
    mock_client.get.return_value = [{"id": 100}]

    result = await get_tracker_report_artifacts(mock_client, report_id=9)

    mock_client.get.assert_called_once_with(
        "/tracker_reports/9/artifacts",
        params={
            "with_unsaved_changes": False,
            "values": "",
            "limit": 10,
            "offset": 0,
            "output_format": "nested",
        },
    )
    assert result == [{"id": 100}]
