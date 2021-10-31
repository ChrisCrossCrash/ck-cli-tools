import unittest
from unittest.mock import patch, mock_open, MagicMock
from typing import Callable, cast

from tools.utils import yes_or_no, load_env_file


class TestError(Exception):
    """A custom exception made for use with assertRaises."""
    pass


def make_mock_input(return_val: str, throw_return_val=False) -> Callable[[str], str]:
    """Return a mock input that will always have the return value of `return_val`."""
    def mock_input(prompt: str):
        if throw_return_val:
            raise TestError(prompt)
        return return_val

    return mock_input


def mock_print(txt: str):
    raise TestError(txt)


class TestWithoutDefault(unittest.TestCase):
    def test_yes_without_default(self):
        self.assertTrue(yes_or_no('Sky is blue?', input_func=make_mock_input('y')))

    def test_no_without_default(self):
        self.assertFalse(yes_or_no('Sky is blue?', input_func=make_mock_input('n')))

    def test_invalid_without_default(self):
        with self.assertRaisesRegex(TestError, "Please answer 'y' or 'n'."):
            yes_or_no('Sky is blue?', input_func=make_mock_input('maybe?'), output_func=mock_print)

    def test_empty_without_default(self):
        with self.assertRaisesRegex(TestError, "Please answer 'y' or 'n'."):
            yes_or_no('Sky is blue?', input_func=make_mock_input(''), output_func=mock_print)


class TestWithDefaultYes(unittest.TestCase):
    def test_yes_with_default_yes(self):
        self.assertTrue(yes_or_no('Sky is blue?', input_func=make_mock_input('y'), default='y'))

    def test_no_with_default_yes(self):
        self.assertFalse(yes_or_no('Sky is blue?', input_func=make_mock_input('n'), default='y'))

    def test_invalid_with_default_yes(self):
        with self.assertRaisesRegex(TestError, "Please answer 'y' or 'n'."):
            yes_or_no('Sky is blue?', input_func=make_mock_input('maybe?'), output_func=mock_print, default='y')

    def test_empty_with_default_yes(self):
        self.assertTrue(yes_or_no('Sky is blue?', input_func=make_mock_input(''), default='y'))


class TestWithDefaultNo(unittest.TestCase):
    def test_yes_with_default_no(self):
        self.assertTrue(yes_or_no('Sky is blue?', input_func=make_mock_input('y'), default='n'))

    def test_no_with_default_no(self):
        self.assertFalse(yes_or_no('Sky is blue?', input_func=make_mock_input('n'), default='n'))

    def test_invalid_with_default_no(self):
        with self.assertRaisesRegex(TestError, "Please answer 'y' or 'n'."):
            yes_or_no('Sky is blue?', input_func=make_mock_input('maybe?'), output_func=mock_print, default='n')

    def test_empty_with_default_no(self):
        self.assertFalse(yes_or_no('Sky is blue?', input_func=make_mock_input(''), default='n'))


class TestDefaultCapitalization(unittest.TestCase):
    def test_no_default_no_capitalizaion(self):
        with self.assertRaisesRegex(TestError, r'\[y/n\]'):
            yes_or_no('Sky is blue?', input_func=make_mock_input('y', throw_return_val=True))

    def test_default_y_capital_y(self):
        with self.assertRaisesRegex(TestError, r'\[Y/n\]'):
            yes_or_no('Sky is blue?', input_func=make_mock_input('y', throw_return_val=True), default='y')

    def test_default_n_capital_n(self):
        with self.assertRaisesRegex(TestError, r'\[y/N\]'):
            yes_or_no('Sky is blue?', input_func=make_mock_input('y', throw_return_val=True), default='n')


class TestInputValidity(unittest.TestCase):
    def test_capital_y_is_valid(self):
        self.assertTrue(yes_or_no('Sky is blue?', input_func=make_mock_input('Y')))

    def test_capital_n_is_valid(self):
        self.assertFalse(yes_or_no('Sky is blue?', input_func=make_mock_input('N')))

    def test_YES_is_valid(self):
        self.assertTrue(yes_or_no('Sky is blue?', input_func=make_mock_input('YES')))

    def test_NO_is_valid(self):
        self.assertFalse(yes_or_no('Sky is blue?', input_func=make_mock_input('NO')))


class TestOther(unittest.TestCase):
    def test_raises_on_invalid_default(self):
        with self.assertRaisesRegex(ValueError, "'The default value must be 'y' or 'n'."):
            # 'Y' is invalid because it should be lowercase.
            yes_or_no('Sky is blue?', default=cast('Y', str))

    def test_valid_input_after_invalid(self):
        # Make a generator the will first yield `maybe?` (invalid), then `n` (valid)
        gen = (i for i in ('maybe?', 'n'))
        with self.assertRaisesRegex(TestError, "Please answer 'y' or 'n'."):
            # The first time `gen.__next__()` is called will yield `maybe?` which will tell
            # the `output_func` to print "Please answer 'y' or 'n'."
            yes_or_no('Sky is blue?', input_func=lambda _: gen.__next__(), output_func=mock_print)
        # The second time `gen.__next__()` is called will yield `n`,
        # which will cause `yes_or_no()` to return False.
        self.assertFalse(yes_or_no('Sky is blue?', input_func=lambda _: gen.__next__()))


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
