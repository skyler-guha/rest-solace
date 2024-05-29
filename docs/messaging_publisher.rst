----------------------------------------------------------------------------------------
Messaging Publisher Class (for sending messages through message-VPN in messaging mode):
----------------------------------------------------------------------------------------


*Class: MessagingPublisher*
-------------------------------
Class for creating a Publisher object for communicating with a broker to publish a message in Messaging mode.

Args:
 - username (str): Username of user with admin level access to the broker.
 - password (str): Password for the username provided.
 - host (str): Broker address (IPv4)
 - rest_vpn_port (str): The port assigned on your vpn of interest where you wish to send messages through REST messaging.
                    We use this port so specify which VPN we wish to send our messages to.
 - verify_ssl (bool): Enable SSL (Does not work as of yet)

Example: 

.. code-block:: python

    from rest_solace import MessagingPublisher

    publish = MessagingPublisher(user_name= "admin", 
                                 password=" admin", 
                                 host= BROKER_IP, 
                                 rest_vpn_port= VPN_PORT #For 'default' VPN it is 9000
                                )


*Function: update_parameters*
-------------------------------
Update the default parameters used to connect with the broker.

Args:
 - username (str): Username of user with admin level access to the broker.
 - password (str): Password for the username provided.
 - host (str): Broker address (IPv4)
 - rest_vpn_port (str): The port assigned on your vpn of interest where you wish to send messages through REST messaging.
                    We use this port so specify which VPN we wish to send our messages to.        
 - verify_ssl (bool): Enable SSL (Does not work as of yet)

Returns:
 - None

Example:

.. code-block:: python

    publish.update_parameters(user_name= "admin", 
                              password=" admin", 
                              host= BROKER_IP, 
                              rest_vpn_port= VPN_PORT #For 'default' VPN it is 9000
                             )


*Function: direct_message_to_queue*
------------------------------------
Publish a message to a queue endpoint in direct mode.
'direct' mode is for sending messages without expecting a reply.

Args:
 - queue_name (str): Name of the queue endpoint you wish to publish to.
 - message (str): The message you wish to send.
 - reply_to_queue (str | None, optional): After the message is received by the consumer, 
                                        chose which queue the consumer reply will go to if provided.
                                        The value must be the name of a queue.
                                        Only works in 'direct' delivery mode.
                                        Defaults to None.
 - reply_for_topic (str | None, optional): After the message is received by the consumer, 
                                        chose which topic string the consumer reply will go to if provided.
                                        The value must be a topic string (NOT the name of a topic endpoint).
                                        Only works in 'direct' delivery mode.
                                        Defaults to None.
 - timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
 - throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                    Defaults to False.
 - client_params (dict, optional): Use custom http client params instead of using the ones 

Raises:
 - ValueError: Can only select either 'reply_to_queue' or 'reply_for_topic', not both.
 - HTTPError: Return code for request indicates an error

Returns:
 - dict: Dictionary containing request information and {'timeout':False}.
        Incase timeout is reached, returned dictionary only contains {'timeout':True}.

Example: 

.. code-block:: python

    publish.direct_message_to_queue(queue_name= "my_queue",
                                    message= "hello world!!")


*Function: direct_message_for_topic*
--------------------------------------
Publish a message for a specific topic. 
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
 - topic_string (str): A string used by an endpoint to attract published messages. 
                    It can contain wildcards to match with multiple sub topic-strings.
 - message (str): The message you wish to send.
 - reply_to_queue (str | None, optional): After the message is received by the consumer, 
                                        chose which queue the consumer reply will go to if provided.
                                        The value must be the name of a queue.
                                        Only works in 'direct' delivery mode.
                                        Defaults to None.
 - reply_for_topic (str | None, optional): After the message is received by the consumer, 
                                        chose which topic string the consumer reply will go to if provided.
                                        The value must be a topic string (NOT the name of a topic endpoint).
                                        Only works in 'direct' delivery mode.
                                        Defaults to None.
 - timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
 - throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                    Defaults to False.

Raises:
 - ValueError: Can only select either 'reply_to_queue' or 'reply_for_topic', not both.
 - HTTPError: Return code for request indicates an error

Returns:
 - dict: Dictionary containing request information and {'timeout':False}.
        Incase timeout is reached, returned dictionary only contains {'timeout':True}.

Example: 

.. code-block:: python

    publish.direct_message_for_topic(topic_string= "test_topic", 
                                     message= "hello world!!")




*Function: persistent_message_to_queue*
----------------------------------------
Publish a message to a queue endpoint in persistent mode.
'persistent' mode is for sending a message and getting a confirmation from the broker if the message was spooled into a queue,
or for sending a message and getting reply from a consumer to confirm for sure the message was not just spooled but also received.

