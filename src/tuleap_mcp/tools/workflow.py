from typing import Any, Dict, List, Optional
from ..client import TuleapClient


async def create_workflow_transition(
    client: TuleapClient, tracker_id: int, from_id: int, to_id: int
) -> Dict[str, Any]:
    """Add a new transition to a tracker's workflow. `from_id`/`to_id` are field value ids
    (use 0 as from_id for a transition from "new artifact")."""
    payload = {"tracker_id": tracker_id, "from_id": from_id, "to_id": to_id}
    return await client.post("/tracker_workflow_transitions", json=payload)


async def delete_workflow_transition(client: TuleapClient, transition_id: int) -> None:
    """Delete a transition from a tracker's workflow."""
    return await client.delete(f"/tracker_workflow_transitions/{transition_id}")


async def get_workflow_transition(
    client: TuleapClient, transition_id: int
) -> Dict[str, Any]:
    """Get the definition of a workflow transition."""
    return await client.get(f"/tracker_workflow_transitions/{transition_id}")


async def update_workflow_transition_conditions(
    client: TuleapClient,
    transition_id: int,
    authorized_user_group_ids: Optional[List[str]] = None,
    not_empty_field_ids: Optional[List[int]] = None,
    is_comment_required: Optional[bool] = None,
) -> Dict[str, Any]:
    """Update the conditions (authorized user groups, required non-empty fields, comment
    requirement) of a workflow transition. `is_comment_required` is ignored for a
    transition from "new artifact"."""
    payload: Dict[str, Any] = {}
    if authorized_user_group_ids is not None:
        payload["authorized_user_group_ids"] = authorized_user_group_ids
    if not_empty_field_ids is not None:
        payload["not_empty_field_ids"] = not_empty_field_ids
    if is_comment_required is not None:
        payload["is_comment_required"] = is_comment_required
    return await client.patch(
        f"/tracker_workflow_transitions/{transition_id}", json=payload
    )


async def get_workflow_transition_actions(
    client: TuleapClient, transition_id: int
) -> List[Dict[str, Any]]:
    """List the post actions (run job, set field value, frozen fields, hidden fieldsets...)
    of a workflow transition."""
    return await client.get(f"/tracker_workflow_transitions/{transition_id}/actions")


async def set_workflow_transition_actions(
    client: TuleapClient, transition_id: int, post_actions: List[Dict[str, Any]]
) -> None:
    """Replace all post actions of a workflow transition. Existing actions matched by "id"
    are updated, actions without "id" are created, and actions not present are removed.
    Each item needs at least a "type" (e.g. "run_job", "set_field_value", "frozen_fields",
    "hidden_fieldsets") plus its type-specific fields (e.g. "job_url", or "field_type" +
    "field_id" + "value" for set_field_value)."""
    return await client.put(
        f"/tracker_workflow_transitions/{transition_id}/actions",
        json={"post_actions": post_actions},
    )
