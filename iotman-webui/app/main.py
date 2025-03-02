import os
import requests
from nicegui import ui

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:80")

def fetch_data(table, status_label):
    status_label.text = "Fetching data..."
    try:
        response = requests.get(f"{BACKEND_URL}/data")
        response.raise_for_status()
        results = response.json().get("items", [])
        
        # Format the rows for the table
        formatted_rows = []
        for row in results:
            formatted_rows.append({
                'battery_id': row["battery_id"],
                'voltage': f'{row["voltage"]:.2f} V',
                'timestamp': row["timestamp"]
            })
        
        # Update the table with the new rows
        table.update_rows(formatted_rows)
        
        status_label.text = f"Loaded {len(results)} logs."
    except Exception as e:
        status_label.text = f"Error: {e}"

# Create page content functions
def create_home_content(container):
    with container:
        ui.label("Welcome to IoTMan").classes("text-3xl font-bold mb-4")
        ui.label("A simple IoT management dashboard").classes("text-xl mb-6")
        
        with ui.card().classes("p-4 bg-gray-800"):
            ui.label("Getting Started").classes("text-2xl mb-2")
            ui.label("Use the sidebar to navigate between different sections:").classes("mb-2")
            ui.label("• Home: This welcome page").classes("mb-1")
            ui.label("• Data: View the latest IoT device logs").classes("mb-1")
            ui.label("• Settings: Configure your dashboard preferences").classes("mb-1")

def create_data_content(container):
    with container:
        ui.label("IoTMan Logs").classes("text-3xl font-bold mb-4")
        
        # Status label
        status_label = ui.label("Click 'Load Logs' to fetch data").classes("mb-2")
        
        # Table container
        with ui.card().classes("p-4 bg-gray-800 mb-4"):
            # Initialize table with columns and empty rows
            columns = [
                {"name": "battery_id", "label": "Battery ID", "field": "battery_id", "align": "left"},
                {"name": "voltage", "label": "Voltage", "field": "voltage", "align": "left"},
                {"name": "timestamp", "label": "Timestamp", "field": "timestamp", "align": "left"}
            ]
            log_table = ui.table(columns=columns, rows=[]).classes("w-full text-left")
        
        # Fetch button
        ui.button("Load Logs",
                on_click=lambda: fetch_data(log_table, status_label),
                ).classes("bg-blue-500 hover:bg-blue-600 text-white font-semibold px-4 py-2 rounded")

def create_settings_content(container):
    with container:
        ui.label("Dashboard Settings").classes("text-3xl font-bold mb-4")
        
        with ui.card().classes("p-4 bg-gray-800 mb-4"):
            ui.label("Theme Preferences").classes("text-xl font-bold mb-2")
            
            dark_mode = ui.switch("Dark Mode", value=True).classes("mb-4")
            
            ui.label("Refresh Interval").classes("text-lg mb-2")
            interval = ui.slider(min=5, max=60, value=30, step=5).classes("mb-4")
            ui.label().bind_text_from(interval, 'value', lambda v: f'Refresh every {v} seconds')
            
            ui.label("Notification Settings").classes("text-xl font-bold mb-2")
            ui.checkbox("Enable alert sounds").classes("mb-2")
            ui.checkbox("Show desktop notifications").classes("mb-2")
            ui.checkbox("Email critical alerts").classes("mb-2")
            
            ui.button("Save Settings").classes("bg-blue-500 hover:bg-blue-600 text-white font-semibold px-4 py-2 rounded mt-4")
            
        with ui.card().classes("p-4 bg-gray-800"):
            ui.label("Advanced Options").classes("text-xl font-bold mb-2")
            ui.button("Reset to Defaults").classes("bg-red-500 hover:bg-red-600 text-white font-semibold px-4 py-2 rounded")
            ui.button("Export Configuration").classes("bg-green-500 hover:bg-green-600 text-white font-semibold px-4 py-2 rounded ml-2")

@ui.page("/")
def main_page():
    # Use custom CSS with classes instead of IDs
    ui.add_head_html("""
    <style>
    body {
        margin: 0;
        padding: 0;
        overflow: hidden;
    }
    .app-container {
        display: flex;
        width: 100vw;
        height: 100vh;
        overflow: hidden;
    }
    .sidebar {
        width: 220px;
        min-width: 220px;
        height: 100vh;
        display: flex;
        flex-direction: column;
        background-color: #1f2937;
        padding: 1rem;
    }
    .content-area {
        flex: 1;
        height: 100vh;
        padding: 2rem;
        overflow-y: auto;
        background-color: #111827;
    }
    </style>
    """)
    
    # Create a content container reference that will be available to all functions
    content_container = None
    
    # Main container using flexbox
    with ui.element('div').classes('app-container text-white').style('display: flex; width: 100vw; height: 100vh;'):
        # Sidebar
        with ui.element('div').classes('sidebar'):
            ui.label("IoTMan").classes("text-2xl font-bold mb-6 text-center")
            
            # Navigation links
            nav_items = []
            
            # Define navigation functions using nonlocal to access content_container
            def show_home():
                nonlocal content_container
                content_container.clear()
                create_home_content(content_container)
                # Update active state
                for item in nav_items:
                    item.set_class('bg-blue-600', item.text == 'Home')
                    item.set_class('bg-gray-700 hover:bg-gray-600', item.text != 'Home')
                
            def show_data():
                nonlocal content_container
                content_container.clear()
                create_data_content(content_container)
                # Update active state
                for item in nav_items:
                    item.set_class('bg-blue-600', item.text == 'Data')
                    item.set_class('bg-gray-700 hover:bg-gray-600', item.text != 'Data')
            
            def show_settings():
                nonlocal content_container
                content_container.clear()
                create_settings_content(content_container)
                # Update active state
                for item in nav_items:
                    item.set_class('bg-blue-600', item.text == 'Settings')
                    item.set_class('bg-gray-700 hover:bg-gray-600', item.text != 'Settings')
            
            # Home button
            home_btn = ui.button('Home', on_click=show_home).classes('w-full mb-2 text-left pl-4 py-2 bg-blue-600 rounded')
            nav_items.append(home_btn)
            
            # Data button
            data_btn = ui.button('Data', on_click=show_data).classes('w-full mb-2 text-left pl-4 py-2 bg-gray-700 hover:bg-gray-600 rounded')
            nav_items.append(data_btn)
            
            # Settings button
            settings_btn = ui.button('Settings', on_click=show_settings).classes('w-full mb-2 text-left pl-4 py-2 bg-gray-700 hover:bg-gray-600 rounded')
            nav_items.append(settings_btn)
            
            # Bottom section of sidebar - spacer and version
            with ui.element('div').style('flex-grow: 1;'):
                ui.label("Version 1.0.0").classes("text-gray-400 text-xs text-center mt-auto")
        
        # Content area - separate from the sidebar
        with ui.element('div').classes('content-area'):
            # Create a container for the content and store it for later use
            content_container = ui.element('div')
            # Initialize with home content
            create_home_content(content_container)

def run_app():
    ui.run(port=8080, host="0.0.0.0")

if __name__ in {"__main__", "__mp_main__"}:
    run_app()
