# UDP client example

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
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while 1:
	data = raw_input("Type something(q or Q to exit): ")
	if (data <> 'q' and data <> 'Q'):
		client_socket.sendto(data, ("localhost",5000))
	else:
		break
client_socket.close()
