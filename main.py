import logging
import time
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
from token_manager import TokenManager
from agent_state_manager import AgentStateManager
from message_sender import send_teams_message
from constants import CALL_DURATION_THRESHOLD_MINUTES

load_dotenv()

logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def has_exceeded_time_limit(timestamp: str, minutes: int) -> bool:
    if not timestamp:
        return False

    given_timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    melbourne_tz = pytz.timezone('Australia/Melbourne')
    current_time_melbourne = datetime.now(melbourne_tz)
    given_timestamp_melbourne = pytz.utc.localize(given_timestamp).astimezone(melbourne_tz)

    time_difference = current_time_melbourne - given_timestamp_melbourne
    return abs(time_difference) > timedelta(minutes=minutes)

def check_agent_states(agent_state_manager: AgentStateManager, alerted_agents: set) -> None:
    agent_states = agent_state_manager.get_agent_states()
    webhook_url = os.getenv("WEBHOOK_URL")

    for agent in agent_states["agentStates"]:
        agent_id = agent["agentId"]
        agent_state_id = agent["agentStateId"]
        call_duration = agent['startDate']
        agent_name = f"{agent['firstName']} {agent['lastName']}"

        if has_exceeded_time_limit(call_duration, CALL_DURATION_THRESHOLD_MINUTES) and agent_state_id == 3 and agent_id not in alerted_agents:
            send_teams_message(webhook_url, f"{agent_name}'s call duration has exceeded {CALL_DURATION_THRESHOLD_MINUTES} minutes, please assist them!")
            alerted_agents.add(agent_id)
            logging.info(f"Alert sent: {agent_name}'s call duration exceeded threshold.")
        elif not has_exceeded_time_limit(call_duration, CALL_DURATION_THRESHOLD_MINUTES) and agent_id in alerted_agents:
            alerted_agents.remove(agent_id)

def main() -> None:
    token_manager = TokenManager(
        base_url=os.getenv("AUTH_BASE_URL"),
        access_key_id=os.getenv("ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ACCESS_KEY_SECRET")
    )
    agent_state_manager = AgentStateManager(
        api_base_url=os.getenv("API_BASE_URL"),
        token_manager=token_manager
    )
    alerted_agents = set()

    while True:
        check_agent_states(agent_state_manager, alerted_agents)
        time.sleep(60)

if __name__ == "__main__":
    main()