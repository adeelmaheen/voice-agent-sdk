# import streamlit as st
# import asyncio
# import numpy as np
# import sounddevice as sd
# import os
# import tempfile
# import io
# from pydub import AudioSegment
# from pydub.playback import play
# import threading
# import time
# from dotenv import load_dotenv
# import json
# import scipy.io.wavfile as wavfile

# # Import your existing modules
# from agents.voice import AudioInput, SingleAgentVoiceWorkflow, VoicePipeline
# from agents_setup import agent, spanish_agent
# from tools import fetch_weather
# from config import APP_CONFIG, AUDIO_CONFIG, AGENTS, CSS_STYLES

# # Load environment variables
# load_dotenv()

# # Page configuration
# st.set_page_config(
#     page_title=APP_CONFIG["title"],
#     page_icon=APP_CONFIG["icon"],
#     layout=APP_CONFIG["layout"],
#     initial_sidebar_state=APP_CONFIG["initial_sidebar_state"]
# )

# # Apply custom CSS
# st.markdown(CSS_STYLES, unsafe_allow_html=True)

# # Initialize session state
# if 'api_key' not in st.session_state:
#     st.session_state.api_key = ""
# if 'selected_agent' not in st.session_state:
#     st.session_state.selected_agent = "Weather Agent"
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
# if 'is_recording' not in st.session_state:
#     st.session_state.is_recording = False
# if 'is_processing' not in st.session_state:
#     st.session_state.is_processing = False

# def setup_agents():
#     """Setup agents with the provided API key"""
#     os.environ["OPENAI_API_KEY"] = st.session_state.api_key
    
#     # Create weather agent
#     weather_agent = agent  # This already has weather tools
    
#     # Create Urdu agent
#     urdu_agent = type(agent)(
#         name="UrduAgent",
#         handoff_description="Handles Urdu conversations.",
#         instructions="You are a polite assistant who always replies in Urdu. Be helpful and conversational.",
#         model="gpt-4o",
#     )
    
#     return {
#         "Weather Agent": weather_agent,
#         "Spanish Agent": spanish_agent,
#         "Urdu Agent": urdu_agent
#     }

# def record_audio(duration=AUDIO_CONFIG["default_duration"]):
#     """Record audio from microphone"""
#     samplerate = AUDIO_CONFIG["sample_rate"]
#     audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=AUDIO_CONFIG["channels"], dtype=np.int16)
#     sd.wait()
#     return audio.flatten(), samplerate

# async def process_voice_input(audio_data, selected_agent):
#     """Process voice input and get agent response"""
#     try:
#         pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(selected_agent))
#         audio_input = AudioInput(buffer=audio_data)
#         result = await pipeline.run(audio_input)
        
#         # Collect the response
#         response_audio = []
#         response_text = ""
        
#         async for event in result.stream():
#             if event.type == "voice_stream_event_audio":
#                 response_audio.append(event.data)
#             elif event.type == "voice_stream_event_text":
#                 response_text += event.text
        
#         return response_text, np.concatenate(response_audio) if response_audio else None
        
#     except Exception as e:
#         return f"Error processing voice input: {str(e)}", None

# def create_audio_player(audio_data, sample_rate):
#     """Create audio player for response audio"""
#     if audio_data is None:
#         return None
    
#     try:
#         # Normalize audio data to 16-bit range
#         if isinstance(audio_data, np.ndarray):
#             if audio_data.dtype != np.int16:
#                 # Normalize to 16-bit range
#                 max_val = np.max(np.abs(audio_data))
#                 if max_val > 0:
#                     audio_normalized = np.int16(audio_data * 32767 / max_val)
#                 else:
#                     audio_normalized = np.int16(audio_data)
#             else:
#                 audio_normalized = audio_data
            
#             # Create a temporary WAV file in memory
#             buffer = io.BytesIO()
#             wavfile.write(buffer, sample_rate, audio_normalized)
#             buffer.seek(0)
            
#             return buffer
            
#     except Exception as e:
#         st.warning(f"Audio processing error: {str(e)}")
#         return None

# def main():
#     # Header
#     st.markdown("""
#     <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem; color: white; text-align: center;">
#         <h1>🎤 Voice Agent Assistant</h1>
#         <p>Your AI-powered voice conversation partner</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Sidebar for API key and agent selection
#     with st.sidebar:
#         st.markdown("### 🔑 Setup")
        
#         # API Key input
#         api_key = st.text_input(
#             "OpenAI API Key",
#             type="password",
#             placeholder="sk-...",
#             value=st.session_state.api_key,
#             help="Enter your OpenAI API key to start using the voice agents"
#         )
        
