# actions/actions.py
import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionCheckBalance(Action):
    def name(self) -> Text:
        return "action_check_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract account entity if available
        account = tracker.get_slot('account')
        
        response = requests.get(f'http://localhost:8000/api/balance?account={account}')
        
        if response.status_code == 200:
            balance = response.json().get('balance')
            dispatcher.utter_message(f"Your balance in {account} is {balance}.")
        else:
            dispatcher.utter_message("Sorry, I couldn't fetch your balance at the moment. Please try again later.")

        return []
