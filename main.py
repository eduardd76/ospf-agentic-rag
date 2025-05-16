# -*- coding: utf-8 -*-
import chainlit as cl
from langchain.schema import Document
from graph import ospf_troubleshooter

def format_solution(solution: dict) -> str:
    steps = "\n- ".join(solution.get('implementation_steps', []))
    cmds = "\n".join(solution.get('cli_commands', []))
    verify = "\n- ".join(solution.get('verification_steps', []))

    return f"""Solution Summary:
{solution.get('solution_summary', '')}

Implementation Steps:
- {steps}

CLI Commands:
```bash
{cmds}
```

Verification Steps:
- {verify}
"""


def format_diagnosis(diagnosis: dict) -> str:
    return f"""Diagnosis
Title: {diagnosis.get('problem_title', '')}
Cause: {diagnosis.get('root_cause', '')}
Severity: {diagnosis.get('severity', '')}
Impact: {diagnosis.get('potential_impact', '')}
"""


def format_validation(validation: dict) -> str:
    status = "Valid Solution" if validation.get("is_valid", False) else "Invalid Solution"

    concerns = validation.get("concerns", [])
    improvements = validation.get("improvements", [])
    revised_cmds = validation.get("revised_commands", [])

    # Convertim în șiruri dacă nu sunt deja
    concerns_text = [str(item) for item in concerns]
    improvements_text = [str(item) for item in improvements]
    revised_cmds_text = [str(item) for item in revised_cmds]

    return f"""Validation Result: {status}

Concerns:
- {chr(10).join(concerns_text) if concerns_text else "None"}

Suggested Improvements:
- {chr(10).join(improvements_text) if improvements_text else "None"}

Revised CLI Commands:
```bash
{chr(10).join(revised_cmds_text) if revised_cmds_text else "None"}
```"""



@cl.on_message
async def handle_log_input(message: cl.Message):
    log_text = message.content.strip()

    if not log_text:
        await cl.Message(content="Please enter an OSPF log message.").send()
        return

    doc = Document(page_content=log_text, metadata={"router_id": "Router1"})
    await cl.Message(content="Analyzing the log...").send()

    result = ospf_troubleshooter.invoke({"log_document": doc})

    issue_type = result.get("issue_type", "Unknown")
    diagnosis = format_diagnosis(result.get("diagnosis", {}))
    solution = format_solution(result.get("solution", {}))
    validation = format_validation(result.get("validation", {}))

    response = f"""Issue Type: `{issue_type}`

{diagnosis}

{solution}

{validation}
"""    

    await cl.Message(content=response).send()
