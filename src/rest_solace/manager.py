from .http_client import HttpClient
from urllib.parse import urlsplit, urlunsplit

class Manager():
    
    def __init__(self, user_name:str, password:str,
                 host:str, semp_port:str= "8080", verify_ssl=False) -> None:
        """Class for creating a Manage object for communicating with a broker regarding management stuff.

        Args:
            username (str): Username of user with admin level access to the broker.
            password (str): Password for the username provided.
            host (str): Broker address (IPv4)
            SEMP_port (str): Management port used for management stuff on the broker side using Solace Element Management Protocol v2.
        """

        self.http_client = HttpClient(host= host,
                                      port= semp_port,
                                      user_name= user_name,
                                      password= password,
                                      verify_ssl= verify_ssl)


    #info
    
    def get_about_api(self, throw_exception= True)->dict:
        """This provides metadata about the SEMP API, such as the version of the API supported by the broker.

        Args:
            throw_exception (bool, optional): Throw exception incase request error code indicates an error. 
                                              Defaults to True.

        Returns:
            dict: Requested data.
        """

        endpoint = "/SEMP/v2/config/about/api"

        res = self.http_client.http_get(endpoint= endpoint)

        if throw_exception:
            res.raise_for_status()
        return res.json()


    #client profile

    
    def fetch_all_client_profiles(self, msgVpnName= "default", select= "*"):


        endpoint = f"/SEMP/v2/config/msgVpns/{msgVpnName}/clientProfiles?count=1&select={select}"

        data= list()
        links= list()
        
        res = self.http_client.http_get(endpoint= endpoint)
        res.raise_for_status()
        res = res.json()


        data.extend(res["data"])
        links.extend(res["links"])
             
        while True:
            paging_url= res['meta'].get('paging')

            if paging_url == None:
                break
            else:
                split= urlsplit(paging_url['nextPageUri'])
                endpoint= urlunsplit(("", "", split.path, split.query, split.fragment))

                res = self.http_client.http_get(endpoint)
                res.raise_for_status()
                res = res.json()

                data.extend(res["data"])
                links.extend(res["links"])
            
        return {"data":data, "links":links}

    def list_all_client_profiles(self, msgVpnName= "default")->list:

        data = self.fetch_all_client_profiles(select= "clientProfileName", msgVpnName= msgVpnName)["data"]
        names = [name["clientProfileName"] for name in data]

        return names

    def client_profile_exists(self, msgVpnName, clientProfileName)->bool:

        names= self.list_all_client_profiles(msgVpnName)
        return True if clientProfileName in names else False

    def update_client_profile(self, msgVpnName, clientProfileName= "default", 
                              allowGuaranteedMsgReceiveEnabled:bool= True,
                              allowGuaranteedMsgSendEnabled:bool= True,
                              throw_exception= True, **kwargs):

        #To change setting manually: 
        #select vpn, access_control tab -> user profiles tab -> <profile name> -> allow client to <setting>
        endpoint = f"/SEMP/v2/config/msgVpns/{msgVpnName}/clientProfiles/{clientProfileName}"
        
        body = {"msgVpnName": msgVpnName,
                "clientProfileName": clientProfileName,
                'allowGuaranteedMsgReceiveEnabled': allowGuaranteedMsgReceiveEnabled, #required for queue binding to work & guaranteed messaging.
                'allowGuaranteedMsgSendEnabled': allowGuaranteedMsgSendEnabled, #required for guaranteed messaging.
                }

        body = body | kwargs

        res = self.http_client.http_patch(endpoint= endpoint, payload= body)

        if throw_exception:
            res.raise_for_status()
        return res.json()


    #client username

    def update_client_username(self, msgVpnName, clientUsername= "default", 
                               enabled:bool= True,
                               throw_exception= True, **kwargs):
        #https://docs.solace.com/API-Developer-Online-Ref-Documentation/swagger-ui/software-broker/config/index.html#/clientUsername/updateMsgVpnClientUsername

        #To change setting manually: 
        #select vpn, access_control tab -> clint usernames tab -> <client user name> -> enable
        endpoint = f"/SEMP/v2/config/msgVpns/{msgVpnName}/clientUsernames/{clientUsername}"
        
        body = {'enabled': enabled}

        body = body | kwargs

        res = self.http_client.http_patch(endpoint= endpoint, payload= body)

        if throw_exception:
            res.raise_for_status()
        return res.json()



    # VPNs

    #Finished. Now need to give same options to fetch.
    def request_vpn_objects(self, count:int= 10, where= None, 
                            select= '*', opaquePassword= None,
                            throw_exception= True)->dict:
        """Get list of message VPNs and info regarding them based on specified parameters.
        
        Note: 
            This function directly passes parameters to an endpoint and could require the use of pagination to access all values.
            It is recommended that you use get_all_vpn_objects() function instead which grantees all info, but uses more bandwidth.

        For more info: 
            https://docs.solace.com/API-Developer-Online-Ref-Documentation/swagger-ui/software-broker/config/index.html#/msgVpn/getMsgVpns

        Args:
            count (int): Limits the number of objects in the response. default is 10.
                         Ideally your applications should always be written to handle pagination instead of massive counts.
            where (str): Specify that a response should include only objects that satisfy certain conditions.
                         Expects comma-separated list of expressions. 
                         All expressions must be true for the object to be included in the response.
                         For more info, consult: https://docs.solace.com/Admin/SEMP/SEMP-Features.htm#Filtering
            select (str): Select only certain attributes to return. 
                          Expects comma-separated list of attribute names.
                          Give value 'msgVpnName,enabled' to see only names and enabled status.
                          For more info, consult: https://docs.solace.com/Admin/SEMP/SEMP-Features.htm#Select
            opaquePassword (str): Password to retrieve attributes with the opaque property. 
            throw_exception (bool, optional): Throw exception incase request error code indicates an error. 
                                              Defaults to True.

        Returns:
            dict: Requested data.
        """

        endpoint = f"/SEMP/v2/config/msgVpns?count={str(count)}&select={select}"

        if where != None:
            endpoint+="&where={where}"

        if opaquePassword != None:
            endpoint+="&opaquePassword={opaquePassword}"

        res = self.http_client.http_get(endpoint= endpoint)
        
        if throw_exception:
            res.raise_for_status()
        return res.json()

    def fetch_all_vpn_objects(self, select= "*")->dict[list, list]:
        """Uses pagination to fetch and compile a list of all vpn objects.

        Args:
            select (str, optional): selection query. Defaults to "*".

        Returns:
            dict: list of pages
        """

        endpoint = f"/SEMP/v2/config/msgVpns?count=100&select={select}"

        data= list()
        links= list()
        
        res = self.http_client.http_get(endpoint= endpoint)
        res.raise_for_status()
        res = res.json()

        data.extend(res["data"])
        links.extend(res["links"])
             
        while True:
            paging_url= res['meta'].get('paging')

            if paging_url == None:
                break
            else:
                split= urlsplit(paging_url['nextPageUri'])
                endpoint= urlunsplit(("", "", split.path, split.query, split.fragment))

                res = self.http_client.http_get(endpoint)
                res.raise_for_status()
                res = res.json()

                data.extend(res["data"])
                links.extend(res["links"])
            
        return {"data":data, "links":links}

    def list_message_vpns(self)->list:

        data = self.fetch_all_vpn_objects(select="msgVpnName")["data"]
        names = [name["msgVpnName"] for name in data]

        return names

    def message_vpn_exists(self, msgVpnName)->bool:

        names= self.list_message_vpns()
        return True if msgVpnName in names else False

    def create_message_vpn(self, msgVpnName:str, enabled:bool= True, 
                           maxMsgSpoolUsage:int= 1500,
                           authenticationBasicEnabled:bool= True, 
                           authenticationBasicType:str= "none",
                           serviceRestIncomingPlainTextEnabled:bool= True,
                           serviceRestIncomingPlainTextListenPort:int= 0,
                           serviceRestMode:str= "messaging",
                           throw_exception= True, **kwargs):
        """Create a new VPN on the broker.

        For more info:
            https://docs.solace.com/API-Developer-Online-Ref-Documentation/swagger-ui/software-broker/config/index.html#/msgVpn/createMsgVpn

        Args:
            msgVpnName (str): Name for the new vpn.
            enabled (bool): enable or disable the vpn.
            authenticationBasicEnabled (bool): Basic authentication is authentication that involves 
                                               the use of a username and password to prove identity.
            authenticationBasicType (str): The type of basic authentication to use for clients connecting to the Message VPN. Can be one of:
                                            1) "internal" - Internal database. Authentication is against Client Usernames.
                                            2) "ldap" - LDAP authentication. An LDAP profile name must be provided.
                                            3) "radius" - RADIUS authentication. A RADIUS profile name must be provided.
                                            4) "none" - No authentication. Anonymous login allowed.

            serviceRestIncomingPlainTextEnabled (bool): Enable or disable the plain-text REST service for incoming clients in the Message VPN.
            serviceRestIncomingPlainTextListenPort (int): The port number for incoming plain-text REST clients that connect to the Message VPN. 
                                                          The port must be unique across the message backbone. 
                                                          A value of 0 means that the listen-port is unassigned and cannot be enabled.
            serviceRestMode (str): The REST service mode for incoming REST clients that connect to the Message VPN. The options are:
                                    1) "messaging" - Act as a message broker on which REST messages are queued.
                                    2) "gateway" - Act as a message gateway through which REST messages are propagated.

        Returns:
            _type_: _description_
        """

        endpoint = f"/SEMP/v2/config/msgVpns"

        body = {"msgVpnName": msgVpnName,
                "enabled": enabled,
                "authenticationBasicEnabled": authenticationBasicEnabled,
                "authenticationBasicType": authenticationBasicType,
                "maxMsgSpoolUsage": maxMsgSpoolUsage,
                "serviceRestIncomingPlainTextEnabled": serviceRestIncomingPlainTextEnabled,
                "serviceRestIncomingPlainTextListenPort": serviceRestIncomingPlainTextListenPort,
                "serviceRestMode": serviceRestMode
                }

        body = body | kwargs

        res = self.http_client.http_post(endpoint= endpoint, payload= body)

        if throw_exception:
            res.raise_for_status()
        return res.json()

    def delete_message_vpn(self, msgVpnName:str, throw_exception= True)->dict:
        endpoint = f"/SEMP/v2/config/msgVpns/{msgVpnName}"

        res = self.http_client.http_delete(endpoint= endpoint)

        if throw_exception:
            res.raise_for_status()
        return res.json()


    # Topic endpoint
    
    def create_topic_endpoint(self, topicEndpointName:str, msgVpnName:str= "default", throw_exception:bool= True, **kwargs) -> dict:
        """Create a topic endpoint to receive messages. 
           A topic endpoint attracts messages published to a topic for which the topic endpoint has a subscriber asking for messages with that topic. 
           They can only be used by subscribers created using Solace Java Message Service (JMS). You cannot subscribe to them using a REST server.

        WARNING: 
            In solace, the concepts of "topic endpoint" and just "topic" are 2 different things!!
            The "topic" for "topic endpoints" is defined by the subscriber who will subscribe to this topic, 
            unlike "queue endpoint" where the "topic" can be defined through the solace broker webUI or a management port. 
            This library does not support subscribing to a topic endpoint.
            

        Args:
            topicEndpointName (str): The Name that you wish to assign to your new topic end point.
            msgVpnName (str, optional): Name of the VPN within which you wish your topic endpoint to exist in. Defaults to "default".
            throw_exception (bool, optional): Throw exception if the response code indicates an error. Defaults to True.
        
        **kwargs: 
            Support for some kwargs parameters may vary between the different versions of solace broker. Consult the docs for this end point to know more:
            solace.com/API-Developer-Online-Ref-Documentation/swagger-ui/software-broker/config/index.html#/topicEndpoint/createMsgVpnTopicEndpoint

        Returns:
            dict: HTTP response converted to json format.
        """
        
        endpoint = f"/SEMP/v2/config/msgVpns/{msgVpnName}/topicEndpoints"

        body = {"msgVpnName": msgVpnName,
                "topicEndpointName": topicEndpointName}

        body = body | kwargs

        res = self.http_client.http_post(endpoint= endpoint, payload= body)

        if throw_exception:
            res.raise_for_status()
        return res.json()
    

    # Queue endpoint

    def create_queue_endpoint(self, queueName:str, msgVpnName:str= "default", ingressEnabled:bool= True, egressEnabled:str= True,
                              permission:str= "consume", respectTtlEnabled= True, throw_exception:bool= True, **kwargs) -> dict:
        """Create a queue endpoint to receive messages. 

        Args:
            queueName (str): The Name that you wish to assign to your new queue end point.
            msgVpnName (str, optional): Name of the VPN within which you wish your queue endpoint to exist in. Defaults to "default".
            ingressEnabled (bool, optional): Enable or disable the reception of messages to the Queue.
            egressEnabled (bool, optional): Enable or disable the transmission of messages from the Queue.
            permission (str, optional): The permission level for all consumers of the Queue, excluding the owner.
            respectTtlEnabled (str, optional): Enable or disable the respecting of the time-to-live (TTL) for messages in the Queue. 
                                               When enabled, expired messages are discarded or moved to the DMQ.
                                               Defaults to True.
            throw_exception (bool, optional): Throw exception if the response code indicates an error. Defaults to True.
        
        **kwargs: 
            Support for some kwargs parameters may vary between the different versions of solace broker. 
            Consult the docs for this end point to know more:
            https://docs.solace.com/API-Developer-Online-Ref-Documentation/swagger-ui/software-broker/config/index.html#/queue/createMsgVpnQueue

        Returns:
            dict: HTTP response converted to json format.
        """
        
        endpoint = f"/SEMP/v2/config/msgVpns/{msgVpnName}/queues"

        body = {"msgVpnName": msgVpnName,
                "queueName": queueName,
                "ingressEnabled": ingressEnabled,
                "egressEnabled": egressEnabled,
                "permission": permission,
                "respectTtlEnabled": respectTtlEnabled
                }

        body = body | kwargs

        res = self.http_client.http_post(endpoint= endpoint, payload= body)

        if throw_exception:
            res.raise_for_status()
        return res.json()
    
    def delete_queue_endpoint(self, queueName:str, msgVpnName:str= "default", throw_exception:bool= True)->dict:
        endpoint = f"/SEMP/v2/config/msgVpns/{msgVpnName}/queues/{queueName}"

        res = self.http_client.http_delete(endpoint= endpoint)

        if throw_exception:
            res.raise_for_status()
        return res.json()

    def subscribe_to_topic_on_queue(self, subscriptionTopic:str, queueName:str, 
                                    msgVpnName:str= "default", throw_exception:bool= True) -> dict:
        """Subscribe to a topic on a queue endpoint. 
        Any messages published with the given topic will end up accumulating in the given queue.
        
        Args:
            subscriptionTopic (str): Name of the topic you wish to subscribe to.
            queueName (str): The name the queue endpoint where the subscription will take place.
            msgVpnName (str, optional): Name of the VPN within which your queue exists. Defaults to "default".
            throw_exception (bool, optional): Throw exception if the response code indicates an error. Defaults to True.
        
        Returns:
            dict: HTTP response converted to json format.
        """
        
        endpoint = f"/SEMP/v2/config/msgVpns/{msgVpnName}/queues/{queueName}/subscriptions"

        body = {"subscriptionTopic": subscriptionTopic,
                "queueName": queueName,
                "msgVpnName": msgVpnName,
                }

        res = self.http_client.http_post(endpoint= endpoint, payload= body)

        if throw_exception:
            res.raise_for_status()
        return res.json()


    # RDP stuff

    def create_rest_delivery_point(self, restDeliveryPointName:str, enabled:str= True, service:str= "REST", vendor:str= "Custom",
                                   clientProfileName:str= 'default', msgVpnName:str= "default", throw_exception:bool= True) -> dict:
        """Create a REST delivery point. A REST Delivery Point manages delivery of messages from queues to a named list of REST Consumers (subscribers).

        Args:
            restDeliveryPointName (str): Name of the new REST delivery point.
            enabled (str, optional): Enable or disable the REST Delivery Point. Defaults to True.
            service (str, optional): The name of the service that this REST Delivery Point connects to. Internally the broker does not use this value; it is informational only. Defaults to "REST".
            vendor (str, optional): The name of the vendor that this REST Delivery Point connects to. Internally the broker does not use this value; it is informational only. Defaults to "Custom".
            clientProfileName (str, optional): Client Profiles are used to assign common configuration properties to clients that have been successfully authorized. Defaults to 'default'.
            msgVpnName (str, optional): Name of the VPN within which you wish your REST delivery point to exist in. Defaults to "default".
            throw_exception (bool, optional): Throw exception if the response code indicates an error. Defaults to True.

        Returns:
            dict: HTTP response converted to json format.
        """
        
        endpoint = f"/SEMP/v2/config/msgVpns/{msgVpnName}/restDeliveryPoints"

        body = {"restDeliveryPointName": restDeliveryPointName,
                "msgVpnName": msgVpnName,
                'enabled': enabled,
                'service': service,
                'vendor': vendor,
                'clientProfileName': clientProfileName
                }

        res = self.http_client.http_post(endpoint= endpoint, payload= body)

        if throw_exception:
            res.raise_for_status()
        return res.json()
    
    def delete_rest_delivery_point(self, restDeliveryPointName:str, msgVpnName:str= "default", throw_exception:bool= True) -> dict:
            
        endpoint = f"/SEMP/v2/config/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}"

        res = self.http_client.http_delete(endpoint= endpoint)

        if throw_exception:
            res.raise_for_status()
        return res.json()

    def specify_rest_consumer(self, restDeliveryPointName:str, restConsumerName:str, remoteHost:str, 
                              remotePort:int, enabled:str= True, msgVpnName:str= "default", 
                              tlsEnabled:bool= False, throw_exception:bool= True, **kwargs) -> dict:
        """Specify a new rest consumer (subscriber) to add to the list of consumers within a REST delivery point. 
        When an incoming message is received in a queue, a queue binding object then sends the messages to the specified Consumers through the REST delivery point.
        Here we specify mainly the host and port of the consumer, along with a name for convince.

        Args:
            restDeliveryPointName (str): Name of the REST delivery point where you wish to specify the new consumer.
            msgVpnName (str, optional): Name of the VPN within which you wish your REST delivery point to exist in. Defaults to "default".
            throw_exception (bool, optional): Throw exception if the response code indicates an error. Defaults to True.

        **kwargs: 
            Support for some kwargs parameters may vary between the different versions of solace broker. Consult the docs for this end point to know more:
            https://docs.solace.com/API-Developer-Online-Ref-Documentation/swagger-ui/software-broker/config/index.html#/all/createMsgVpnRestDeliveryPointRestConsumer


        Returns:
            dict: HTTP response converted to json format.
        """
        
        endpoint = f"/SEMP/v2/config/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/restConsumers"

        body = {"restDeliveryPointName": restDeliveryPointName,
                "msgVpnName": msgVpnName,
                "restConsumerName": restConsumerName,
                "remoteHost": remoteHost,
                "remotePort": remotePort,
                "enabled": enabled,
                "tlsEnabled": tlsEnabled
                }
        
        body = body | kwargs

        res = self.http_client.http_post(endpoint= endpoint, payload= body)

        if throw_exception:
            res.raise_for_status()
        return res.json()
    
    def create_queue_binding(self, restDeliveryPointName:str, queueBindingName:str, postRequestTarget:str= "/",
                             requestTargetEvaluation:str= "none", msgVpnName:str= "default", throw_exception:bool= True) -> dict:
        """A Queue Binding for a REST Delivery Point attracts messages to be delivered to REST consumers.

        Note:
            If the queue does not exist it can be created subsequently.
            Also, for more info in this endpoint, visit: https://docs.solace.com/API-Developer-Online-Ref-Documentation/swagger-ui/software-broker/config/index.html#/all/createMsgVpnRestDeliveryPointQueueBinding

        Args:
            restDeliveryPointName (str): Name of the REST delivery point where you wish to bind a queue to a consumer.
            queueBindingName (str): Name of the queue which you wish to bind to a REST consumer.
            postRequestTarget (str, optional): The request-target string to use when sending requests.
            requestTargetEvaluation (str, optional): The type of evaluation to perform on the request target. Defaults to "none".
            msgVpnName (str, optional): Name of the VPN within which you wish your queue binding to exist in. Defaults to "default".
            throw_exception (bool, optional): Throw exception if the response code indicates an error. Defaults to True.. Defaults to True.

        Returns:
            dict: HTTP response converted to json format.
        """
        
        endpoint = f"/SEMP/v2/config/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}/queueBindings"

        body = {"restDeliveryPointName": restDeliveryPointName,
                "queueBindingName": queueBindingName,
                "postRequestTarget": postRequestTarget,
                "gatewayReplaceTargetAuthorityEnabled": False, #Only applicable in Rest Gateway mode
                "msgVpnName": msgVpnName,
                "requestTargetEvaluation": requestTargetEvaluation
                }

        res = self.http_client.http_post(endpoint= endpoint, payload= body)

        if throw_exception:
            res.raise_for_status()
        return res.json()

    def restart_rest_delivery_point(self, restDeliveryPointName:str, msgVpnName:str= "default"):

        endpoint = f"/SEMP/v2/config/msgVpns/{msgVpnName}/restDeliveryPoints/{restDeliveryPointName}"

        #disable rdp
        self.http_client.http_patch(endpoint= endpoint, payload= {'enabled': False})

        #enable rdp
        self.http_client.http_patch(endpoint= endpoint, payload= {'enabled': True})


    #miscellaneous 

    def auto_rest_messaging_setup_utility(self, msgVpnName:str, queueName:str, subscriptionTopic:str|None, 
                                          restDeliveryPointName:str, restConsumerName:str,
                                          remoteHost:str, remotePort:int, postRequestTarget='/',
                                          clientProfileName= "default", clientUsername= "default")->None:
        """
        A single utility function that automatically sets up a queue for you that is ready to communicate with your consumer out of the box!!
        Makes it so that you can start sending messages after running just this one function.
        
        Note: 
            * Requires a message VPN set to messaging mode.
            * All brokers come with a default messaging VPN named "default". 
            * The default VPN is already set to messaging mode.
            * Before running this function, it is advised to bring up your consumer in the background.
    
        It performs the following steps:
            0) Updates VPN parameters to allow sending and receiving persistent messages.
            1) Create a new queue with input output enabled and permission to be used by consumers.\n
            2) Have the queue subscribe to a new topic (optional).\n
            3) Create a new rest delivery endpoint to manage rest message delivery.\n
            4) Register your consumer to the rest delivery endpoint.\n
            5) Register a queue binding in your rest delivery endpoint to bind your queue to your consumer.\n

            
        Args:
            msgVpnName (str): The message VPN where your setup will be done. 
            queueName (str|None): Name for new queue where the setup will be done. 
            subscriptionTopic (str): Name of a topic you want your queue to subscribe to. This is recommended but optional. To skip pass None.
            restDeliveryPointName (str): Name for your new rest delivery endpoint to manage rest message delivery.
            restConsumerName (str): Assign a rest consumer to your rest delivery endpoint with the given name. This name is just for your reference.
            remoteHost (str): IPv4 address at which your consumer is running at.
            remotePort (int): The port that your consumer uses to listen for incoming messages.
            postRequestTarget (str): The rest endpoint on the consumer side that will be targeted when sending the message.
            clientProfileName (str, optional): Client Profiles are used to assign common configuration properties to clients that have been successfully authorized. Defaults to 'default'.
            clientUsername (str, optional): A client is only authorized to connect to a Message VPN that is associated with a Client Username that the client has been assigned.
        """

        #step0
        self.update_client_profile(msgVpnName= msgVpnName, clientProfileName= clientProfileName)
        self.update_client_username(msgVpnName= msgVpnName, clientUsername= clientUsername)

        #step1
        self.create_queue_endpoint(queueName=queueName, msgVpnName=msgVpnName, throw_exception= False)

        #step2
        if subscriptionTopic != None:
            self.subscribe_to_topic_on_queue(msgVpnName= msgVpnName,
                                             subscriptionTopic= subscriptionTopic,
                                             queueName= queueName)
            
        #step3
        res = self.create_rest_delivery_point(msgVpnName= msgVpnName, 
                                              restDeliveryPointName= restDeliveryPointName, 
                                              throw_exception=False,
                                              clientProfileName= clientProfileName)
        #print(res)

        #step4
        res = self.specify_rest_consumer(msgVpnName= msgVpnName, 
                                         restDeliveryPointName= restDeliveryPointName,
                                        restConsumerName= restConsumerName,
                                        remoteHost= remoteHost,
                                        remotePort= remotePort, throw_exception= False)
        
        #print(res)
        
        # #step5
        res = self.create_queue_binding(msgVpnName= msgVpnName,
                                        restDeliveryPointName= restDeliveryPointName,
                                        queueBindingName= queueName,
                                        postRequestTarget= postRequestTarget, throw_exception= False)
        
        #print(res)

    def update_parameters(self, user_name:str, password:str,
                        host:str, SEMP_port:str, verify_ssl=False):
    
        self.http_client = HttpClient(host= host,
                                      port= SEMP_port,
                                      user_name= user_name,
                                      password= password,
                                      verify_ssl= verify_ssl)
    
