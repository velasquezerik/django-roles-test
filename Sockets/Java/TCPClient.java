//TCPClient.java

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

import java.io.*;
import java.net.*;

class TCPClient
{
 public static void main(String argv[]) throws Exception
 {
  String FromServer;
  String ToServer;

  Socket clientSocket = new Socket("localhost", 5000);

  BufferedReader inFromUser =
                 new BufferedReader(new InputStreamReader(System.in));

  PrintWriter outToServer = new PrintWriter(
     clientSocket.getOutputStream(),true);

  BufferedReader inFromServer = new BufferedReader(new InputStreamReader(
     clientSocket.getInputStream()));

  while (true)
  {

    FromServer = inFromServer.readLine();

    if ( FromServer.equals("q") || FromServer.equals("Q"))
        {
        clientSocket.close();
        break;
        }

    else

        {
         System.out.println("RECIEVED:" + FromServer);
         System.out.println("SEND(Type Q or q to Quit):");

         ToServer = inFromUser.readLine();

         if (ToServer.equals("Q") || ToServer.equals("q"))
         {
         outToServer.println (ToServer) ;
         clientSocket.close();
            break;
         }

        else
        {
            outToServer.println(ToServer);
        }
      }
    }
  }
}
