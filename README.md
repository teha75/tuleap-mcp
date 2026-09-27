# Tuleap MCP Server

[![CI](https://github.com/shamil2/tuleap-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/shamil2/tuleap-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A secure, fully-tested **Model Context Protocol (MCP)** server for interacting with [Tuleap](https://tuleap.net/). This allows your favorite AI assistants (Claude, OpenCode, Cursor, Gemini, etc.) to safely read and manage your Agile projects, track artifacts, list Git repositories, and query users directly from your IDE or chat interface.

---

## 🌟 Features

Exposes the following Tuleap domains to your AI assistant:
- **Agile & Projects**: Search projects, retrieve Epics, list User Stories, and create new Epics or User Stories. Get summarized Epic progress.
- **Trackers & Artifacts**: Search for specific artifacts, get rich details (status, assigned to, dates, custom fields), update artifact fields, and link artifacts together. Get tracker definitions, run/read tracker reports, and query artifacts with structured or TQL (expert) queries.
- **Workflow**: Manage a tracker's workflow transitions (create/delete/read), their access conditions, and their post actions (run job, set field value, freeze fields, hide fieldsets).
- **Files & Repositories**: List Git repositories linked to a project. Upload files (as temporary files, in chunks) and read back attachments to attach to artifacts.
- **Pull Requests**: List and filter pull requests, read details/commits/files/diffs, create pull requests, merge/abandon/reopen them, manage reviewers and labels, and read/post/edit comments (both general and inline).
- **Users**: Search for Tuleap users by name or email.

## 🔐 Security & Best Practices

- **Zero Hardcoded Secrets**: Tokens are passed strictly via your local environment variables.
- **No Personal Data Logging**: The server acts purely as a conduit and does not cache or log your Tuleap data.
- **Automated Security Scans**: CI pipelines run `bandit` to ensure no common vulnerabilities are introduced.
- **Test-Driven**: Comprehensive tests with `pytest` and `respx` ensure data is mocked accurately without hitting live environments.

## 📦 Prerequisites & Installation

1. **Prerequisites**:
   - Python 3.10 or higher.
   - A Tuleap instance URL.
   - A Tuleap Personal Access Token (API Key) generated via the Tuleap user settings.

2. **Clone & Setup**:
   ```bash
   git clone https://github.com/shamil2/tuleap-mcp.git
   cd tuleap_mcp
   
   # Create a virtual environment
   python3 -m venv .venv
   source .venv/bin/activate
   
   # Install the package
   pip install -e .
   ```

3. **Verify Executable Path**:
   Once installed, the MCP binary will be located at:
   `/absolute/path/to/tuleap_mcp/.venv/bin/tuleap-mcp`

---

## 🚀 Configuration & Usage

Configure your AI assistant by pointing it to the virtual environment's executable.

### Using with Claude Desktop

Add this to your `claude_desktop_config.json` file (typically `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "tuleap": {
      "command": "/absolute/path/to/tuleap_mcp/.venv/bin/tuleap-mcp",
      "env": {
        "TULEAP_URL": "https://your-tuleap-instance.com",
        "TULEAP_API_KEY": "your-tuleap-api-key"
      }
    }
  }
}
```

### Using with OpenCode

Add the server under the `mcp` block in your `~/.config/opencode/opencode.json`. Note that OpenCode uses `environment` instead of `env`, requires `type: local`, and uses a list for the `command`:

```json
{
  "mcp": {
    "tuleap": {
      "type": "local",
      "command": [
        "/absolute/path/to/tuleap_mcp/.venv/bin/tuleap-mcp"
      ],
      "environment": {
        "TULEAP_URL": "https://your-tuleap-instance.com",
        "TULEAP_API_KEY": "your-tuleap-api-key"
      },
      "enabled": true
    }
  }
}
```

### Using with OpenAI / ChatGPT
Currently, ChatGPT does not support running local MCP servers natively. However, you can use frameworks like [LangChain](https://github.com/hwchase17/langchain) or [LlamaIndex](https://github.com/jerryjliu/llama_index) to bridge this server to an OpenAI model in a custom Python script.

### Using with Gemini / Cursor / Zed
Most modern AI IDEs that support the official MCP spec configure servers similarly to Claude Desktop. Point their MCP settings menu to the full path of `.venv/bin/tuleap-mcp` and inject the `TULEAP_URL` and `TULEAP_API_KEY` environment variables.

---

## 🛠️ Available MCP Tools

Once connected, your AI assistant can use the following tools natively:
- `search_projects(query)`: Find Tuleap projects.
- `get_project_epics(project_id)`: Retrieve epics for a project via the Epic tracker.
- `get_project_user_stories(project_id, epic_id)`: Retrieve user stories for a project, optionally filtering by parent Epic.
- `create_epic(project_id, values)`: Create a new Epic artifact.
- `create_user_story(project_id, values)`: Create a new User Story artifact.
- `link_to_epic(epic_id, child_artifact_id)`: Link an artifact to a parent Epic.
- `get_epic_progress(epic_id)`: Get summarized progress information for an Epic (Status, Progress, Effort).
- `search_artifacts(tracker_id, query)`: Search for generic artifacts using TQL queries or keywords.
- `get_artifact(artifact_id)`: Get deep metadata and fields for a specific artifact.
- `update_artifact(artifact_id, values, comment)`: Update an artifact's fields or add a comment.
- `get_tracker(tracker_id)`: Get the definition of a tracker (fields, semantics, workflow, structure).
- `get_tracker_reports(tracker_id, limit, offset)`: List the reports (saved searches) defined on a tracker.
- `get_tracker_artifacts(tracker_id, values, limit, offset, query, expert_query, order)`: List all artifacts of a tracker, with structured or TQL (expert) filtering.
- `get_tracker_parent_artifacts(tracker_id, limit, offset)`: List possible parent artifacts for a new artifact in a tracker.
- `update_tracker_workflow(tracker_id, workflow)`: Configure a tracker's workflow (transitions field, simple/advanced mode, legacy mode).
- `get_tracker_report(report_id, with_unsaved_changes)`: Get the definition of a tracker report.
- `get_tracker_report_artifacts(report_id, with_unsaved_changes, values, limit, offset, output_format)`: Get the artifacts matching a report's criteria.
- `create_workflow_transition(tracker_id, from_id, to_id)`: Add a new transition to a tracker's workflow.
- `delete_workflow_transition(transition_id)`: Delete a workflow transition.
- `get_workflow_transition(transition_id)`: Get the definition of a workflow transition.
- `update_workflow_transition_conditions(transition_id, authorized_user_group_ids, not_empty_field_ids, is_comment_required)`: Update a transition's access conditions.
- `get_workflow_transition_actions(transition_id)`: List a transition's post actions.
- `set_workflow_transition_actions(transition_id, post_actions)`: Replace a transition's post actions.
- `search_users(query)`: Search for Tuleap users.
- `get_git_repos(project_id)`: Fetch a list of git repositories linked to a project.
- `get_artifact_file_chunk(file_id, offset, limit)`: Read a chunk of a file already attached to an artifact.
- `list_temporary_files(limit, offset)`: List the current user's uploaded-but-not-yet-attached temporary files.
- `get_temporary_file_chunk(file_id, offset, limit)`: Read a chunk of a temporary file.
- `create_temporary_file(name, mimetype, content_base64, description)`: Upload the first chunk (max 1MB) of a new file, to later attach it to an artifact.
- `append_temporary_file_chunk(file_id, content_base64, offset)`: Upload a further chunk of a large temporary file.
- `delete_temporary_file(file_id)`: Delete a temporary file.
- `list_pull_requests(repository_id, status, authors, labels, search, target_branches, reviewers, related_to, order, limit, offset)`: List/filter pull requests of a git repository.
- `get_pull_request_authors(repository_id, limit, offset)`: List the authors of pull requests in a repository.
- `get_repository_pull_request_reviewers(repository_id, limit, offset)`: List the reviewers of pull requests in a repository.
- `get_pull_request(pull_request_id)`: Get details of a specific pull request.
- `create_pull_request(repository_id, repository_dest_id, branch_src, branch_dest)`: Create a new pull request.
- `update_pull_request(pull_request_id, status, title, description, description_format)`: Merge/abandon/reopen a pull request, or edit its title/description.
- `get_pull_request_commits(pull_request_id, limit, offset)`: List the commits of a pull request.
- `get_pull_request_files(pull_request_id)`: List the files impacted by a pull request.
- `get_pull_request_file_diff(pull_request_id, path)`: Get the unified diff of a single file in a pull request.
- `get_pull_request_timeline(pull_request_id, limit, offset)`: Get the timeline of a pull request.
- `get_pull_request_comments(pull_request_id, limit, offset, order)`: List the general comments of a pull request.
- `add_pull_request_comment(pull_request_id, content, format, parent_id)`: Post a new general comment.
- `update_pull_request_comment(comment_id, content)`: Update an existing general comment.
- `add_pull_request_inline_comment(pull_request_id, content, file_path, unidiff_offset, position, format, parent_id)`: Post a new inline (diff) comment.
- `update_pull_request_inline_comment(comment_id, content)`: Update an existing inline comment.
- `reply_to_pull_request_inline_comment(comment_id, content, format)`: Reply to an inline comment.
- `get_pull_request_labels(pull_request_id, limit, offset)`: List the labels of a pull request.
- `update_pull_request_labels(pull_request_id, add, remove)`: Add/remove labels on a pull request.
- `get_pull_request_reviewers(pull_request_id)`: List the reviewers of a pull request.
- `set_pull_request_reviewers(pull_request_id, users)`: Set (replace) the reviewers of a pull request.

---

## 👨‍💻 Development & Contributing

We welcome contributions! To set up the development environment, run tests, and format code:

```bash
# Activate your venv
source .venv/bin/activate

# Install dev dependencies (pytest, ruff, bandit, etc.)
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=src/tuleap_mcp tests/

# Run linter and formatter
ruff check .
ruff format .

# Run security checks
bandit -r src/
```

### CI/CD Pipeline
Every Pull Request runs a GitHub Actions workflow (`.github/workflows/ci.yml`) ensuring:
1. All unit tests pass.
2. Code follows the Ruff formatting rules.
3. Bandit flags no common security issues.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
