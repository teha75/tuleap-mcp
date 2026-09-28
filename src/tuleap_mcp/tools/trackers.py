import json
from typing import List, Dict, Any, Optional
from ..client import TuleapClient


async def get_tracker(client: TuleapClient, tracker_id: int) -> Dict[str, Any]:
    """Get the definition of a tracker (fields, semantics, workflow, structure)."""
    return await client.get(f"/trackers/{tracker_id}")


async def get_tracker_reports(
    client: TuleapClient, tracker_id: int, limit: int = 10, offset: int = 0
) -> List[Dict[str, Any]]:
    """List the reports (saved searches) defined on a tracker."""
    params = {"limit": limit, "offset": offset}
    return await client.get(f"/trackers/{tracker_id}/tracker_reports", params=params)


async def get_tracker_artifacts(
    client: TuleapClient,
    tracker_id: int,
    values: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    query: Optional[Dict[str, Any]] = None,
    expert_query: Optional[str] = None,
    order: str = "asc",
) -> List[Dict[str, Any]]:
    """List all artifacts of a tracker. `values="all"` includes field values (otherwise
    just id/title/status). `query` is a dict of field_id/field_shortname -> value (or
    {"operator":..., "value":...}) criteria. `expert_query` is a TQL expression (AND, OR,
    WITH/WITHOUT PARENT, BETWEEN(), IN(), MYSELF()...). `query` and `expert_query` are
    mutually exclusive; `order` only applies when neither is given."""
    params = {
        "values": values or "",
        "limit": limit,
        "offset": offset,
        "query": json.dumps(query) if query else "",
        "expert_query": expert_query or "",
        "order": order,
    }
    return await client.get(f"/trackers/{tracker_id}/artifacts", params=params)


async def get_tracker_parent_artifacts(
    client: TuleapClient, tracker_id: int, limit: int = 100, offset: int = 0
) -> List[Dict[str, Any]]:
    """List the open artifacts of a tracker's parent tracker (possible parents for a new artifact)."""
    params = {"limit": limit, "offset": offset}
    return await client.get(f"/trackers/{tracker_id}/parent_artifacts", params=params)


async def update_tracker_workflow(
    client: TuleapClient, tracker_id: int, workflow: Dict[str, Any]
) -> Dict[str, Any]:
    """Partially update a tracker's workflow configuration. `workflow` is passed as-is, e.g.
    {"set_transitions_rules": {"field_id": 1234}}, {"set_transitions_rules": {"is_used": true}},
    {"delete_transitions_rules": true}, {"is_legacy": false} or {"is_advanced": true}."""
    return await client.patch(f"/trackers/{tracker_id}", json={"workflow": workflow})


async def get_tracker_report(
    client: TuleapClient, report_id: int, with_unsaved_changes: bool = False
) -> Dict[str, Any]:
    """Get the definition of a tracker report."""
    params = {"with_unsaved_changes": with_unsaved_changes}
    return await client.get(f"/tracker_reports/{report_id}", params=params)


async def get_tracker_report_artifacts(
    client: TuleapClient,
    report_id: int,
    with_unsaved_changes: bool = False,
    values: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    output_format: str = "nested",
) -> List[Dict[str, Any]]:
    """Get the artifacts matching a tracker report's criteria. `values` may be "all" to
    include field values. `output_format` may be "nested" (default), "flat" or
    "flat_with_semicolon_string_array"."""
    params = {
        "with_unsaved_changes": with_unsaved_changes,
        "values": values or "",
        "limit": limit,
        "offset": offset,
        "output_format": output_format,
    }
    return await client.get(f"/tracker_reports/{report_id}/artifacts", params=params)


async def get_artifact_details(
    client: TuleapClient, artifact_id: int
) -> Dict[str, Any]:
    """Get details of a specific artifact."""
    return await client.get(f"/artifacts/{artifact_id}")


async def search_artifacts(
    client: TuleapClient, tracker_id: int, query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search for artifacts in a tracker."""
    params = {"tracker_id": tracker_id}
    if query:
        params["query"] = query
    return await client.get("/artifacts", params=params)


async def update_artifact(
    client: TuleapClient,
    artifact_id: int,
    values: List[Dict[str, Any]],
    comment: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an artifact's fields or add a comment."""
    payload = {"values": values}
    if comment:
        payload["comment"] = {"body": comment, "format": "text"}
    return await client.put(f"/artifacts/{artifact_id}", json=payload)
