import unittest
from DNSHeader import DNSHeader


class DNSHeaderTest(unittest.TestCase):

    def setUp(self):
        self.header = DNSHeader()
    

    def test_get_flags(self):
        self.header.set_dor(0)
        self.header.set_opcode(0)
        self.header.set_aa()
        self.header.set_tc()
        self.header.set_rd(0)
        self.header.set_ra()
        self.header.set_z()
        self.header.set_rcode()
        self.header.set_flags()

        self.assertEqual(self.header.get_flags(), b'\x00\x00')

if __name__ == '__main__':
    unittest.main()