#         if api_key:
#             st.session_state.api_key = api_key
#             st.success("✅ API Key configured")
        
#         st.markdown("### 🤖 Select Agent")
        
#         # Agent selection
#         selected_agent_name = st.selectbox(
#             "Choose your agent:",
#             list(AGENTS.keys()),
#             index=list(AGENTS.keys()).index(st.session_state.selected_agent)
#         )
        
#         st.session_state.selected_agent = selected_agent_name
        
#         # Agent description with icon
#         agent_info = AGENTS[selected_agent_name]
#         st.info(f"{agent_info['icon']} **{selected_agent_name}**: {agent_info['description']}")
        
#         # Status indicator
#         st.markdown("### 📊 Status")
#         if st.session_state.is_recording:
#             st.markdown("🔴 Recording...")
#         elif st.session_state.is_processing:
#             st.markdown("🟡 Processing...")
#         else:
#             st.markdown("🟢 Ready")
    
#     # Main content area
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.markdown("### 💬 Conversation")
        
#         # Chat history display
#         for message in st.session_state.chat_history:
#             if message["type"] == "user":
#                 st.markdown(f'<div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 0.75rem; border-radius: 10px; margin: 0.5rem 0; text-align: right; max-width: 80%; margin-left: auto;">🎤 You: {message["text"]}</div>', unsafe_allow_html=True)
#             else:
#                 st.markdown(f'<div style="background: white; border: 1px solid #e0e0e0; padding: 0.75rem; border-radius: 10px; margin: 0.5rem 0; max-width: 80%;">🤖 {message["agent"]}: {message["text"]}</div>', unsafe_allow_html=True)
                
#                 # Display audio player if available
#                 if "audio_data" in message and message["audio_data"] is not None:
#                     audio_buffer = create_audio_player(message["audio_data"], message.get("sample_rate", 44100))
#                     if audio_buffer:
#                         st.audio(audio_buffer, format="audio/wav")
    
#     with col2:
#         st.markdown("### 📋 Instructions")
#         st.markdown("""
#         1. **Enter your OpenAI API key** in the sidebar
#         2. **Select an agent** from the dropdown
#         3. **Click "Start Recording"** to begin voice interaction
#         4. **Speak clearly** into your microphone
#         5. **Wait for the AI response** in voice and text
        
#         **Available Agents:**
#         - **Weather Agent**: Get weather info and general help
#         - **Spanish Agent**: Spanish conversations
#         - **Urdu Agent**: Urdu conversations
#         """)
        
#         st.markdown("### ⚙️ Settings")
#         recording_duration = st.slider(
#             "Recording Duration (seconds)", 
#             AUDIO_CONFIG["min_duration"], 
#             AUDIO_CONFIG["max_duration"], 
#             AUDIO_CONFIG["default_duration"]
#         )
        
#         # Recording controls
#         st.markdown("### 🎙️ Controls")
        
#         # Check if API key is provided
#         if not api_key:
#             st.warning("⚠️ Please enter your OpenAI API key first!")
#             record_button_disabled = True
#         elif st.session_state.is_recording or st.session_state.is_processing:
#             record_button_disabled = True
#         else:
#             record_button_disabled = False
        
#         if st.button("🎤 Start Recording", disabled=record_button_disabled, use_container_width=True):
#             st.session_state.is_recording = True
#             st.rerun()
        
#         if st.button("🗑️ Clear Chat", use_container_width=True):
#             st.session_state.chat_history = []
#             st.rerun()
    
#     # Handle recording and processing
#     if st.session_state.is_recording and api_key:
#         try:
#             # Setup agents
#             agents = setup_agents()
#             selected_agent = agents[st.session_state.selected_agent]
            
#             # Record audio
#             with st.spinner("🎤 Recording..."):
#                 audio_data, samplerate = record_audio(recording_duration)
            
#             st.session_state.is_recording = False
#             st.session_state.is_processing = True
            
#             # Add user message to chat
#             st.session_state.chat_history.append({
#                 "type": "user",
#                 "text": "🎤 Voice message",
#                 "agent": "User"
#             })
            
#             # Process with agent
#             with st.spinner("🤖 Processing..."):
#                 # Run the async function
#                 loop = asyncio.new_event_loop()
#                 asyncio.set_event_loop(loop)
#                 try:
#                     response_text, response_audio = loop.run_until_complete(
#                         process_voice_input(audio_data, selected_agent)
#                     )
#                 finally:
#                     loop.close()
            
