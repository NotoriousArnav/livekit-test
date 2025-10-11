from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.plugins import sarvam, openai

import os

# from tools import install_package
# from tools import update_system
# from tools import kill_process
# from tools import system_info
# from tools import check_memory
# from tools import set_volume
# from tools import open_application

load_dotenv(".env.local")

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful female voice AI assistant name Vidya who talks in Hindi.
                You eagerly assist users with their questions by providing information from your extensive knowledge.
                Your responses are concise, to the point, and without any complex formatting or punctuation including emojis, asterisks, or other symbols.
                You are curious, friendly, and have a sense of humor.""",
            # tools = [
            #     install_package,
            #     update_system,
            #     system_info,
            #     check_memory,
            #     set_volume,
            #     kill_process,
            #     open_application
            # ]
        )

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=sarvam.STT(
            language="hi-IN",
            model="saarika:v2.5"
        ),
        # llm = openai.LLM.with_ollama(
        #     model="sarvam-m",
        #     base_url="https://952c0285347b.ngrok-free.app/v1",
        # ),
        llm=openai.LLM(   # properly instantiate using a supported plugin class
            model="sarvam-m",
            api_key=os.getenv("SARVAM_API_KEY", ''),
            base_url="https://api.sarvam.ai/v1",
            reasoning_effort=None
        ),
        # llm = groq.LLM(
        #     model="openai/gpt-oss-20b"
        # ),
        tts=sarvam.TTS(
            target_language_code="hi-IN",
            model="bulbul:v2",
            speaker="vidya",
            enable_preprocessing=True
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
