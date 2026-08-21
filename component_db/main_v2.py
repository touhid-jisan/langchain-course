"""
Given a server model (e.g. "Cisco APIC-L2", part number APIC-SERVER-L2),
search the web for its officially supported/compatible CPU list, then
extract that list into structured records via a local LLM.
"""

from asyncio import base_futures
import os
from dotenv import load_dotenv
import re
from typing import Optional, List

from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_tavily import TavilySearch
load_dotenv()
class CompatibleCPU(BaseModel):
    """One CPU model listed as compatible with the target server."""
    manufacturer: Optional[str] = None
    family: Optional[str] = None
    model_name: str
    part_number: Optional[str] = None
    architecture: Optional[str] = None
    generation: Optional[str] = None


class CompatibleCPUList(BaseModel):
    """Full set of CPUs compatible with a given server model."""
    server_model: str
    cpus: List[CompatibleCPU] = Field(default_factory=list)


_tavily = TavilySearch(
    max_results=5,
    search_depth="advanced",
    include_raw_content=False,
)


@tool
def search_compatible_cpus(server_model: str, part_number: str = "") -> str:
    """Search the web for the list of CPU models officially supported by a
    given server or blade model (e.g. spec sheets, QuickSpecs, or
    compatibility matrices from the vendor or resellers).

    Args:
        server_model: Full server model name, e.g. "Cisco APIC-L2".
        part_number: Optional vendor part/SKU number to disambiguate the
            exact server config, e.g. "APIC-SERVER-L2".

    Returns:
        Combined short text snippets from the top matching search results
        describing which CPU models/families the server supports. This is
        NOT a final answer — it is raw source text meant to be passed to
        an LLM extraction step to pull out structured CPU records.
    """
    query = f"{server_model} {part_number} supported CPU processor options compatibility list".strip()
    results = _tavily.invoke({"query": query})
    
    return results


llm = ChatOllama(
    model="llama3.1:8b",
    base_url=os.getenv("SERVER_OLLAMA_BASE_URL"),
    temperature=0,
    num_ctx=8192,
)


server_model = "Cisco APIC-L2"
part_number = "APIC-SERVER-L2"
source_text = search_compatible_cpus.invoke({
    "server_model": server_model,
    "part_number": part_number,
})


prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You extract CPU compatibility data from source text about a server. "
     "List every distinct CPU model mentioned as supported/compatible. "
     "If a field (part_number, architecture, generation, family) isn't "
     "explicitly stated for a given CPU, leave it null — do not guess. "
     "If the text gives no CPU information at all, return an empty cpus list."),
    ("human", "Server: {server_model} (part number: {part_number})\n\nSource text:\n{source_text}"),
])

structured_llm = llm.with_structured_output(CompatibleCPUList)
chain = prompt | structured_llm

result = chain.invoke({
    "server_model": server_model,
    "part_number": part_number,
    "source_text": source_text,
})

print(f"Server: {result.server_model}")
for cpu in result.cpus:
    print(cpu)