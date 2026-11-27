from app.tools import *

print(execute_tool(
    "get_asset",
    {"asset_tag": "AST-1002"}
))

print()

print(execute_tool(
    "get_ticket",
    {"ticket_id": "INC-2041"}
))

print()

print(execute_tool(
    "list_support_teams",
    {}
))

print()

print(
    prepare_incident_draft(
        "AST-1002",
        "Screen flickers",
        "High"
    )
)