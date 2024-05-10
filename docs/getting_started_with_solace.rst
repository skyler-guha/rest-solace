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
(there is another kind of endpoint called "topic_endpoint, but you can ignore it as it is just a vestigial feature").

There is also the concept of "topic" strings (not to be confused with topic-endpoints).
Each queue can subscribe to a topic string. And instead of punishing a message directly to a queue,
you could send the broker a message for a topic string, and every queue with the matching 
topic string will get the message. Topic strings also have other features like wildcards, and 
you can read all about it `here <https://docs.solace.com/Get-Started/what-are-topics.htm>`_.

