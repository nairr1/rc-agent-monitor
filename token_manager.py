import requests
import logging

class TokenManager:
  def __init__(self, base_url, access_key_id, access_key_secret):
    self.base_url = base_url
    self.access_key_id = access_key_id
    self.access_key_secret = access_key_secret
    self.refresh_token_value = ""
    self.access_token_data = {}
    self.fetch_access_token()

  def fetch_access_token(self):
    endpoint = "/authentication/v1/token/access-key"
    url = f"{self.base_url}{endpoint}"

    payload = {
      'accessKeyId': self.access_key_id,
      'accessKeySecret': self.access_key_secret,
      'grant_type': 'refresh_token' if self.refresh_token_value else None,
      'refresh_token': self.refresh_token_value or None
    }

    response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)

    if response.status_code != 200:
      logging.error(f"Error fetching access token: {response.json()}")
      raise Exception(f"Error fetching access token: {response.text}")

    self.access_token_data = response.json()
    self.refresh_token_value = self.access_token_data.get('refresh_token', self.refresh_token_value)

  def refresh_token(self):
    self.fetch_access_token()

  def get_access_token(self):
    return self.access_token_data.get('access_token')