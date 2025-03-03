# Clinic AI Phone Agent

AI assistant that helps collect patient's information over the phone, then store and email it to admin.

## Requirements

*   Python 3.12.x+
*   LiveKit CLI
*   API Keys in .env file
*   Required services: Twilio phone number & SIP, LiveKit setups.

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

Windows instructions (click to expand)

```
:: Windows (CMD/PowerShell)
cd project-name
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
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