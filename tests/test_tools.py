import unittest

from app.tools import (
    execute_tool,
    prepare_incident_draft
)


class ToolTests(unittest.TestCase):

    def test_asset_lookup(self):

        result = execute_tool(
            "get_asset",
            {"asset_tag": "AST-1001"}
        )

        self.assertTrue(result["ok"])

    def test_unknown_asset(self):

        result = execute_tool(
            "get_asset",
            {"asset_tag": "AST-9999"}
        )

        self.assertFalse(result["ok"])

    def test_ticket_lookup(self):

        result = execute_tool(
            "get_ticket",
            {"ticket_id": "INC-2041"}
        )

        self.assertTrue(result["ok"])

    def test_team_list(self):

        result = execute_tool(
            "list_support_teams",
            {}
        )

        self.assertTrue(result["ok"])

    def test_unapproved_tool(self):

        result = execute_tool(
            "delete_database",
            {}
        )

        self.assertFalse(result["ok"])

    def test_incident_draft(self):

        result = prepare_incident_draft(
            "AST-1002",
            "Screen flickers",
            "High"
        )

        self.assertTrue(result["ok"])

    def test_invalid_incident(self):

        result = prepare_incident_draft(
            "AST-9999",
            "",
            "High"
        )

        self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()