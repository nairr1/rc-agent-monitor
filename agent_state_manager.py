import requests
import logging

class AgentStateManager:
  def __init__(self, api_base_url, token_manager, fetch_interval_seconds=60):
    self.api_base_url = api_base_url
    self.token_manager = token_manager
    self.fetch_interval_seconds = fetch_interval_seconds
    self.agent_states = {}
    self.schedule_agent_state_fetch()

  def fetch_agent_states(self):
    endpoint = "/incontactapi/services/v27.0/agents/states"
    url = f"{self.api_base_url}{endpoint}"

    access_token = self.token_manager.get_access_token()
    response = requests.get(url, headers={'Authorization': f'Bearer {access_token}'})

    if response.status_code == 401:
      self.token_manager.refresh_token()
      access_token = self.token_manager.get_access_token()
      response = requests.get(url, headers={'Authorization': f'Bearer {access_token}'})

    if response.status_code != 200:
      logging.error(f"Error fetching agent states: {response.json()}")
      raise Exception(f"Error fetching agent states: {response.text}")

    self.agent_states = response.json()

  def schedule_agent_state_fetch(self):
    from threading import Timer
    
    def fetch_states():
      try:
        self.fetch_agent_states()
      except Exception as e:
        logging.error(f"Error fetching agent states: {e}")
      Timer(self.fetch_interval_seconds, fetch_states).start()
    
    fetch_states()

  def get_agent_states(self):
    return self.agent_states