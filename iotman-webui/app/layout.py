"""
Layout module for the IoTMan web UI.
Contains functions for creating common page layouts and components.
"""
from typing import Dict, Callable, Optional, Tuple, List
from nicegui import ui
from . import design

def create_app_layout() -> Tuple[ui.element, Dict, Callable]:
    """
    Creates the main application layout with sidebar and content area.
    
    Returns:
        A tuple of (content_container, nav_items_dict, update_nav_active_function)
    """
    # Add main CSS to page
    ui.add_head_html(design.MAIN_CSS)
    
    # Store references to UI elements we'll need to access later
    content_container = None
    nav_items = {}
    sidebar_element = None
    sidebar_toggle_container = None
    is_sidebar_collapsed = False
    
    # Function to update active navigation button
    def update_nav_active(active_page: str) -> None:
        for page, btn in nav_items.items():
            if page == active_page:
                btn.classes(design.CSS_CLASSES['nav_button_active'])
                btn.classes(remove=design.CSS_CLASSES['nav_button_inactive'])
            else:
                btn.classes(design.CSS_CLASSES['nav_button_inactive'])
                btn.classes(remove=design.CSS_CLASSES['nav_button_active'])
    
    # Function to toggle sidebar collapse state
    def toggle_sidebar() -> None:
        nonlocal sidebar_toggle_container, is_sidebar_collapsed
        
        # Clear the toggle container first
        sidebar_toggle_container.clear()
        
        if is_sidebar_collapsed:
            # Reopen the sidebar
            sidebar_element.classes(remove='collapsed')
            is_sidebar_collapsed = False
            # Add the left chevron icon and "Collapse" text for expanded state
            with sidebar_toggle_container:
                ui.icon('chevron_left')
                with ui.element('span').classes('toggle-text'):
                    ui.label("Collapse")
        else:
            # Collapse the sidebar
            sidebar_element.classes('collapsed') 
            is_sidebar_collapsed = True
            # Add the right chevron icon for collapsed state
            with sidebar_toggle_container:
                ui.icon('chevron_right')
                with ui.element('span').classes('toggle-text'):
                    ui.label("Expand")
    
    # Main container using flexbox
    with ui.element('div').classes('app-container'):
        # Sidebar
        sidebar_element = ui.element('div').classes('sidebar')
        
        # Sidebar content
        with sidebar_element:
            # Logo and app name
            with ui.element('div').classes('logo-area'):
                ui.icon('bolt')
                with ui.element('span').classes('logo-text'):
                    ui.label("IoTMan")
            
            with ui.element('div').classes('sidebar-content'):
                # Navigation section
                with ui.element('div').classes(design.CSS_CLASSES['sidebar_section']):
                    # Create navigation menu items with consistent structure
                    home_btn = ui.button('', on_click=lambda: None).classes(design.CSS_CLASSES['nav_button_active'])
                    with home_btn:
                        with ui.element('div').classes('nav-content'):
                            ui.element('div').classes('nav-indicator')
                            with ui.element('div').classes('nav-icon'):
                                ui.icon('home')
                            with ui.element('div').classes('nav-text'):
                                ui.label("Home")
                    nav_items['Home'] = home_btn
                    
                    dashboard_btn = ui.button('', on_click=lambda: None).classes(design.CSS_CLASSES['nav_button_inactive'])
                    with dashboard_btn:
                        with ui.element('div').classes('nav-content'):
                            ui.element('div').classes('nav-indicator')
                            with ui.element('div').classes('nav-icon'):
                                ui.icon('dashboard')
                            with ui.element('div').classes('nav-text'):
                                ui.label("Dashboard")
                    nav_items['Dashboard'] = dashboard_btn
                    
                    settings_btn = ui.button('', on_click=lambda: None).classes(design.CSS_CLASSES['nav_button_inactive'])
                    with settings_btn:
                        with ui.element('div').classes('nav-content'):
                            ui.element('div').classes('nav-indicator')
                            with ui.element('div').classes('nav-icon'):
                                ui.icon('settings')
                            with ui.element('div').classes('nav-text'):
                                ui.label("Settings")
                    nav_items['Settings'] = settings_btn
                
                # Bottom section with version info and collapse button
                with ui.element('div').style('margin-top: auto; padding-top: 1rem;'):
                    # Add sidebar toggle button at the bottom
                    sidebar_toggle_container = ui.element('div').classes('sidebar-toggle').on('click', toggle_sidebar)
                    with sidebar_toggle_container:
                        ui.icon('chevron_left')
                        with ui.element('span').classes('toggle-text'):
                            ui.label("Collapse")
                    
                    # Version info
                    with ui.element('div').style('opacity: 0.5; text-align: center;'):
                        ui.label("Version 1.0.0").classes('text-xs')
        
        # Content area with header and body
        with ui.element('div').classes('content-area'):
            # Header section
            with ui.element('div').classes('content-header'):
                ui.label("IoT Management Dashboard").classes('text-xl font-semibold')
            
            # Main content body
            with ui.element('div').classes('content-body'):
                # Create a container for the content and store it for later use
                content_container = ui.element('div')
    
    return content_container, nav_items, update_nav_active

