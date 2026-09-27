import pytest
from unittest.mock import AsyncMock
from tuleap_mcp.tools import platform
from tuleap_mcp.client import TuleapClient


@pytest.mark.asyncio
async def test_get_platform_banner():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {
        "message": "Maintenance tonight",
        "importance": "warning",
    }

    result = await platform.get_platform_banner(client_mock)

    client_mock.get.assert_called_once_with("/banner")
    assert result == {"message": "Maintenance tonight", "importance": "warning"}


@pytest.mark.asyncio
async def test_set_platform_banner():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.put.return_value = None

    await platform.set_platform_banner(
        client_mock, message="Maintenance tonight", importance="critical"
    )

    client_mock.put.assert_called_once_with(
        "/banner", json={"message": "Maintenance tonight", "importance": "critical"}
    )


@pytest.mark.asyncio
async def test_set_platform_banner_with_expiration():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.put.return_value = None

    await platform.set_platform_banner(
        client_mock,
        message="Maintenance tonight",
        importance="warning",
        expiration_date="2100-06-30T09:44:34+01:00",
    )

    client_mock.put.assert_called_once_with(
        "/banner",
        json={
            "message": "Maintenance tonight",
            "importance": "warning",
            "expiration_date": "2100-06-30T09:44:34+01:00",
        },
    )


@pytest.mark.asyncio
async def test_delete_platform_banner():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.delete.return_value = None

    await platform.delete_platform_banner(client_mock)

    client_mock.delete.assert_called_once_with("/banner")


@pytest.mark.asyncio
async def test_get_project_banner():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"message": "Project banner"}

    result = await platform.get_project_banner(client_mock, project_id=1)

    client_mock.get.assert_called_once_with("/projects/1/banner")
    assert result == {"message": "Project banner"}


@pytest.mark.asyncio
async def test_set_project_banner():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.put.return_value = None

    await platform.set_project_banner(client_mock, project_id=1, message="Hello")

    client_mock.put.assert_called_once_with(
        "/projects/1/banner", json={"message": "Hello", "importance": "standard"}
    )


@pytest.mark.asyncio
async def test_delete_project_banner():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.delete.return_value = None

    await platform.delete_project_banner(client_mock, project_id=1)

    client_mock.delete.assert_called_once_with("/projects/1/banner")


@pytest.mark.asyncio
async def test_get_system_events():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = [{"id": 1, "status": "error"}]

    result = await platform.get_system_events(client_mock, status="error")

    client_mock.get.assert_called_once_with(
        "/system_event", params={"limit": 10, "offset": 0, "status": "error"}
    )
    assert result == [{"id": 1, "status": "error"}]


@pytest.mark.asyncio
async def test_get_system_events_no_filter():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = []

    await platform.get_system_events(client_mock)

    client_mock.get.assert_called_once_with(
        "/system_event", params={"limit": 10, "offset": 0}
    )
