import requests

class RivetClient:
    def __init__(self):
        self.base_url = 'https://rivet.soax.tech/api/pipelines/operations'

    def forward_first_payment(self, json):
        url = f"{self.base_url}/first_payment_date_amount"
        try:
            search_data = {"inputs": {"webhook_data": {"type": "object", "value": json}}}
            print(f"Body sent to rivet: {search_data}")
            response = requests.post(url, json=search_data)
            print(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        
    def forward_user_for_won_deals(self, json):
        url = f"{self.base_url}/create_user_for_won_deals"
        try:
            search_data = {"inputs": {"webhook_data": {"type": "object", "value": json}}}
            print(f"Body sent to rivet: {search_data}")
            response = requests.post(url, json=search_data)
            print(response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def slashid_to_attio_user_creation(self, json):
        url = f"{self.base_url}/slashid_to_attio_user"
        try:
            search_data = {"inputs": {"webhook_data": {"type": "object", "value": json}}}
            print(f"Body sent to rivet: {search_data}")
            response = requests.post(url, json=search_data)
            print(response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        
    def chargebee_to_attio(self, json_data):
        url = f"{self.base_url}/chargebee_handler"
        try:
            search_data = {"inputs": {"webhook_data": {"type": "object", "value": json_data}}}
            # print(f"Body sent to rivet: {search_data}")
            response = requests.post(url, json=search_data)
            response.raise_for_status()  # Поднимет исключение, если ответ содержит статус ошибки
            print(f"Response from rivet: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return {"error": str(e)}
    
    def orb_to_attio(self, json_data):
        url = f"{self.base_url}/orb_handler"
        try:
            search_data = {"inputs": {"webhook_data": {"type": "object", "value": json_data}}}
            print(f"Body sent to rivet: {search_data}")
            response = requests.post(url, json=search_data)
            response.raise_for_status()  
            print(f"Response from rivet: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return {"error": str(e)}

    def intercom_dashboard(self, json_data):
        url = f"{self.base_url}/intercom_dashboard"
        try:
            search_data = {"inputs": {"webhook_data": {"type": "object", "value": json_data}}}
            print(f"Body sent to rivet: {search_data}")
            response = requests.post(url, json=search_data)
            response.raise_for_status()
            print(f"Response from rivet: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return {"error": str(e)}