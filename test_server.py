import http
import unittest
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler
import http.client
import json
import threading

class TestServerGET(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8000)
        cls.server = HTTPServer(cls.server_address, SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()
    

    def test_get_method(self):
        # Connect to the server and send a GET request
        connection = http.client.HTTPConnection(*self.server_address)
        connection.request('GET', '/')
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        #check That the response as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data, {'message': 'This is a GET request response'})
        
class TestServerPOST(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8000)
        cls.server = HTTPServer(cls.server_address, SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def test_post_method(self):
        # Data to be sent in the POST request
        data = {'key': 'value'}

        # Convert data to JSON format
        json_data = json.dumps(data)

        # Connect to the server and send a POST request
        connection = http.client.HTTPConnection(*self.server_address)
        connection.request('POST', '/', json_data, headers={'Content-Type': 'application/json'})
        response = connection.getresponse()

        # Read and Decode the response
        response_data = response.read().decode()
        connection.close()

        # Check that the response is as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        parsed_response_data = json.loads(response_data)
        self.assertEqual(parsed_response_data, {'received': {'key': 'value'}})

        
if __name__ == '__main__':
    unittest.main()