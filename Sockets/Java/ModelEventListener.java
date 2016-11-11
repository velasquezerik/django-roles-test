//ModelEventListener.java

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
import java.util.*;

public class ModelEventListener implements ModelListener
{
  Socket _connected;
  PrintWriter outToClient;
  public ModelEventListener(Socket connected) 
  {

    try
    {
      _connected = connected;
      //Buffer out for client data
      outToClient = new PrintWriter( connected.getOutputStream(),true);
    }
    catch (IOException e) {
        System.out.println(e);
        System.exit(1);
    }
  }
  public void modelReceived( ModelEvent event )
  {
    System.out.println ("Event " + event.type() + " description: " + event.description() );
    String data = "Event " + event.type() + " description: " + event.description() ;
    outToClient.println(data);
  }
}
