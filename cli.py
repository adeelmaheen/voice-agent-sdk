import asyncio
import numpy as np
import sounddevice as sd
import os
from dotenv import load_dotenv

from agents.voice import AudioInput, SingleAgentVoiceWorkflow, VoicePipeline
from agents_setup import agent

load_dotenv()

async def main():
    print("🎤 Speak into your mic...")

    pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(agent))

    # Record real mic input
    samplerate = 24000
    duration = 4  # seconds
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()

    audio_input = AudioInput(buffer=audio.flatten())

    result = await pipeline.run(audio_input)

    # Play AI response
    player = sd.OutputStream(samplerate=samplerate, channels=1, dtype=np.int16)
    player.start()

    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            player.write(event.data)

if __name__ == "__main__":
    asyncio.run(main())


