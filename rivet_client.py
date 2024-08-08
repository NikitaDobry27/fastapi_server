import requests


class RivetClient:
    def __init__(self):
        self.base_url = 'https://services.kirill-markin.com/rivet-soax-server/api/pipelines/operations'

    def forward_first_payment(self, json):
        url = f"{self.base_url}/first_payment_date_amount"
        try:
            search_data = {"inputs": {"webhook_data": {"type": "object", "value": json}}}
            response = requests.post(url, json=search_data)
            print(json)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        
    def forward_user_for_won_deals(self, json):
        url = f"{self.base_url}/create_user_for_won_deals"
        try:
            search_data = {"inputs": {"webhook_data": {"type": "object", "value": json}}}
            response = requests.post(url, json=search_data)
            print(json)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
