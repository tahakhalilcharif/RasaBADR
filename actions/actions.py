from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionCheckBalance(Action):
    def name(self) -> Text:
        return "action_check_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message

        metadata = latest_message.get('metadata', {})
        token = metadata.get("authorization")
        print(latest_message)
        if token:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get('http://127.0.0.1:8000/api/balance', headers=headers)

            if response.status_code == 200:
                balance_data = response.json()
                balance = balance_data.get('balance')
                if balance is not None:
                    dispatcher.utter_message(f"Your current balance is {balance}.")
                else:
                    dispatcher.utter_message("Unable to fetch balance.")
            else:
                if response.status_code == 401:
                    dispatcher.utter_message("Unauthenticated.. Please try again later.")
        else:
            dispatcher.utter_message("Token not provided in request.")

        return []
