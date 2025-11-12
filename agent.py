from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.plugins import cartesia

# from livekit.plugins import openai
from livekit.plugins import sarvam, groq

import os
from tools import get_stt_language
from tools import (
    change_stt_language,
    get_current_stt_language,
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


class Assistant(Agent):
    def __init__(self, prompt: str | None = None) -> None:
        instructions = (
            """You are a helpful female voice AI assistant name Vidya who talks in Hindi. You eagerly assist users with their questions by providing information from your extensive knowledge.Your responses are concise, to the point, and without any complex formatting or punctuation including emojis, asterisks, or other symbols.You are curious, friendly, and have a sense of humor."""
            if prompt is None or prompt.strip() == ""
            else prompt
        )
        super().__init__(
            instructions=instructions,
            tools=[
                change_stt_language,
                get_current_stt_language,
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
    with open("prompts/vidya.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    session = AgentSession(
        stt=sarvam.STT(language=get_stt_language(), model="saarika:v2.5"),
        tts=cartesia.TTS(
            model="sonic-3",
            voice=os.getenv("CARTESIA_VOICE", "hi-IN-Wavenet-A"),
        ),
        llm=groq.LLM(model="groq/compound-mini"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(prompt=prompt),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions=(
            "<|system|> SYSTEM INSTRUCTION:"
            "Greet the user and offer your assistance."
            "You have been appointed by OMX Digital Marketing Agency as their AI assistant to help users with their queries related to digital marketing."
            "Keep your responses concise and to the point."
            "<|endofsystem|>"
        ),
        allow_interruptions=True,
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
