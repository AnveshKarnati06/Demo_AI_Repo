"""
IT Service and Asset Operations tools.

Contains:
- Asset lookup
- Ticket lookup
- Support team listing
- Incident draft creation
- Tool execution allowlist
"""

from datetime import datetime

# Fictional Asset Register
ASSETS = {
    "AST-1001": {"device": "Dell Latitude 5440","assigned_employee": "Nisha Rao","department": "Finance","status": "In service",},
    "AST-1002": {"device": "HP EliteBook 840","assigned_employee": "Arjun Mehta","department": "Engineering","status": "In service",},
    "AST-1003": {"device": "Lenovo ThinkPad T14","assigned_employee": "Maya Sen","department": "Operations","status": "Under repair",},
    "AST-1004": {"device": "Dell Precision 3581","assigned_employee": "Kabir Das","department": "Engineering","status": "In service",},
}

# Fictional Service Tickets
TICKETS = {
    "INC-2041": {"category": "Laptop display","priority": "High","status": "In progress","assigned_team": "Endpoint Support",},
    "INC-2042": {"category": "VPN access","priority": "Medium","status": "Waiting for user","assigned_team": "Network Support",},
    "INC-2043": {"category": "Printer issue","priority": "Low","status": "Resolved","assigned_team": "Workplace Technology",},
    "INC-2044": {"category": "Email access","priority": "High","status": "Open","assigned_team": "Identity Support",},
}

# Support Teams
SUPPORT_TEAMS = {
    "Endpoint Support": "Laptops, desktops, monitors and peripherals.",
    "Network Support": "VPN, Wi-Fi, connectivity and network access.",
    "Identity Support": "Password resets, authentication and account access.",
    "Workplace Technology": "Printers, meeting rooms and collaboration devices.",
}

# Incident Draft Storage
INCIDENT_DRAFTS = []
# Tool Definitions
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_asset",
            "description": (
                "Retrieve a fictional IT asset record "
                "using an asset tag."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "asset_tag": {"type": "string"}
                },
                "required": ["asset_tag"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ticket",
            "description": (
                "Retrieve a fictional service ticket."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "string"}
                },
                "required": ["ticket_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_support_teams",
            "description": (
                "List support teams and responsibilities."
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


# Lookup Tool Dispatcher
def execute_tool(name, arguments):
    # Executes approved tools only.
    if not isinstance(arguments, dict):
        return {
            "ok": False,
            "error": "Arguments must be a JSON object."
        }

    # Asset Lookup
    if name == "get_asset":
        asset_tag = (str(arguments.get("asset_tag", "")).strip().upper() )
        if not asset_tag:
            return {"ok": False,"error": "Asset tag is required."}
        asset = ASSETS.get(asset_tag)
        if not asset:
            return {"ok": False,"error": f"Asset {asset_tag} was not found."}
        return {"ok": True,"asset_tag": asset_tag,**asset}
    # Ticket Lookup
    if name == "get_ticket":
        ticket_id = (str(arguments.get("ticket_id", "")).strip().upper())
        if not ticket_id:
            return {"ok": False,"error": "Ticket ID is required."}
        ticket = TICKETS.get(ticket_id)
        if not ticket:
            return {"ok": False,"error": f"Ticket {ticket_id} was not found."}
        return {"ok": True,"ticket_id": ticket_id,**ticket}
    # Support Teams
    if name == "list_support_teams":
        teams = []
        for team_name, responsibility in SUPPORT_TEAMS.items():
            teams.append({"team": team_name,"responsibility": responsibility})
        return {"ok": True,"count": len(teams),"teams": teams}

    # Any Unknown Tool
    return {"ok": False,"error": f"Tool '{name}' is not approved."}

# Incident Draft Creation
def prepare_incident_draft(asset_tag, issue_description, priority):
    # Creates a draft only. Never submits an incident.
    asset_tag = str(asset_tag).strip().upper()
    if asset_tag not in ASSETS:
        return {"ok": False,"error": "Unknown asset tag."}
    issue_description = str(issue_description).strip()
    if not issue_description:
        return {"ok": False,"error": "Issue description is required."}
    if len(issue_description) > 250:
        return {"ok": False,"error": ("Issue description cannot exceed 250 characters.")}
    priority = str(priority).strip().title()
    if priority not in {"High", "Medium", "Low"}:
        return {"ok": False,"error": ("Priority must be High, Medium or Low.")}
    draft = {
        "draft_id":
            f"IR-{len(INCIDENT_DRAFTS)+1:03d}",
        "asset_tag": asset_tag,
        "priority": priority,
        "issue_description": issue_description,
        "created_at":
            datetime.now().isoformat(),
        "status":
            "AWAITING HUMAN REVIEW"
    }

    INCIDENT_DRAFTS.append(draft)
    return {"ok": True,**draft}