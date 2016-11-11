//ModelListener.java

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

public interface ModelListener
{
    public void modelReceived( ModelEvent event ) ;
}
