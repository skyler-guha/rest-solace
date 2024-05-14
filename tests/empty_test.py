"""
This file is not testing, but for development.
This is where you can test functions out before you add them to an actual test.
"""
from rest_solace import Manager, MessagingPublisher
from util import get_timestamp

SEMP_HOST= "172.17.0.1"
SEMP_PORT= "8080"
SEMP_USERNAME= "admin"
SEMP_PASSWORD= "admin"

NEW_VPN_NAME= "test_vpn_"+get_timestamp()
NEW_VPN_PORT=  6969

CONSUMER_HOST= "127.0.0.1"
CONSUMER_PORT= 5000

manager = Manager(user_name= SEMP_USERNAME, 
                  password= SEMP_PASSWORD, 
                  host= SEMP_HOST, 
                  semp_port= SEMP_PORT)

res = manager.request_vpn_objects(count=10, where="none")

print(res)