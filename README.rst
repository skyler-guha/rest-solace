rest-solace
===============

**rest-solace** is a rest based python library for Solace Message Broker that allows you to Publish, Consume, & Manage!!

It is written with the intent to be easy to understand, functional, and pythonic.
Input and output parameters for every function is always one of int, float, str, bool, list, dict and None; 
making them directly compatible with json data types. 

| Check it out at `PyPI <https://pypi.org/project/rest-solace/>`_.
| View the code at `Github <https://github.com/skyler-guha/rest-solace/>`_.
| Read the docs from `Here <https://github.com/skyler-guha/rest-solace/blob/master/docs/index.rst/>`_.

Note: 
    | Right now the focus of this library is on the 'messaging' mode for solace message VPNs.
    | In the future I plan to add better support for 'gateway' mode as well.
    | This library currently uses SEMPv2 for management. 

Getting started with Solace:
-----------------------------
If you are new to solace and confused about the terminology and workflows around it, it is **highly** recommended 
that you read `this <https://github.com/skyler-guha/rest-solace/blob/master/docs/getting_started_with_solace.rst/>`_ document first.
It gives a brief explanation on the different components of solace; and that too within the context of this library.

|

Sending messages (for message-VPN in messaging mode):
-----------------------------------------------------
(Note: The single message sending functions in this example have async versions as well)

.. code-block:: python

    from rest_solace import MessagingPublisher

    publish = MessagingPublisher(user_name= "admin", 
                                       password=" admin", 
                                       host= BROKER_IP, 
                                       rest_vpn_port= VPN_PORT #For 'default' VPN it is 9000
                                       )

    #Publish to a queue and (only confirms if the message was received by the broker)
    publish.direct_message_to_queue(queue_name= "my_queue",
                                    message= "hello world!!")
    
    #Publish for a topic string (only confirms if the message was received by the broker)
    publish.direct_message_for_topic(topic_string= "test_topic", 
                                     message= "hello world!!")


    #Publish to a queue and wait for confirmation on if the message was spooled into a queue
    publish.persistent_message_to_queue(queue_name= "my_queue", 
                                        message= "hello world!!",
                                        request_reply= False)                               

    #Publish for a topic string and wait for confirmation on if the message was spooled into a queue
    publish.persistent_message_for_topic(topic_string= "test_topic", 
                                         message= "hello world!!",
                                         request_reply= False)


    #Publish to a queue and wait for reply from a consumer
    response = publish.persistent_message_to_queue(queue_name= "my_queue", 
                                                   message= "hello world!!",
                                                   request_reply= True)                               
    print(response)

    #Publish for a topic string and wait for reply from a consumer
    response = publish.persistent_message_for_topic(topic_string= "test_topic", 
                                                    message= "hello world!!"
                                                    request_reply= True)
    print(response)

|

Receiving messages and sending back a response:
-----------------------------------------------
(You can use your own REST server too. The one included with this library is only for simple uses and testing)

.. code-block:: python

    from rest_solace import Consumer

    consumer_obj = Consumer()

    #Receive a single message and get the value returned to you.
    incoming_message = consumer_obj.startConsumer(host= CONSUMER_HOST, 
                                                  port= CONSUMER_PORT, 
                                                  auto_stop= True #Required for single message mode
                                                  )
    print(incoming_message)


    #Keep receiving messages and handle them through a callback function

    def return_uppercase(event:dict, kill_function):
    """Convert request message string to upper case to return as response.
    Stops the consumer server if message is "kill".

    Args:
        event (dict): contains info about the received request.
        kill_function (function): stops the consumer server if you run it.
    Returns:
        str: Returns the incoming message to the publisher in uppercase
    """
    byte_string_content= event["content"][1:-1]
    regular_string_content= byte_string_content.decode("utf-8")
    uppercase_response= str.upper( regular_string_content ) 
    
    if regular_string_content == "kill":
        kill_function()
    
    return uppercase_response

    #You can run this function on a septate thread too if you want.
    consumer_obj.startConsumer(host= CONSUMER_HOST, 
                               port= CONSUMER_PORT,
                               callback_function= return_uppercase, 
                               log= True) 

|

Setting up a message VPN for message broking (in messaging mode):
------------------------------------------------------------------
(This is a bit advance but the library includes lots of utility functions to make initial setup easy)

.. code-block:: python

    from rest_solace import Manager

    manager = Manager(user_name= admin, 
                      password= admin, 
                      host= BROKER_IP, 
                      semp_port= SEMP_PORT) #Default rest management port is 8080

    
    #Creating a custom message VPN 
    #(can automatically apply required VPN configuration for rest based communication).
    manager.create_message_vpn(
        msgVpnName= NEW_VPN_NAME,
        serviceRestIncomingPlainTextListenPort= VPN_PORT, #Assign it an unused port
        serviceRestMode= "messaging" #auto configuration will be influenced by this parameter
    )

    
    #Automatically setting up your Message VPN for rest based communication
    manager.auto_rest_messaging_setup_utility(
        msgVpnName= NEW_VPN_NAME,                   #Existing message VPN
        queueName= 'my_queue',                      #Creates a new queue
        subscriptionTopic="test_topic",             #The topic the queue should subscribe to
        restDeliveryPointName='myRDP',              #New RDP to handle incoming messages
        restConsumerName= 'myConsumer',             #A name for your consumer
        remoteHost= CONSUMER_HOST, 
        remotePort= CONSUMER_PORT
    )

                                              
    #Doing the same setup manually (Shown for comparison)
    manager.update_client_profile(msgVpnName= NEW_VPN_NAME, 
                                  clientProfileName= "default",
                                  allowGuaranteedMsgReceiveEnabled= True,
                                  allowGuaranteedMsgSendEnabled= True)
    manager.update_client_username(msgVpnName=NEW_VPN_NAME, 
                                   clientUsername= "default",
                                   enabled= True)
    manager.create_queue_endpoint(queueName='my_queue', msgVpnName=NEW_VPN_NAME)
    manager.subscribe_to_topic_on_queue(subscriptionTopic= "test_topic", queueName= 'my_queue')
    manager.create_rest_delivery_point(msgVpnName= NEW_VPN_NAME, 
                                       restDeliveryPointName= 'myRDP', 
                                       clientProfileName= "default")
    manager.specify_rest_consumer(msgVpnName= NEW_VPN_NAME, 
                                  restDeliveryPointName= 'myRDP',
                                  restConsumerName= 'myConsumer',
                                  remoteHost= CONSUMER_HOST,
                                  remotePort= CONSUMER_PORT)
    manager.create_queue_binding(msgVpnName= NEW_VPN_NAME,
                                 restDeliveryPointName= 'myRDP',
                                 queueBindingName= 'my_queue',
                                 postRequestTarget= '/')


    #Turning your RDP off and on again (Useful if solace has trouble connecting to your consumer)
    manager.restart_rest_delivery_point(msgVpnName= NEW_VPN_NAME, restDeliveryPointName= 'myRDP')

    


    
..
   _Note: Make sure to indent using spaces in the code blocks!