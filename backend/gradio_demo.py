"""Simple Gradio interface for testing MM-Search."""
import requests
import gradio as gr

BASE_URL = "http://127.0.0.1:5050/api"


def upload_file(file: gr.FileData) -> str:
    """Upload a file to the backend."""
    if file is None:
        return "No file selected"
    with open(file.name, "rb") as fh:
        response = requests.post(f"{BASE_URL}/upload/file", files={"file": fh})
    if response.status_code == 201:
        fid = response.json().get("file_id")
        return f"Uploaded file. id={fid}"
    return f"Error: {response.text}"


def ask_question(query: str) -> dict:
    """Send a search query to the backend."""
    if not query:
        return {"error": "Query required"}
    response = requests.post(f"{BASE_URL}/search", json={"query": query})
    try:
        return response.json()
    except ValueError:
        return {"error": response.text}


def build_ui() -> gr.Blocks:
    """Create the Gradio UI."""
    with gr.Blocks() as demo:
        gr.Markdown("# MM-Search Demo")
        with gr.Row():
            file_input = gr.File(label="Upload file")
            upload_btn = gr.Button("Upload")
        upload_output = gr.Textbox(label="Upload result")
        upload_btn.click(upload_file, inputs=file_input, outputs=upload_output)

        query = gr.Textbox(label="Ask a question")
        search_btn = gr.Button("Search")
        result_box = gr.JSON(label="Search result")
        search_btn.click(ask_question, inputs=query, outputs=result_box)
    return demo


if __name__ == "__main__":
    ui = build_ui()
    ui.launch()
