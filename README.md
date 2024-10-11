
# Ring Central Agent Monitor

A script that retrieves an auth token from RingCentral's API and then fetches agent state data. It checks each agent in an "inbound" state for their current call duration at 1-minute intervals. If the agent's call duration has exceeded 20 minutes, a message is sent via a Microsoft Teams webhook to a Teams group chat to inform recipients that an agent requires assistance on their call.

## Features
- Retrieves authentication tokens from the RingCentral API.
- Fetches agent state data at regular intervals.
- Sends alerts to a Microsoft Teams channel if agents exceed call duration thresholds.

## Requirements
- Python 3.x
- External Libraries:
  - requests
  - python-dotenv
  - pytz

## Setup Instructions
- Clone the repository:
   ```bash
   git clone https://github.com/nairr1/rc-agent-monitor.git
   cd rc-agent-monitor
- Create a ```.env``` file in the root directory and add your API keys and webhook URL:
   - **NICE_ACCESS_KEY_ID**=<your_access_key_id>
   - **NICE_ACCESS_KEY_SECRET**=<your_access_key_secret>
   - **NICE_API_BASE_URL**=<your_api_base_url>
   - **NICE_AUTH_BASE_URL**=<your_auth_base_url>
   - **MS_TEAMS_WEBHOOK_URL**=<your_teams_webhook_url>
- Install the required Python packages:
   ```bash
   pip install -r requirements.txt
- Run the script:
   ```bash
   python main.py