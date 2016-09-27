import sys
import unittest
sys.path.append("/")
import dnsclientjk
from dnsclientjk import DNSHeader


class DNSHeaderTest(unittest.TestCase):

    def test_set_flags(self):
        dns_header = DNSHeader(0, 0, 0, 0, 0, 0)
        dns_header.set_flags()
        self.assertEqual(dns_header.get_flags(), b'\x00\x00')
    
    def test_set_counts(self):
        dns_header = DNSHeader(0, 0, 1, 0, 0, 0)
        self.assertEqual(dns_header.get_counts(), b'\x00\x01\x00\x00\x00\x00\x00\x00')

if __name__ == '__main__':
    unittest.main()
