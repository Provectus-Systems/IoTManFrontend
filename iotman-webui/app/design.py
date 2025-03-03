"""
Design module for the IoTMan web UI.
Contains color schemes, CSS styles, and layout configurations.
"""

# Color schemes
COLOR_SCHEME = {
    'primary': '#2563eb',
    'primary_light': '#3b82f6',
    'primary_dark': '#1d4ed8',
    'secondary': '#4b5563',
    'secondary_light': '#6b7280',
    'secondary_dark': '#374151',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'background': '#f8fafc',
    'card': '#ffffff',
    'text': '#1e293b',
    'text_light': '#64748b',
    'border': '#e2e8f0',
    'chart_bg': '#ffffff',
    'chart_grid': 'rgba(226, 232, 240, 0.6)',
    'chart_line': 'rgba(148, 163, 184, 0.8)',
    'sidebar_bg': '#2e1065',  # Dark purple background
    'sidebar_text': '#f8fafc', # White text
    'sidebar_active': 'rgba(255, 255, 255, 0.1)'  # Translucent white for active item
}

# Colors for plots and visualizations
PLOT_COLORS = [
    '#2563eb',  # primary
    '#10b981',  # success
    '#f59e0b',  # warning
    '#ef4444',  # danger
    '#8b5cf6',  # purple
    '#06b6d4',  # cyan
    '#f97316',  # orange
    '#ec4899',  # pink
    '#14b8a6',  # teal
    '#6366f1',  # indigo
]

# Responsive breakpoints
BREAKPOINTS = {
    'sm': '640px',
    'md': '768px',
    'lg': '1024px',
    'xl': '1280px',
    '2xl': '1536px',
}

# Sizing variables
SIZES = {
    'sidebar_width': '240px',
    'sidebar_collapsed_width': '60px',
    'header_height': '60px',
}

# CSS classes for common UI components
CSS_CLASSES = {
    # Layout
    'full_width': 'w-full',
    'container': 'container mx-auto px-4',
    
    # Flexbox
    'flex_row': 'flex flex-row',
    'flex_col': 'flex flex-col',
    'flex_wrap': 'flex-wrap',
    'items_center': 'items-center',
    'justify_center': 'justify-center',
    'justify_between': 'justify-between',
    'justify_end': 'justify-end',
    'gap_2': 'gap-2',
    'gap_4': 'gap-4',
    
    # Spacing
    'p_2': 'p-2',
    'p_4': 'p-4',
    'py_2': 'py-2',
    'px_4': 'px-4',
    'mb_4': 'mb-4',
    'mt_2': 'mt-2',
    'ml_auto': 'ml-auto',
    
    # Cards
    'card': 'bg-white rounded-lg shadow-sm p-4 border border-gray-100',
    'full_width_card': 'w-full bg-white rounded-lg shadow-sm p-4 border border-gray-100',
    
    # Navigation
    'sidebar_header': 'text-xs font-bold text-gray-400 px-3 py-2 uppercase tracking-wide',
    'sidebar_section': 'flex flex-col w-full',
    'nav_button_active': 'w-full transition-all duration-200',
    'nav_button_inactive': 'w-full transition-all duration-200',
    
    # Buttons
    'primary_button': 'px-4 py-2 bg-primary text-white rounded hover:bg-primary-dark transition-colors',
    'secondary_button': 'px-4 py-2 bg-secondary text-white rounded hover:bg-secondary-dark transition-colors',
    'success_button': 'px-4 py-2 bg-success text-white rounded hover:bg-success-dark transition-colors',
    'danger_button': 'px-4 py-2 bg-danger text-white rounded hover:bg-danger-dark transition-colors',
    'small_button': 'px-3 py-1 text-sm',
    
    # Typography
    'page_title': 'text-2xl font-bold mb-4',
    'section_title': 'text-xl font-semibold mb-2',
    'subsection_title': 'text-lg font-medium mb-2',
    'text_faded': 'text-gray-500',
    'text_sm': 'text-sm',
    'text_xs': 'text-xs',
    
    # Forms
    'form_label': 'block text-sm font-medium text-gray-700 mb-1',
    'form_input': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
    'form_error': 'text-sm text-danger mt-1',
    
    # Misc
    'badge': 'px-2 py-1 text-xs rounded-full',
    'divider': 'border-t border-gray-200 my-4',
}

