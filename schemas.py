from typing import List
from pydantic import BaseModel, Field


def Source(BaseModel):
    """Schema for a source used by the agent"""
    url: str = Field(description="The URL of the source")

def AgentResponse(BaseModel):
    """Schema for agent response with answer to the query"""
    answer: str = Field(description="The agent's answer to t he query")
    sources: List[Source] = Field(
        default_factory=list,
        description="List of success used to generate the answer"
    )

