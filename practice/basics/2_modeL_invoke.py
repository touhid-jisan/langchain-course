from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()

model = init_chat_model(
    model = 'ornith-1.5:9b',
    model_provider='ollama',
    base_url=os.getenv("SERVER_OLLAMA_BASE_URL"),
    temperature=1
)

response = model.invoke("whats the capital of Moon")
print(response.content)