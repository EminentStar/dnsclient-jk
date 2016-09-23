import unittest
import dnsclient

class DnsclientTest(unittest.TestCase):
    
    def test_get_ip_addr(self):
        result = dnsclient.get_ip_addr('www.naver.com')
        self.assertEqual(result, '202.179.177.22')

if __name__ == '__main__':
    unittest.main()
