This is a short into to get you started if you are new to solace.
Solace is a message broking software.

Message VPNs
=============

A solace message broker can have multiple Message VPNs, 
which are segregated spaces for message communication to take place.
Each such VPN will have its own unique listening PORT for receiving messages, 
and you can define a separate PORT for each message sending protocol (like REST, MQTT, AMQP, etc).
When sending a message, you have to specify the message VPN, 
and you will have to do that with its listening PORT number (incase of this library, the REST listening port).


Endpoints
===========

A VPN can contain many endpoints called "queues" which are used to 
receive, store, and pass along incoming messages 
(there is another kind of endpoint called "topic_endpoint", but you can ignore it as it is just a vestigial feature.).

There is also the concept of "topic" strings (not to be confused with topic-endpoints).
Each queue can subscribe to a topic string. And instead of punishing a message directly to a queue,
you could send the broker a message for a topic string, and every queue with the matching 
topic string will get the message. Topic strings also have other features like wildcards, and 
you can read all about it `here <https://docs.solace.com/Get-Started/what-are-topics.htm>`_.

Publisher, Consumer, and Subscriber
======================================

The one sending the message is called the "Publisher". 

When it comes to receiving messages, there are 2 terms that are often use interchangeably, 
but for this library will be defined as 2 distinct concepts. They are:

* Subscriber- This is when someone subscribes to a queue by creating a session with the broker. 
  This is the case with the Solace Java Message Service (JMS) API. 
  More info can be found about it `here <https://tutorials.solace.dev/jms/publish-subscribe/#Connecting-to-Solace-Messaging>`_.
* Consumer- This is when you start a server on a certain host and port, 
  then add that server (its host address and port) to the list of consumers for a given queue.
  When a message comes to the queue, the broker automatically sends the message to the relevant consumers, 
  without a need for there to be a consent session between the two. 
  Rest consumers work in this way. When you make a consumer using this library, you are creating a server which is
  going to listen for incoming messages.


Direct VS Persistent message delivery modes:
============================================

Direct Mode:
--------------
This uses TCP protocol and does not confirm if the message was spooled (stored) into a queue or received by a consumer.
It is good for cases where always getting the data is not important.

Persistent Mode:
-----------------
This also uses TCP protocol but also does additional set of acknowledgments. It can tell you if a message was spooled into a queue,
or received by the consumer.

You may learn more about this topic here:
https://solace.com/blog/delivery-modes-direct-messaging-vs-persistent-messaging/


SEMP2 and Accessing Data "Objects"
====================================

Solace Element Management Protocol version 2 (SEMP v2) is a RESTful API that 
provides a programmable way to configure PubSub+ event brokers. 

It is what is used by this library's management class for doing management stuff.

An important thing to note is that under SEMP2 information about the brokers configurations 
is stored in a Object Oriented way. For example all the message VPNs are accessed in SEMP2 as if you
are getting a list of "Objects" which contain a multiple attributes such as VPNn name, their settings, etc.
These objects in turn can be converted to python dictionaries since the objects contain only 
attributes and no methods (so the name of the attribute becomes key name, and its value becomes the key's value).

This library tries to hide that object oriented abstraction in favor of functions that simply give you a specific type of data 
like list of VPNs, list of queues, etc. However sometimes in the documentation it might get mentioned as list 
of VPN objects, list of queue objects etc. All it implies is that the function gives you list of individual 
entities of a certain type (like VPNs or queues) and it is good to be mindful of that. It DOES NOT mean 
the library will give you an actual python class object.



