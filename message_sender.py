import requests
import logging

def send_teams_message(webhook_url, message):
  adaptive_card = {
    "contentType": "application/vnd.microsoft.card.adaptive",
    "content": {
      "type": "AdaptiveCard",
      "body": [{"type": "TextBlock", "text": message, "size": "small"}],
      "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
      "version": "1.0"
    }
  }

  payload = {"type": "message", "attachments": [adaptive_card]}
  response = requests.post(webhook_url, json=payload, headers={'Content-Type': 'application/json'})

  if response.status_code not in (200, 202):
    logging.error(f"Failed to send Adaptive Card. Status code: {response.status_code}, Error: {response.text}")
  else:
    logging.info("Adaptive Card sent successfully!")
