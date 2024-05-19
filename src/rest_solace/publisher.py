from .http_client import HttpClient
from requests.exceptions import ReadTimeout
from aiohttp.client_exceptions import ServerTimeoutError

class MessagingPublisher():
    
    def __init__(self, user_name:str, password:str,
                 host:str, rest_vpn_port:str, verify_ssl=False) -> None:
        """Class for creating a Publisher object for communicating with a broker to publish a message in Messaging mode.

        Args:
            username (str): Username of user with admin level access to the broker.
            password (str): Password for the username provided.
            host (str): Broker address (IPv4)
            rest_vpn_port (str): The port assigned on your vpn of interest where you wish to send messages through REST messaging.
                                We use this port so specify which VPN we wish to send our messages to.
        """

        self.http_client = HttpClient(host= host,
                                      port= rest_vpn_port,
                                      user_name= user_name,
                                      password= password,
                                      verify_ssl= verify_ssl)
        
    def update_parameters(self, user_name:str, password:str,
                          host:str, rest_vpn_port:str, verify_ssl=False):
        """Update parameters used to connect with the broker.

        Args:
            username (str): Username of user with admin level access to the broker.
            password (str): Password for the username provided.
            host (str): Broker address (IPv4)
            rest_vpn_port (str): The port assigned on your vpn of interest where you wish to send messages through REST messaging.
                                We use this port so specify which VPN we wish to send our messages to.        """
        
        self.http_client = HttpClient(host= host,
                                      port= rest_vpn_port,
                                      user_name= user_name,
                                      password= password,
                                      verify_ssl= verify_ssl)

    def direct_message_to_queue(self, queue_name:str, message:str, 
                                reply_to_queue:str|None= None, reply_for_topic:str|None= None, 
                                timeout:str|None= 120, throw_exception:bool= False)->dict:
        
        """Publish a message to a queue endpoint in direct mode.
        'direct' mode is for sending messages without expecting a reply.

        Args:
            queue_name (str): Name of the queue endpoint you wish to publish to.
            message (str): The message you wish to send.
            reply_to_queue (str | None, optional): After the message is received by the consumer, 
                                                   chose which queue the consumer reply will go to if provided.
                                                   The value must be the name of a queue.
                                                   Only works in 'direct' delivery mode.
                                                   Defaults to None.
            reply_for_topic (str | None, optional): After the message is received by the consumer, 
                                                    chose which topic string the consumer reply will go to if provided.
                                                    The value must be a topic string (NOT the name of a topic endpoint).
                                                    Only works in 'direct' delivery mode.
                                                    Defaults to None.
            timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
            throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                              Defaults to False.

        Raises:
            ValueError: Can only select either 'reply_to_queue' or 'reply_for_topic', not both.
            HTTPError: Return code for request indicates an error

        Returns:
            dict: Dictionary containing request information and {'timeout':False}.
                  Incase timeout is reached, returned dictionary only contains {'timeout':True}.
        """

        endpoint = f"/QUEUE/{queue_name}"

        headers = {'Content-Type': 'text/plain',
                   'Solace-Delivery-Mode': 'direct'}

        if reply_to_queue == None and reply_for_topic == None:
            pass
        elif reply_to_queue != None and reply_for_topic != None:
            raise ValueError("Can only select either 'reply_to_queue' or 'reply_for_topic', not both.")
        elif reply_to_queue != None:
            headers['Solace-Reply-To-Destination'] = f"/QUEUE/{reply_to_queue}"
        else:
            headers['Solace-Reply-To-Destination'] = f"/TOPIC/{reply_for_topic}"
            
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
       
    def direct_message_for_topic(self, topic_string:str, message:str, 
                        reply_to_queue:str|None= None, reply_for_topic:str|None= None, 
                        timeout:str|None= 120, throw_exception:bool= False)->dict:

        """Publish a message for a specific topic. 
        'direct' mode is for sending messages without expecting a reply.
        A topic is a string that allows for attracting specific messages to specific endpoints.
        Endpoints subscribe to a specific topic string, and messages with matching strings go to those endpoints.
        Learn more at: https://docs.solace.com/Get-Started/what-are-topics.htm   

        Note: 
            This is not to be confused with publishing to a topic endpoint.
            Publishing directly to a topic endpoint is not possible anyway,
            and topic endpoints only receive messages through the topic they are subscribed to.
            Also, the topic-string a topic endpoint is subscribed to cannot be configured manually and
            is defined by the subscriber subscribing to the topic endpoint.
            This library does not support subscribing to a topic endpoint.

        Args:
            topic_string (str): A string used by an endpoint to attract published messages. 
                                It can contain wildcards to match with multiple sub topic-strings.
            message (str): The message you wish to send.
            reply_to_queue (str | None, optional): After the message is received by the consumer, 
                                                   chose which queue the consumer reply will go to if provided.
                                                   The value must be the name of a queue.
                                                   Only works in 'direct' delivery mode.
                                                   Defaults to None.
            reply_for_topic (str | None, optional): After the message is received by the consumer, 
                                                    chose which topic string the consumer reply will go to if provided.
                                                    The value must be a topic string (NOT the name of a topic endpoint).
                                                    Only works in 'direct' delivery mode.
                                                    Defaults to None.
            timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
            throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                              Defaults to False.

        Raises:
            ValueError: Can only select either 'reply_to_queue' or 'reply_for_topic', not both.
            HTTPError: Return code for request indicates an error

        Returns:
            dict: Dictionary containing request information and {'timeout':False}.
                  Incase timeout is reached, returned dictionary only contains {'timeout':True}.
        """

        endpoint = f"/TOPIC/{topic_string}"

        headers = {'Content-Type': 'text/plain',
                   'Solace-Delivery-Mode': 'direct'}

        if reply_to_queue == None and reply_for_topic == None:
            pass
        elif reply_to_queue != None and reply_for_topic != None:
            raise ValueError("Can only select either 'reply_to_queue' or 'reply_for_topic', not both.")
        elif reply_to_queue != None:
            headers['Solace-Reply-To-Destination'] = f"/QUEUE/{reply_to_queue}"
        else:
            headers['Solace-Reply-To-Destination'] = f"/TOPIC/{reply_for_topic}"
            
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
       
    def persistent_message_to_queue(self, queue_name:str, message:str, request_reply:bool= False,
                                    time_to_live:int|None= None, DMQ_eligible:bool= False,
                                    timeout:str|None= 120, throw_exception:bool= False)->dict:
        
        """Publish a message to a queue endpoint in persistent mode.
        'persistent' mode is for sending a message and getting a confirmation from the broker if the message was spooled into a queue,
        or for sending a message and getting reply from a consumer to confirm for sure the message was not just spooled but also received.

        Args:
            queue_name (str): Name of the queue endpoint you wish to publish to.
            message (str): The message you wish to send.
            request_reply (bool): If false, tells the broker to just conform if the message was spooled into a queue.
                                  if true, tells the broker to wait for a reply from the consumer and return that to confirm message delivery.
            time_to_live (int | None, optional): Lifetime for a guaranteed message (in milliseconds). 
                                                 If the message is not delivered by this time limit,
                                                 it is either discarded from the queue or moved to dead message queue if eligible.
                                                 Only works in 'persistent' delivery mode.
                                                 Defaults to None.
            DMQ_eligible (bool, optional): Set the message as eligible for a Dead Message Queues (DMQ). 
                                           Only works in 'persistent' delivery mode.
                                           Defaults to False.
            timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
            throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                              Defaults to False.

        Raises:
            HTTPError: Return code for request indicates an error

        Returns:
            dict: Dictionary containing request information and {'timeout':False}.
                  Incase timeout is reached, returned dictionary only contains {'timeout':True}.
        """

        endpoint = f"/QUEUE/{queue_name}"

        headers = {'Content-Type': 'text/plain',
                   'Solace-Delivery-Mode': 'persistent',
                   'Solace-Reply-Wait-Time-In-ms': "FOREVER" 
                   }
        
        if request_reply == True:
            headers['Solace-Reply-Wait-Time-In-ms'] = "FOREVER" #specifies to broker that reply is expected

        if time_to_live != None:
            headers['Solace-Time-To-Live-In-ms'] = str(time_to_live) #Time after which the message is removed from queue.

        if DMQ_eligible != None:
            headers['Solace-DMQ-Eligible'] = 'true' if DMQ_eligible == True else 'false'
    
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

    def persistent_message_for_topic(self, topic_string:str, message:str, request_reply:bool= False,
                                    time_to_live:int|None= None, DMQ_eligible:bool= False,
                                    timeout:str|None= 120, throw_exception:bool= False)->dict:

        """Publish a message for a specific topic. 
        'persistent' mode is for sending a message and getting a confirmation from the broker if the message was spooled into a queue,
        or for sending a message and getting reply from a consumer to confirm for sure the message was not just spooled but also received.
        A topic is a string that allows for attracting specific messages to specific endpoints.
        Endpoints subscribe to a specific topic string, and messages with matching strings go to those endpoints.
        Learn more at: https://docs.solace.com/Get-Started/what-are-topics.htm   

        Note: 
            This is not to be confused with publishing to a topic endpoint.
            Publishing directly to a topic endpoint is not possible anyway,
            and topic endpoints only receive messages through the topic they are subscribed to.
            Also, the topic-string a topic endpoint is subscribed to cannot be configured manually and
            is defined by the subscriber subscribing to the topic endpoint.
            This library does not support subscribing to a topic endpoint.

        Args:
            topic_string (str): A string used by an endpoint to attract published messages. 
            It can contain wildcards to match with multiple sub topic-strings.
            message (str): The message you wish to send.
            request_reply (bool): If false, tells the broker to just conform if the message was spooled into a queue.
                                  if true, tells the broker to wait for a reply from the consumer and return that to confirm message delivery.
            time_to_live (int | None, optional): Lifetime for a guaranteed message (in milliseconds). 
                                                 If the message is not delivered by this time limit,
                                                 it is either discarded from the queue or moved to dead message queue if eligible.
                                                 Only works in 'persistent' delivery mode.
                                                 Defaults to None.
            DMQ_eligible (bool, optional): Set the message as eligible for a Dead Message Queues (DMQ). 
                                           Only works in 'persistent' delivery mode.
                                           Defaults to False.
            timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
            throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                              Defaults to False.

        Raises:
            HTTPError: Return code for request indicates an error

        Returns:
            dict: Dictionary containing request information and {'timeout':False}.
                  Incase timeout is reached, returned dictionary only contains {'timeout':True}.
        """

        endpoint = f"/TOPIC/{topic_string}"

        headers = {'Content-Type': 'text/plain',
                   'Solace-Delivery-Mode': 'persistent'
                   }

        if request_reply == True:
            headers['Solace-Reply-Wait-Time-In-ms'] = "FOREVER" #specifies to broker that reply is expected

        if time_to_live != None:
            headers['Solace-Time-To-Live-In-ms'] = str(time_to_live) #Time after which the message is removed from queue.

        if DMQ_eligible != None:
            headers['Solace-DMQ-Eligible'] = 'true' if DMQ_eligible == True else 'false'
    
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

    #Async functions of the above 4 functions. (you will have to remake each one and with aiohttp)

    async def async_direct_message_to_queue(self, queue_name:str, message:str, 
                                            reply_to_queue:str|None= None, reply_for_topic:str|None= None, 
                                            timeout:str|None= 120, throw_exception:bool= False)->dict:
        
        """Publish a message to a queue endpoint in direct mode.
        'direct' mode is for sending messages without expecting a reply.

        Args:
            queue_name (str): Name of the queue endpoint you wish to publish to.
            message (str): The message you wish to send.
            reply_to_queue (str | None, optional): After the message is received by the consumer, 
                                                   chose which queue the consumer reply will go to if provided.
                                                   The value must be the name of a queue.
                                                   Only works in 'direct' delivery mode.
                                                   Defaults to None.
            reply_for_topic (str | None, optional): After the message is received by the consumer, 
                                                    chose which topic string the consumer reply will go to if provided.
                                                    The value must be a topic string (NOT the name of a topic endpoint).
                                                    Only works in 'direct' delivery mode.
                                                    Defaults to None.
            timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
            throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                              Defaults to False.

        Raises:
            ValueError: Can only select either 'reply_to_queue' or 'reply_for_topic', not both.
            HTTPError: Return code for request indicates an error

        Returns:
            dict: Dictionary containing request information and {'timeout':False}.
                  Incase timeout is reached, returned dictionary only contains {'timeout':True}.
        """

        endpoint = f"/QUEUE/{queue_name}"

        headers = {'Content-Type': 'text/plain',
                   'Solace-Delivery-Mode': 'direct'}

        if reply_to_queue == None and reply_for_topic == None:
            pass
        elif reply_to_queue != None and reply_for_topic != None:
            raise ValueError("Can only select either 'reply_to_queue' or 'reply_for_topic', not both.")
        elif reply_to_queue != None:
            headers['Solace-Reply-To-Destination'] = f"/QUEUE/{reply_to_queue}"
        else:
            headers['Solace-Reply-To-Destination'] = f"/TOPIC/{reply_for_topic}"
            
        res = None
        try:
            res = await self.http_client.async_http_post(endpoint= endpoint, payload= message, headers= headers, timeout= timeout)
        except ServerTimeoutError as e:
            if throw_exception == True:
                raise e
            else:
                return {'timeout':True} 

        if res != None:
            if throw_exception:
                res.raise_for_status()
            
            content = await res.content.read()
            return {"status_code":res.status, "headers":dict(res.headers), 
                    "content":content.decode("utf8"), 'timeout':False}
       
    async def async_direct_message_for_topic(self, topic_string:str, message:str, 
                                             reply_to_queue:str|None= None, reply_for_topic:str|None= None, 
                                             timeout:str|None= 120, throw_exception:bool= False)->dict:

        """Publish a message for a specific topic. 
        'direct' mode is for sending messages without expecting a reply.
        A topic is a string that allows for attracting specific messages to specific endpoints.
        Endpoints subscribe to a specific topic string, and messages with matching strings go to those endpoints.
        Learn more at: https://docs.solace.com/Get-Started/what-are-topics.htm   

        Note: 
            This is not to be confused with publishing to a topic endpoint.
            Publishing directly to a topic endpoint is not possible anyway,
            and topic endpoints only receive messages through the topic they are subscribed to.
            Also, the topic-string a topic endpoint is subscribed to cannot be configured manually and
            is defined by the subscriber subscribing to the topic endpoint.
            This library does not support subscribing to a topic endpoint.

        Args:
            topic_string (str): A string used by an endpoint to attract published messages. 
                                It can contain wildcards to match with multiple sub topic-strings.
            message (str): The message you wish to send.
            reply_to_queue (str | None, optional): After the message is received by the consumer, 
                                                   chose which queue the consumer reply will go to if provided.
                                                   The value must be the name of a queue.
                                                   Only works in 'direct' delivery mode.
                                                   Defaults to None.
            reply_for_topic (str | None, optional): After the message is received by the consumer, 
                                                    chose which topic string the consumer reply will go to if provided.
                                                    The value must be a topic string (NOT the name of a topic endpoint).
                                                    Only works in 'direct' delivery mode.
                                                    Defaults to None.
            timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
            throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                              Defaults to False.

        Raises:
            ValueError: Can only select either 'reply_to_queue' or 'reply_for_topic', not both.
            HTTPError: Return code for request indicates an error

        Returns:
            dict: Dictionary containing request information and {'timeout':False}.
                  Incase timeout is reached, returned dictionary only contains {'timeout':True}.
        """

        endpoint = f"/TOPIC/{topic_string}"

        headers = {'Content-Type': 'text/plain',
                   'Solace-Delivery-Mode': 'direct'}

        if reply_to_queue == None and reply_for_topic == None:
            pass
        elif reply_to_queue != None and reply_for_topic != None:
            raise ValueError("Can only select either 'reply_to_queue' or 'reply_for_topic', not both.")
        elif reply_to_queue != None:
            headers['Solace-Reply-To-Destination'] = f"/QUEUE/{reply_to_queue}"
        else:
            headers['Solace-Reply-To-Destination'] = f"/TOPIC/{reply_for_topic}"
            
        res = None
        try:
            res = await self.http_client.async_http_post(endpoint= endpoint, payload= message, headers= headers, timeout=timeout)
        except ServerTimeoutError as e:
            if throw_exception == True:
                raise e
            else:
                return {'timeout':True} 
        
        if res != None:
            if throw_exception:
                res.raise_for_status()

            content = await res.content.read()
            return {"status_code":res.status, "headers":dict(res.headers), 
                    "content":content.decode("utf8"), 'timeout':False}
       
    async def async_persistent_message_to_queue(self, queue_name:str, message:str, request_reply:bool= False,
                                                time_to_live:int|None= None, DMQ_eligible:bool= False,
                                                timeout:str|None= 120, throw_exception:bool= False)->dict:
        
        """Publish a message to a queue endpoint in persistent mode.
        'persistent' mode is for sending a message and getting a confirmation from the broker if the message was spooled into a queue,
        or for sending a message and getting reply from a consumer to confirm for sure the message was not just spooled but also received.

        Args:
            queue_name (str): Name of the queue endpoint you wish to publish to.
            message (str): The message you wish to send.
            request_reply (bool): If false, tells the broker to just conform if the message was spooled into a queue.
                                  if true, tells the broker to wait for a reply from the consumer and return that to confirm message delivery.
            time_to_live (int | None, optional): Lifetime for a guaranteed message (in milliseconds). 
                                                 If the message is not delivered by this time limit,
                                                 it is either discarded from the queue or moved to dead message queue if eligible.
                                                 Only works in 'persistent' delivery mode.
                                                 Defaults to None.
            DMQ_eligible (bool, optional): Set the message as eligible for a Dead Message Queues (DMQ). 
                                           Only works in 'persistent' delivery mode.
                                           Defaults to False.
            timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
            throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                              Defaults to False.

        Raises:
            HTTPError: Return code for request indicates an error

        Returns:
            dict: Dictionary containing request information and {'timeout':False}.
                  Incase timeout is reached, returned dictionary only contains {'timeout':True}.
        """

        endpoint = f"/QUEUE/{queue_name}"

        headers = {'Content-Type': 'text/plain',
                   'Solace-Delivery-Mode': 'persistent',
                   'Solace-Reply-Wait-Time-In-ms': "FOREVER" 
                   }
        
        if request_reply == True:
            headers['Solace-Reply-Wait-Time-In-ms'] = "FOREVER" #specifies to broker that reply is expected

        if time_to_live != None:
            headers['Solace-Time-To-Live-In-ms'] = str(time_to_live) #Time after which the message is removed from queue.

        if DMQ_eligible != None:
            headers['Solace-DMQ-Eligible'] = 'true' if DMQ_eligible == True else 'false'
    
        res = None
        try:
            res = await self.http_client.async_http_post(endpoint= endpoint, payload= message, headers= headers, timeout=timeout)
        except ServerTimeoutError as e:
            if throw_exception == True:
                raise e
            else:
                return {'timeout':True} 
        
        if res != None:
            if throw_exception:
                res.raise_for_status()

            content = await res.content.read()
            return {"status_code":res.status, "headers":dict(res.headers), 
                    "content":content.decode("utf8"), 'timeout':False}

    async def async_persistent_message_for_topic(self, topic_string:str, message:str, request_reply:bool= False,
                                                 time_to_live:int|None= None, DMQ_eligible:bool= False,
                                                 timeout:str|None= 120, throw_exception:bool= False)->dict:

        """Publish a message for a specific topic. 
        'persistent' mode is for sending a message and getting a confirmation from the broker if the message was spooled into a queue,
        or for sending a message and getting reply from a consumer to confirm for sure the message was not just spooled but also received.
        A topic is a string that allows for attracting specific messages to specific endpoints.
        Endpoints subscribe to a specific topic string, and messages with matching strings go to those endpoints.
        Learn more at: https://docs.solace.com/Get-Started/what-are-topics.htm   

        Note: 
            This is not to be confused with publishing to a topic endpoint.
            Publishing directly to a topic endpoint is not possible anyway,
            and topic endpoints only receive messages through the topic they are subscribed to.
            Also, the topic-string a topic endpoint is subscribed to cannot be configured manually and
            is defined by the subscriber subscribing to the topic endpoint.
            This library does not support subscribing to a topic endpoint.

        Args:
            topic_string (str): A string used by an endpoint to attract published messages. 
            It can contain wildcards to match with multiple sub topic-strings.
            message (str): The message you wish to send.
            request_reply (bool): If false, tells the broker to just conform if the message was spooled into a queue.
                                  if true, tells the broker to wait for a reply from the consumer and return that to confirm message delivery.
            time_to_live (int | None, optional): Lifetime for a guaranteed message (in milliseconds). 
                                                 If the message is not delivered by this time limit,
                                                 it is either discarded from the queue or moved to dead message queue if eligible.
                                                 Only works in 'persistent' delivery mode.
                                                 Defaults to None.
            DMQ_eligible (bool, optional): Set the message as eligible for a Dead Message Queues (DMQ). 
                                           Only works in 'persistent' delivery mode.
                                           Defaults to False.
            timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
            throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                              Defaults to False.

        Raises:
            HTTPError: Return code for request indicates an error

        Returns:
            dict: Dictionary containing request information and {'timeout':False}.
                  Incase timeout is reached, returned dictionary only contains {'timeout':True}.
        """

        endpoint = f"/TOPIC/{topic_string}"

        headers = {'Content-Type': 'text/plain',
                   'Solace-Delivery-Mode': 'persistent'
                   }

        if request_reply == True:
            headers['Solace-Reply-Wait-Time-In-ms'] = "FOREVER" #specifies to broker that reply is expected

        if time_to_live != None:
            headers['Solace-Time-To-Live-In-ms'] = str(time_to_live) #Time after which the message is removed from queue.

        if DMQ_eligible != None:
            headers['Solace-DMQ-Eligible'] = 'true' if DMQ_eligible == True else 'false'
    
        res = None
        try:
            res = await self.http_client.async_http_post(endpoint= endpoint, payload= message, headers= headers, timeout=timeout)
        except ServerTimeoutError as e:
            if throw_exception == True:
                raise e
            else:
                return {'timeout':True} 
        
        if res != None:
            if throw_exception:
                res.raise_for_status()

            content = await res.content.read()
            return {"status_code":res.status, "headers":dict(res.headers), 
                    "content":content.decode("utf8"), 'timeout':False}



    #A single sync function to send many messages based on parameters from list of dictionary (That you could import from a CSV)
    #Should have flag to turn on and off async
    #https://www.geeksforgeeks.org/load-csv-data-into-list-and-dictionary-using-python/


#Add a class to validate inputs for the different functions.
#this would validate input for all functions. Also makes it so you can validate all the input for the multi message function first.