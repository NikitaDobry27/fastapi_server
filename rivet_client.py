import requests


class RivetClient:
    def __init__(self):
        self.base_url = 'https://1b4a-109-243-67-140.ngrok-free.app/api/pipelines/first_payment_date_amount'

    def forward_first_payment(self, json):
        url = f"{self.base_url}/main"
        try:
            search_data = {"inputs": {"webhook_data": {"type": "object", "value": json}}}
            response = requests.post(url, json=search_data)
            print(json)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
