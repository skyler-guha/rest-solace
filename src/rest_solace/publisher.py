from .http_client import HttpClient
from requests.exceptions import ReadTimeout

class MessagingPublisher():
    
    def __init__(self, user_name:str, password:str,
                 host:str, REST_VPNport:str, verify_ssl=False) -> None:
        """Class for creating a Publisher object for communicating with a broker to publish a message in Messaging mode.

        Args:
            username (str): Username of user with admin level access to the broker.
            password (str): Password for the username provided.
            host (str): Broker address (IPv4)
            REST_VPNport (str): The port assigned on your vpn of interest where you wish to send messages through REST messaging.
                                We use this port so specify which VPN we wish to send our messages to.
        """

        self.http_client = HttpClient(host= host,
                                      port= REST_VPNport,
                                      user_name= user_name,
                                      password= password,
                                      verify_ssl= verify_ssl)
        
    def update_parameters(self, user_name:str, password:str,
                          host:str, REST_VPNport:str, verify_ssl=False):
        """Update parameters used to connect with the broker.

        Args:
            username (str): Username of user with admin level access to the broker.
            password (str): Password for the username provided.
            host (str): Broker address (IPv4)
            REST_VPNport (str): The port assigned on your vpn of interest where you wish to send messages through REST messaging.
                                We use this port so specify which VPN we wish to send our messages to.        """
        
        self.http_client = HttpClient(host= host,
                                      port= REST_VPNport,
                                      user_name= user_name,
                                      password= password,
                                      verify_ssl= verify_ssl)

    def publishToQueueEndpoint(self, queue_name:str, message:str, delivery_mode:str= "direct", 
                                reply_to_queue:str|None= None, reply_for_topic:str|None= None, 
                                time_to_live:int|None= None, DMQ_eligible:bool= False,
                                timeout:str|None= 120, throw_exception:bool= False)->dict:
        
        """Publish a message to a queue endpoint.

        Args:
            queue_name (str): Name of the queue endpoint you wish to publish to.
            message (str): The message you wish to send.
            delivery_mode (str, optional): Mode of delivery for sending a message. 
                                           'direct' for sending messages without expecting a reply.
                                           'persistent' for getting a reply from the consumer to confirm if the message was received.
                                           Defaults to "direct".
            reply_to_queue (str | None, optional): After the message is received by the consumer, 
                                                   chose which queue the consumer reply will go to if provided.
                                                   The value must be the name of a queue.
                                                   Only works in 'direct' delivery_mode.
                                                   Defaults to None.
            reply_for_topic (str | None, optional): After the message is received by the consumer, 
                                                    chose which topic string the consumer reply will go to if provided.
                                                    The value must be a topic string (NOT the name of a topic endpoint).
                                                    Only works in 'direct' delivery_mode.
                                                    Defaults to None.
            time_to_live (int | None, optional): Lifetime for a guaranteed message (in milliseconds). 
                                                 If the message is not delivered by this time limit,
                                                 it is either discarded from the queue or moved to dead message queue if eligible.
                                                 Only works in 'persistent' delivery_mode.
                                                 Defaults to None.
            DMQ_eligible (bool, optional): Set the message as eligible for a Dead Message Queues (DMQ). 
                                           Only works in 'persistent' delivery_mode.
                                           Defaults to False.
            timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
            throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                              Defaults to False.

        Raises:
            ValueError: Can only select either 'reply_to_queue' or 'reply_for_topic', not both.
            ValueError: Cannot select 'reply_to_queue' or 'reply_for_topic' options when delivery_mode = 'persistent'
            ValueError: 'delivery_mode' parameter can only be 'direct' or 'persistent'
            HTTPError: Return code for request indicates an error

        Returns:
            dict: Dictionary containing request information and {'timeout':False}.
                  Incase timeout is reached, returned dictionary only contains {'timeout':True}.
        """

        endpoint = f"/QUEUE/{queue_name}"

        headers = {'Content-Type': 'text/plain'}

        if delivery_mode == 'direct':

            headers['Solace-Delivery-Mode'] = 'direct'

            if reply_to_queue == None and reply_for_topic == None:
                pass
            elif reply_to_queue != None and reply_for_topic != None:
                raise ValueError("Can only select either 'reply_to_queue' or 'reply_for_topic', not both.")
            elif reply_to_queue != None:
                headers['Solace-Reply-To-Destination'] = f"/QUEUE/{reply_to_queue}"
            else:
                headers['Solace-Reply-To-Destination'] = f"/TOPIC/{reply_for_topic}"

        elif delivery_mode == 'persistent':

            headers['Solace-Delivery-Mode'] = 'persistent'
            headers['Solace-Reply-Wait-Time-In-ms'] = "FOREVER" #specifies to broker that reply is expected

            if time_to_live != None:
                headers['Solace-Time-To-Live-In-ms'] = str(time_to_live) #Time after which the message is removed from queue.

            if DMQ_eligible != None:
                headers['Solace-DMQ-Eligible'] = 'true' if DMQ_eligible == True else 'false'

            if (reply_to_queue != None) or (reply_for_topic != None):
                raise ValueError("Cannot select 'reply_to_queue' or 'reply_for_topic' options when delivery_mode = 'persistent'")
        
        else:
            raise ValueError("'delivery_mode' parameter can only be 'direct' or 'persistent'")
            
        res = None
        try:
            res = self.http_client.http_post(endpoint= endpoint, payload= message, headers= headers, timeout=timeout)
        except ReadTimeout as e:
            if throw_exception == True:
                raise e
            else:
                return {'timeout':True} 
        

        if res != None:
            if throw_exception:
                res.raise_for_status()
            return {"status_code":res.status_code, "headers":res.headers, 
                    "content":res.content, 'timeout':False}
        

    def publishForTopic(self, topic_string:str, message:str, delivery_mode:str= "direct", 
                        reply_to_queue:str|None= None, reply_for_topic:str|None= None, 
                        time_to_live:int|None= None, DMQ_eligible:bool= False,
                        timeout:str|None= 120, throw_exception:bool= False)->dict:

        """Publish a message for a specific topic. 
        A topic is a string that allows for attracting specific messages to specific endpoints.
        Endpoints subscribe to a specific topic string and messages with matching strings go to those endpoints.
        Learn more at: https://docs.solace.com/Get-Started/what-are-topics.htm   

        Note: 
            This is not to be confused with publishing to a topic endpoint.
            Publishing directly to a topic endpoint is not possible anyway,
            and topic endpoints only receive messages through the topic they are subscribed to.
            Also, the topic-string a topic endpoint is subscribed to cannot be configured manually and
            is defined by the subscriber subscribing to the topic endpoint.
            This library does not support subscribing to a topic endpoint.

        Args:
            topic_string (str): A string used to attract published messages. It can contain wildcards to match with multiple sub topic-strings.
            message (str): The message you wish to send.
            delivery_mode (str, optional): Mode of delivery for sending a message. 
                                           'direct' for sending messages without expecting a reply.
                                           'persistent' for getting a reply from the consumer to confirm if the message was received.
                                           Defaults to "direct".
            reply_to_queue (str | None, optional): After the message is received by the consumer, 
                                                   chose which queue the consumer reply will go to if provided.
                                                   The value must be the name of a queue.
                                                   Only works in 'direct' delivery_mode.
                                                   Defaults to None.
            reply_for_topic (str | None, optional): After the message is received by the consumer, 
                                                    chose which topic string the consumer reply will go to if provided.
                                                    The value must be a topic string (NOT the name of a topic endpoint).
                                                    Only works in 'direct' delivery_mode.
                                                    Defaults to None.
            time_to_live (int | None, optional): Lifetime for a guaranteed message (in milliseconds). 
                                                 If the message is not delivered by this time limit,
                                                 it is either discarded from the queue or moved to dead message queue if eligible.
                                                 Only works in 'persistent' delivery_mode.
                                                 Defaults to None.
            DMQ_eligible (bool, optional): Set the message as eligible for a Dead Message Queues (DMQ). 
                                           Only works in 'persistent' delivery_mode.
                                           Defaults to False.
            timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
            throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                              Defaults to False.

        Raises:
            ValueError: Can only select either 'reply_to_queue' or 'reply_for_topic', not both.
            ValueError: Cannot select 'reply_to_queue' or 'reply_for_topic' options when delivery_mode = 'persistent'
            ValueError: 'delivery_mode' parameter can only be 'direct' or 'persistent'
            HTTPError: Return code for request indicates an error

        Returns:
            dict: Dictionary containing request information and {'timeout':False}.
                  Incase timeout is reached, returned dictionary only contains {'timeout':True}.
        """

        endpoint = f"/TOPIC/{topic_string}"

        headers = {'Content-Type': 'text/plain'}

        if delivery_mode == 'direct':

            headers['Solace-Delivery-Mode'] = 'direct'

            if reply_to_queue == None and reply_for_topic == None:
                pass
            elif reply_to_queue != None and reply_for_topic != None:
                raise ValueError("Can only select either 'reply_to_queue' or 'reply_for_topic', not both.")
            elif reply_to_queue != None:
                headers['Solace-Reply-To-Destination'] = f"/QUEUE/{reply_to_queue}"
            else:
                headers['Solace-Reply-To-Destination'] = f"/TOPIC/{reply_for_topic}"

        elif delivery_mode == 'persistent':

            headers['Solace-Delivery-Mode'] = 'persistent'
            headers['Solace-Reply-Wait-Time-In-ms'] = "FOREVER" #specifies to broker that reply is expected

            if time_to_live != None:
                headers['Solace-Time-To-Live-In-ms'] = str(time_to_live) #Time after which the message is removed from queue.

            if DMQ_eligible != None:
                headers['Solace-DMQ-Eligible'] = 'true' if DMQ_eligible == True else 'false'

            if (reply_to_queue != None) or (reply_for_topic != None):
                raise ValueError("Cannot select 'reply_to_queue' or 'reply_for_topic' options when delivery_mode = 'persistent'")
        
        else:
            raise ValueError("'delivery_mode' parameter can only be 'direct' or 'persistent'")
            
        res = None
        try:
            res = self.http_client.http_post(endpoint= endpoint, payload= message, headers= headers, timeout=timeout)
        except ReadTimeout as e:
            if throw_exception == True:
                raise e
            else:
                return {'timeout':True} 
        

        if res != None:
            if throw_exception:
                res.raise_for_status()
            return {"status_code":res.status_code, "headers":res.headers, 
                    "content":res.content, 'timeout':False}


