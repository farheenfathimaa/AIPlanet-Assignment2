# Math Routing Agent API Documentation

## Base URL
`/api`

## Endpoints

### 1. Ask a Math Question
* **Endpoint:** `/ask`
* **Method:** `POST`
* **Description:** Submits a mathematical question and receives a generated step-by-step solution.
* **Request Body (`application/json`):**
    ```json
    {
      "question": "string"
    }
    ```
* **Success Response (200 OK):**
    ```json
    {
      "question": "string",
      "solution": "string",
      "source": "knowledge_base" | "web_search"
    }
    ```
* **Error Responses:**
    * `400 Bad Request`: Input guardrail failed (e.g., non-math query).
    * `500 Internal Server Error`: An unexpected error occurred in the agentic workflow or output guardrail.

### 2. Submit Feedback
* **Endpoint:** `/feedback`
* **Method:** `POST`
* **Description:** Allows users to provide feedback on the quality of a generated solution. This data is used for continuous agent improvement.
* **Request Body (`application/json`):**
    ```json
    {
      "question": "string",
      "solution": "string",
      "rating": 5,
      "comments": "string"
    }
    ```
* **Success Response (200 OK):**
    ```json
    {
      "message": "Feedback submitted successfully."
    }
    ```