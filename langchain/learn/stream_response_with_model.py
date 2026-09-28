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