# Main CSS for the application
MAIN_CSS = """
<style>
/* Reset and base styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: var(--text);
  background-color: var(--background);
  line-height: 1.5;
  height: 100vh;
  overflow: hidden;
}

/* CSS Variables for colors and sizes */
:root {
  --primary: """ + COLOR_SCHEME['primary'] + """;
  --primary-light: """ + COLOR_SCHEME['primary_light'] + """;
  --primary-dark: """ + COLOR_SCHEME['primary_dark'] + """;
  --secondary: """ + COLOR_SCHEME['secondary'] + """;
  --secondary-light: """ + COLOR_SCHEME['secondary_light'] + """;
  --secondary-dark: """ + COLOR_SCHEME['secondary_dark'] + """;
  --success: """ + COLOR_SCHEME['success'] + """;
  --warning: """ + COLOR_SCHEME['warning'] + """;
  --danger: """ + COLOR_SCHEME['danger'] + """;
  --background: """ + COLOR_SCHEME['background'] + """;
  --card: """ + COLOR_SCHEME['card'] + """;
  --text: """ + COLOR_SCHEME['text'] + """;
  --text-light: """ + COLOR_SCHEME['text_light'] + """;
  --border: """ + COLOR_SCHEME['border'] + """;
  --sidebar-bg: """ + COLOR_SCHEME['sidebar_bg'] + """;
  --sidebar-text: """ + COLOR_SCHEME['sidebar_text'] + """;
  --sidebar-active: """ + COLOR_SCHEME['sidebar_active'] + """;
  
  --sidebar-width: """ + SIZES['sidebar_width'] + """;
  --sidebar-collapsed-width: """ + SIZES['sidebar_collapsed_width'] + """;
  --header-height: """ + SIZES['header_height'] + """;
}

/* Main layout */
.app-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* Sidebar */
.sidebar {
  display: flex;
  flex-direction: column;
  background-color: var(--sidebar-bg);
  width: var(--sidebar-width);
  height: 100%;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  color: var(--sidebar-text);
  position: relative;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

/* Fixed icon column */
.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: var(--sidebar-collapsed-width);
  height: 100%;
  background-color: rgba(0, 0, 0, 0.15);
  z-index: 0;
}

.logo-area {
  display: flex;
  position: relative;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  height: var(--header-height);
  z-index: 1;
}

.logo-area i {
  font-size: 1.5rem;
  color: var(--sidebar-text);
  position: absolute;
  left: calc(var(--sidebar-collapsed-width) / 2 - 12px);
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
}

.logo-text {
  position: absolute;
  left: var(--sidebar-collapsed-width);
  top: 50%;
  transform: translateY(-50%);
  transition: opacity 0.3s ease, visibility 0.3s ease;
  white-space: nowrap;
  padding-left: 8px;
}

.sidebar.collapsed .logo-text {
  opacity: 0;
  visibility: hidden;
}

.sidebar-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 1rem 0;
  overflow-y: auto;
  position: relative;
  z-index: 1;
}

/* Navigation Buttons */
button.nav-button-active,
button.nav-button-inactive {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  background: none !important;
  padding: 0 !important;
  min-height: 42px !important;
  margin: 2px 0 !important;
  text-align: left !important;
  width: 100% !important;
  overflow: visible !important;
  transition: all 0.3s ease !important;
  position: relative !important;
}

.nav-icon {
  position: absolute !important;
  left: calc(var(--sidebar-collapsed-width) / 2 - 12px) !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  width: 24px !important;
  height: 24px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 2 !important;
}

.nav-icon i {
  font-size: 1.25rem !important;
  opacity: 0.9 !important;
  position: relative !important;
}

button.nav-button-active .nav-icon i {
  opacity: 1;
}

.nav-content {
  position: relative;
  height: 100%;
  width: 100%;
  display: flex;
}

.nav-indicator {
  position: absolute;
  left: 0;
  top: 12px;
  bottom: 12px;
  width: 3px;
  background-color: transparent;
  transition: background-color 0.2s ease;
}

button.nav-button-active .nav-indicator {
  background-color: rgba(255, 255, 255, 0.8);
}

button.nav-button-inactive:hover .nav-indicator {
  background-color: rgba(255, 255, 255, 0.2);
}

.nav-text {
  position: absolute;
  left: var(--sidebar-collapsed-width);
  top: 50%;
  transform: translateY(-50%);
  transition: opacity 0.3s ease, visibility 0.3s ease;
  white-space: nowrap;
  padding-left: 8px;
}

.nav-text span {
  font-size: 0.95rem !important;
  white-space: nowrap !important;
}

button.nav-button-active .nav-text span {
  color: white !important;
}

button.nav-button-inactive .nav-text span {
  color: rgba(255, 255, 255, 0.6) !important;
}

button.nav-button-inactive:hover .nav-text span {
  color: rgba(255, 255, 255, 0.8) !important;
}

.sidebar.collapsed .nav-text {
  opacity: 0;
  visibility: hidden;
}

/* Sidebar toggle button */
.sidebar-toggle {
  display: flex;
  align-items: center;
  position: relative;
  margin: 0 auto;
  margin-top: auto;
  width: 75%;
  height: 38px;
  cursor: pointer;
  color: var(--sidebar-text);
  border-radius: 0.25rem;
  background-color: rgba(255, 255, 255, 0.1);
  z-index: 1;
}

.sidebar-toggle:hover {
  background-color: rgba(255, 255, 255, 0.15);
}

.sidebar-toggle i {
  position: absolute;
  left: calc(var(--sidebar-collapsed-width) / 2 - 12px);
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.25rem;
  z-index: 2;
}

.sidebar-toggle .toggle-text {
  position: absolute;
  left: var(--sidebar-collapsed-width);
  transform: translateY(-50%);
  top: 50%;
  transition: opacity 0.3s ease, visibility 0.3s ease;
  white-space: nowrap;
  padding-left: 8px;
  font-size: 0.9rem;
}

.sidebar.collapsed .sidebar-toggle .toggle-text {
  opacity: 0;
  visibility: hidden;
}

/* Content area */
.content-area {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.content-header {
  height: var(--header-height);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  background-color: var(--card);
}

.content-body {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  background-color: var(--background);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    z-index: 100;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  }
  
  .sidebar.collapsed {
    transform: translateX(-100%);
  }
}

/* Override NiceGUI default styles */
.nicegui-content {
  max-width: 100% !important;
  padding: 0 !important;
  height: 100vh !important;
  background-color: var(--background) !important;
}

/* Card Styles */
.card {
  background-color: var(--card);
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* Plot container styles */
.plot-container {
  height: 300px;
  width: 100%;
}

.plot-container > div {
  width: 100% !important;
  height: 100% !important;
}

/* Remove range slider from plot axis */
.plot-container .modebar-group:last-child {
  display: none !important;
}

/* Grid layout for dashboard */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1rem;
  width: 100%;
}

.grid-container > div {
  min-height: 200px;
}

@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: 1fr;
  }
}
</style>
"""

