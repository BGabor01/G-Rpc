import pika
import uuid
import logging
from .decorators.retry_dec import retry

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("pika").setLevel(logging.WARNING)

class Client:

    def __init__(self, service_name, host='localhost'):
        self.logger = logging.getLogger('Client')
        self.logger.info("Client initialized.")

        self.host = host
        self.service_name = service_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.response_queue = self.channel.queue_declare(queue='', exclusive=True).method.queue
        self.channel.basic_consume(
            queue=self.response_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None
        self.corr_id = None
       

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body


    @retry(max_retries=3, delay=2, exceptions=(TimeoutError,))
    def send_request(self, method_name, request_body, time_limit = 5):
        self.logger.info(f"Sending request with body: {request_body}")
        self.response = None
        self.corr_id = str(uuid.uuid4())
        routing_key = f"{self.service_name}.{method_name}"
        self.channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            properties=pika.BasicProperties(
                reply_to=self.response_queue,
                correlation_id=self.corr_id,
            ),
            body=request_body
        )

        self.connection.process_data_events(time_limit=time_limit)

        if self.response is None:
            raise TimeoutError("RPC call time out!")

        return self.response

if __name__ == "__main__":
    client = Client(service_name='example_service')
    response = client.send_request(method_name='echo', request_body="Hello, RPC!")
    print("Received:", response.decode())
