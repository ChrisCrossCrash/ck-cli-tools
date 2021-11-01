import unittest
from unittest.mock import patch, mock_open, MagicMock
from typing import cast

from tools.utils import yes_or_no, load_env_file


class ExpectedTestError(Exception):
    """A custom exception made for use with assertRaises."""
    pass


class TestWithoutDefault(unittest.TestCase):
    @patch('builtins.input', lambda *args: 'y')
    def test_yes_without_default(self):
        self.assertTrue(yes_or_no('Sky is blue?'))

    @patch('builtins.input', lambda *args: 'n')
    def test_no_without_default(self):
        self.assertFalse(yes_or_no('Sky is blue?'))

    @patch('builtins.input', lambda *args: 'maybe?')
    def test_invalid_without_default(self):
        with patch('builtins.print') as mock_print:
            mock_print.side_effect = ExpectedTestError
            with self.assertRaises(ExpectedTestError):
                yes_or_no('Sky is blue?')
            mock_print.assert_called_with("Please answer 'y' or 'n'.")

    @patch('builtins.input', lambda *args: '')
    def test_empty_without_default(self):
        with patch('builtins.print') as mock_print:
            mock_print.side_effect = ExpectedTestError
            with self.assertRaises(ExpectedTestError):
                yes_or_no('Sky is blue?')
            mock_print.assert_called_with("Please answer 'y' or 'n'.")


class TestWithDefaultYes(unittest.TestCase):
    @patch('builtins.input', lambda *args: 'y')
    def test_yes_with_default_yes(self):
        self.assertTrue(yes_or_no('Sky is blue?', default='y'))

    @patch('builtins.input', lambda *args: 'n')
    def test_no_with_default_yes(self):
        self.assertFalse(yes_or_no('Sky is blue?', default='y'))

    @patch('builtins.input', lambda *args: 'maybe?')
    def test_invalid_with_default_yes(self):
        with patch('builtins.print') as mock_print:
            mock_print.side_effect = ExpectedTestError
            with self.assertRaises(ExpectedTestError):
                yes_or_no('Sky is blue?', default='y')
            mock_print.assert_called_with("Please answer 'y' or 'n'.")

    @patch('builtins.input', lambda *args: '')
    def test_empty_with_default_yes(self):
        self.assertTrue(yes_or_no('Sky is blue?', default='y'))


class TestWithDefaultNo(unittest.TestCase):
    @patch('builtins.input', lambda *args: 'y')
    def test_yes_with_default_no(self):
        self.assertTrue(yes_or_no('Sky is blue?', default='n'))

    @patch('builtins.input', lambda *args: 'n')
    def test_no_with_default_no(self):
        self.assertFalse(yes_or_no('Sky is blue?', default='n'))

    @patch('builtins.input', lambda *args: 'maybe?')
    def test_invalid_with_default_no(self):
        with patch('builtins.print') as mock_print:
            mock_print.side_effect = ExpectedTestError
            with self.assertRaises(ExpectedTestError):
                yes_or_no('Sky is blue?', default='n')
            mock_print.assert_called_with("Please answer 'y' or 'n'.")

    @patch('builtins.input', lambda *args: '')
    def test_empty_with_default_no(self):
        self.assertFalse(yes_or_no('Sky is blue?', default='n'))


class TestDefaultCapitalization(unittest.TestCase):
    def test_no_default_no_capitalizaion(self):
        with patch('builtins.input') as mock_input:
            mock_input.return_value = 'y'
            yes_or_no('Sky is blue?')
            mock_input.assert_called_with('Sky is blue? [y/n] ')

    def test_default_y_capital_y(self):
        with patch('builtins.input') as mock_input:
            mock_input.return_value = 'y'
            yes_or_no('Sky is blue?', default='y')
            mock_input.assert_called_with('Sky is blue? [Y/n] ')

    def test_default_n_capital_n(self):
        with patch('builtins.input') as mock_input:
            mock_input.return_value = 'y'
            yes_or_no('Sky is blue?', default='n')
            mock_input.assert_called_with('Sky is blue? [y/N] ')


class TestInputValidity(unittest.TestCase):
    @patch('builtins.input', lambda *args: 'Y')
    def test_capital_y_is_valid(self):
        self.assertTrue(yes_or_no('Sky is blue?'))

    @patch('builtins.input', lambda *args: 'N')
    def test_capital_n_is_valid(self):
        self.assertFalse(yes_or_no('Sky is blue?'))

    @patch('builtins.input', lambda *args: 'YES')
    def test_YES_is_valid(self):
        self.assertTrue(yes_or_no('Sky is blue?'))

    @patch('builtins.input', lambda *args: 'NO')
    def test_NO_is_valid(self):
        self.assertFalse(yes_or_no('Sky is blue?'))


class TestOther(unittest.TestCase):
    def test_raises_on_invalid_default(self):
        with self.assertRaisesRegex(ValueError, "'The default value must be 'y' or 'n'."):
            # 'Y' is invalid because it should be lowercase.
            yes_or_no('Sky is blue?', default=cast('Y', str))

    def test_valid_input_after_invalid(self):
        # Make a generator the will first yield `maybe?` (invalid), then `n` (valid)
        gen = (i for i in ('maybe?', 'n'))
        with patch('builtins.input', lambda *args: next(gen)):
            # The first time `next(gen)` is called will yield `maybe?` which will tell
            # the `mock_print` to print "Please answer 'y' or 'n'."
            with patch('builtins.print') as mock_print:
                # Should return false, since the first valid response is `n`
                self.assertFalse(yes_or_no('Sky is blue?'))
                # This should have been called after the invalid `maybe?` response
                mock_print.assert_called_with("Please answer 'y' or 'n'.")


class TestLoadEnvFile(unittest.TestCase):
    valid_env_str_data = 'TELEGRAM_TOKEN=0123456789:ThisIsAFakeTelegramToken01234567890\nTELEGRAM_CHAT_ID=0123456789'
    valid_env_dict_data = {
        'TELEGRAM_TOKEN': '0123456789:ThisIsAFakeTelegramToken01234567890',
        'TELEGRAM_CHAT_ID': '0123456789'
    }

    @patch('builtins.open', new_callable=mock_open, read_data=valid_env_str_data)
    def test_loads_env_data(self, _: MagicMock):
        self.assertEqual(load_env_file('.env'), self.valid_env_dict_data)

    @patch('builtins.open', new_callable=mock_open, read_data='# comment\n' + valid_env_str_data)
    def test_ignores_comments(self, _: MagicMock):
        self.assertEqual(load_env_file('.env'), self.valid_env_dict_data)

    @patch('builtins.open', new_callable=mock_open, read_data=valid_env_str_data.replace('\n', '\n\n'))
    def test_ignores_empty_line(self, _: MagicMock):
        self.assertEqual(load_env_file('.env'), self.valid_env_dict_data)

    @patch('builtins.open', new_callable=mock_open, read_data=valid_env_str_data.replace('\n', '\n \t\n'))
    def test_ignores_whitespace_line(self, _: MagicMock):
        self.assertEqual(load_env_file('.env'), self.valid_env_dict_data)


if __name__ == '__main__':
    unittest.main()
