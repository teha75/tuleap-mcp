import os
import sys
from mcp.server.fastmcp import FastMCP
from .client import TuleapClient
from .tools import users, trackers, agile, files, pull_requests, workflow


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
async def get_tracker(tracker_id: int) -> str:
    """Get the definition of a tracker (fields, semantics, workflow, structure)."""
    client = get_client()
    return str(await trackers.get_tracker(client, tracker_id))


@mcp.tool()
async def get_tracker_reports(tracker_id: int, limit: int = 10, offset: int = 0) -> str:
    """List the reports (saved searches) defined on a tracker."""
    client = get_client()
    return str(await trackers.get_tracker_reports(client, tracker_id, limit, offset))


@mcp.tool()
async def get_tracker_artifacts(
    tracker_id: int,
    values: str = None,
    limit: int = 100,
    offset: int = 0,
    query: dict = None,
    expert_query: str = None,
    order: str = "asc",
) -> str:
    """List all artifacts of a tracker. values="all" includes field values. query is a dict
    of field_id/field_shortname -> value (or {"operator":..., "value":...}) criteria.
    expert_query is a TQL expression (AND, OR, WITH/WITHOUT PARENT, BETWEEN(), IN(),
    MYSELF()...). query and expert_query are mutually exclusive."""
    client = get_client()
    return str(
        await trackers.get_tracker_artifacts(
            client, tracker_id, values, limit, offset, query, expert_query, order
        )
    )


@mcp.tool()
async def get_tracker_parent_artifacts(
    tracker_id: int, limit: int = 100, offset: int = 0
) -> str:
    """List the open artifacts of a tracker's parent tracker (possible parents for a new artifact)."""
    client = get_client()
    return str(
        await trackers.get_tracker_parent_artifacts(client, tracker_id, limit, offset)
    )


@mcp.tool()
async def update_tracker_workflow(tracker_id: int, workflow: dict) -> str:
    """Partially update a tracker's workflow configuration. workflow is passed as-is, e.g.
    {"set_transitions_rules": {"field_id": 1234}}, {"set_transitions_rules": {"is_used": true}},
    {"delete_transitions_rules": true}, {"is_legacy": false} or {"is_advanced": true}."""
    client = get_client()
    return str(await trackers.update_tracker_workflow(client, tracker_id, workflow))


@mcp.tool()
async def get_tracker_report(report_id: int, with_unsaved_changes: bool = False) -> str:
    """Get the definition of a tracker report."""
    client = get_client()
    return str(
        await trackers.get_tracker_report(client, report_id, with_unsaved_changes)
    )


@mcp.tool()
async def get_tracker_report_artifacts(
    report_id: int,
    with_unsaved_changes: bool = False,
    values: str = None,
    limit: int = 10,
    offset: int = 0,
    output_format: str = "nested",
) -> str:
    """Get the artifacts matching a tracker report's criteria. values may be "all" to
    include field values. output_format may be "nested" (default), "flat" or
    "flat_with_semicolon_string_array"."""
    client = get_client()
    return str(
        await trackers.get_tracker_report_artifacts(
            client,
            report_id,
            with_unsaved_changes,
            values,
            limit,
            offset,
            output_format,
        )
    )


@mcp.tool()
async def create_workflow_transition(tracker_id: int, from_id: int, to_id: int) -> str:
    """Add a new transition to a tracker's workflow. from_id/to_id are field value ids
    (use 0 as from_id for a transition from "new artifact")."""
    client = get_client()
    return str(
        await workflow.create_workflow_transition(client, tracker_id, from_id, to_id)
    )


@mcp.tool()
async def delete_workflow_transition(transition_id: int) -> str:
    """Delete a transition from a tracker's workflow."""
    client = get_client()
    return str(await workflow.delete_workflow_transition(client, transition_id))


@mcp.tool()
async def get_workflow_transition(transition_id: int) -> str:
    """Get the definition of a workflow transition."""
    client = get_client()
    return str(await workflow.get_workflow_transition(client, transition_id))


@mcp.tool()
async def update_workflow_transition_conditions(
    transition_id: int,
    authorized_user_group_ids: list = None,
    not_empty_field_ids: list = None,
    is_comment_required: bool = None,
) -> str:
    """Update the conditions (authorized user groups, required non-empty fields, comment
    requirement) of a workflow transition. is_comment_required is ignored for a transition
    from "new artifact"."""
    client = get_client()
    return str(
        await workflow.update_workflow_transition_conditions(
            client,
            transition_id,
            authorized_user_group_ids,
            not_empty_field_ids,
            is_comment_required,
        )
    )


@mcp.tool()
async def get_workflow_transition_actions(transition_id: int) -> str:
    """List the post actions (run job, set field value, frozen fields, hidden fieldsets...)
    of a workflow transition."""
    client = get_client()
    return str(await workflow.get_workflow_transition_actions(client, transition_id))


@mcp.tool()
async def set_workflow_transition_actions(
    transition_id: int, post_actions: list
) -> str:
    """Replace all post actions of a workflow transition. Existing actions matched by "id"
    are updated, actions without "id" are created, and actions not present are removed.
    Each item needs at least a "type" (e.g. "run_job", "set_field_value", "frozen_fields",
    "hidden_fieldsets") plus its type-specific fields (e.g. "job_url", or "field_type" +
    "field_id" + "value" for set_field_value)."""
    client = get_client()
    return str(
        await workflow.set_workflow_transition_actions(
            client, transition_id, post_actions
        )
    )


@mcp.tool()
async def get_artifact_file_chunk(
    file_id: int, offset: int = 0, limit: int = 1048576
) -> str:
    """Get a (base64-encoded) chunk of a file already attached to an artifact."""
    client = get_client()
    return str(await files.get_artifact_file_chunk(client, file_id, offset, limit))


@mcp.tool()
async def list_temporary_files(limit: int = 10, offset: int = 0) -> str:
    """List the current user's temporary files (uploaded but not yet attached to an artifact)."""
    client = get_client()
    return str(await files.list_temporary_files(client, limit, offset))


@mcp.tool()
async def get_temporary_file_chunk(
    file_id: int, offset: int = 0, limit: int = 1048576
) -> str:
    """Get a (base64-encoded) chunk of one of the current user's temporary files."""
    client = get_client()
    return str(await files.get_temporary_file_chunk(client, file_id, offset, limit))


@mcp.tool()
async def create_temporary_file(
    name: str, mimetype: str, content_base64: str, description: str = None
) -> str:
    """Create a temporary file from its first (base64-encoded) chunk, max 1MB. Use
    append_temporary_file_chunk for larger files. Attach the resulting file id to an
    artifact via update_artifact's values on a File field."""
    client = get_client()
    return str(
        await files.create_temporary_file(
            client, name, mimetype, content_base64, description
        )
    )


@mcp.tool()
async def append_temporary_file_chunk(
    file_id: int, content_base64: str, offset: int
) -> str:
    """Append a (base64-encoded) chunk to an existing temporary file. offset is the 1-based
    index of this chunk (the first chunk from create_temporary_file is offset 1, so the
    next one is 2, etc.)."""
    client = get_client()
    return str(
        await files.append_temporary_file_chunk(client, file_id, content_base64, offset)
    )


@mcp.tool()
async def delete_temporary_file(file_id: int) -> str:
    """Delete one of the current user's temporary files."""
    client = get_client()
    return str(await files.delete_temporary_file(client, file_id))


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
