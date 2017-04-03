import socket
import cfg
import re

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")


def parseresponse(sock, res):
    """
        Parse the server response
        Keyword arguments:
        socket -- the current socket
        msg  -- the received response
    """
    if res == "PING :tmi.twitch.tv\r\n":
        sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", res).group(0)  # return the entire match
        message = CHAT_MSG.sub("", res)
        print(username + ": " + message)
        parts = message.split(" ")
        checkhello(sock, username, parts)
        if message.startswith("!"):
            parsechatcommand(sock, username, message)


def checkhello(sock, user, parts):
    for part in parts:
        for pattern in cfg.HELLO:
            if re.match(pattern, part):
                hi(sock, user, part)
                return


def parsechatcommand(sock, user, msg):
    """
    Parses the user message and apply the corresponding command
    :param sock: the current socket
    :param user: the user who sent the message 
    :param msg: the message
    :return: nothing
    """
    print("found a cmd")


def chat(sock, msg):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    print(msg)
    sock.send("PRIVMSG {} :{} \r\n".format(cfg.CHAN.lower(), msg).encode("utf-8"))


def hi(sock, user, greet):
    """
    Sends hi to the user
    :param sock: the current socket
    :param user: the user to send the message
    :return: nothing
    """
    chat(sock, "{} {}".format(greet.rstrip().title(), user))
