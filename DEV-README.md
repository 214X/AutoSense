Downloads:
brew install ollama
ollama pull llama3.2

To run the model:
ollama run llama3.2

To use ollama API:
ollama serve // Opens a new service at port 11434

    if (port is not available):
        lsof -i :11434
        kill -9 <PID>