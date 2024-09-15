import requests
import logging

class KeyVaultClient:
    def __init__(self, server_url='http://localhost:38680'):
        self.server_url = server_url
        self.logger = logging.getLogger(__name__)

    def get_key(self, key_name):
        try:
            response = requests.get(f"{self.server_url}/get_key/{key_name}")
            response.raise_for_status()
            return response.json().get(key_name)
        except requests.RequestException as e:
            self.logger.error(f"Error fetching key {key_name}: {str(e)}")
            raise

    def list_keys(self):
        try:
            response = requests.get(f"{self.server_url}/list_keys")
            response.raise_for_status()
            return response.json().get('keys')
        except requests.RequestException as e:
            self.logger.error(f"Error fetching keys list: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = KeyVaultClient()

    try:
        # Get a specific key
        api_key = client.get_key('OPENAI_API_KEY')
        print("API Key:", api_key)

        # List all keys
        keys = client.list_keys()
        print("Available keys:", keys)
    except Exception as e:
        print(f"An error occurred: {str(e)}")