import json
import pytest
from unittest.mock import AsyncMock
from tuleap_mcp.tools import pull_requests
from tuleap_mcp.client import TuleapClient


@pytest.mark.asyncio
async def test_list_pull_requests_no_filters():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"total_size": 0, "collection": []}

    result = await pull_requests.list_pull_requests(client_mock, repository_id=3)

    client_mock.get.assert_called_once_with(
        "/git/3/pull_requests",
        params={"query": "", "order": "desc", "limit": 50, "offset": 0},
    )
    assert result == {"total_size": 0, "collection": []}


@pytest.mark.asyncio
async def test_list_pull_requests_with_filters():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"total_size": 1, "collection": [{"id": 1}]}

    result = await pull_requests.list_pull_requests(
        client_mock,
        repository_id=3,
        status="open",
        authors=[102],
        labels=[4],
        search=["fix"],
        target_branches=["master"],
        reviewers=[103],
        related_to=None,
        order="asc",
        limit=10,
        offset=5,
    )

    args, kwargs = client_mock.get.call_args
    assert args == ("/git/3/pull_requests",)
    sent_query = json.loads(kwargs["params"]["query"])
    assert sent_query == {
        "status": "open",
        "authors": [{"id": 102}],
        "labels": [{"id": 4}],
        "search": [{"keyword": "fix"}],
        "target_branches": [{"name": "master"}],
        "reviewers": [{"id": 103}],
    }
    assert kwargs["params"]["order"] == "asc"
    assert kwargs["params"]["limit"] == 10
    assert kwargs["params"]["offset"] == 5
    assert result == {"total_size": 1, "collection": [{"id": 1}]}


@pytest.mark.asyncio
async def test_get_pull_request_authors():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = [{"id": 102, "username": "jdoe"}]

    result = await pull_requests.get_pull_request_authors(client_mock, repository_id=3)

    client_mock.get.assert_called_once_with(
        "/git/3/pull_requests_authors", params={"limit": 50, "offset": 0}
    )
    assert result == [{"id": 102, "username": "jdoe"}]


@pytest.mark.asyncio
async def test_get_repository_pull_request_reviewers():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = [{"id": 103, "username": "reviewer"}]

    result = await pull_requests.get_repository_pull_request_reviewers(
        client_mock, repository_id=3
    )

    client_mock.get.assert_called_once_with(
        "/git/3/pull_requests_reviewers", params={"limit": 50, "offset": 0}
    )
    assert result == [{"id": 103, "username": "reviewer"}]


@pytest.mark.asyncio
async def test_get_pull_request():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"id": 42, "title": "My PR"}

    result = await pull_requests.get_pull_request(client_mock, pull_request_id=42)

    client_mock.get.assert_called_once_with("/pull_requests/42")
    assert result == {"id": 42, "title": "My PR"}


@pytest.mark.asyncio
async def test_create_pull_request():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = {"id": 7, "uri": "pull_requests/7"}

    result = await pull_requests.create_pull_request(
        client_mock,
        repository_id=3,
        repository_dest_id=3,
        branch_src="dev",
        branch_dest="master",
    )

    client_mock.post.assert_called_once_with(
        "/pull_requests",
        json={
            "repository_id": 3,
            "repository_dest_id": 3,
            "branch_src": "dev",
            "branch_dest": "master",
        },
    )
    assert result == {"id": 7, "uri": "pull_requests/7"}


@pytest.mark.asyncio
async def test_update_pull_request_status():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.patch.return_value = {"id": 42, "status": "merge"}

    result = await pull_requests.update_pull_request(
        client_mock, pull_request_id=42, status="merge"
    )

    client_mock.patch.assert_called_once_with(
        "/pull_requests/42", json={"status": "merge"}
    )
    assert result == {"id": 42, "status": "merge"}


@pytest.mark.asyncio
async def test_update_pull_request_info():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.patch.return_value = {"id": 42, "title": "New title"}

    result = await pull_requests.update_pull_request(
        client_mock, pull_request_id=42, title="New title", description="New desc"
    )

    client_mock.patch.assert_called_once_with(
        "/pull_requests/42",
        json={"title": "New title", "description": "New desc"},
    )
    assert result == {"id": 42, "title": "New title"}


@pytest.mark.asyncio
async def test_get_pull_request_commits():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = [{"sha1": "abc123"}]

    result = await pull_requests.get_pull_request_commits(
        client_mock, pull_request_id=42
    )

    client_mock.get.assert_called_once_with(
        "/pull_requests/42/commits", params={"limit": 50, "offset": 0}
    )
    assert result == [{"sha1": "abc123"}]


@pytest.mark.asyncio
async def test_get_pull_request_files():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = [{"path": "src/main.py"}]

    result = await pull_requests.get_pull_request_files(client_mock, pull_request_id=42)

    client_mock.get.assert_called_once_with("/pull_requests/42/files")
    assert result == [{"path": "src/main.py"}]


