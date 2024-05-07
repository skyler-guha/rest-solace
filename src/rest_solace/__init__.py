from .manager import Manager
from .publisher import MessagingPublisher
from .consumer import Consumer



#curl -X POST -d "{'body':'Hello World Topic'}" http://172.17.0.3:9000/TOPIC/TestTopic1 --header "Content-Type: text/plain" -u admin:admin -v

#curl -X POST -d "Hello World Queue" http://172.17.0.3:9000/QUEUE/test_queue --header "Content-Type: text/plain"

#curl -X POST -d "Hello World Request Reply" http://172.17.0.3:9000/TOPIC/rr --header "Solace-Reply-Wait-Time-In-ms:30000" --header "Solace-Correlation-ID:x"
