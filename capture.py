import scapy.interfaces
from scapy import all
import queue
from scapy.arch.common import compile_filter
import threading
class Capture:
    def __init__(self):
        self.interfaces = self.GetAllInterfaceName()
        self.filter = ""
        self.sniffIface = None
        self.packetQueue = queue.Queue()
        self.semaphore = threading.Semaphore(0)
        self.running = True
        self.packetNumber = 0
        self.sniffer = None
        pass

    def GetAllInterfaceName(self):
        ifaces = scapy.interfaces.get_working_ifaces()
        ifaceNames = []
        for iface in ifaces:
            ifaceNames.append(iface.name)
        return ifaceNames

    # GetAllInterface()

    def RunSniff(self):
        if self.sniffIface not in self.interfaces:
            print(f"Interface {self.sniffIface} not found ")
            return
        if self.sniffer:
            self.sniffer.stop()
            self.sniffer = None
        self.sniffer = all.AsyncSniffer(iface=self.sniffIface, prn=self.PacketCallback, filter=self.filter)
        self.sniffer.start()

    def PacketCallback(self,packet):
        self.packetQueue.put(packet)
        self.semaphore.release()

    def CheckFilter(self,filterText):
        exp = filterText.strip()
        if len(exp)==0:
            return True
        try:
            compile_filter(filter_exp=exp)
        except Exception:
            return False
        return True


