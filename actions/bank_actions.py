from typing import Any, Text, Dict, List
from rasa.actions.action import Action
from rasa.events.slot_mappings import SlotMapping
from rasa.events.user import UserUttered
from rasa.nlu.model import Interpreter
from rasa.core.events import SlotSet
import requests

class ActionGetBalance(Action):
    def name(self) -> Text:
        return "action_get_balance"

    def run(self, dispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[EventType]:

        # Fetch balance information from your Laravel backend
        response = requests.get("http://localhost:8000/api/getBalance")
        balance = response.json()['balance']

        # Set the balance as a slot
        dispatcher.utter_message(text=f"Your account balance is: {balance}")
        return [SlotSet("balance", balance)]
    