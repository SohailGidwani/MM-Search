# gradio_demo.py

"""
Gradio frontend for MM-Search (Gradio 4.44.1).
Ensures that `file_type` is sent as a multipart form-part so the backend’s NOT NULL
constraint on files.file_type is never violated.
"""

import requests
import mimetypes
import gradio as gr

BASE_URL = "http://127.0.0.1:5050/api"


def upload_file(file: gr.FileData) -> str:
    """
    1) Guess a MIME type from the filename (e.g. 'notes.txt' -> 'text/plain').
    2) Take the top-level category (e.g. 'text', 'image', 'application').
    3) Send both the file-byte stream *and* a multipart form-part called "file_type"
       in the `files=` dict so that Flask’s request.form["file_type"] (or even
       request.files if someone mistakenly tried that) is never None.
    """
    if file is None:
        return "No file selected"

    # Guess something like "text/plain", "image/jpeg", etc.
    guessed_mime, _ = mimetypes.guess_type(file.name)

    # Extract the part before "/" ("text", "image", "application"), or default to "application"
    if guessed_mime and "/" in guessed_mime:
        top_category = guessed_mime.split("/")[0]
    else:
        top_category = "application"

    # Build the multipart payload:
    #
    # - "file":       (open file object)
    # - "file_type":  a 0-byte “file” part with value top_category
    #
    # In requests, (None, value) in the files dict means “send a form field, not a real file.”
    files_payload = {
        "file": open(file.name, "rb"),
        "file_type": (None, top_category)
    }

    # POST to /upload/file. No need to also send data=, since file_type is already in files=.
    response = requests.post(f"{BASE_URL}/upload/file", files=files_payload)

    if response.status_code == 201:
        fid = response.json().get("file_id")
        return f"Uploaded file. id={fid}"
    else:
        return f"Error {response.status_code}: {response.text}"


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
    """Create the Gradio UI (compatible with 4.44.1)."""
    theme = gr.themes.Default(
        primary_hue="blue", secondary_hue="purple",
        spacing_size="md", radius_size="md", text_size="md"
    )

    with gr.Blocks(theme=theme, css="""
        /* Center the title */
        #title {
            text-align: center;
            margin-bottom: 1rem;
        }
        /* Styling for “cards” */
        .upload-card, .query-card {
            padding: 1rem;
            border: 1px solid var(--secondary-300);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-sm);
            background-color: var(--background-secondary);
        }
        .upload-card .gr-button, .query-card .gr-button {
            margin-top: 0.75rem;
        }
        /* Preview image styling */
        .preview-img {
            max-height: 220px;
            object-fit: contain;
            border: 1px dashed var(--secondary-500);
            border-radius: var(--radius-sm);
        }
        /* Simple vertical-gap utility */
        .vertical-gap {
            margin-top: 1rem;
        }
    """) as demo:
        # ==== Title ====
        gr.Markdown("## MM-Search Demo", elem_id="title")

        # ==== 1) Upload Section (two columns) ====
        with gr.Row(elem_id="upload-section"):
            # Left column: file upload controls
            with gr.Column(scale=1):
                with gr.Column(elem_classes="upload-card"):
                    gr.Markdown("### 1) Upload a File")
                    file_input = gr.File(
                        label="Choose or drag a file here",
                        file_types=[".pdf", ".txt", ".png", ".jpg", ".jpeg"],
                        show_label=False
                    )
                    upload_btn = gr.Button("Upload", variant="primary")
                    upload_output = gr.Textbox(
                        label="Upload result", interactive=False, placeholder="—"
                    )
                    # Bind our new upload handler
                    upload_btn.click(upload_file, inputs=file_input, outputs=upload_output)

            # Right column: image preview (if the selected file is an image)
            with gr.Column(scale=1):
                with gr.Column(elem_classes="upload-card"):
                    gr.Markdown("### 2) Preview (if Image)")
                    preview = gr.Image(
                        label="Preview",
                        interactive=False,
                        elem_classes="preview-img"
                    )

                # Whenever the file selection changes, show a preview if it's .png/.jpg/.jpeg
                def get_preview(f):
                    if f is None:
                        return None
                    if any(f.name.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
                        return f.name
                    return None

                file_input.change(get_preview, inputs=file_input, outputs=preview)

        # Manual vertical gap (Gradio 4.44.1 has no Spacer component)
        gr.Markdown("<br>", elem_classes="vertical-gap")

        # ==== 2) Query / Search Section ====
        with gr.Row(elem_id="query-section"):
            with gr.Column():
                with gr.Column(elem_classes="query-card"):
                    gr.Markdown("### 3) Ask a Question")
                    query = gr.Textbox(
                        label="Enter your query here",
                        placeholder="e.g. ‘What does page 2 say about embeddings?’"
                    )
                    search_btn = gr.Button("Search", variant="primary")
                    result_box = gr.JSON(label="Search result")

                    # Bind the search handler
                    search_btn.click(ask_question, inputs=query, outputs=result_box)

        # Another small gap before footer
        gr.Markdown("<br>", elem_classes="vertical-gap")

        # ==== Footer ====
        gr.Markdown(
            "<center><small>Use via API 🚀 • Built with Gradio 🌟</small></center>",
            elem_id="footer-text"
        )

    return demo


if __name__ == "__main__":
    ui = build_ui()
    ui.launch(server_name="0.0.0.0", server_port=7860, show_api=False)
