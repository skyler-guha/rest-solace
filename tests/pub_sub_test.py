from rest_solace import Manager, MessagingPublisher, Consumer
from util import get_timestamp
from consumer_test import return_uppercase
import threading

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

#Step1: setup broker to send and receive messages
print("Setting up Message VPN, queue endpoint, and RDP.")

res = manager.create_message_vpn(msgVpnName= NEW_VPN_NAME,
                                 serviceRestIncomingPlainTextListenPort= NEW_VPN_PORT)

res = manager.auto_rest_messaging_setup_utility(msgVpnName= NEW_VPN_NAME, queueName= 'queue_rest_consumer', subscriptionTopic=None, 
                                                        restDeliveryPointName='myRDP', restConsumerName='myConsumer', 
                                                        remoteHost= CONSUMER_HOST, remotePort= CONSUMER_PORT)

#Step2: setup consumer in the background to return message in uppercase
print("\nStarting consumer to receive messages")

args = ("127.0.0.1", 5000, return_uppercase, False, True)

consumer_thread = threading.Thread(target= consumer_obj.startConsumer, name="test_consumer", args= args)
consumer_thread.start()

#Step3: restart RDP 
print("\nRestarting RDP")

manager.restart_rest_delivery_point(restDeliveryPointName= "myRDP", 
                                    msgVpnName= NEW_VPN_NAME)

#Step4: setup publisher, publish a message, and get response
print("\nPublishing a message and waiting for uppercase response\nSending message:", INPUT_MESSAGE)

res = publish.persistent_message_to_queue(queue_name="queue_rest_consumer", 
                                          message= INPUT_MESSAGE,
                                          request_reply= True,
                                          time_to_live= 10000 #waits 1 min
                                         )

print("\nResponse:\n",res)

if res.get('content') == EXPECTED_OUTPUT_MESSAGE:
    print("\nTest was a Success")
else:
    print("\nTest was a Failure")


#Step5: cleanup
print("\nCleaning up (deleting vpn)")

manager.delete_queue_endpoint(msgVpnName= NEW_VPN_NAME, queueName= 'queue_rest_consumer')
manager.delete_rest_delivery_point(msgVpnName= NEW_VPN_NAME, restDeliveryPointName= 'myRDP')
manager.delete_message_vpn(msgVpnName= NEW_VPN_NAME)