#             # Add agent response to chat with audio
#             st.session_state.chat_history.append({
#                 "type": "agent",
#                 "text": response_text,
#                 "agent": st.session_state.selected_agent,
#                 "audio_data": response_audio,  # Store audio data
#                 "sample_rate": samplerate
#             })

#             st.session_state.is_processing = False
#             st.success("✅ Response received!")
#             st.rerun()
            
#         except Exception as e:
#             st.error(f"Error: {str(e)}")
#             st.session_state.is_recording = False
#             st.session_state.is_processing = False

# if __name__ == "__main__":
#     main()


import streamlit as st
import asyncio
import numpy as np
import os
import io
import scipy.io.wavfile as wavfile
from audio_recorder_streamlit import audio_recorder
from dotenv import load_dotenv

# Import your existing modules
from agents.voice import AudioInput, SingleAgentVoiceWorkflow, VoicePipeline
from agents_setup import agent, spanish_agent
from tools import fetch_weather
from config import APP_CONFIG, AUDIO_CONFIG, AGENTS, CSS_STYLES

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Voice Agent Assistant",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CSS_STYLES, unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'selected_agent' not in st.session_state:
    st.session_state.selected_agent = "Weather Agent"
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False
if 'last_audio_bytes' not in st.session_state:
    st.session_state.last_audio_bytes = None

def setup_agents():
    """Setup agents with the provided API key"""
    os.environ["OPENAI_API_KEY"] = st.session_state.api_key
    
    # Create weather agent
    weather_agent = agent
    
    # Create Urdu agent
    urdu_agent = type(agent)(
        name="UrduAgent",
        handoff_description="Handles Urdu conversations.",
        instructions="You are a polite assistant who always replies in Urdu. Be helpful and conversational.",
        model="gpt-4o",
    )
    
    return {
        "Weather Agent": weather_agent,
        "Spanish Agent": spanish_agent,
        "Urdu Agent": urdu_agent
    }

def convert_audio_bytes_to_numpy(audio_bytes):
    """Convert audio bytes to numpy array"""
    try:
        # Create BytesIO object from bytes
        audio_io = io.BytesIO(audio_bytes)
        
        # Read the WAV file
        sample_rate, audio_data = wavfile.read(audio_io)
        
        # Convert to float32 and normalize
        if audio_data.dtype == np.int16:
            audio_data = audio_data.astype(np.float32) / 32768.0
        elif audio_data.dtype == np.int32:
            audio_data = audio_data.astype(np.float32) / 2147483648.0
        
        # Handle stereo by taking the first channel
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]
            
        return audio_data, sample_rate
        
    except Exception as e:
        st.error(f"Error converting audio: {str(e)}")
        return None, None

async def process_voice_input(audio_data, selected_agent):
    """Process voice input and get agent response"""
    try:
        pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(selected_agent))
        audio_input = AudioInput(buffer=audio_data)
        result = await pipeline.run(audio_input)
        
        # Collect the response
        response_audio = []
        response_text = ""
        
        async for event in result.stream():
            if event.type == "voice_stream_event_audio":
                response_audio.append(event.data)
            elif event.type == "voice_stream_event_text":
                response_text += event.text
        
        return response_text, np.concatenate(response_audio) if response_audio else None
        
    except Exception as e:
        return f"Error processing voice input: {str(e)}", None

def create_audio_player(audio_data, sample_rate=44100):
    """Create audio player for response audio"""
    if audio_data is None:
        return None
    
    try:
        # Normalize audio data to 16-bit range
        if isinstance(audio_data, np.ndarray):
            if audio_data.dtype != np.int16:
                max_val = np.max(np.abs(audio_data))
                if max_val > 0:
                    audio_normalized = np.int16(audio_data * 32767 / max_val)
                else:
                    audio_normalized = np.int16(audio_data)
            else:
                audio_normalized = audio_data
            
            # Create WAV file in memory
            buffer = io.BytesIO()
            wavfile.write(buffer, sample_rate, audio_normalized)
            buffer.seek(0)
            return buffer
            
    except Exception as e:
        st.warning(f"Audio processing error: {str(e)}")
        return None

