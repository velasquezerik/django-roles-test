# TCP server example

"""
    <GALATEA WEB: Web system simulations>
    Copyright (C) 2016  Erik Velasquez erikvelasquez.25@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 5000))
server_socket.listen(5)

print "TCPServer Waiting for client on port 5000"

while 1:
	client_socket, address = server_socket.accept()
	print "I got a connection from ", address
	while 1:
		data = raw_input ( "SEND( TYPE q or Q to Quit):" )
	 	if (data == 'Q' or data == 'q'):
			client_socket.send (data)
			client_socket.close()
			break;
		else:
			client_socket.send(data)

                data = client_socket.recv(512)
                if ( data == 'q' or data == 'Q'):
			client_socket.close()
			break;
		else:
			print "RECIEVED:" , data
