import pytest
from unittest.mock import AsyncMock
from tuleap_mcp.tools import workflow
from tuleap_mcp.client import TuleapClient


@pytest.mark.asyncio
async def test_create_workflow_transition():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = {"id": 1, "from_id": 0, "to_id": 2}

    result = await workflow.create_workflow_transition(
        client_mock, tracker_id=5, from_id=0, to_id=2
    )

    client_mock.post.assert_called_once_with(
        "/tracker_workflow_transitions",
        json={"tracker_id": 5, "from_id": 0, "to_id": 2},
    )
    assert result == {"id": 1, "from_id": 0, "to_id": 2}


@pytest.mark.asyncio
async def test_delete_workflow_transition():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.delete.return_value = None

    await workflow.delete_workflow_transition(client_mock, transition_id=1)

    client_mock.delete.assert_called_once_with("/tracker_workflow_transitions/1")


@pytest.mark.asyncio
async def test_get_workflow_transition():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"id": 1}

    result = await workflow.get_workflow_transition(client_mock, transition_id=1)

    client_mock.get.assert_called_once_with("/tracker_workflow_transitions/1")
    assert result == {"id": 1}


@pytest.mark.asyncio
async def test_update_workflow_transition_conditions():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.patch.return_value = {"id": 1}

    result = await workflow.update_workflow_transition_conditions(
        client_mock,
        transition_id=1,
        authorized_user_group_ids=["3"],
        not_empty_field_ids=[10],
        is_comment_required=True,
    )

    client_mock.patch.assert_called_once_with(
        "/tracker_workflow_transitions/1",
        json={
            "authorized_user_group_ids": ["3"],
            "not_empty_field_ids": [10],
            "is_comment_required": True,
        },
    )
    assert result == {"id": 1}


@pytest.mark.asyncio
async def test_get_workflow_transition_actions():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = [{"id": 1, "type": "run_job"}]

    result = await workflow.get_workflow_transition_actions(
        client_mock, transition_id=1
    )

    client_mock.get.assert_called_once_with("/tracker_workflow_transitions/1/actions")
    assert result == [{"id": 1, "type": "run_job"}]


@pytest.mark.asyncio
async def test_set_workflow_transition_actions():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.put.return_value = None

    post_actions = [{"id": None, "type": "run_job", "job_url": "http://example.com"}]
    await workflow.set_workflow_transition_actions(
        client_mock, transition_id=1, post_actions=post_actions
    )

    client_mock.put.assert_called_once_with(
        "/tracker_workflow_transitions/1/actions",
        json={"post_actions": post_actions},
    )
