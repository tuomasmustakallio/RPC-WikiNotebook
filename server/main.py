from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
from datetime import datetime
import wikipedia

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
        def get_note(topic):
            try: 
                et = ET.parse('db.xml')
                elements = et.getroot()
                res = []
                for e in elements.findall('topic'):
                    if e.attrib['name'] == topic:
                        notes = e.findall('note')
                        for n in notes:
                                res.append(n.attrib['name'])
                                res.append(getattr(n.find('text'), 'text', None).strip())
                                res.append(n.find('date').text.strip())

                return res
            except Exception as e:
                print(e)
                return []
            
        @server.register_function
        def add_note(topic, name, text):
            try:
                et = ET.parse('db.xml')
                elements = et.getroot()
                for e in elements:
                    if e.attrib['name'] == topic:
                        note = ET.SubElement(e, 'note')
                        note.set('name', name)
                        text_el = ET.SubElement(note, 'text')
                        text_el.text = text
                        date_el = ET.SubElement(note, 'date')
                        date_el.text = datetime.now().strftime("%m/%d/%y, %H:%M:%S")
                        et.write('db.xml')
                        return True
                ## If topic not found create new topic
                topic_el = ET.SubElement(elements, 'topic')
                topic_el.set('name', topic)
                note = ET.SubElement(topic_el, 'note')
                note.set('name', name)
                text_el = ET.SubElement(note, 'text')
                text_el.text = text
                date_el = ET.SubElement(note, 'date')
                date_el.text = datetime.now().strftime("%m/%d/%y, %H:%M:%S")
                et.write('db.xml')
                return True
            except Exception as e:
                print(e)
                return False
            
        @server.register_function
        def fetch_wikipedia_summary(topic):
            try:
                return wikipedia.summary(topic, sentences=2)
            except Exception as e:
                print(e)
                return "No wikipedia page found"
        
        @server.register_function
        def fetch_wikipedia_page(topic):
            try:
                return wikipedia.page(topic).url
            except Exception as e:
                print(e)
                return "No wikipedia page found"
        
        @server.register_function
        def add_wikipedia_summary(topic):
            try:
                return add_note(topic, f"{topic} according to Wikipedia", fetch_wikipedia_summary(topic))
            except Exception as e:
                print(e)
                return False
            
        
        print('Server is running on port {}'.format(PORT))
        server.serve_forever()

if __name__ == '__main__':
    main()
