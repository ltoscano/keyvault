import unittest
from unittest.mock import patch
from keyvault.client import KeyVaultClient

class TestKeyVaultClient(unittest.TestCase):

    @patch('keyvault.client.requests.get')
    def test_get_key(self, mock_get):
        mock_get.return_value.json.return_value = {'test_key': 'test_value'}
        mock_get.return_value.status_code = 200

        client = KeyVaultClient()
        result = client.get_key('test_key')

        self.assertEqual(result, 'test_value')
        mock_get.assert_called_once_with('http://localhost:38680/get_key/test_key')

    @patch('keyvault.client.requests.get')
    def test_list_keys(self, mock_get):
        mock_get.return_value.json.return_value = {'keys': ['key1', 'key2']}
        mock_get.return_value.status_code = 200

        client = KeyVaultClient()
        result = client.list_keys()

        self.assertEqual(result, ['key1', 'key2'])
        mock_get.assert_called_once_with('http://localhost:38680/list_keys')

if __name__ == '__main__':
    unittest.main()