import unittest

from src.config import Config, parse_config, Meeting


class TestConfig(unittest.TestCase):

    def test_default_parse_config(self):
        config: Config = parse_config("resources/empty_config.yml")
        self.assertEqual(False, config.compromise)
        self.assertEqual(0, len(config.meetings))

    def test_parse_config(self):
        config: Config = parse_config("resources/config.yml")
        self.assertEqual(True, config.compromise)
        self.assertEqual(2, len(config.meetings))

        self.assertEqual('https://zoom.us/j/94783345143?pwd=bitxbmJwMnBNUmU3SExrY3VlUWhuZz09', config.meetings[0].link)
        self.assertEqual('Test', config.meetings[0].description)
        self.assertEqual('monday', config.meetings[0].day)
        self.assertEqual('10:85', config.meetings[0].time)
        self.assertEqual(5, config.meetings[0].duration)

        self.assertEqual('94783345143', config.meetings[1].id)
        self.assertEqual('bitxbmJwMnBNUmU3SExrY3VlUWhuZz09', config.meetings[1].password)
        self.assertEqual('Other Test', config.meetings[1].description)
        self.assertEqual('monday', config.meetings[1].day)
        self.assertEqual('0:05', config.meetings[1].time)
        self.assertEqual(5, config.meetings[1].duration)


if __name__ == '__main__':
    unittest.main()
