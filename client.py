import zmq
import _thread
import json

class client:

    def __init__(self, server_adress : tuple):
        self.server_adress = server_adress
        context = zmq.Context()
        self.requester = context.socket(zmq.REQ)
        self.requester.connect("tcp://" + self.server_adress[0] + ":" + self.server_adress[1])
        self.subscriber = context.socket(zmq.SUB)
        self.subscriber.connect("tcp://" + self.server_adress[0] + ":" + str(int(self.server_adress[1])+1))
        self.subscriber.subscribe("")


    def send_request(self, msg_send : dict) -> dict:

        self.requester.send_json(msg_send)

        msg_recv = self.requester.recv_json()
        return msg_recv


    def wait_for_event(self):

        while True:
            msg = self.subscriber.recv_json()
            if msg != '':
                return msg

cli = client(('100.115.99.81', '5555'))

#print('Received (after request) : ', cli.send_request(input(), input()), sep = "")
#print('Received (published) : ', cli.wait_for_event(), sep = "")
