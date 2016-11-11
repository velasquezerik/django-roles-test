import java.io.*;
import galatea.glider.*;
class Gate extends Node {
    Gate() {
        super("gate", 'I');
        Glider.nodesl.add(this);
    }
    @Override
    public void fact() {
        it(GRnd.expo(ModelThread.InArrTime));
        System.out.print("ARRIVE:\t" + Glider.getTime());
        Glider.act(0, ModelThread.showLength);
        sendto(Glider.mess, ModelThread.teller);
    }
}
