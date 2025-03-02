import asyncio
from nicegui import ui

@ui.page('/')
async def index_page():
    ui.label('Hello from IoTMan Web UI!')
    ui.label('We are running on Python 3.12 with NiceGUI.')

@ui.page('/async-demo')
async def async_demo_page():
    ui.label('This page demonstrates asynchronous functionality.')
    
    async def do_something():
        await asyncio.sleep(1)
        return "Async task complete!"
    
    async def on_click():
        result = await do_something()
        result_label.text = result

    ui.button('Run Async Task', on_click=on_click)
    result_label = ui.label('')

def run_app():
    """
    Start the NiceGUI event loop on port 8080.
    In production, you could also configure uvicorn with multiple workers
    (though real-time features and websockets can be trickier with multiple workers).
    """
    ui.run(port=8080)

if __name__ == '__main__':
    run_app()
