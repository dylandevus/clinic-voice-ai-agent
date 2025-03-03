# Clinic AI Phone Agent

This application provides an AI-powered phone agent solution for healthcare clinics, automating patient intake and information collection. By leveraging Python and the LiveKit platform, this system streamlines the process of gathering essential patient data, reducing administrative burden and improving efficiency. The agent utilizes advanced language processing technologies, including Large Language Models (LLMs), Text-to-Speech (TTS), Speech-to-Text (STT), and Voice Activity Detection (VAD), to facilitate natural and seamless interactions with patients. 

## Requirements

*   Python 3.12.x+
*   LiveKit CLI
*   API Keys (as specified in the `.env` file)
*   Twilio phone number and SIP configuration:
    *   Acquire a Twilio phone number
    *   Configure the associated SIP trunk with an `origination URI` similar to `sip:xxxxxx.sip.livekit.cloud;transport=tcp`
    *   Update the `inbound-trunk.json` file with the designated phone number
*   LiveKit CLI for SIP configuration:
    *   Dispatch rule: run: `lk sip dispatch create dispatch-rule.json`
    *   Inbound trunk: run: `lk sip inbound create inbound-trunk.json`

## Dev Setup

Clone the repository and install dependencies to a virtual environment:

```
# Linux/macOS
cd project-name
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 agent.py download-files
```

Populate the `.env` file with the necessary API keys and configuration values.

Alternatively, utilize the LiveKit CLI for automated environment setup:

```
lk app env
```

Run the agent:

```
python3 agent.py dev
```

Execute unit tests:

```
python3 test_utils.py
```

Build the Docker image:

```
docker build -t clinic-agent .
```