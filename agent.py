import logging
from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    Agent,
    AgentSession,
)
from livekit.plugins import google
# IMPORT ALL NEW TOOLS
from api import (
    lookup_car, 
    create_car, 
    has_selected_car, 
    book_appointment, 
    cancel_appointment, 
    reschedule_appointment
)
from prompts import INSTRUCTIONS, WELCOME_MESSAGE

load_dotenv()
logger = logging.getLogger("voice-agent")

async def entrypoint(ctx: JobContext):
    logger.info("starting entrypoint")

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    await ctx.wait_for_participant()

    final_instructions = INSTRUCTIONS + f"\n\nIMPORTANT: Start with: '{WELCOME_MESSAGE}'"

    model = google.beta.realtime.RealtimeModel(
        instructions=final_instructions,
        voice="Aoede",
        temperature=0.8,
        modalities=["AUDIO"]
    )

    session = AgentSession(
        llm=model,
    )

    await session.start(
        room=ctx.room,
        agent=Agent(
            instructions=final_instructions,
            # REGISTER ALL TOOLS HERE
            tools=[
                lookup_car, 
                create_car, 
                has_selected_car, 
                book_appointment, 
                cancel_appointment, 
                reschedule_appointment
            ]
        )
    )

    await session.generate_reply()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))