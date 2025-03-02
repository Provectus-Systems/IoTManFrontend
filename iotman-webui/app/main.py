import os
import requests
import json
from datetime import datetime, timedelta
from nicegui import ui
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:80")

def fetch_data(container, status_label, start_time=None, end_time=None):
    """Fetch battery data and update visualizations"""
    status_label.text = "Fetching data..."
    try:
        # Build query parameters for time filtering
        params = {}
        if start_time:
            params['start_time'] = start_time.isoformat()
        if end_time:
            params['end_time'] = end_time.isoformat()
        
        # Make the API request with query parameters
        response = requests.get(f"{BACKEND_URL}/data", params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data or 'items' not in data or not data['items']:
            status_label.text = "No data available."
            return
            
        # Process the data for visualization
        create_visualizations(container, data, status_label, start_time, end_time)
        
        status_label.text = f"Data loaded successfully. Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC"
    except Exception as e:
        status_label.text = f"Error fetching data: {e}"
        
def create_visualizations(container, data, status_label, start_time=None, end_time=None):
    """Create visualizations based on the data"""
    with container:
        # Clear existing charts if any
        container.clear()
        
        try:
            # Process data for plotting - focusing on the correct format with 'items'
            items = data.get('items', [])
            total_items = data.get('total_items', len(items))
            
            if not items:
                ui.label("No battery data available.").classes("text-xl text-red-500")
                return
                
            # Convert to pandas DataFrame for easier manipulation
            df = pd.DataFrame(items)
            
            # Convert timestamps to datetime objects
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Sort by timestamp
            df = df.sort_values('timestamp')
            
            # Create an interactive voltage over time chart
            fig = make_subplots(specs=[[{"secondary_y": False}]])
            
            # Add a trace for each unique battery_id
            unique_batteries = df['battery_id'].unique()
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
            
            for i, battery_id in enumerate(unique_batteries):
                battery_data = df[df['battery_id'] == battery_id]
                color = colors[i % len(colors)]
                
                fig.add_trace(
                    go.Scatter(
                        x=battery_data['timestamp'],
                        y=battery_data['voltage'],
                        mode='lines+markers',
                        name=f'Battery {battery_id}',
                        line=dict(color=color, width=2),
                        marker=dict(size=8, color=color),
                        hovertemplate='<b>%{x}</b><br>' + 
                                    'Voltage: %{y:.2f}V<br>' +
                                    f'Battery: {battery_id}',
                    )
                )
            
            # Create time range description for title
            time_range_desc = ""
            if start_time and end_time:
                time_range_desc = f" ({start_time.strftime('%Y-%m-%d %H:%M')} to {end_time.strftime('%Y-%m-%d %H:%M')} UTC)"
            elif start_time:
                time_range_desc = f" (since {start_time.strftime('%Y-%m-%d %H:%M')} UTC)"
            elif end_time:
                time_range_desc = f" (until {end_time.strftime('%Y-%m-%d %H:%M')} UTC)"
            
            # Customize the chart
            fig.update_layout(
                title=f"Battery Voltage Over Time{time_range_desc}<br>({len(unique_batteries)} batteries, {total_items} readings)",
                title_font_size=24,
                title_x=0.5,  # Center the title
                plot_bgcolor='rgba(32, 32, 40, 1)',  # Dark background
                paper_bgcolor='rgba(32, 32, 40, 1)',
                font=dict(color='white'),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(l=20, r=20, t=80, b=20),
                xaxis=dict(
                    title="Time (UTC)",
                    gridcolor='rgba(80, 80, 90, 0.3)',
                    showline=True,
                    linecolor='rgba(180, 180, 190, 0.5)',
                    tickfont=dict(size=12),
                ),
                yaxis=dict(
                    title="Voltage (V)",
                    gridcolor='rgba(80, 80, 90, 0.3)',
                    showline=True,
                    linecolor='rgba(180, 180, 190, 0.5)',
                    tickfont=dict(size=12),
                    ticksuffix=' V',
                ),
                hovermode="x unified",
            )
            
            # Restore the range slider with time selector buttons
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=15, label="15m", step="minute", stepmode="backward"),
                        dict(count=1, label="1h", step="hour", stepmode="backward"),
                        dict(count=12, label="12h", step="hour", stepmode="backward"),
                        dict(count=1, label="1d", step="day", stepmode="backward"),
                        dict(count=7, label="1w", step="day", stepmode="backward"),
                        dict(step="all", label="All")
                    ]),
                    bgcolor='rgba(60, 60, 70, 0.7)',
                    activecolor='rgba(0, 120, 255, 0.7)',
                )
            )
            
            # Create plot
            plot = ui.plotly(fig).classes('w-full h-96 mt-4')
            
            # Create summary stats card
            with ui.card().classes('w-full mt-4 p-4 bg-gray-800'):
                ui.label("Battery Summary").classes("text-xl font-bold mb-4")
                
                # Calculate stats
                summary_rows = []
                for battery_id in unique_batteries:
                    battery_data = df[df['battery_id'] == battery_id]
                    latest_reading = battery_data.iloc[-1] if not battery_data.empty else None
                    
                    if latest_reading is not None:
                        summary_rows.append({
                            'battery_id': battery_id,
                            'latest_voltage': f"{latest_reading['voltage']:.2f} V",
                            'latest_timestamp': latest_reading['timestamp'].strftime('%Y-%m-%d %H:%M:%S') + " UTC",
                            'readings_count': len(battery_data),
                            'min_voltage': f"{battery_data['voltage'].min():.2f} V",
                            'max_voltage': f"{battery_data['voltage'].max():.2f} V",
                            'avg_voltage': f"{battery_data['voltage'].mean():.2f} V"
                        })
                
                # Create summary table
                summary_columns = [
                    {"name": "battery_id", "label": "Battery ID", "field": "battery_id", "align": "left"},
                    {"name": "latest_voltage", "label": "Latest Voltage", "field": "latest_voltage", "align": "right"},
                    {"name": "readings_count", "label": "# Readings", "field": "readings_count", "align": "right"},
                    {"name": "min_voltage", "label": "Min Voltage", "field": "min_voltage", "align": "right"},
                    {"name": "max_voltage", "label": "Max Voltage", "field": "max_voltage", "align": "right"},
                    {"name": "avg_voltage", "label": "Avg Voltage", "field": "avg_voltage", "align": "right"},
                    {"name": "latest_timestamp", "label": "Last Updated", "field": "latest_timestamp", "align": "right"}
                ]
                
                ui.table(columns=summary_columns, rows=summary_rows).classes('w-full')
        
        except Exception as e:
            ui.label(f"Error creating visualizations: {e}").classes("text-red-500")