Args:
 - queue_name (str): Name of the queue endpoint you wish to publish to.
 - message (str): The message you wish to send.
 - request_reply (bool): If false, tells the broker to just conform if the message was spooled into a queue.
                        if true, tells the broker to wait for a reply from the consumer and return that to confirm message delivery.
 - time_to_live (int | None, optional): Lifetime for a guaranteed message (in milliseconds). 
                                        If the message is not delivered by this time limit,
                                        it is either discarded from the queue or moved to dead message queue if eligible.
                                        Only works in 'persistent' delivery mode.
                                        Defaults to None.
 - DMQ_eligible (bool, optional): Set the message as eligible for a Dead Message Queues (DMQ). 
                                Only works in 'persistent' delivery mode.
                                Defaults to False.
 - timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
 - throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                    Defaults to False.

Raises:
 - HTTPError: Return code for request indicates an error

Returns:
 - dict: Dictionary containing request information and {'timeout':False}.
        Incase timeout is reached, returned dictionary only contains {'timeout':True}.

Example:

.. code-block:: python

    response = publish.persistent_message_to_queue(queue_name= "my_queue", 
                                                   message= "hello world!!",
                                                   request_reply= True)                               
    print(response)


*Function: persistent_message_for_topic*
------------------------------------------
Publish a message for a specific topic. 
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
 - topic_string (str): A string used by an endpoint to attract published messages. 
                    It can contain wildcards to match with multiple sub topic-strings.
 - message (str): The message you wish to send.
 - request_reply (bool): If false, tells the broker to just conform if the message was spooled into a queue.
                        if true, tells the broker to wait for a reply from the consumer and return that to confirm message delivery.
 - time_to_live (int | None, optional): Lifetime for a guaranteed message (in milliseconds). 
                                        If the message is not delivered by this time limit,
                                        it is either discarded from the queue or moved to dead message queue if eligible.
                                        Only works in 'persistent' delivery mode.
                                        Defaults to None.
 - DMQ_eligible (bool, optional): Set the message as eligible for a Dead Message Queues (DMQ). 
                                Only works in 'persistent' delivery mode.
                                Defaults to False.
 - timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
 - throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                    Defaults to False.

Raises:
 - HTTPError: Return code for request indicates an error

Returns:
 - dict: Dictionary containing request information and {'timeout':False}.
        Incase timeout is reached, returned dictionary only contains {'timeout':True}.

Example:

.. code-block:: python

    response = publish.persistent_message_for_topic(topic_string= "test_topic", 
                                                    message= "hello world!!"
                                                    request_reply= True)                           
    print(response)


*Function: async_direct_message_to_queue*
------------------------------------------
Publish a message to a queue endpoint in direct mode asynchronously.
'direct' mode is for sending messages without expecting a reply.

Args:
 - queue_name (str): Name of the queue endpoint you wish to publish to.
 - message (str): The message you wish to send.
 - reply_to_queue (str | None, optional): After the message is received by the consumer, 
                                        chose which queue the consumer reply will go to if provided.
                                        The value must be the name of a queue.
                                        Only works in 'direct' delivery mode.
                                        Defaults to None.
 - reply_for_topic (str | None, optional): After the message is received by the consumer, 
                                        chose which topic string the consumer reply will go to if provided.
                                        The value must be a topic string (NOT the name of a topic endpoint).
                                        Only works in 'direct' delivery mode.
                                        Defaults to None.
 - timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
 - throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                    Defaults to False.
 - client_params (dict, optional): Use custom http client params instead of using the ones 

Raises:
 - ValueError: Can only select either 'reply_to_queue' or 'reply_for_topic', not both.
 - HTTPError: Return code for request indicates an error

Returns:
 - dict: Dictionary containing request information and {'timeout':False}.
        Incase timeout is reached, returned dictionary only contains {'timeout':True}.

Example: 

.. code-block:: python

    import asyncio
    coroutine_obj= async_direct_message_to_queue(queue_name= "my_queue",
                                                 message= "hello world!!")
    asyncio.run(coroutine_obj)


*Function: async_direct_message_for_topic*
-------------------------------------------
Publish a message for a specific topic. 
'direct' mode is for sending messages without expecting a reply asynchronously.
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
 - topic_string (str): A string used by an endpoint to attract published messages. 
                    It can contain wildcards to match with multiple sub topic-strings.
 - message (str): The message you wish to send.
 - reply_to_queue (str | None, optional): After the message is received by the consumer, 
                                        chose which queue the consumer reply will go to if provided.
                                        The value must be the name of a queue.
                                        Only works in 'direct' delivery mode.
                                        Defaults to None.
 - reply_for_topic (str | None, optional): After the message is received by the consumer, 
                                        chose which topic string the consumer reply will go to if provided.
                                        The value must be a topic string (NOT the name of a topic endpoint).
                                        Only works in 'direct' delivery mode.
                                        Defaults to None.
 - timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
 - throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                    Defaults to False.

