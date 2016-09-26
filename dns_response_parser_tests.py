import unittest
import dns_response_parser


class Dns_response_parserTest(unittest.TestCase):

    def test_get_pointer_reference_location(self):
        input = b'\xc0\x09'
        output = dns_response_parser.get_pointer_reference_location(input)
        self.assertEqual(output, 9)


if __name__ == '__main__':
    unittest.main()
