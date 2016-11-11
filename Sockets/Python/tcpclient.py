# TCP client example

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
"""

data = "0 Exit"
data = "1 Start"
data = "2 Sleep value"
data = "3 Stop"
data = "4 Yield"
data = "5 Pause"
data = "6 Set Var value"
data = "7 Get Var"
data = "8 Informacion"
data = "9 Informacion"
"""
import time
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 5000))

"""
while 1:
    print "Waiting respond:"
    data = client_socket.recv(512)
    if ( data == 'q' or data == 'Q'):
        client_socket.close()
        break;
    else:
        print "RECIEVED:" , data
        data = raw_input ( "SEND( TYPE q or Q to Quit):" )
        if (data <> 'Q' and data <> 'q'):
            client_socket.sendall(data)
        else:
            client_socket.send(data)
            client_socket.close()
            break;
"""
"""
while 1:
    for x in range(1,10):
        data = str(x) + " Informacion\n"
        client_socket.sendall(data)
        time.sleep(5)

    data = "0 Informacion\n"
    client_socket.sendall(data)
    client_socket.close()
    break;
"""
data = "7 Get valores"
client_socket.sendall(data)
time.sleep(5)

data = "1 Start"
client_socket.sendall(data)
time.sleep(5)

data = "7 Get valores"
client_socket.sendall(data)
time.sleep(5)

data = "6 Set valores 1000"
client_socket.sendall(data)
time.sleep(5)

data = "7 Get valores"
client_socket.sendall(data)
time.sleep(5)

data = "0 Exit"
client_socket.sendall(data)
time.sleep(1)
client_socket.close()
