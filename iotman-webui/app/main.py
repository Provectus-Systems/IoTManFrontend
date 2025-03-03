import os
import requests
import json
from datetime import datetime, timedelta
from nicegui import ui
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Import our design and layout modules
from . import design
from . import layout

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
        status_label.text = f"Making request to {BACKEND_URL}/data..."
        response = requests.get(f"{BACKEND_URL}/data", params=params)
        response.raise_for_status()
        data = response.json()
        
        # Debug logging
        status_label.text = f"Received response. Status: {response.status_code}, Content length: {len(response.content)} bytes"
        
        if not data:
            status_label.text = "Error: Received empty response from server"
            return
            
        if 'items' not in data:
            status_label.text = f"Error: Response missing 'items' key. Keys received: {list(data.keys())}"
            return
            
        if not data['items']:
            status_label.text = "No data available for the selected time range."
            return
            
        # Log data details before visualization
        item_count = len(data['items'])
        battery_ids = set(item['battery_id'] for item in data['items'])
        status_label.text = f"Processing {item_count} readings from {len(battery_ids)} batteries..."
            
        # Process the data for visualization
        create_visualizations(container, data, status_label, start_time, end_time)
        
        status_label.text = f"Data loaded successfully. Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC"
    except requests.exceptions.RequestException as e:
        status_label.text = f"Network error: {str(e)}\nBackend URL: {BACKEND_URL}"
    except json.JSONDecodeError as e:
        status_label.text = f"Invalid JSON response: {str(e)}\nResponse content: {response.text[:200]}..."
    except Exception as e:
        status_label.text = f"Error fetching data: {str(e)}"
        
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
            
            for i, battery_id in enumerate(unique_batteries):
                battery_data = df[df['battery_id'] == battery_id]
                color = design.PLOT_COLORS[i % len(design.PLOT_COLORS)]
                
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
            
            # Get plot layout from design module
            title_desc = f"({len(unique_batteries)} batteries, {total_items} readings)"
            plot_layout = design.get_plot_layout("Battery Voltage Over Time" + time_range_desc, title_desc)
            fig.update_layout(**plot_layout)
            
            # Update x-axis with time selectors
            fig.update_xaxes(**design.get_time_axis_config())
            
            # Create plot
            plot = ui.plotly(fig).classes('w-full h-96 mt-4')
            
            # Create summary stats card
            with layout.create_card("Battery Summary"):
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
        ui.label("Welcome to IoTMan").classes(design.CSS_CLASSES['page_title'])
        ui.label("A simple IoT management dashboard").classes("text-xl mb-6")
        
        # Feature highlights
        with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-4 mb-6'):
            with layout.create_card(full_width=False):
                ui.icon('speed', size='xl').classes('mb-2 text-blue-500')
                ui.label("Real-time Monitoring").classes('text-lg font-semibold mb-2')
                ui.label("Monitor your IoT devices in real-time with automatic data refresh.").classes('text-gray-600')
                
            with layout.create_card(full_width=False):
                ui.icon('notifications', size='xl').classes('mb-2 text-green-500')
                ui.label("Alerts & Notifications").classes('text-lg font-semibold mb-2')
                ui.label("Set up custom alerts to be notified when values exceed thresholds.").classes('text-gray-600')
                
            with layout.create_card(full_width=False):
                ui.icon('trending_up', size='xl').classes('mb-2 text-purple-500')
                ui.label("Data Analytics").classes('text-lg font-semibold mb-2')
                ui.label("Analyze historical data to identify patterns and trends.").classes('text-gray-600')

        with layout.create_card("Getting Started"):
            ui.label("Use the sidebar to navigate between different sections:").classes("mb-2")
            
            with ui.element('div').classes('pl-4'):
                with ui.element('div').classes('flex items-center mb-2'):
                    ui.icon('home', size='sm').classes('mr-2 text-indigo-500')
                    ui.label("Home: This welcome page").classes('text-gray-700')
                
                with ui.element('div').classes('flex items-center mb-2'):
                    ui.icon('dashboard', size='sm').classes('mr-2 text-indigo-500')
                    ui.label("Dashboard: View the latest IoT device logs").classes('text-gray-700')
                
                with ui.element('div').classes('flex items-center mb-2'):
                    ui.icon('settings', size='sm').classes('mr-2 text-indigo-500')
                    ui.label("Settings: Configure your dashboard preferences").classes('text-gray-700')

