# Clinic AI Phone Agent

AI assistant that helps collect patient's information over the phone, then store and email it to admin.

## Requirements

*   Python 3.12.x+
*   LiveKit CLI
*   API Keys in .env file
*   Twilio phone number & SIP:
    *   Purchase a phone number
    *   Set up its SIP trunk, the `origination URI` looks similar likes this `sip:xxxxxx.sip.livekit.cloud;transport=tcp`
    *   Edit phone number in `inbound-trunk.json`
*   LiveKit CLI
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

Set up the environment by copying `.env.example` to `.env` and filling in the required values.

You can also do this automatically using the LiveKit CLI:

```
lk app env
```

Run the agent:

```
python3 agent.py dev
```

Run unit tests:

```
python3 test_utils.py
```