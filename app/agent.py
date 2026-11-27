"""
Agent Controller

Handles:
- System Prompt
- Tool Definitions
- Tool Routing
- IT Guide Search
- Incident Draft Creation
- Agent Loop
"""

import json

from .config import MAX_AGENT_STEPS
from .knowledge import retrieve_guide
from .ollama_client import chat
from .tools import (TOOL_DEFINITIONS, execute_tool, prepare_incident_draft)

# System Prompt
SYSTEM_PROMPT = """
You are a helpful IT Service and Asset Operations Assistant.
Rules:
1. Use tools whenever asset, ticket or team information is required.
2. Use the IT guide search tool when policy evidence is needed.
3. Include the source section title when answering policy questions.
4. If the supplied guide does not contain an answer,
   clearly state that the guide does not contain the information.
5. Never invent assets, tickets, policies or tool results.
6. Incident reports can only be prepared as drafts.
7. Never claim a real incident was submitted.
8. Keep answers concise and professional.
You may use tools before answering.
"""

# RAG Search Tool
def search_it_guide(question):
    results = retrieve_guide(question)
    if not results:
        return {
            "ok": False,
            "no_answer": True,
            "message":
            (
                "No supporting evidence found "
                "in the IT Operations Guide."
            )
        }
    return {
        "ok": True,
        "matches": [
            {
                "section": item["title"],
                "text": item["text"],
                "similarity": item["score"]
            }
            for item in results
        ]
    }

# Additional Tool Definitions
def all_tool_definitions():
    guide_tool = {
        "type": "function",
        "function": {
            "name": "search_it_guide",
            "description":
                "Search the IT Operations Guide.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string"
                    }
                },
                "required": ["question"]
            }
        }
    }

    incident_tool = {
        "type": "function",
        "function": {
            "name": "prepare_incident_draft",
            "description":
                "Prepare an incident report draft. "
                "Never submits a real ticket.",
            "parameters": {
                "type": "object",
                "properties": {
                    "asset_tag": {
                        "type": "string"
                    },
                    "issue_description": {
                        "type": "string"
                    },
                    "priority": {
                        "type": "string"
                    }
                },
                "required": [
                    "asset_tag",
                    "issue_description",
                    "priority"
                ]
            }
        }
    }

    return TOOL_DEFINITIONS + [
        guide_tool,
        incident_tool
    ]


# Tool Router
def run_tool(name, args):
    if name == "search_it_guide":
        question = str(
            args.get("question", "")
        ).strip()
        if not question:
            return {
                "ok": False,
                "error": "Question is required."
            }
        return search_it_guide(question)
    if name == "prepare_incident_draft":
        return prepare_incident_draft(
            args.get("asset_tag", ""),
            args.get("issue_description", ""),
            args.get("priority", "")
        )

    return execute_tool(name, args)

# Agent Loop
def run_agent(user_message, history=None):
    # Bounded plan-act-observe loop.
    history = history or []
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Use only recent history
    messages.extend(
        history[-8:]
    )

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    trace = []

    # Agent Loop
    for step in range(MAX_AGENT_STEPS):
        assistant_message = chat(
            messages,
            tools=all_tool_definitions()
        )
        tool_calls = assistant_message.get(
            "tool_calls",
            []
        )
        # Final Answer
        if not tool_calls:
            return {
                "answer":
                    assistant_message.get(
                        "content",
                        "No answer returned."
                    ),
                "trace": trace,
                "steps": step + 1
            }
        messages.append(
            assistant_message
        )

        # Execute Tool Calls
        for call in tool_calls:
            function = call.get(
                "function",
                {}
            )
            tool_name = function.get(
                "name",
                ""
            )

            arguments = function.get(
                "arguments",
                {}
            )

            if not isinstance(arguments, dict):
                arguments = {}

            result = run_tool(
                tool_name,
                arguments
            )

            # Deterministic No-Answer Handling
            # --------------------------------------------------

            if (
                tool_name == "search_it_guide"
                and result.get("no_answer")
            ):
                return {
                    "answer":
                    (
                        "The supplied IT Operations Guide "
                        "does not contain information about "
                        "that topic."
                    ),
                    "trace": [
                        {
                            "tool": "search_it_guide",
                            "result":
                            "No supporting evidence found."
                        }
                    ],
                    "steps": step + 1
                }

            trace.append(
                {
                    "step": step + 1,
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": result
                }
            )

            messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(
                        result,
                        ensure_ascii=False
                    )
                }
            )

    # ----------------------------------------------------------
    # Step Limit Reached
    # ----------------------------------------------------------

    messages.append(
        {
            "role": "system",
            "content":
                "Tool limit reached. "
                "Summarize available information only."
        }
    )

    final = chat(messages)

    return {
        "answer":
            final.get(
                "content",
                "Maximum steps reached."
            ),
        "trace": trace,
        "steps": MAX_AGENT_STEPS,
        "notice":
            "Maximum agent steps reached."
    }