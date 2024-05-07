"""
module for http client
"""
import json
import requests
from requests.auth import HTTPBasicAuth


class HttpClient:
    """class to make http/https requests"""

    def __init__(self, host:str, port:str, user_name:str, password:str, verify_ssl:bool|str=False):

        self.verify_ssl = verify_ssl
        self.protocol = 'http' if verify_ssl == False else 'https'
        self.base_url = f'{self.protocol}://{host}:{port}'

        self.user_name = user_name
        self.password = password
        self.authHeader = HTTPBasicAuth(self.user_name, self.password)
        
        self.content_type_headers = {"json": {'Content-Type': 'application/json'},
                                     "plain_text": {'Content-Type': 'text/plain'},
                                     "binary": {'Content-Type':'application/octet-stream'}}


    def http_get(self, endpoint: str, headers:dict= None):
        """method to get the http endpoint
        Args:
            endpoint: endpoint string

        Raises:
            HTTP GET request failed. with response status code or
            HTTP error occurred while HTTP GET exception
        """
        url = f"{self.base_url}{endpoint}"

        req = requests.get(url, auth= self.authHeader, 
                           headers= headers,
                           verify= self.verify_ssl)
        return req


    def http_patch(self, endpoint:str, payload, headers:dict= {'Content-Type': 'application/json'}):
        """method to update the http endpoint
        Args:
            endpoint: endpoint string
            payload: request payload

        Raises:
            HTTP PATCH request failed. with response status code or
            HTTP error occurred while HTTP PATCH exception
        """
        url = f"{self.base_url}{endpoint}"
        
        req = requests.patch(url, auth=self.authHeader, data=json.dumps(payload),
                                headers=headers, verify=self.verify_ssl)
        return req


    def http_post(self, endpoint: str, payload:dict|str, headers:dict= {'Content-Type': 'application/json'}, timeout=None):
        """method for http post
        Args:
            endpoint: endpoint string
            payload: request payload

        Raises:
            HTTP POST request failed. with response status code or
            HTTP error occurred while HTTP POST exception
        """

        url = f"{self.base_url}{endpoint}"
    
        req = requests.post(url, auth=self.authHeader, data=json.dumps(payload),
                            headers=headers, verify=self.verify_ssl, timeout= timeout)
        return req


    def http_delete(self, endpoint:str, headers:dict= {'Content-Type': 'application/json'}):
        """method for http delete
        Args:
            endpoint: endpoint string

        Raises:
            HTTP DELETE request failed. with response status code or
            HTTP error occurred while HTTP DELETE exception
        """
        url = f"{self.base_url}{endpoint}"
        
        req = requests.delete(url, auth=self.authHeader, headers=headers,
                              verify=self.verify_ssl)
    
        return req
    
