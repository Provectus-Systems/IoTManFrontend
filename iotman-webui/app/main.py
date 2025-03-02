import os
from nicegui import ui

# Fetch backend URL from environment variables (set in Docker Compose)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:80")

@ui.page('/')
def index_page():
    ui.label('Hello from IoTMan Web UI!')
    ui.label(f'Connected to Backend: {BACKEND_URL}')

def run_app():
    """Starts the NiceGUI server"""
    ui.run(port=8080, host='0.0.0.0')

if __name__ in {"__main__", "__mp_main__"}:
    run_app()
