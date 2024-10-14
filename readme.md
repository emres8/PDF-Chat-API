# PDF Chat Service

## Overview

PDF Chat Service is a FastAPI-based application that allows users to upload PDFs, process them, and interact with them using Natural Language Processing (NLP). The service integrates various Large Language Models (LLMs), such as Gemini, Langchain, and LlamaIndex, to generate context-aware responses based on the content of uploaded PDF files. It also supports caching for frequently asked questions using Redis.

### Key Features
- Upload PDFs and extract content.
- Ask questions about the content of PDFs using LLMs.
- Use different LLMs: Gemini, Langchain, LlamaIndex.
- Cache frequently asked questions in Redis.
- Integration with MongoDB for storing PDF metadata and content.
- Custom error handling middleware and structured logging.

## Project Setup

### Docker Image Usage

* You can run this FastAPI application directly using the pre-built Docker image available on Docker Hub.
* Make sure you have Docker installed on your machine.

#### Steps to Run the Application
Pull the Docker image from Docker Hub

```bash
docker pull emres8/sevenapps-case-app:latest
```
Run the Docker container

```bash
docker run -d -p 8000:8000 --name sevenapps-case-app
emres8/sevenapps-case-app:latest
```

This will start the FastAPI app and expose it on port 8000.


* If you don't want to use Docker Image you can follow manual instructions to run the project:

## Manual Instructions
### Prerequisites
- Python 3.9+
- MongoDB (local or cloud instance)
- Redis (local or cloud instance)


#### Environment Configuration

Create a `.env` file in the project by referencing `.sample_env`

#### Copy code
```bash
git clone https://github.com/emres8/PDF-Chat-API.git
cd PDF-Chat-API
```

#### Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
#### Install the required dependencies:

```bash
pip install -r requirements.txt
```
#### Set up MongoDB and Redis:
* Ensure MongoDB is running either locally or via a cloud provider like MongoDB Atlas.
* Ensure Redis is running on the specified `REDIS_HOST` and `REDIS_PORT`.

#### Running the Application
Run the FastAPI application with Uvicorn:
```bash
uvicorn app.main:app --reload
```
## API Reference

#### Upload PDF

```
  POST /v1/pdf
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `file` | `file` | **Required**.  The PDF file to upload |

Example Usage

```
curl --location 'http://localhost:8000/v1/pdf' \
--form 'file=@"/Desktop/sample.pdf"'
```
Response
```json
{
  "pdf_id": "670a8a39c8e846c029106fc1"
}
```

#### Get PDF by ID

```
  GET /v1/pdf/${id}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `pdf_id` | `string` | **Required**. The ID of the PDF to retrieve |

Example Usage

```bash
curl -X GET "http://localhost:8000/v1/pdf/670a8a39c8e846c029106fc1"

```
Response
```json
{
  "file_name": "test.pdf",
  "text": "This is the content of the PDF.",
  "metadata": {
    "page_count": 2,
    "file_name": "test.pdf"
  }
}

```

#### Chat with PDF

```
    POST /v1/chat/{pdf_id}
```
Allows the user to ask questions about the content of the PDF using a specific language model (e.g., ```gemini```, ```langchain```, ```llamaindex```).


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `pdf_id` | `string` | **Required**.  The ID of the PDF to query |
| `message` | `string` | **Required**.  The question you want to ask |
| `language_model_name` | `string` | **Optional**. The LLM to use (gemini by default)(can only take ```gemini```, ```langchain```, ```llamaindex```) |

Example Usage

```
curl -X POST "http://localhost:8000/v1/chat/670a8a39c8e846c029106fc1" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{
  "message": "What does this document say?",
  "language_model_name": "gemini"
}'
```
Response
```json
{
  "response": "The document discusses the following topic..."
}
```

After project is ready you can also access the API documentation locally at:
* http://localhost:8000/docs for the interactive API documentation (Swagger UI).
* http://localhost:8000/redoc for ReDoc documentation.





## Testing

#### Install the required dependencies:

```bash
pip install -r requirements.txt
```

#### Run the tests using pytest:

```bash
pytest
```
*  Running Specific Tests
To run a specific test file, you can provide the path to the test file:

```bash
pytest tests/integration/test_pdf_router.py
```


Or, to run a specific test function within a test file:

```bash
pytest tests/integration/test_pdf_router.py::test_get_pdf_valid
```

Default Project state should return
```
============================================= test session starts =============================================
platform darwin -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: /Users/emresafter/sevenapps-case
configfile: pytest.ini
testpaths: tests
plugins: asyncio-0.24.0, env-1.1.5, anyio-4.6.0
asyncio: mode=Mode.AUTO, default_loop_scope=function
collected 32 items                                                                                            

tests/integration/test_chat_router.py .....                                                             [ 15%]
tests/integration/test_pdf_router.py .....                                                              [ 31%]
tests/unit/test_chat_service.py ..                                                                      [ 37%]
tests/unit/test_gemini_language_model.py .                                                              [ 40%]
tests/unit/test_pdf_processor.py ................                                                       [ 90%]
tests/unit/test_pdf_service.py ...                                                                      [100%]

============================================= 32 passed in 0.14s ==============================================
```

## Potential Enhancements
* Not mocking db and redis but use test database and test container for testing
* Testing for two other language model not added. They could be added 
* Deployment to cloud


