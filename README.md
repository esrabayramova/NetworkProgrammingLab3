# NetworkProgrammingLab3

## Description

This is a server-client based console application. The server and the client is created using object oriented approach. The client sends a link to the server. The server counts the number of the images and the leaf paragraph nodes (a paragraph that does not have another paragraph inside) and sends it to the client. 

## Installation

```
git clone https://github.com/esrabayramova/NetworkProgrammingLab3
```


## Usage

Firstly, two terminals are opened, one for the server and one for the client. After writing 'python3' and specifying the name of the file, the role must be shown - either client or server. Then, if it is a client console, the link must be typed as a string by writing '-p' before it. After the connection is established, the client console will display the results.

```
python3 tcp_server_web.py server
python3 tcp_server_web.py client -p "https://www.pcworld.com"
```

Client side terminates after receiving the message from the server, however, you should stop server by pressing Ctrl + C. As long as the server is running, it can make a connection with different clients. 
