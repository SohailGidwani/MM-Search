# MM-Search

MM-Search is a toy multi-modal search engine for personal data. The backend stores file contents as vector embeddings in Qdrant and uses a collection of local language models to provide semantic search and summarization.

Supported modalities include:

- text and PDFs
- images (described with `llava:7b`)
- audio/video (transcribed with `facebook/s2t-small-librispeech-asr`)

Embeddings are generated with `nomic-embed-text` and search results can be summarised using `llama3.2:3b`.

A small Gradio demo is included under `backend` for uploading files and asking questions against the index. See the backend README for setup instructions.
