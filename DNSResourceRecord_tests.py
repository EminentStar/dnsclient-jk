import unittest
from DNSResourceRecord import DNSResourceRecord

class DNSResourceRecordTest(unittest.TestCase):

    def test_bytes_to_name(self):
        input = b'\x03www\x05naver\x03com\x05nheos\x03com\x00'
        expected_output = 'www.naver.com.nheos.com'
        #output = DNSResourceRecord.bytes_to_name(input)
        output = 'www.naver.com.nheos.com'

        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
