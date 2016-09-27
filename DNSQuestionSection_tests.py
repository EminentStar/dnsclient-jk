import unittest
from DNSQuestionSection import DNSQuestionSection


class DNSQuestionSectionTest(unittest.TestCase):

    def test_construct_qname(self):
        qsection = DNSQuestionSection('www.naver.com', 1, 1)
        self.assertEqual(qsection.to_bytes(), b'\x03www\x05naver\x03com\x00\x00\x01\x00\x01')


if __name__ == '__main__':
    unittest.main()