@pytest.mark.asyncio
async def test_get_pull_request_file_diff():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"lines": []}

    result = await pull_requests.get_pull_request_file_diff(
        client_mock, pull_request_id=42, path="src/main.py"
    )

    client_mock.get.assert_called_once_with(
        "/pull_requests/42/file_diff", params={"path": "src/main.py"}
    )
    assert result == {"lines": []}


@pytest.mark.asyncio
async def test_get_pull_request_timeline():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"total_size": 0, "collection": []}

    result = await pull_requests.get_pull_request_timeline(
        client_mock, pull_request_id=42
    )

    client_mock.get.assert_called_once_with(
        "/pull_requests/42/timeline", params={"limit": 10, "offset": 0}
    )
    assert result == {"total_size": 0, "collection": []}


@pytest.mark.asyncio
async def test_get_pull_request_comments():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = [{"id": 1, "content": "hi"}]

    result = await pull_requests.get_pull_request_comments(
        client_mock, pull_request_id=42
    )

    client_mock.get.assert_called_once_with(
        "/pull_requests/42/comments", params={"limit": 10, "offset": 0, "order": "asc"}
    )
    assert result == [{"id": 1, "content": "hi"}]


@pytest.mark.asyncio
async def test_add_pull_request_comment():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = {"id": 9, "content": "LGTM"}

    result = await pull_requests.add_pull_request_comment(
        client_mock, pull_request_id=42, content="LGTM", format="commonmark"
    )

    client_mock.post.assert_called_once_with(
        "/pull_requests/42/comments",
        json={"content": "LGTM", "format": "commonmark"},
    )
    assert result == {"id": 9, "content": "LGTM"}


@pytest.mark.asyncio
async def test_update_pull_request_comment():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.patch.return_value = {"id": 9, "content": "Updated"}

    result = await pull_requests.update_pull_request_comment(
        client_mock, comment_id=9, content="Updated"
    )

    client_mock.patch.assert_called_once_with(
        "/pull_request_comments/9", json={"content": "Updated"}
    )
    assert result == {"id": 9, "content": "Updated"}


@pytest.mark.asyncio
async def test_add_pull_request_inline_comment():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = {"id": 11, "content": "Nit"}

    result = await pull_requests.add_pull_request_inline_comment(
        client_mock,
        pull_request_id=42,
        content="Nit",
        file_path="src/main.py",
        unidiff_offset=12,
        position="right",
    )

    client_mock.post.assert_called_once_with(
        "/pull_requests/42/inline-comments",
        json={
            "content": "Nit",
            "file_path": "src/main.py",
            "unidiff_offset": 12,
            "position": "right",
        },
    )
    assert result == {"id": 11, "content": "Nit"}


@pytest.mark.asyncio
async def test_update_pull_request_inline_comment():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.patch.return_value = {"id": 11, "content": "Updated nit"}

    result = await pull_requests.update_pull_request_inline_comment(
        client_mock, comment_id=11, content="Updated nit"
    )

    client_mock.patch.assert_called_once_with(
        "/pull_request_inline_comments/11", json={"content": "Updated nit"}
    )
    assert result == {"id": 11, "content": "Updated nit"}


@pytest.mark.asyncio
async def test_reply_to_inline_comment():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.post.return_value = {"id": 12, "content": "Fixed"}

    result = await pull_requests.reply_to_inline_comment(
        client_mock, comment_id=11, content="Fixed"
    )

    client_mock.post.assert_called_once_with(
        "/pull_request_inline_comments/11/reply",
        json={"content": "Fixed", "format": "commonmark"},
    )
    assert result == {"id": 12, "content": "Fixed"}


@pytest.mark.asyncio
async def test_get_pull_request_labels():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"labels": []}

    result = await pull_requests.get_pull_request_labels(
        client_mock, pull_request_id=42
    )

    client_mock.get.assert_called_once_with(
        "/pull_requests/42/labels", params={"limit": 50, "offset": 0}
    )
    assert result == {"labels": []}


@pytest.mark.asyncio
async def test_update_pull_request_labels():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.patch.return_value = None

    await pull_requests.update_pull_request_labels(
        client_mock, pull_request_id=42, add=[{"id": 1}], remove=[{"id": 2}]
    )

    client_mock.patch.assert_called_once_with(
        "/pull_requests/42/labels",
        json={"add": [{"id": 1}], "remove": [{"id": 2}]},
    )


@pytest.mark.asyncio
async def test_get_pull_request_reviewers():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.get.return_value = {"users": []}

    result = await pull_requests.get_pull_request_reviewers(
        client_mock, pull_request_id=42
    )

    client_mock.get.assert_called_once_with("/pull_requests/42/reviewers")
    assert result == {"users": []}


@pytest.mark.asyncio
async def test_set_pull_request_reviewers():
    client_mock = AsyncMock(spec=TuleapClient)
    client_mock.put.return_value = None

    await pull_requests.set_pull_request_reviewers(
        client_mock, pull_request_id=42, users=[{"id": 102}]
    )

    client_mock.put.assert_called_once_with(
        "/pull_requests/42/reviewers", json={"users": [{"id": 102}]}
    )
