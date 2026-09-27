import os
import sys
from mcp.server.fastmcp import FastMCP
from .client import TuleapClient
from .tools import users, trackers, agile, files, pull_requests


def get_client() -> TuleapClient:
    tuleap_url = os.getenv("TULEAP_URL")
    tuleap_api_key = os.getenv("TULEAP_API_KEY")

    if not tuleap_url or not tuleap_api_key:
        print(
            "Error: TULEAP_URL and TULEAP_API_KEY environment variables must be set.",
            file=sys.stderr,
        )
        sys.exit(1)

    return TuleapClient(tuleap_url, tuleap_api_key)


mcp = FastMCP("Tuleap MCP Server")


@mcp.tool()
async def search_users(query: str = None) -> str:
    """Search for users in Tuleap."""
    client = get_client()
    return str(await users.get_users(client, query))


@mcp.tool()
async def get_artifact(artifact_id: int) -> str:
    """Get details of a specific artifact. This includes the fields and values like status, start_date, end_date."""
    client = get_client()
    return str(await trackers.get_artifact_details(client, artifact_id))


@mcp.tool()
async def update_artifact(
    artifact_id: int, values: list = None, comment: str = None
) -> str:
    """Update an artifact's fields or add a comment. Values should be a list of dictionaries with field updates. At least one of values or comment is required."""
    client = get_client()
    if not values and not comment:
        return "Error: Must provide either values or comment to update."
    if values is None:
        values = []
    return str(await trackers.update_artifact(client, artifact_id, values, comment))


@mcp.tool()
async def search_artifacts(tracker_id: int, query: str = None) -> str:
    """Search for artifacts in a specific tracker."""
    client = get_client()
    return str(await trackers.search_artifacts(client, tracker_id, query))


@mcp.tool()
async def search_projects(query: str = None) -> str:
    """Search for projects."""
    client = get_client()
    return str(await agile.search_projects(client, query))


@mcp.tool()
async def get_project_epics(project_id: int) -> str:
    """Get epics for a project. To see details like start/end dates, you might need to use get_artifact on the returned IDs."""
    client = get_client()
    return str(await agile.get_epics(client, project_id))


@mcp.tool()
async def get_project_user_stories(project_id: int, epic_id: int = None) -> str:
    """Get user stories for a project, optionally filtered by an Epic ID."""
    client = get_client()
    return str(await agile.get_user_stories(client, project_id, epic_id))


@mcp.tool()
async def create_user_story(project_id: int, values: list) -> str:
    """Create a new user story artifact in a project. Values should be a list of dictionaries defining the story fields."""
    client = get_client()
    return str(await agile.create_user_story(client, project_id, values))


@mcp.tool()
async def get_git_repos(project_id: int) -> str:
    """Get git repositories for a project."""
    client = get_client()
    return str(await files.get_git_repositories(client, project_id))


@mcp.tool()
async def create_epic(project_id: int, values: list) -> str:
    """Create a new epic artifact in a project."""
    client = get_client()
    return str(await agile.create_epic(client, project_id, values))


@mcp.tool()
async def link_to_epic(epic_id: int, child_artifact_id: int) -> str:
    """Link a child artifact (e.g. User Story) to a parent epic."""
    client = get_client()
    return str(await agile.link_to_epic(client, epic_id, child_artifact_id))


@mcp.tool()
async def get_epic_progress(epic_id: int) -> str:
    """Get summarized progress information for an epic (Status, Progress, Effort)."""
    client = get_client()
    return str(await agile.get_epic_progress(client, epic_id))


@mcp.tool()
async def list_pull_requests(
    repository_id: int,
    status: str = None,
    authors: list = None,
    labels: list = None,
    search: list = None,
    target_branches: list = None,
    reviewers: list = None,
    related_to: int = None,
    order: str = "desc",
    limit: int = 50,
    offset: int = 0,
) -> str:
    """List pull requests of a git repository. Filter by status ("open"/"closed"), authors/reviewers
    (lists of user IDs), labels (list of label IDs), search (list of keywords matched against title/description),
    target_branches (list of branch names) or related_to (a single user ID, matches author OR reviewer)."""
    client = get_client()
    return str(
        await pull_requests.list_pull_requests(
            client,
            repository_id,
            status,
            authors,
            labels,
            search,
            target_branches,
            reviewers,
            related_to,
            order,
            limit,
            offset,
        )
    )


@mcp.tool()
async def get_pull_request_authors(
    repository_id: int, limit: int = 50, offset: int = 0
) -> str:
    """List the authors of pull requests in a git repository."""
    client = get_client()
    return str(
        await pull_requests.get_pull_request_authors(
            client, repository_id, limit, offset
        )
    )


@mcp.tool()
async def get_repository_pull_request_reviewers(
    repository_id: int, limit: int = 50, offset: int = 0
) -> str:
    """List the reviewers of pull requests in a git repository."""
    client = get_client()
    return str(
        await pull_requests.get_repository_pull_request_reviewers(
            client, repository_id, limit, offset
        )
    )


@mcp.tool()
async def get_pull_request(pull_request_id: int) -> str:
    """Get details of a specific pull request (title, description, status, branches, author...)."""
    client = get_client()
    return str(await pull_requests.get_pull_request(client, pull_request_id))


@mcp.tool()
async def create_pull_request(
    repository_id: int, repository_dest_id: int, branch_src: str, branch_dest: str
) -> str:
    """Create a new pull request from branch_src (in repository_id) to branch_dest (in repository_dest_id)."""
    client = get_client()
    return str(
        await pull_requests.create_pull_request(
            client, repository_id, repository_dest_id, branch_src, branch_dest
        )
    )


