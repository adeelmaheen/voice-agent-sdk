from agents import Agent
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from tools import fetch_weather

spanish_agent = Agent(
    name="SpanishAgent",
    handoff_description="Handles Spanish conversations.",
    instructions=prompt_with_handoff_instructions(
        "You are a polite assistant who always replies in Spanish."
    ),
    model="gpt-4o",
)

agent = Agent(
    name="VoiceAssistant",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human. Be polite and helpful. If the user speaks in Spanish or mixes Spanish and English, handoff to the Spanish agent.",
    ),
    model="gpt-4o",
    handoffs=[spanish_agent],
    tools=[fetch_weather],
)