# Plot layout defaults
def get_plot_layout(title: str, title_desc: str = None) -> dict:
    """
    Returns a default plot layout with the IoTMan styling.
    
    Args:
        title: The main title for the plot
        title_desc: Optional descriptive subtitle
    
    Returns:
        Dictionary with plot layout configuration
    """
    full_title = title
    if title_desc:
        full_title = f"{title}<br>{title_desc}"
        
    return {
        'title': full_title,
        'title_font_size': 24,
        'title_x': 0.5,  # Center the title
        'plot_bgcolor': COLOR_SCHEME['chart_bg'],
        'paper_bgcolor': COLOR_SCHEME['chart_bg'],
        'font': dict(color=COLOR_SCHEME['text']),
        'legend': dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        'margin': dict(l=20, r=20, t=80, b=20),
        'xaxis': dict(
            title="Time (UTC)",
            gridcolor=COLOR_SCHEME['chart_grid'],
            showline=True,
            linecolor=COLOR_SCHEME['chart_line'],
            tickfont=dict(size=12),
        ),
        'yaxis': dict(
            title="Voltage (V)",
            gridcolor=COLOR_SCHEME['chart_grid'],
            showline=True,
            linecolor=COLOR_SCHEME['chart_line'],
            tickfont=dict(size=12),
            ticksuffix=' V',
        ),
        'hovermode': "x unified",
    }

# Standard plot axis configuration - without the date range selector
def get_time_axis_config() -> dict:
    """
    Returns the standard time axis configuration without range selectors.
    
    Returns:
        Dictionary with axis configuration
    """
    return {
        'rangeslider_visible': False,  # Remove the range slider
    } 