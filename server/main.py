from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

ADDRESS = 'localhost'
PORT = 8000


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Main server function
def main():
    with SimpleXMLRPCServer(('localhost', 8000), 
                            requestHandler=RequestHandler) as server:
        server.register_introspection_functions()
        
        @server.register_function
        def read_notes(topic: str):
            
        

if __name__ == '__main__':
    main()