def main():
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem; color: white; text-align: center;">
        <h1>🎤 Voice Agent Assistant</h1>
        <p>Record your voice and chat with AI agents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔑 Setup")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            value=st.session_state.api_key,
            help="Enter your OpenAI API key"
        )
        
        if api_key:
            st.session_state.api_key = api_key
            st.success("✅ API Key configured")
        
        st.markdown("### 🤖 Select Agent")
        
        # Agent selection
        selected_agent_name = st.selectbox(
            "Choose your agent:",
            list(AGENTS.keys()),
            index=list(AGENTS.keys()).index(st.session_state.selected_agent)
        )
        
        st.session_state.selected_agent = selected_agent_name
        
        # Agent description
        agent_info = AGENTS[selected_agent_name]
        st.info(f"{agent_info['icon']} **{selected_agent_name}**: {agent_info['description']}")
        
        st.markdown("### 🎙️ Voice Recording")
        
        # Audio recorder component
        audio_bytes = audio_recorder(
            text="Click to record",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_name="microphone-lines",
            icon_size="6x",
            pause_threshold=2.0,
            sample_rate=44100,
        )
        
        # Status indicator
        if st.session_state.is_processing:
            st.warning("🟡 Processing your message...")
        else:
            st.success("🟢 Ready to record!")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Conversation")
        
        # Chat history display
        if not st.session_state.chat_history:
            st.info("👋 Start a conversation by recording your voice!")
        
        for message in st.session_state.chat_history:
            if message["type"] == "user":
                st.markdown(f'<div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 0.75rem; border-radius: 10px; margin: 0.5rem 0; text-align: right; max-width: 80%; margin-left: auto;">🎤 You: {message["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background: white; border: 1px solid #e0e0e0; padding: 0.75rem; border-radius: 10px; margin: 0.5rem 0; max-width: 80%;">🤖 {message["agent"]}: {message["text"]}</div>', unsafe_allow_html=True)
                
                # Display audio player if available
                if "audio_data" in message and message["audio_data"] is not None:
                    audio_buffer = create_audio_player(message["audio_data"], message.get("sample_rate", 44100))
                    if audio_buffer:
                        st.audio(audio_buffer, format="audio/wav")
    
    with col2:
        st.markdown("### 📋 How to Use")
        st.markdown("""
        **Simple Steps:**
        1. 🔑 Enter your OpenAI API key
        2. 🤖 Select an agent
        3. 🎤 Click the microphone to record
        4. 🗣️ Speak your message
        5. 🎤 Click again to stop recording
        6. 🤖 Wait for AI response!
        
        **Available Agents:**
        - 🌤️ **Weather Agent**: Weather info & general help
        - 🇪🇸 **Spanish Agent**: Spanish conversations  
        - 🇵🇰 **Urdu Agent**: اردو میں گفتگو
        """)
        
        st.markdown("### ⚙️ Tips")
        st.markdown("""
        - 🎯 Speak clearly and at normal pace
        - 🔇 Make sure your microphone works
        - ⏸️ Recording stops after 2 seconds of silence
        - 📱 Works on mobile devices too!
        - 🌍 Try different languages with different agents
        """)
        
        # Display current recording if available
        if audio_bytes and audio_bytes != st.session_state.last_audio_bytes:
            st.success("✅ New recording received!")
            
            # Play back the recorded audio
            st.audio(audio_bytes, format="audio/wav")
            
            # Process the audio if API key is provided
            if st.session_state.api_key and not st.session_state.is_processing:
                st.session_state.is_processing = True
                st.session_state.last_audio_bytes = audio_bytes
                
                try:
                    # Convert audio to numpy array
                    with st.spinner("🎵 Converting audio..."):
                        audio_data, sample_rate = convert_audio_bytes_to_numpy(audio_bytes)
                    
                    if audio_data is not None:
                        # Setup agents
                        agents = setup_agents()
                        selected_agent = agents[st.session_state.selected_agent]
                        
                        # Add user message to chat
                        st.session_state.chat_history.append({
                            "type": "user",
                            "text": "🎤 Voice message",
                            "agent": "User"
                        })
                        
                        # Process with agent
                        with st.spinner("🤖 Getting AI response..."):
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            try:
                                response_text, response_audio = loop.run_until_complete(
                                    process_voice_input(audio_data, selected_agent)
                                )
                            finally:
                                loop.close()
                        
                        # Add agent response to chat
                        st.session_state.chat_history.append({
                            "type": "agent",
                            "text": response_text,
                            "agent": st.session_state.selected_agent,
                            "audio_data": response_audio,
                            "sample_rate": sample_rate
                        })
                        
                        st.success("🎉 Response received!")
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error processing audio: {str(e)}")
                finally:
                    st.session_state.is_processing = False
            
            elif not st.session_state.api_key:
                st.warning("⚠️ Please enter your OpenAI API key to process audio!")

if __name__ == "__main__":
    main()