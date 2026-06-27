import os
import requests

def run_prd_reconciliation():
    # 1. Read source configurations and current implementation layers into memory buffers
    with open("docs/PRD.md", "r", encoding="utf-8") as f:
        prd_content = f.read()

    current_code = ""
    if os.path.exists("src/App.jsx"):
        with open("src/App.jsx", "r", encoding="utf-8") as f:
            current_code = f.read()

    # 2. Establish strict system formatting prompts
    system_prompt = (
        "You are an expert React engineer and QA Automation tester. Your task is to review the provided PRD "
        "and update the React frontend application code and unit test files to perfectly align with requirements. "
        "Output ONLY the updated, valid code content of src/App.jsx, followed immediately by a unique divider string "
        "'===FILE_SPLIT_TOKEN===', followed by the complete code content of src/App.test.jsx. "
        "Do not wrap files in markdown blocks, formatting markers, or introductory chatter."
    )

    user_prompt = f"PRD specification:\n{prd_content}\n\nCurrent App.jsx:\n{current_code}"

    payload = {
        "model": "gpt-4o", # Can be swapped with any model endpoint provider you integrate
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.0 # Pinning to 0.0 prevents hallucinations
    }

    print("Transmitting PRD requirements to the LLM compiler...")

    # 3. Request generation from your LLM provider api
    headers = {"Authorization": f"Bearer {os.environ.get('LLM_API_KEY')}"}
    response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
    raw_output = response.json()['choices'][0]['message']['content']

    # 4. Parse output blocks and programmatically rewrite your local application files
    print("Parsing generation streams and updating application source tracks...")
    file_segments = raw_output.split("===FILE_SPLIT_TOKEN===")

    app_jsx = file_segments[0].strip().replace("```jsx", "").replace("```", "")
    app_test = file_segments[1].strip().replace("```jsx", "").replace("```", "")

    with open("src/App.jsx", "w", encoding="utf-8") as f:
        f.write(app_jsx)

    with open("src/App.test.jsx", "w", encoding="utf-8") as f:
        f.write(app_test)

    print("Successfully written application files and automated test suites.")

if __name__ == "__main__":
    run_prd_reconciliation()