@mcp.tool()
async def update_pull_request(
    pull_request_id: int,
    status: str = None,
    title: str = None,
    description: str = None,
    description_format: str = None,
) -> str:
    """Merge or abandon a pull request (status="merge"/"abandon"), reopen an abandoned one
    (status="review"), or edit its title/description. At least one argument besides
    pull_request_id is required."""
    client = get_client()
    if status is None and title is None and description is None:
        return "Error: Must provide status, or title/description, to update."
    return str(
        await pull_requests.update_pull_request(
            client, pull_request_id, status, title, description, description_format
        )
    )


@mcp.tool()
async def get_pull_request_commits(
    pull_request_id: int, limit: int = 50, offset: int = 0
) -> str:
    """List the commits of a pull request."""
    client = get_client()
    return str(
        await pull_requests.get_pull_request_commits(
            client, pull_request_id, limit, offset
        )
    )


@mcp.tool()
async def get_pull_request_files(pull_request_id: int) -> str:
    """List the files impacted by a pull request."""
    client = get_client()
    return str(await pull_requests.get_pull_request_files(client, pull_request_id))


@mcp.tool()
async def get_pull_request_file_diff(pull_request_id: int, path: str) -> str:
    """Get the unified diff of a single file in a pull request."""
    client = get_client()
    return str(
        await pull_requests.get_pull_request_file_diff(client, pull_request_id, path)
    )


@mcp.tool()
async def get_pull_request_timeline(
    pull_request_id: int, limit: int = 10, offset: int = 0
) -> str:
    """Get the timeline of a pull request: comments, inline comments, status and reviewer changes."""
    client = get_client()
    return str(
        await pull_requests.get_pull_request_timeline(
            client, pull_request_id, limit, offset
        )
    )


@mcp.tool()
async def get_pull_request_comments(
    pull_request_id: int, limit: int = 10, offset: int = 0, order: str = "asc"
) -> str:
    """List the general (non-inline) comments of a pull request."""
    client = get_client()
    return str(
        await pull_requests.get_pull_request_comments(
            client, pull_request_id, limit, offset, order
        )
    )


@mcp.tool()
async def add_pull_request_comment(
    pull_request_id: int,
    content: str,
    format: str = None,
    parent_id: int = None,
) -> str:
    """Post a new general comment on a pull request. format may be "text" or "commonmark"."""
    client = get_client()
    return str(
        await pull_requests.add_pull_request_comment(
            client, pull_request_id, content, format, parent_id
        )
    )


@mcp.tool()
async def update_pull_request_comment(comment_id: int, content: str) -> str:
    """Update the content of an existing general pull request comment."""
    client = get_client()
    return str(
        await pull_requests.update_pull_request_comment(client, comment_id, content)
    )


@mcp.tool()
async def add_pull_request_inline_comment(
    pull_request_id: int,
    content: str,
    file_path: str,
    unidiff_offset: int,
    position: str,
    format: str = None,
    parent_id: int = None,
) -> str:
    """Post a new inline comment on a pull request file at a given diff line. position must be "left" or "right"."""
    client = get_client()
    return str(
        await pull_requests.add_pull_request_inline_comment(
            client,
            pull_request_id,
            content,
            file_path,
            unidiff_offset,
            position,
            format,
            parent_id,
        )
    )


@mcp.tool()
async def update_pull_request_inline_comment(comment_id: int, content: str) -> str:
    """Update the content of an existing inline pull request comment."""
    client = get_client()
    return str(
        await pull_requests.update_pull_request_inline_comment(
            client, comment_id, content
        )
    )


@mcp.tool()
async def reply_to_pull_request_inline_comment(
    comment_id: int, content: str, format: str = "commonmark"
) -> str:
    """Reply to an existing inline comment on a pull request. format must be "text" or "commonmark"."""
    client = get_client()
    return str(
        await pull_requests.reply_to_inline_comment(client, comment_id, content, format)
    )


@mcp.tool()
async def get_pull_request_labels(
    pull_request_id: int, limit: int = 50, offset: int = 0
) -> str:
    """List the labels attached to a pull request."""
    client = get_client()
    return str(
        await pull_requests.get_pull_request_labels(
            client, pull_request_id, limit, offset
        )
    )


@mcp.tool()
async def update_pull_request_labels(
    pull_request_id: int, add: list = None, remove: list = None
) -> str:
    """Add or remove labels on a pull request. add/remove are lists of dicts, e.g. [{"id": 1}]
    to use an existing project label, or [{"label": "Emergency Fix"}] to create/reuse one by name."""
    client = get_client()
    if not add and not remove:
        return "Error: Must provide add and/or remove to update labels."
    return str(
        await pull_requests.update_pull_request_labels(
            client, pull_request_id, add, remove
        )
    )


@mcp.tool()
async def get_pull_request_reviewers(pull_request_id: int) -> str:
    """List the reviewers of a pull request."""
    client = get_client()
    return str(await pull_requests.get_pull_request_reviewers(client, pull_request_id))


@mcp.tool()
async def set_pull_request_reviewers(pull_request_id: int, users: list) -> str:
    """Set (replace) the reviewers of a pull request. users is a list of dicts referencing
    users, e.g. [{"id": 102}] or [{"username": "jdoe"}]."""
    client = get_client()
    return str(
        await pull_requests.set_pull_request_reviewers(client, pull_request_id, users)
    )


def main():
    mcp.run()


if __name__ == "__main__":
    main()