Raises:
 - ValueError: Can only select either 'reply_to_queue' or 'reply_for_topic', not both.
 - HTTPError: Return code for request indicates an error

Returns:
 - dict: Dictionary containing request information and {'timeout':False}.
        Incase timeout is reached, returned dictionary only contains {'timeout':True}.

Example: 

.. code-block:: python

    import asyncio
    coroutine_obj= publish.async_direct_message_for_topic(topic_string= "test_topic", 
                                                          message= "hello world!!")
    asyncio.run(coroutine_obj)


*Function: async_persistent_message_to_queue*
-----------------------------------------------
Publish a message to a queue endpoint in persistent mode asynchronously.
'persistent' mode is for sending a message and getting a confirmation from the broker if the message was spooled into a queue,
or for sending a message and getting reply from a consumer to confirm for sure the message was not just spooled but also received.

Args:
 - queue_name (str): Name of the queue endpoint you wish to publish to.
 - message (str): The message you wish to send.
 - request_reply (bool): If false, tells the broker to just conform if the message was spooled into a queue.
                        if true, tells the broker to wait for a reply from the consumer and return that to confirm message delivery.
 - time_to_live (int | None, optional): Lifetime for a guaranteed message (in milliseconds). 
                                        If the message is not delivered by this time limit,
                                        it is either discarded from the queue or moved to dead message queue if eligible.
                                        Only works in 'persistent' delivery mode.
                                        Defaults to None.
 - DMQ_eligible (bool, optional): Set the message as eligible for a Dead Message Queues (DMQ). 
                                Only works in 'persistent' delivery mode.
                                Defaults to False.
 - timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
 - throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                    Defaults to False.

Raises:
 - HTTPError: Return code for request indicates an error

Returns:
 - dict: Dictionary containing request information and {'timeout':False}.
        Incase timeout is reached, returned dictionary only contains {'timeout':True}.

Example:

.. code-block:: python

    import asyncio
    coroutine_obj= publish.async_persistent_message_to_queue(queue_name= "my_queue", 
                                                             message= "hello world!!",
                                                             request_reply= True)
    response= asyncio.run(coroutine_obj)
    print(response)


*Function: async_persistent_message_for_topic*
------------------------------------------------
Publish a message for a specific topic asynchronously. 
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
 - topic_string (str): A string used by an endpoint to attract published messages. 
                    It can contain wildcards to match with multiple sub topic-strings.
 - message (str): The message you wish to send.
 - request_reply (bool): If false, tells the broker to just conform if the message was spooled into a queue.
                        if true, tells the broker to wait for a reply from the consumer and return that to confirm message delivery.
 - time_to_live (int | None, optional): Lifetime for a guaranteed message (in milliseconds). 
                                        If the message is not delivered by this time limit,
                                        it is either discarded from the queue or moved to dead message queue if eligible.
                                        Only works in 'persistent' delivery mode.
                                        Defaults to None.
 - DMQ_eligible (bool, optional): Set the message as eligible for a Dead Message Queues (DMQ). 
                                Only works in 'persistent' delivery mode.
                                Defaults to False.
 - timeout (str | None, optional): http/https request timeout set on the client side. Defaults to 120.
 - throw_exception (bool, optional): Throw exception incase request error code indicates an error or timeout has been reached.
                                    Defaults to False.

Raises:
 - HTTPError: Return code for request indicates an error

Returns:
 - dict: Dictionary containing request information and {'timeout':False}.
        Incase timeout is reached, returned dictionary only contains {'timeout':True}.

Example:

.. code-block:: python

    import asyncio
    coroutine_obj= publish.async_persistent_message_for_topic(topic_string= "test_topic", 
                                                              message= "hello world!!"
                                                              request_reply= True)
    response= asyncio.run(coroutine_obj)
    print(response)


*Function: send_messages (EXPERIMENTAL)*
-------------------------------------------
Send multiple messages in a batch.

Args:
 - data (list | str): Either a list of dictionaries containing message data, 
            or a string containing path to a json file with the data.
            async_mode (bool, optional): To send the message asynchronously or not. Defaults to True.

Returns:
 - list: Output values.

Example:

.. code-block:: python

    message_data= [
        {
            "direct_message_to_queue": {
                "queue_name": "queue_rest_consumer",
                "message": "hello world!!",
                "timeout": 120,
                "throw_exception": false
            }
        },
        {
            "direct_message_for_topic": {
                "topic_string": "my_topic",
                "message": "hello world!!",
                "timeout": 120,
                "throw_exception": false
            }
        }
    ]

    res= publish.send_messages(data= message_data)
    print(res)