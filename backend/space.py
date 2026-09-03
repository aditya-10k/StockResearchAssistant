import uvicorn
from app.main import app as fastapi_app

try:
    import gradio as gr
    with gr.Blocks(title="Stock Research Assistant API") as demo:
        gr.Markdown("# Stock Research Assistant - Backend API")
        gr.Markdown("FastAPI backend is active and healthy.")
        gr.Markdown("- Endpoint: `/query/stream`")
        gr.Markdown("- Model: `qwen/qwen3.8-27b` via Groq")
    app = gr.mount_gradio_app(fastapi_app, demo, path="/ui")
except ImportError:
    print("Gradio not installed locally, running pure FastAPI.")
    app = fastapi_app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
