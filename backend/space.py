import os
import sys
import socket
import time
import subprocess
import uvicorn
from app.main import app as fastapi_app

print("=== HF SPACE DIAGNOSTIC ===")
print("PORT env:", os.environ.get("PORT"))
print("GRADIO_SERVER_PORT env:", os.environ.get("GRADIO_SERVER_PORT"))
try:
    ps = subprocess.run(["ps", "-ef"], capture_output=True, text=True)
    print("Active processes in container:\n", ps.stdout)
except Exception as e:
    print("Could not inspect processes:", e)

try:
    import gradio as gr
    with gr.Blocks(title="Stock Research Assistant API") as demo:
        gr.Markdown("# Stock Research Assistant - Backend API")
        gr.Markdown("FastAPI backend is active and healthy.")
        gr.Markdown("- Endpoint: `/query/stream`")
        gr.Markdown("- Model: `qwen/qwen3.8-27b` via Groq")
    app = gr.mount_gradio_app(fastapi_app, demo, path="/ui")
except ImportError:
    app = fastapi_app

if __name__ == "__main__":
    target_port = int(os.environ.get("GRADIO_SERVER_PORT", os.environ.get("PORT", 7860)))
    
    # Wait for any lingering socket in TIME_WAIT to release
    for attempt in range(15):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(("0.0.0.0", target_port))
            s.close()
            print(f"Port {target_port} is free and ready!")
            break
        except OSError as err:
            s.close()
            print(f"Attempt {attempt+1}: Port {target_port} busy ({err}), waiting 2s for release...")
            time.sleep(2)

    uvicorn.run(app, host="0.0.0.0", port=target_port)