def create_card(title: Optional[str] = None, full_width: bool = True) -> ui.card:
    """
    Creates a styled card with an optional title.
    
    Args:
        title: Optional title to display at the top of the card
        full_width: Whether the card should take full width
        
    Returns:
        The card element
    """
    card_classes = design.CSS_CLASSES['full_width_card'] if full_width else design.CSS_CLASSES['card']
    card = ui.card().classes(card_classes)
    
    if title:
        with card:
            ui.label(title).classes(design.CSS_CLASSES['subsection_title'])
    
    return card

def create_button_row(*buttons, wrap: bool = True) -> ui.row:
    """
    Creates a row of buttons with proper spacing.
    
    Args:
        *buttons: Button elements to include
        wrap: Whether the buttons should wrap when space is limited
        
    Returns:
        The row element containing the buttons
    """
    row_classes = [design.CSS_CLASSES['flex_row'], design.CSS_CLASSES['gap_2']]
    if wrap:
        row_classes.append(design.CSS_CLASSES['flex_wrap'])
        
    row = ui.row().classes(' '.join(row_classes))
    
    for button in buttons:
        row.add(button)
        
    return row

def create_time_range_selector(callback: Callable) -> ui.card:
    """
    Creates a time range selector card with pre-defined time range buttons.
    
    Args:
        callback: Function to call when a time range is selected with signature (value, unit)
        
    Returns:
        The card element containing the time range selector
    """
    card = create_card(title="Time Range")
    
    with card:
        with ui.row().classes(f"{design.CSS_CLASSES['flex_row']} {design.CSS_CLASSES['gap_2']} {design.CSS_CLASSES['flex_wrap']}"):
            ui.button("Last 15 Minutes", 
                     on_click=lambda: callback(15, 'minute')
                    ).classes(f"{design.CSS_CLASSES['primary_button']} {design.CSS_CLASSES['small_button']}")
            
            ui.button("Last Hour", 
                     on_click=lambda: callback(1, 'hour')
                    ).classes(f"{design.CSS_CLASSES['primary_button']} {design.CSS_CLASSES['small_button']}")
            
            ui.button("Last 12 Hours", 
                     on_click=lambda: callback(12, 'hour')
                    ).classes(f"{design.CSS_CLASSES['primary_button']} {design.CSS_CLASSES['small_button']}")
            
            ui.button("Last Day", 
                     on_click=lambda: callback(1, 'day')
                    ).classes(f"{design.CSS_CLASSES['primary_button']} {design.CSS_CLASSES['small_button']}")
            
            ui.button("Last Week", 
                     on_click=lambda: callback(7, 'day')
                    ).classes(f"{design.CSS_CLASSES['primary_button']} {design.CSS_CLASSES['small_button']}")
            
            ui.button("All Data", 
                     on_click=lambda: callback(None, None)
                    ).classes(f"{design.CSS_CLASSES['success_button']} {design.CSS_CLASSES['small_button']}")
            
            # Refresh button
            ui.button("Refresh", 
                     on_click=lambda: callback(1, 'hour'), 
                     icon='refresh'
                    ).classes(f"{design.CSS_CLASSES['primary_button']} {design.CSS_CLASSES['small_button']} ml-auto")
    
    return card

def create_tabs(tabs: List[Dict[str, str]], active_tab: Optional[str] = None) -> Tuple[ui.tabs, Dict[str, ui.tab]]:
    """
    Creates a set of tabs for navigation within a page.
    
    Args:
        tabs: List of dictionaries with 'name' and 'label' keys
        active_tab: Name of the tab that should be active initially
        
    Returns:
        A tuple of (tabs_container, tab_elements_dict)
    """
    tabs_container = ui.tabs().classes('w-full')
    tab_elements = {}
    
    for tab_info in tabs:
        name = tab_info['name']
        label = tab_info['label']
        icon = tab_info.get('icon')
        
        if icon:
            tab = ui.tab(name).classes('px-4 py-2')
            with tab:
                with ui.element('div').classes('flex items-center'):
                    ui.icon(icon).classes('mr-2')
                    ui.label(label)
        else:
            tab = ui.tab(name, label).classes('px-4 py-2')
            
        tab_elements[name] = tab
    
    if active_tab and active_tab in tab_elements:
        tabs_container.set_value(active_tab)
    
    return tabs_container, tab_elements 