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
            dispatcher.utter_message("Unauthenticated")

        return []

class ActionViewTransactions(Action):
    def name(self) -> Text:
        return "action_view_transactions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message
        metadata = latest_message.get('metadata', {})
        token = metadata.get("authorization")
        print(latest_message)


        if token:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get('http://127.0.0.1:8000/api/transactions', headers=headers)

            if response.status_code == 200:
                transactions_data = response.json()
                transactions = transactions_data.get('transactions', [])
                if transactions:
                    message = "Here are your recent transactions:\n"
                    for transaction in transactions:
                        message += f"- {transaction['date']}: {transaction['amount']} {transaction['currency']} ({transaction['type']}) {transaction['destination_account']}\n \n"
                    dispatcher.utter_message(message)
                else:
                    dispatcher.utter_message("No transactions found.")
            else:
                if response.status_code == 401:
                    dispatcher.utter_message("Unauthenticated. Please try again later.")
        else:
            dispatcher.utter_message("Unauthenticated")

        return []


class ActionTransferMoney(Action):
    def name(self) -> Text:
        return "action_transfer_money"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message
        metadata = latest_message.get('metadata', {})
        token = metadata.get("authorization")
        amount = tracker.get_slot('amount')
        recipient = tracker.get_slot('recipient')
        source = tracker.get_slot('source')
        
        print(f"Recipient: {recipient}")
        print(f"Amount: {amount}")
        print(f"Source: {source}")
        print(f"Token: {token}")

        if token and amount and recipient and source:
            headers = {"Authorization": f"Bearer {token}"}
            data = {
                "amount": amount,
                "recipient": recipient,
                "source": source
            }
            
            #print(f"Request Data: {data}")

            response = requests.post('http://127.0.0.1:8000/api/transfer', headers=headers, json=data)

            print(f"Response Status Code: {response.status_code}")
            #print(f"Response Content: {response.content}")

            if response.status_code == 200:
                transfer_data = response.json()
                if transfer_data.get('status') == 'success':
                    dispatcher.utter_message(f"Successfully transferred {amount} to {recipient} from {source}.")
                else:
                    dispatcher.utter_message("Transfer failed. Please try again later.")
            else:
                if response.status_code == 401:
                    dispatcher.utter_message("Unauthenticated. Please try again later.")
                else:
                    dispatcher.utter_message(f"Failed with status code: {response.status_code} : {response.message}")
        else:
            dispatcher.utter_message("Unauthenticated or missing transfer details.")

        return []

class ActionViewAccountDetails(Action):
    def name(self) -> Text:
        return "action_view_account_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message
        metadata = latest_message.get('metadata', {})
        token = metadata.get("authorization")

        if token:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get('http://127.0.0.1:8000/api/account_details', headers=headers)

            if response.status_code == 200:
                account_data = response.json()
                account_number = account_data.get('account_number')
                account_type = account_data.get('account_type')
                balance = account_data.get('balance')
                dispatcher.utter_message(f"Account Number: {account_number}\nAccount Type: {account_type}\nBalance: {balance}")
            else:
                if response.status_code == 401:
                    dispatcher.utter_message("Unauthenticated. Please try again later.")
        else:
            dispatcher.utter_message("Unauthenticated")

        return []

class ActionOrderProduct(Action):
    def name(self) -> Text:
        return "action_order_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message
        metadata = latest_message.get('metadata', {})
        token = metadata.get("authorization")
        product = tracker.get_slot('product')

        if token and product:
            headers = {"Authorization": f"Bearer {token}"}
            data = {
                "product": product
            }
            response = requests.post('http://127.0.0.1:8000/api/order_product', headers=headers, json=data)

            if response.status_code == 200:
                order_data = response.json()
                if order_data.get('status') == 'success':
                    dispatcher.utter_message(f"Successfully ordered {product}.")
                else:
                    dispatcher.utter_message("Order failed. Please try again later.")
            else:
                if response.status_code == 401:
                    dispatcher.utter_message("Unauthenticated. Please try again later.")
        else:
            dispatcher.utter_message("Unauthenticated or missing product details.")

        return []

class ActionCheckStatus(Action):
    def name(self) -> Text:
        return "action_check_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message
        metadata = latest_message.get('metadata', {})
        token = metadata.get("authorization")
        print(latest_message)

        if token:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get('http://127.0.0.1:8000/api/check_status', headers=headers)

            if response.status_code == 200:
                status_data = response.json()
                status = status_data.get('status')
                dispatcher.utter_message(f"The status of your request is: {status}")
            else:
                if response.status_code == 401:
                    dispatcher.utter_message("Unauthenticated. Please try again later.")
        else:
            dispatcher.utter_message("Unauthenticated")

        return []


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="I'm sorry, I didn't understand that. Can you please rephrase?")
        return []
