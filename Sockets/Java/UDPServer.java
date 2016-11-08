//UDPServer.java

/*
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
*/

import java.net.*;
import java.io.*;


class UDPServer
{
   public static void main(String args[]) throws Exception
      {

      	 byte[] receive_data = new byte[1024];
         byte[] send_data = new byte[1024];

         int recv_port;

         DatagramSocket server_socket = new DatagramSocket(5000);

         System.out.println ("UDPServer Waiting for client on port 5000");


         while(true)
         {

          DatagramPacket receive_packet = new DatagramPacket(receive_data, receive_data.length);

                  server_socket.receive(receive_packet);

                  String data = new String(receive_packet.getData(),0 , 0, receive_packet.getLength());

                  InetAddress IPAddress = receive_packet.getAddress();

                  recv_port = receive_packet.getPort();

                  if (data.equals("q") || data.equals("Q"))
                  break;

                  else

                  System.out.println("( " + IPAddress + " , " + recv_port + " ) said :" + data );


         }
      }
}
