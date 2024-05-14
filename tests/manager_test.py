"""
This script is for testing the manager class.

This is a manual sequential test with some inspiration from unit tests.
"""
from rest_solace import Manager
import logging
from util import testCount, get_timestamp

SEMP_HOST= "172.17.0.1"
SEMP_PORT= "8080"
SEMP_USERNAME= "admin"
SEMP_PASSWORD= "admin"

NEW_VPN_NAME= "test_vpn_"+get_timestamp()
NEW_VPN_PORT=  6969

log = logging.getLogger("Manager_Test")
logging.basicConfig(level=logging.INFO)


count= testCount(title="#Manager test", total_tests= 11)


#Testing getting an instance of manager class
try:
    count.add_count()
    manager = Manager(user_name= SEMP_USERNAME, 
                      password= SEMP_PASSWORD, 
                      host= SEMP_HOST, 
                      semp_port= SEMP_PORT)
    log.info("Testing the creation of manager instance: PASS\n")
    count.passed()
except Exception as e:
    count.failed()
    log.error("Testing the creation of manager instance: FAIL")
    print("Stopping test early as unable to create instance of manager class")
    print(count.get_stats())
    log.error("Error str: "+str(e))
    exit(1)



#Testing "get_about_api" function
try:
    count.add_count()
    res = manager.get_about_api()
    log.info("Function 'get_about_api': PASS")  
    log.info(str(res)+'\n')
    count.passed()
except Exception as e:
    count.failed()
    log.info("Function 'get_about_api': FAIL")  
    log.error("Error str: "+str(e))


#Testing "fetch_all_vpn_objects" function
try:
    count.add_count()
    res = manager.fetch_all_vpn_objects()
    log.info("Function 'fetch_all_vpn_objects': PASS")  
    log.info(str(res)+'\n')
    count.passed()
except Exception as e:
    count.failed()
    log.info("Function 'fetch_all_vpn_objects': FAIL")  
    log.error("Error str: "+str(e))


#Testing "list_message_vpns" function
try:
    count.add_count()
    res = manager.list_message_vpns()
    log.info("Function 'list_message_vpns': PASS") 
    log.info(str(res)+'\n') 
    count.passed()
except Exception as e:
    count.failed()
    log.info("Function 'list_message_vpns': FAIL")  
    log.error("Error str: "+str(e))


#Testing "fetch_all_client_profiles" function
try:
    count.add_count()
    res = manager.fetch_all_client_profiles(msgVpnName= "default")
    log.info("Function 'fetch_all_client_profiles': PASS") 
    log.info(str(res)+'\n') 
    count.passed()
except Exception as e:
    count.failed()
    log.info("Function 'fetch_all_client_profiles': FAIL")  
    log.error("Error str: "+str(e))

#Testing "list_all_client_profiles" function
try:
    count.add_count()
    res = manager.list_all_client_profiles("default")
    log.info("Function 'list_all_client_profiles': PASS") 
    log.info(str(res)+'\n') 
    count.passed()
except Exception as e:
    count.failed()
    log.info("Function 'list_all_client_profiles': FAIL")  
    log.error("Error str: "+str(e))

#Testing "client_profile_exists" function
try:
    count.add_count()
    res = manager.client_profile_exists(msgVpnName= "default", clientProfileName= "default")
    log.info("Function 'client_profile_exists': PASS") 
    log.info(str(res)+'\n') 
    count.passed()
except Exception as e:
    count.failed()
    log.info("Function 'client_profile_exists': FAIL")  
    log.error("Error str: "+str(e))
   
#Creating a new vpn and doing tests inside it
try:
    #Testing "create_message_vpn" function
    count.add_count()
    res = manager.create_message_vpn(msgVpnName= NEW_VPN_NAME,
                                    serviceRestIncomingPlainTextListenPort= NEW_VPN_PORT)
    log.info("Function 'create_message_vpn': PASS") 
    log.info(str(res)+'\n')
    count.passed()

    #Testing "auto_rest_messaging_setup_utility" function. 
    #Uses: create_queue_endpoint, subscribe_to_topic_on_queue, create_rest_delivery_point, specify_rest_consumer, & create_queue_binding
    try:
        count.add_count()
        res = manager.auto_rest_messaging_setup_utility(msgVpnName= NEW_VPN_NAME, queueName= 'queue_rest_consumer', subscriptionTopic=None, 
                                                        restDeliveryPointName='myRDP', restConsumerName='myConsumer', 
                                                        remoteHost= "127.0.0.1", remotePort= 5000)
        log.info("Function 'auto_rest_messaging_setup_utility': PASS") 
        log.info(str(res)+'\n')
        count.passed()

        #Testing "update_client_profile" function
        try:
            count.add_count()
            res = manager.update_client_profile(msgVpnName= NEW_VPN_NAME, 
                                                clientProfileName= "default",
                                                allowGuaranteedMsgReceiveEnabled= True, 
                                                allowGuaranteedMsgSendEnabled= True)
            
            log.info("Function 'update_client_profile': PASS") 
            log.info(str(res)+'\n')
            count.passed()
        except Exception as e:
            count.failed()
            log.info("Function 'update_client_profile': FAIL")  
            log.error("Error str: "+str(e))

        #Testing "delete_queue_endpoint" function
        try:
            count.add_count()
            res = manager.delete_queue_endpoint(msgVpnName= NEW_VPN_NAME, queueName= 'queue_rest_consumer')
            log.info("Function 'delete_queue_endpoint': PASS") 
            log.info(str(res)+'\n')
            count.passed()
        except Exception as e:
            count.failed()
            log.info("Function 'delete_queue_endpoint': FAIL")  
            log.error("Error str: "+str(e))

        #Testing "delete_rest_delivery_point" function
        try:
            count.add_count()
            res = manager.delete_rest_delivery_point(msgVpnName= NEW_VPN_NAME, restDeliveryPointName= 'myRDP')
            log.info("Function 'delete_rest_delivery_point': PASS") 
            log.info(str(res)+'\n')
            count.passed()
        except Exception as e:
            count.failed()
            log.info("Function 'delete_rest_delivery_point': FAIL")  
            log.error("Error str: "+str(e))

    except Exception as e:
        count.failed()
        log.info("Function 'auto_rest_messaging_setup_utility': FAIL")  
        log.error("Error str: "+str(e))

except Exception as e:
    count.failed()
    log.info("Function 'create_message_vpn': FAIL")  
    log.error("Error str: "+str(e))


#Testing "delete_message_vpn" function
try:
    count.add_count()
    res = manager.delete_message_vpn(msgVpnName= NEW_VPN_NAME)
    count.passed()
    log.info("Function 'delete_message_vpn': PASS")  
    log.info(str(res)+'\n')
except Exception as e:
    count.failed()
    log.info("Function 'delete_message_vpn': FAIL")
    log.warning("Deleting the testing VPN failed. Kindly delete it manually if it exists before starting the test again.")
    log.error("Error str: "+str(e))


print(count.get_stats())