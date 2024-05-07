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
                      SEMP_port= SEMP_PORT)

publish_obj = MessagingPublisher(user_name="admin", password="admin", 
                                 host= SEMP_HOST, REST_VPNport=NEW_VPN_PORT)

print("Setting up Message VPN, queue endpoint, and RDP.")

res = manager.create_message_vpn(msgVpnName= NEW_VPN_NAME,
                                 serviceRestIncomingPlainTextListenPort= NEW_VPN_PORT)

res = manager.auto_rest_messaging_setup_utility(msgVpnName= NEW_VPN_NAME, queueName= 'queue_rest_consumer', subscriptionTopic=None, 
                                                        restDeliveryPointName='myRDP', restConsumerName='myConsumer', 
                                                        remoteHost= CONSUMER_HOST, remotePort= CONSUMER_PORT)

#Run consumer function separately in the background

print("Publishing messages.")
#Add Test here
try:
    res = publish_obj.publishToQueueEndpoint(queue_name= 'queue_rest_consumer',
                                        message= "hello world",
                                        delivery_mode= "persistent",
                                        DMQ_eligible= True,
                                        throw_exception=False)

    print(res)

except Exception as e:
    print(e)



#Step5: cleanup
print("\nCleaning up (deleting vpn)")

manager.delete_queue_endpoint(msgVpnName= NEW_VPN_NAME, queueName= 'queue_rest_consumer')
manager.delete_rest_delivery_point(msgVpnName= NEW_VPN_NAME, restDeliveryPointName= 'myRDP')
manager.delete_message_vpn(msgVpnName= NEW_VPN_NAME)

