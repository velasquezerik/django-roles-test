//UDPClient.java

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

class UDPClient
{
   public static void main(String args[]) throws Exception
   {

   	  byte[] send_data = new byte[1024];

      BufferedReader infromuser =
                        new BufferedReader(new InputStreamReader(System.in));

      DatagramSocket client_socket = new DatagramSocket();

      InetAddress IPAddress =  InetAddress.getByName("127.0.0.1");

      while (true)
      {

      	System.out.println("Type Something (q or Q to quit): ");

      	String data = infromuser.readLine();

      	if (data.equals("q") || data.equals("Q"))
      	break;

      	else

      	{

      	send_data = data.getBytes();

        DatagramPacket send_packet = new DatagramPacket(send_data, send_data.length, IPAddress, 5000);

        client_socket.send(send_packet);

        }

      }

      client_socket.close();
   }
}
