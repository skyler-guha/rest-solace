from rest_solace import Manager, MessagingPublisher, Consumer
from util import get_timestamp
from consumer_test import return_uppercase
import threading
import time
import asyncio
import logging
logging.basicConfig(level=logging.WARNING)

SEMP_HOST= "172.17.0.1"
SEMP_PORT= "8080"
SEMP_USERNAME= "admin"
SEMP_PASSWORD= "admin"

NEW_VPN_NAME= "test_vpn_"+get_timestamp()
NEW_VPN_PORT=  6969

CONSUMER_HOST= "127.0.0.1"
CONSUMER_PORT= 5000

INPUT_MESSAGE= "hello world!!"
EXPECTED_OUTPUT_MESSAGE= bytes("HELLO WORLD!!", 'utf-8')

manager = Manager(user_name= SEMP_USERNAME, 
                      password= SEMP_PASSWORD, 
                      host= SEMP_HOST, 
                      semp_port= SEMP_PORT)

publish = MessagingPublisher(user_name="admin", password="admin", 
                             host= SEMP_HOST, rest_vpn_port=NEW_VPN_PORT)

consumer_obj = Consumer()

def setup():

    manager.create_message_vpn(msgVpnName= NEW_VPN_NAME,
                           serviceRestIncomingPlainTextListenPort= NEW_VPN_PORT)

    manager.auto_rest_messaging_setup_utility(msgVpnName= NEW_VPN_NAME, queueName= 'queue_rest_consumer', subscriptionTopic='my_topic', 
                                              restDeliveryPointName='myRDP', restConsumerName='myConsumer', 
                                              remoteHost= CONSUMER_HOST, remotePort= CONSUMER_PORT)
        
    args = ("127.0.0.1", 5000, return_uppercase, True, True, 10)

    consumer_thread = threading.Thread(target= consumer_obj.startConsumer, 
                                       args= args)
    consumer_thread.start()

    manager.restart_rest_delivery_point(restDeliveryPointName= "myRDP", 
                                        msgVpnName= NEW_VPN_NAME)


def teardown():
    manager.delete_queue_endpoint(msgVpnName= NEW_VPN_NAME, queueName= 'queue_rest_consumer')
    manager.delete_rest_delivery_point(msgVpnName= NEW_VPN_NAME, restDeliveryPointName= 'myRDP')
    manager.delete_message_vpn(msgVpnName= NEW_VPN_NAME)


#Sync functions
def test_direct_message_to_queue():
    print("\nTesting Function: 'direct_message_to_queue'")
    setup()
    try:
        res = publish.direct_message_to_queue(queue_name= "queue_rest_consumer",
                                              message= INPUT_MESSAGE,
                                              timeout=5)
        print("\nResponse:\n",res)
    except Exception as e:
        print(e)
    teardown()

def test_direct_message_for_topic():
    print("\nTesting Function: 'direct_message_for_queue'")
    setup()
    try:
        res = publish.direct_message_for_topic(topic_string= "my_topic",
                                               message= INPUT_MESSAGE,
                                               timeout=5)
        print("\nResponse:\n",res)
    except Exception as e:
        print(e)
    teardown()

def test_persistent_message_to_queue():
    print("\nTesting Function: 'persistent_message_to_queue'")
    setup()
    try:
        res = publish.persistent_message_to_queue(queue_name= "queue_rest_consumer",
                                                  message= INPUT_MESSAGE,
                                                  timeout=5,
                                                  request_reply= True)
        print("\nResponse:\n",res)
    except Exception as e:
        print(e)
    teardown()

def test_persistent_message_for_topic():
    print("\nTesting Function: 'persistent_message_for_topic'")
    setup()
    try:
        res = publish.persistent_message_for_topic(topic_string= "my_topic",
                                                   message= INPUT_MESSAGE,
                                                   timeout=5,
                                                   request_reply= True)
        print("\nResponse:\n",res)
    except Exception as e:
        print(e)
    teardown()

#Async functions
async def test_async_direct_message_to_queue():
    print("\nTesting Function: 'async_direct_message_to_queue'")
    setup()
    try:
        res = await publish.async_direct_message_to_queue(queue_name= "queue_rest_consumer",
                                                          message= INPUT_MESSAGE,
                                                          timeout=5)
        print("\nResponse:\n",res)
    except Exception as e:
        print(e)
    teardown()

async def test_async_direct_message_for_topic():
    print("\nTesting Function: 'async_direct_message_for_topic'")
    setup()
    try:
        res = await publish.async_direct_message_for_topic(topic_string= "my_topic",
                                                            message= INPUT_MESSAGE,
                                                            timeout=5)
        print("\nResponse:\n",res)
    except Exception as e:
        print(e)
    teardown()

async def test_async_persistent_message_to_queue():
    print("\nTesting Function: 'async_persistent_message_to_queue'")
    setup()
    try:
        res = await publish.async_persistent_message_to_queue(queue_name= "queue_rest_consumer",
                                                              message= INPUT_MESSAGE,
                                                              timeout=5,
                                                              request_reply= True)
        print("\nResponse:\n",res)
    except Exception as e:
        print(e)
    teardown()

async def test_async_persistent_message_for_topic():
    print("\nTesting Function: 'async_persistent_message_for_topic'")
    setup()
    try:
        res = await publish.async_persistent_message_for_topic(topic_string= "my_topic",
                                                               message= INPUT_MESSAGE,
                                                               timeout=5,
                                                               request_reply= True)
        print("\nResponse:\n",res)
    except Exception as e:
        print(e)
    teardown()


#Running all sync tests
test_direct_message_to_queue()
time.sleep(10)
test_direct_message_for_topic()
time.sleep(10)
test_persistent_message_to_queue()
time.sleep(10)
test_persistent_message_for_topic()
time.sleep(10)

#Running all async tests
asyncio.run(test_async_direct_message_to_queue())
time.sleep(15)
asyncio.run(test_async_direct_message_for_topic())
time.sleep(15)
asyncio.run(test_async_persistent_message_to_queue())
time.sleep(15)
asyncio.run(test_async_persistent_message_for_topic())










