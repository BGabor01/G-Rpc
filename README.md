# G-Rpc
g-rpc is a simple RPC (Remote Procedure Call) implementation for Python. It allows for inter-process communication using the lightweight pika library.

### Installation
pip install git+https://github.com/baloghG01/G-Rpc


### Usage
#### Server
- __Set up server__ <br>
from g_rpc.server import Server <br>
server = Server(service_name='example_service')<br>


- __Connect to it__ <br>
server.connect() <br>

- __Add your rpc commands__ <br>
server.add_method('echo', handle_echo_request) <br>

- __Start the server__ <br>
server.start()

#### Client
- __Set up client__ <br>
from g_rpc import Client <br>
client = Client("example_service") <br>

- __Make a request to the server__ <br>
client.send_request('echo', request_body)


### Dependencies
- __pika__


