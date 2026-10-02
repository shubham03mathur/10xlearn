"""
This module demonstrate the message streaming technique with agent/chat model.
This example uses the chat model approach but the same can be extended with agent as well

Streaming response is essential to not having user waiting until agent generates the full response,
In this technique agent/llm returns the data chunk which can be rendered via UI app to
show `typing` effect same as modern chat apps like chatGPT, Gemini or Claude.

"""

from langchain.chat_models import init_chat_model

model = init_chat_model('ollama:gemma4:12b-mlx')

fullText = None
chunks = []
for chunk in model.stream('Hey!'):
    if chunk.text:
        chunks.append(chunk.text)
    fullText = chunk.text if fullText is None else fullText + chunk.text

print(fullText) # Hello! How can I help you today?
print(chunks) # ['Hello', '!', ' How', ' can', ' I', ' help', ' you', ' today', '?']