def create_dashboard_content(container):
    with container:
        # Create tabs for different dashboard views
        tabs, tab_elements = layout.create_tabs([
            {'name': 'overview', 'label': 'Overview', 'icon': 'dashboard'},
            {'name': 'devices', 'label': 'Devices', 'icon': 'devices'},
            {'name': 'analytics', 'label': 'Analytics', 'icon': 'analytics'}
        ], active_tab='overview')
        
        # Tab content containers
        overview_container = ui.element('div').classes('mt-4')
        devices_container = ui.element('div').classes('mt-4')
        analytics_container = ui.element('div').classes('mt-4')
        
        # Function to switch tab content
        def switch_tab(e):
            tab_name = e.value
            overview_container.set_visibility(tab_name == 'overview')
            devices_container.set_visibility(tab_name == 'devices')
            analytics_container.set_visibility(tab_name == 'analytics')
        
        tabs.on('value_change', switch_tab)
        
        # Initial visibility
        devices_container.set_visibility(False)
        analytics_container.set_visibility(False)
        
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
        
        # Overview Tab Content
        with overview_container:
            # Time range selector
            layout.create_time_range_selector(refresh_with_time_range)
            
            # Data visualization container
            data_viz_container = ui.element('div').classes('w-full mt-4')
            
            # Auto-load data with last hour by default
            ui.timer(0.1, lambda: refresh_with_time_range(1, 'hour'), once=True)
        
        # Devices Tab Content
        with devices_container:
            ui.label("Device Management").classes(design.CSS_CLASSES['page_title'])
            
            with layout.create_card("Connected Devices"):
                ui.label("This feature is coming soon").classes("text-gray-500 italic")
        
        # Analytics Tab Content
        with analytics_container:
            ui.label("Data Analytics").classes(design.CSS_CLASSES['page_title'])
            
            with layout.create_card("Historical Analysis"):
                ui.label("This feature is coming soon").classes("text-gray-500 italic")

def create_settings_content(container):
    with container:
        ui.label("Dashboard Settings").classes(design.CSS_CLASSES['page_title'])
        
        # Create tabs for different settings categories
        tabs, tab_elements = layout.create_tabs([
            {'name': 'general', 'label': 'General', 'icon': 'tune'},
            {'name': 'notifications', 'label': 'Notifications', 'icon': 'notifications'},
            {'name': 'advanced', 'label': 'Advanced', 'icon': 'code'}
        ], active_tab='general')
        
        # Tab content containers
        general_container = ui.element('div').classes('mt-4')
        notifications_container = ui.element('div').classes('mt-4')
        advanced_container = ui.element('div').classes('mt-4')
        
        # Function to switch tab content
        def switch_tab(e):
            tab_name = e.value
            general_container.set_visibility(tab_name == 'general')
            notifications_container.set_visibility(tab_name == 'notifications')
            advanced_container.set_visibility(tab_name == 'advanced')
        
        tabs.on('value_change', switch_tab)
        
        # Initial visibility
        notifications_container.set_visibility(False)
        advanced_container.set_visibility(False)
        
        # General Settings Tab
        with general_container:
            with layout.create_card("Theme Preferences"):
                dark_mode = ui.switch("Dark Mode", value=True).classes("mb-4")
                
                ui.label("Refresh Interval").classes("text-lg mb-2")
                interval = ui.slider(min=5, max=60, value=30, step=5).classes("mb-4")
                ui.label().bind_text_from(interval, 'value', lambda v: f'Refresh every {v} seconds')
            
                ui.button("Save Settings").classes(design.CSS_CLASSES['primary_button'])
        
        # Notifications Tab
        with notifications_container:
            with layout.create_card("Notification Settings"):
                ui.checkbox("Enable alert sounds").classes("mb-2")
                ui.checkbox("Show desktop notifications").classes("mb-2")
                ui.checkbox("Email critical alerts").classes("mb-2")
                
                ui.button("Save Settings").classes(design.CSS_CLASSES['primary_button'])
        
        # Advanced Tab
        with advanced_container:
            with layout.create_card("Advanced Options"):
                ui.button("Reset to Defaults").classes(design.CSS_CLASSES['danger_button'])
                ui.button("Export Configuration").classes(design.CSS_CLASSES['success_button'] + " ml-2")

@ui.page("/")
def main_page():
    # Create app layout using our layout module
    content_container, nav_items, update_nav_active = layout.create_app_layout()
    
    # Define navigation functions
    def show_home():
        content_container.clear()
        create_home_content(content_container)
        update_nav_active('Home')
        
    def show_dashboard():
        content_container.clear()
        create_dashboard_content(content_container)
        update_nav_active('Dashboard')
    
    def show_settings():
        content_container.clear()
        create_settings_content(content_container)
        update_nav_active('Settings')
    
    # Set button click handlers
    nav_items['Home'].on_click(show_home)
    nav_items['Dashboard'].on_click(show_dashboard)
    nav_items['Settings'].on_click(show_settings)
    
    # Initialize with home content
    show_home()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(host='0.0.0.0', port=3000)