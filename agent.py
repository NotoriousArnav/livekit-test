from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.plugins import cartesia, openai
from livekit.plugins import groq

import os
from tools import (
    analyze_code,
    suggest_improvements,
    get_code_context,
    install_package,
    update_system,
    system_info,
    check_memory,
    set_volume,
    wifi_status,
    kill_process,
    open_application,
)

load_dotenv(".env.local")
load_dotenv(".env")


class CodeAssistant(Agent):
    def __init__(self, prompt: str | None = None) -> None:
        instructions = (
            """You are an expert Code Assistant who helps developers with programming advice, code review, and debugging. You speak fluently in Bengali, Hindi, and English, automatically detecting and responding in the user's preferred language. Your responses are concise, practical, and focused on solving real coding problems. You provide code examples, best practices, performance optimization tips, and security advice. You are patient, encouraging, and have a deep understanding of multiple programming languages and frameworks. Keep responses clear without excessive formatting."""
            if prompt is None or prompt.strip() == ""
            else prompt
        )
        super().__init__(
            instructions=instructions,
            tools=[
                analyze_code,
                suggest_improvements,
                get_code_context,
                install_package,
                update_system,
                system_info,
                check_memory,
                set_volume,
                wifi_status,
                kill_process,
                open_application,
            ],
        )


async def entrypoint(ctx: agents.JobContext):
    with open("prompts/code_assistant.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    session = AgentSession(
        # Using OpenAI Whisper for multilingual STT
        # Supports 99 languages including Bengali, Hindi, English with automatic detection
        stt=openai.STT(model="whisper-1"),
        tts=cartesia.TTS(
            model="sonic-3",
            voice=os.getenv("CARTESIA_VOICE", "en-US-Neural"),
        ),
        llm=groq.LLM(model="llama-3.3-70b-versatile"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=CodeAssistant(prompt=prompt),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions=(
            "Greet the user warmly and introduce yourself as a Code Assistant. "
            "Tell them you can help with programming advice, code review, debugging, and best practices. "
            "Ask what programming challenge or code they'd like help with today. "
            "Be friendly and encouraging."
        ),
        allow_interruptions=True,
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
