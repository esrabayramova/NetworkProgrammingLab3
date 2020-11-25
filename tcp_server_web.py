import socket, sys, argparse, requests
from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema, SSLError, ConnectionError

class Node:
	def __init__(self, data):
    		self.data = data
    		self.children = []

class Server:
	MAX_BYTES = 65535

	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.count_leaf_p = 0
		self.count_img = 0

	def run(self):
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('localhost', 1234))
		self.sock.listen(1)
		print("Server is listening at ", self.sock.getsockname())

		while True:
			s, sockname = self.sock.accept()
			print("Connection accepted from the client ", sockname)
			url = (s.recv(self.MAX_BYTES)).decode()
			try:
				self.processing(url)
				result = "The number of the leaf paragraph nodes: "+str(self.count_leaf_p)+"\nThe number of the images: "+str(self.count_img)
			except (MissingSchema, SSLError):
				result = "Not a correct URL. "
			except ConnectionError:
				result = "Connection Error. Try again. (Check URL). "
			s.sendall(result.encode())
			self.count_img = 0
			self.count_leaf_p = 0

	def processing(self, url):
		content = requests.get(url).text
 		soup = BeautifulSoup(content, 'lxml')
		html = soup.html   #root tag

 		c = 0   #the number of all the tags
		for tag in soup.findAll():
			c += 1

		num = []   #for the names of the nodes
		for i in range(0, c):
			num.append(i)

		node_name = "node" + str(num[0])
		num.remove(num[0])
		globals()[node_name] = Node(html)   #node of the root tag
		self.create_tree(node0, num)
		self.traverse_leaf_p(node0)
		self.traverse_img(node0)

	def create_tree(self, node, arr):
		node_children = [ch for ch in node.data.children if ch.name is not None]
		for x in node_children:
			 node_name = "node" + str(arr[0])
			 arr.remove(arr[0])
			 globals()[node_name] = Node(x)
			 node.children.append(globals()[node_name])
			 self.create_tree(globals()[node_name], arr)

	def traverse_leaf_p(self, node):
		node_desc = [desc.name for desc in node.data.descendants if desc.name is not None]
		if node.data.name == 'p' and 'p' not in node_desc:
			self.count_leaf_p += 1
		for x in node.children:
			self.traverse_leaf_p(x)

	def traverse_img(self, node):
		if node.data.name == 'img':
			self.count_img += 1
		for x in node.children:
			self.traverse_img(x)

class Client:
	MAX_BYTES = 65535

	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def run(self, url):
		self.sock.connect(('localhost', 1234))
		print("Client is running at ", self.sock.getsockname())
		print("Connection established with the server ", self.sock.getpeername())

		self.sock.sendall(url.encode())
		received = (self.sock.recv(self.MAX_BYTES)).decode()
		print(received)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "sending data by TCP")
	choices = {"client": Client, "server": Server}
	parser.add_argument("role", choices = choices, help = "server or client")
	if sys.argv[1] == "client":
		parser.add_argument("-p", type = str, help = "link of the web page")

	args = parser.parse_args()
	classname = choices[args.role]

	if args.role == "client":
		endpoint = classname()
		endpoint.run(args.p)
	elif args.role == "server":
		endpoint = classname()
		endpoint.run()
