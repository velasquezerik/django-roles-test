import galatea.glider.*;
class Teller extends Node {
    Teller() {
        super("teller", 'R');
        Glider.nodesl.add(this);
    }
    @Override
    public void fact() {
        sendto(Glider.mess, ModelThread.exit);
    }
    @Override
    public void fscan() {
        stay(GRnd.gauss(ModelThread.MeSerTime, ModelThread.DeSerTime));
    }
}
