"""Creates a simple consumer.
This test is just to see if it will run.
"""
from rest_solace import Consumer

def return_uppercase(event:dict, kill_function):
    """Convert request message string to upper case to return as response

    Args:
        event (dict): contains info about the received request

    Returns:
        str: Returns the incoming message in uppercase
    """
    byte_string_content= event["content"][1:-1]
    regular_string_content= byte_string_content.decode("utf-8")
    uppercase_response= str.upper( regular_string_content ) 
    return uppercase_response

if __name__ == "__main__":

    consumer_obj = Consumer()

    ret = consumer_obj.startConsumer(host= "127.0.0.1", port=5000, 
                                callback_function= return_uppercase, log=True,
                                auto_stop= True)
    
    print(ret)


