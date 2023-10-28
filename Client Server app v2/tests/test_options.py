import unittest
from options import Options
from unittest.mock import patch, mock_open


class TestOptions(unittest.TestCase):

    def test_uptime_command(self):
        options = Options()
        uptime_response = options.uptime()  # Wywołanie funkcji uptime
        print("Uptime response:", uptime_response)

        info_response = options.info("Server Info")
        print("Info response:", info_response)

        help_response = options.help()
        print("Help response:", help_response)

        # Sprawdzenie czy otrzymany JSON zawiera klucz 'uptime'
        self.assertIn("uptime", uptime_response)
        self.assertIn("info", info_response)
        self.assertIn("help", help_response)


class TestOptionsMethods(unittest.TestCase):

    def setUp(self):
        self.options = Options()

    def test_register(self):
        mock_users_data = '{"users": [{"nick": "testuser", "password": "testpass", "role": "user"}]}'
        with patch("builtins.open", mock_open(read_data=mock_users_data)):
            result = self.options.register("newuser", "newpass")
            print(result)
            self.assertEqual(result, '{"register": "Registration successful."}')

    def test_register_existing_user(self):
        mock_users_data = '{"users": [{"nick": "existinguser", "password": "existingpass", "role": "user"}]}'
        with patch("builtins.open", mock_open(read_data=mock_users_data)):
            result = self.options.register("existinguser", "existingpass")
            print(result)
            self.assertEqual(result, '{"register": "Username already exists."}')

    def test_login(self):
        mock_users_data = '{"users": [{"nick": "testuser", "password": "testpass", "role": "user"}]}'
        with patch("builtins.open", mock_open(read_data=mock_users_data)):
            result = self.options.login("testuser", "testpass")
            print(result)
            self.assertEqual(result, '{"login": "Login successful."}')


if __name__ == '__main__':
    unittest.main()
