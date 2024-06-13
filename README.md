# YAMR LLM Server

This is a server project that uses the langchain framework to provide natural language processing services for the YAMR application.

Please note that this is still a WIP and different bugs are definitely possible.

## Requirements

- Python between 3.8 and 3.11
- OpenAI API key

## Usage

Before running the server, you need to provide your OpenAI API key in a `.env` file in the root directory of the project.

By default, the server will start under `http://localhost:2334`, as specified in `run.ps1`. This URL is currently hardcoded in the client app.

### Start locally

The `run.ps1` script is created to streamline the process of running the server locally. When executed, it first detects the version of Python that is compatible with the project. It then creates a virtual environment named `.venv` in the project directory and activates it. Within this environment, the script installs all the required dependencies from `requirements.txt`. Finally, it starts the Uvicorn server, making the application accessible at specified in `run.ps1` address.

```powershell
./run.ps1
```

To recreate the virtual environment and reinstall all the packages, delete the existing `.venv` directory before executing the script.
