import cfg
import socket
import time
import atexit
import re
import chat_commands






def partandclose(sock):
    """
    Part the channel and close the socket
    :param sock: the socket
    :return: nothing
    """
    print("yolo")
    sock.send("PART {}\r\n".format(cfg.CHAN).lower().encode("utf-8"))
    res = sock.recv(1024).decode("utf-8")
    chat_commands.parseresponse(sock, res)
    sock.close()
    print("closed")


# create the socket and join the channel
s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(cfg.CHAN).lower().encode("utf-8"))
atexit.register(partandclose, s)


while True:
    response = s.recv(1024).decode("utf-8")
    chat_commands.parseresponse(s, response)
    time.sleep(1 / cfg.RATE)



