from dotenv  import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

load_dotenv()

def main():
    information = """
        Elon Reeve Musk (born June 28, 1971) is a businessman and former public official who is the CEO and largest shareholder of Tesla and SpaceX. Musk has been the wealthiest person in the world since 2025, and became the only trillionaire in terms of US dollars in June 2026; as of August 8, 2026, Forbes estimates his net worth to be US$823 billion.

        """
    summary_template = """
        Given the information {information} about a person i want you to create a:
        1. a short summary
        2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template
    )

    # print(summary_prompt_template)
    llm = ChatOpenRouter(
        model="google/gemma-4-26b-a4b-it:free", 
        temperature=0,
        api_key=os.getenv("OPENROUTER_API_KEY")
        )

    # print(llm)

    chain = summary_prompt_template | llm
    # print(chain)
    response = chain.invoke({"information": information})
    print(response.content)

if __name__ == "__main__":
    main()
