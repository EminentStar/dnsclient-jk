import unittest
import dns_response_parser


class Dns_response_parserTest(unittest.TestCase):

    def test_get_pointer_reference_location(self):
        input = b'\xc0\x09'
        output = dns_response_parser.get_pointer_reference_location(input)
        self.assertEqual(output, 9)
    

    def test_parse_flags(self):
        input = b'\x81\x80'
        expected_output = {'qr':'1', 'opcode': '0000', 'aa': '0', 'tc':'0', 'rd':'1', 'ra':'1',
                'z':'000', 'rcode':'0000'}
        output = dns_response_parser.parse_flags(input)
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
