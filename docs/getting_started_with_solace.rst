This is a short into to get you started if you are new to solace.
Solace is a message broking software.

A solace message broker can have multiple Message VPNs, 
which are segregated spaces for message communication to take place.
Each such VPN will have its own unique listening PORT for receiving messages, 
and you can define a separate PORT for each message sending protocol (like REST, MQTT, AMQP, etc).
When sending a message, you have to specify the message VPN, 
and you will have to do that with its listening PORT number (incase of this library, the REST listening port).

A VPN can contain many endpoints called "queues" which are used to 
receive, store, and pass along incoming messages 
(there is another kind of endpoint called "topic_endpoint", but you can ignore it as it is just a vestigial feature.).

There is also the concept of "topic" strings (not to be confused with topic-endpoints).
Each queue can subscribe to a topic string. And instead of punishing a message directly to a queue,
you could send the broker a message for a topic string, and every queue with the matching 
topic string will get the message. Topic strings also have other features like wildcards, and 
you can read all about it `here <https://docs.solace.com/Get-Started/what-are-topics.htm>`_.

The one sending the message is called the "Publisher". 

When it comes to receving messages, there are 2 terms that are often use interchangebly, 
but for this library will be defined as 2 distinct concepts. They are:

* Subscriber- This is when someone subscribes to a queue by creating a session with the broker. 
  This is the case with the Solace Java Message Service (JMS) API. 
  More info can be found about it `here <https://tutorials.solace.dev/jms/publish-subscribe/#Connecting-to-Solace-Messaging>`_.
* Consumer- This is when you start a server on a certain host and port, 
  then add that server (its host address and port) to the list of consumers for a given queue.
  When a message comes to the queue, the broker automaticly sends the message to the relevent consumers, 
  without a need for there to be a constent session between the two. 
  Rest consumers work in this way. When you make a consumer using this library, you are creating a server which is
  going to listen for incoming messages.