# Create page content functions
def create_home_content(container):
    with container:
        ui.label("Welcome to IoTMan").classes("text-3xl font-bold mb-4")
        ui.label("A simple IoT management dashboard").classes("text-xl mb-6")
        
        with ui.card().classes("p-4 bg-gray-800"):
            ui.label("Getting Started").classes("text-2xl mb-2")
            ui.label("Use the sidebar to navigate between different sections:").classes("mb-2")
            ui.label("• Home: This welcome page").classes("mb-1")
            ui.label("• Dashboard: View the latest IoT device logs").classes("mb-1")
            ui.label("• Settings: Configure your dashboard preferences").classes("mb-1")

def create_dashboard_content(container):
    with container:
        ui.label("Dashboard").classes("text-3xl font-bold mb-4")
        
        # Status label
        status_label = ui.label("Loading data...").classes("mb-2")
        
        # Function to refresh data with time range
        def refresh_with_time_range(value, unit):
            if value is None or unit is None:
                # Fetch all data
                fetch_data(data_viz_container, status_label)
            else:
                # Calculate time range in UTC
                now = datetime.utcnow()
                
                if unit == 'minute':
                    start_time = now - timedelta(minutes=value)
                elif unit == 'hour':
                    start_time = now - timedelta(hours=value)
                elif unit == 'day':
                    start_time = now - timedelta(days=value)
                else:
                    start_time = None
                
                fetch_data(data_viz_container, status_label, start_time=start_time, end_time=now)
        
        # Time range selector at the top of page
        with ui.card().classes('w-full mb-4 p-4 bg-gray-800'):
            ui.label("Time Range").classes("text-xl font-bold mb-2")
            
            with ui.row().classes('gap-2 flex-wrap'):
                ui.button("Last 15 Minutes", on_click=lambda: refresh_with_time_range(15, 'minute')).classes("bg-blue-500 hover:bg-blue-600 text-white font-semibold px-3 py-1 rounded")
                ui.button("Last Hour", on_click=lambda: refresh_with_time_range(1, 'hour')).classes("bg-blue-600 hover:bg-blue-700 text-white font-semibold px-3 py-1 rounded")  # Default selected
                ui.button("Last 12 Hours", on_click=lambda: refresh_with_time_range(12, 'hour')).classes("bg-blue-500 hover:bg-blue-600 text-white font-semibold px-3 py-1 rounded")
                ui.button("Last Day", on_click=lambda: refresh_with_time_range(1, 'day')).classes("bg-blue-500 hover:bg-blue-600 text-white font-semibold px-3 py-1 rounded")
                ui.button("Last Week", on_click=lambda: refresh_with_time_range(7, 'day')).classes("bg-blue-500 hover:bg-blue-600 text-white font-semibold px-3 py-1 rounded")
                ui.button("All Data", on_click=lambda: refresh_with_time_range(None, None)).classes("bg-green-500 hover:bg-green-600 text-white font-semibold px-3 py-1 rounded")
                
                # Refresh button
                ui.button("Refresh", on_click=lambda: refresh_with_time_range(1, 'hour'), icon='refresh').classes("ml-auto bg-blue-500 hover:bg-blue-600 text-white font-semibold px-3 py-1 rounded")
        
        # Data visualization container
        data_viz_container = ui.element('div').classes('w-full mt-4')
        
        # Auto-load data with last hour by default
        ui.timer(0.1, lambda: refresh_with_time_range(1, 'hour'), once=True)

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
            nav_items = {}
            
            # Function to update active button
            def update_nav_active(active_page):
                for page, btn in nav_items.items():
                    if page == active_page:
                        btn.classes('bg-blue-600')
                        btn.classes(remove='bg-gray-700 hover:bg-gray-600')
                    else:
                        btn.classes('bg-gray-700 hover:bg-gray-600')
                        btn.classes(remove='bg-blue-600')
            
            # Define navigation functions using nonlocal to access content_container
            def show_home():
                nonlocal content_container
                content_container.clear()
                create_home_content(content_container)
                update_nav_active('Home')
                
            def show_dashboard():
                nonlocal content_container
                content_container.clear()
                create_dashboard_content(content_container)
                update_nav_active('Dashboard')
            
            def show_settings():
                nonlocal content_container
                content_container.clear()
                create_settings_content(content_container)
                update_nav_active('Settings')
            
            # Home button
            home_btn = ui.button('Home', on_click=show_home).classes('w-full mb-2 text-left pl-4 py-2 bg-blue-600 rounded')
            nav_items['Home'] = home_btn
            
            # Dashboard button
            dashboard_btn = ui.button('Dashboard', on_click=show_dashboard).classes('w-full mb-2 text-left pl-4 py-2 bg-gray-700 hover:bg-gray-600 rounded')
            nav_items['Dashboard'] = dashboard_btn
            
            # Settings button
            settings_btn = ui.button('Settings', on_click=show_settings).classes('w-full mb-2 text-left pl-4 py-2 bg-gray-700 hover:bg-gray-600 rounded')
            nav_items['Settings'] = settings_btn
            
            # Bottom section of sidebar - spacer and version
            with ui.element('div').style('flex-grow: 1;'):
                ui.label("Version 1.0.0").classes("text-gray-400 text-xs text-center mt-auto")
        
        # Content area - separate from the sidebar
        with ui.element('div').classes('content-area'):
            # Create a container for the content and store it for later use
            content_container = ui.element('div')
            # Initialize with home content
            create_home_content(content_container)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(host='0.0.0.0', port=3000)