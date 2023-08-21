import pika

class Client:

    def __init__(self, service_name, method_name, host='localhost'):
        self.host = host
        self.service_name = service_name
        self.method_name = method_name
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()

    def send_message(self, message_body):
        if not self.channel:
            raise ValueError("Must connect to the server before sending a message")

        routing_key = f"{self.service_name}.{self.method_name}"

        self.channel.queue_declare(queue=routing_key)

        self.channel.basic_publish(exchange='', routing_key=routing_key, body=message_body)