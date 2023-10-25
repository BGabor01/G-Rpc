import pika
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Server:

    def __init__(self, service_name, host='localhost', user_name='guest', password='guest'):
        self.logger = logging.getLogger('Server')
        self.logger.info("RPC server initialized.")

        self.host = host
        self.service_name = service_name
        self.user_name = user_name
        self.password = password
       
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self.user_name, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, credentials=credentials))
        self.channel = self.connection.channel()

    def start(self):
        self.logger.info(f"RPC Server for {self.service_name} started. Awaiting requests.")
        self.channel.start_consuming()

    def add_method(self, method_name, callback):
        """
        Add a method to listen to and provide its callback function.
        """
        routing_key = f"{self.service_name}_{method_name}"
        self.channel.queue_declare(queue=routing_key)

        def on_request(ch, method, properties, body):
            try:
                request_data = json.loads(body.decode())
                self.logger.info(f"Received request on method {method_name} with body: {request_data}")
                response_queue_name = request_data['responseQueueName']
                corr_id = request_data['correlationId']

                response_data = callback(request_data)
                response = json.dumps(response_data).encode()

                ch.basic_publish(
                    exchange='',
                    routing_key=response_queue_name,
                    properties=pika.BasicProperties(
                        correlation_id=corr_id
                    ),
                    body=response
                )
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                self.logger.error(f"Error processing request: {e}")

        self.channel.basic_consume(queue=routing_key, on_message_callback=on_request)



def handle_echo_request(body):
    return body

if __name__ == '__main__':
    server = Server(service_name='example_service', user_name="username", password="password")
    server.connect()
    server.add_method('echo', handle_echo_request)
    server.start()
