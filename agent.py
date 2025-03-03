import json
import logging
from dataclasses import dataclass
from typing import Annotated
from utils import send_email, save_customer_info, format_customer_info_html

from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.pipeline import VoicePipelineAgent, AgentCallContext
from livekit.plugins import (
    openai,
    deepgram,
    silero,
    elevenlabs,
    turn_detector,
)

load_dotenv()
logger = logging.getLogger("voice-agent")


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


class CustomerInfoFnc(llm.FunctionContext):
    """
    A class defining LLM functions for collecting customer information.
    """

    @llm.ai_callable()
    async def collect_customer_info(
        self,
        name: Annotated[str, llm.TypeInfo(description="The patient's full name")],
        date_of_birth: Annotated[
            str, llm.TypeInfo(description="The patient's date of birth")
        ],
        insurance_payer: Annotated[
            str, llm.TypeInfo(description="The insurance payer's full name")
        ],
        insurance_plan_id: Annotated[
            str, llm.TypeInfo(description="The insurance plan ID")
        ],
        referral: Annotated[
            str, llm.TypeInfo(description="The referral (from which physician)")
        ],
        reason: Annotated[
            str, llm.TypeInfo(description="The chief medical complaint or reason")
        ],
        address: Annotated[str, llm.TypeInfo(description="The patient's address")],
        phone: Annotated[str, llm.TypeInfo(description="The patient's phone number")],
        email: Annotated[
            str, llm.TypeInfo(description="The patient's email (optional)")
        ],
        appointment_time: Annotated[
            str, llm.TypeInfo(description="Specific date and time for the appointment")
        ],
    ):
        """Called to collect user's information."""

        agent = AgentCallContext.get_current().agent

        # Store the information (in a real application, you'd save this to a database)
        json_data = {
            "name": name,
            "date_of_birth": date_of_birth,
            "insurance_payer": insurance_payer,
            "insurance_plan_id": insurance_plan_id,
            "referral": referral,
            "reason": reason,
            "address": address,
            "phone": phone,
            "email": email,
            "appointment_time": appointment_time,
        }
        if (
            hasattr(agent, "proc")
            and agent.proc
            and hasattr(agent.proc, "userdata")
            and agent.proc.userdata
        ):
            agent.proc.userdata["customer_info"] = json_data

        # Write the customer info to a text file
        if not save_customer_info(json_data):
            await agent.say(
                "I encountered an error saving your information. Please try again later."
            )
            return {"status": "error", "message": "Failed to save information"}

        subject = "Customer Info"
        html_content = format_customer_info_html(json_data)
        send_email("catechlabus@gmail.com", "mrducat@gmail.com", subject, html_content)

        confirmation_message = (
            f"Thank you, {name}. I have collected your information. "
            "How can I assist you further?"
        )
        await agent.say(confirmation_message)  # Confirm with the user
        return {"status": "success"}


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant for a health clinic. Your interface with users will be voice over the phone. "
            "Your first task is to collect customer information."
            "Confirm with user by reading the input back after every user's input. "
            "For scheduling, you know that Dr. John is available from Monday to Thursday 9am to 5pm. Only allow schedules when doctor is available. "
            "Be polite and conversational. Use short and concise responses, and avoiding usage of unpronouncable punctuation. "
            "After collecting the information, no need to repeat all inputs again, ask how else you can help them. "
        ),
    )

    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait for the first participant to connect
    participant = await ctx.wait_for_participant()
    logger.info(f"starting voice assistant for participant {participant.identity}")

    eleven_tts = elevenlabs.tts.TTS(
        model="eleven_turbo_v2_5",
        voice=elevenlabs.tts.Voice(
            id="EXAVITQu4vr4xnSDxMaL",
            name="Bella",
            category="premade",
            settings=elevenlabs.tts.VoiceSettings(
                stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True
            ),
        ),
        language="en",
        streaming_latency=3,
        enable_ssml_parsing=False,
        chunk_length_schedule=[80, 120, 200, 260],
    )

    fnc_ctx = CustomerInfoFnc()  # Create instance of the function context

    openai_tts = openai.tts.TTS(model="tts-1", voice="nova")

    # more plugins: https://docs.livekit.io/agents/plugins
    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(model="nova-3-general"),  # nova-2-phonecall
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai_tts,  # eleven_tts,  # elevenlabs.TTS(),  # cartesia.TTS(),
        turn_detector=turn_detector.EOUModel(),
        # minimum delay for endpointing, used when turn detector believes the user is done with their turn
        min_endpointing_delay=0.5,
        fnc_ctx=fnc_ctx,
        chat_ctx=initial_ctx,
    )

    agent.start(ctx.room, participant)

    # The agent should be polite and greet the user when it joins :)
    await agent.say(
        "Hey, this is ACME Clinic. How can I help you today?", allow_interruptions=True
    )


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint, prewarm_fnc=prewarm, agent_name="inbound-agent"
        ),
    )
