import os
from typing import List, Optional

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from pydantic import BaseModel

load_dotenv()


class CPUSpec(BaseModel):
    """Structured CPU specification extracted from web search results.

    Fields are left as None when the source text doesn't explicitly
    state a value -- the LLM is instructed not to guess or infer.
    """

    manufacturer: Optional[str] = None
    model_name: str
    cores: Optional[int] = None
    threads: Optional[int] = None
    base_clock_ghz: Optional[float] = None
    socket: Optional[str] = None
    supported_memory_types: Optional[List[str]] = None


_tavily = TavilySearch(
    max_results=5, search_depth="advanced", include_raw_content=False, country="Japan"
)


@tool
def search_cpu_specs(model_name: str) -> str:
    """Search the web for a CPU's technical specifications
    (cores, threads, clock speed, socket, memory type) and return
    the combined page text from the top matching spec-sheet sites.
    """
    query = f"{model_name} cores threads clock speed socket memory type specifications"
    results = _tavily.invoke({"query": query})
    return "\n\n".join(r.get("raw_content") or r["content"] for r in results["results"])


llm = ChatOllama(
    model="llama3.2",
    # base_url=os.getenv("SERVER_OLLAMA_BASE_URL"),
    temperature=0,
)

model_name = "Intel Xeon E5-2609 v3"
page_text = search_cpu_specs.invoke({"model_name": model_name})

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Extract CPU specs from the text. Leave fields null if not present.",
        ),
        ("human", "CPU: {model_name}\n\nText:\n{page_text}"),
    ]
)

structured_llm = llm.with_structured_output(CPUSpec)
chain = prompt | structured_llm

result = chain.invoke({"model_name": model_name, "page_text": page_text})

print(result)
