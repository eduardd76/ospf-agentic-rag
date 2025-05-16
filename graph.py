
from typing import Dict, Any, Optional, TypedDict
import json
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

# ----------------- State definition -----------------
class OSPFTroubleshootingState(TypedDict):
    log_document: Document
    issue_type: Optional[str]
    ospf_knowledge: Optional[str]
    diagnosis: Optional[Dict[str, Any]]
    solution: Optional[Dict[str, Any]]
    validation: Optional[Dict[str, Any]]
    router_id: Optional[str]

# ----------------- Load knowledge base -----------------
def load_knowledge_base():
    with open("knowledge_base/ospf_troubleshooting.txt", "r") as f:
        content = f.read()
    return content

def initialize_vector_db(ospf_knowledge: str):
    document = Document(page_content=ospf_knowledge)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents([document])
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(chunks, embeddings)

# ----------------- Prompts and Chains -----------------
llm = ChatOpenAI(model="gpt-4")

log_parser_prompt = ChatPromptTemplate.from_template("""
You are an OSPF expert. Identify the OSPF issue type from this log:

Log:
{log_content}

Options:
- Authentication Mismatch
- MTU Mismatch
- Hello/Dead Timer Mismatch
- Network Type Mismatch
- Area Type Mismatch
- Unknown

Issue:
""")
log_parsing_chain = (
    {"log_content": lambda x: x}
    | log_parser_prompt
    | llm
    | StrOutputParser()
)

diagnosis_prompt = ChatPromptTemplate.from_template("""
You are diagnosing an OSPF issue. Provide a JSON response with:

- problem_title
- root_cause
- severity
- potential_impact

Log:
{log_message}

Issue: {issue_type}

Knowledge:
{ospf_knowledge}

Diagnosis:
""")
diagnosis_chain = diagnosis_prompt | llm | StrOutputParser()

solution_prompt = ChatPromptTemplate.from_template("""
Given the OSPF diagnosis and knowledge, propose a fix in JSON with:

- solution_summary
- implementation_steps
- cli_commands
- verification_steps

Diagnosis:
{diagnosis}

Knowledge:
{ospf_knowledge}

Router: {router_id}

Solution:
""")
solution_chain = solution_prompt | llm | StrOutputParser()

validation_prompt = ChatPromptTemplate.from_template("""
Check the proposed OSPF solution. Provide JSON:

- is_valid
- concerns
- improvements
- revised_commands

Diagnosis:
{diagnosis}
Solution:
{solution}
Knowledge:
{ospf_knowledge}

Validation:
""")
validation_chain = validation_prompt | llm | StrOutputParser()

# ----------------- LangGraph nodes -----------------
def parse_logs(state: OSPFTroubleshootingState) -> OSPFTroubleshootingState:
    log_content = state["log_document"].page_content
    router_id = state["log_document"].metadata.get("router_id", "unknown")
    issue_type = log_parsing_chain.invoke(log_content)
    return {**state, "issue_type": issue_type, "router_id": router_id}

def retrieve_knowledge(state: OSPFTroubleshootingState) -> OSPFTroubleshootingState:
    query = f"OSPF troubleshooting for {state['issue_type']}"
    docs = vector_store.similarity_search(query, k=2)
    knowledge = "\n\n".join([doc.page_content for doc in docs])
    return {**state, "ospf_knowledge": knowledge}

def diagnose_problem(state: OSPFTroubleshootingState) -> OSPFTroubleshootingState:
    output = diagnosis_chain.invoke({
        "log_message": state["log_document"].page_content,
        "ospf_knowledge": state["ospf_knowledge"],
        "issue_type": state["issue_type"]
    })
    try:
        diagnosis = json.loads(output)
    except:
        diagnosis = {"problem_title": "Parsing Error", "raw_output": output}
    return {**state, "diagnosis": diagnosis}

def generate_solution(state: OSPFTroubleshootingState) -> OSPFTroubleshootingState:
    output = solution_chain.invoke({
        "diagnosis": json.dumps(state["diagnosis"]),
        "ospf_knowledge": state["ospf_knowledge"],
        "router_id": state["router_id"]
    })
    try:
        solution = json.loads(output)
    except:
        solution = {"solution_summary": "Parsing Error", "raw_output": output}
    return {**state, "solution": solution}

def validate_solution(state: OSPFTroubleshootingState) -> OSPFTroubleshootingState:
    output = validation_chain.invoke({
        "diagnosis": json.dumps(state["diagnosis"]),
        "solution": json.dumps(state["solution"]),
        "ospf_knowledge": state["ospf_knowledge"]
    })
    try:
        validation = json.loads(output)
    except:
        validation = {"is_valid": False, "raw_output": output}
    return {**state, "validation": validation}

# ----------------- LangGraph workflow -----------------
workflow = StateGraph(OSPFTroubleshootingState)
workflow.add_node("parse_logs", parse_logs)
workflow.add_node("retrieve_knowledge", retrieve_knowledge)
workflow.add_node("diagnose_problem", diagnose_problem)
workflow.add_node("generate_solution", generate_solution)
workflow.add_node("validate_solution", validate_solution)

def should_regenerate(state: OSPFTroubleshootingState) -> str:
    return "generate_solution" if not state.get("validation", {}).get("is_valid", True) else END

workflow.add_edge("parse_logs", "retrieve_knowledge")
workflow.add_edge("retrieve_knowledge", "diagnose_problem")
workflow.add_edge("diagnose_problem", "generate_solution")
workflow.add_edge("generate_solution", "validate_solution")
workflow.add_conditional_edges("validate_solution", should_regenerate, {
    "generate_solution": "generate_solution",
    END: END
})
workflow.set_entry_point("parse_logs")
ospf_troubleshooter = workflow.compile()

# ----------------- Load vector store -----------------
ospf_knowledge = load_knowledge_base()
vector_store = initialize_vector_db(ospf_knowledge)
