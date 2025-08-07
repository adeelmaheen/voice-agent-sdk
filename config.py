"""
Configuration settings for the Voice Agent Streamlit App
"""

# App Configuration
APP_CONFIG = {
    "title": "Voice Agent Assistant",
    "icon": "🎤",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Audio Configuration
AUDIO_CONFIG = {
    "sample_rate": 24000,
    "channels": 1,
    "dtype": "int16",
    "default_duration": 5,  # seconds
    "min_duration": 3,
    "max_duration": 10
}

# Agent Configuration
AGENTS = {
    "Weather Agent": {
        "description": "Get weather information and general assistance",
        "icon": "🌤️",
        "color": "#667eea"
    },
    "Spanish Agent": {
        "description": "Conversation in Spanish",
        "icon": "🇪🇸",
        "color": "#48dbfb"
    },
    "Urdu Agent": {
        "description": "Conversation in Urdu",
        "icon": "🇵🇰",
        "color": "#ff6b6b"
    }
}

# UI Colors
COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2",
    "success": "#48dbfb",
    "warning": "#feca57",
    "error": "#ff6b6b",
    "background": "#f8f9fa"
}

# CSS Styles
CSS_STYLES = """
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .agent-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.75rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: right;
        max-width: 80%;
        margin-left: auto;
    }
    
    .agent-message {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 0.75rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-recording {
        background-color: #ff6b6b;
        animation: pulse 1.5s infinite;
    }
    
    .status-processing {
        background-color: #feca57;
        animation: pulse 1.5s infinite;
    }
    
    .status-ready {
        background-color: #48dbfb;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
""" 