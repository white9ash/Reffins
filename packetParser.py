from scapy.layers.inet import UDP, TCP, IP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import ARP
from scapy.packet import Padding, Raw


class Parser:
    def __init__(self):
        self.packetdict = {}
        self.pid = None

    def UpdateDict(self,packet):
        pid = str(id(packet))
        self.packetdict[pid] = packet
        self.pid = pid
        return pid

    def ParsePacket(self,pid,time):
        packet = self.packetdict[pid]
        info = {
            "protocol": "Unknown",
            "source": "N/A",
            "destination": "N/A",
            "time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "length":len(packet),
            "summary": packet.summary()
        }
        if IP in packet:
            ip_layer = packet[IP]
            info['source'] = ip_layer.src
            info['destination'] = ip_layer.dst
            # print(f"IP Packet: {ip_layer.src} -> {ip_layer.dst}")
            if TCP in packet:
                info["protocol"] = "TCP"
                info['source'] = f"{ip_layer.src}:{packet[TCP].sport}"
                info['destination'] = f"{ip_layer.dst}:{packet[TCP].dport}"
            elif UDP in packet:
                info["protocol"] = "UDP"
                info['source'] = f"{ip_layer.src}:{packet[UDP].sport}"
                info['destination'] = f"{ip_layer.dst}:{packet[UDP].dport}"
            # 检查 IPv6 包
        elif IPv6 in packet:
            ip_layer = packet[IPv6]
            info['source'] = ip_layer.src
            info['destination'] = ip_layer.dst
            # print(f"IP Packet: {ip_layer.src} -> {ip_layer.dst}")
            if TCP in packet:
                info["protocol"] = "(IPv6)TCP"
                info['source'] = f"{ip_layer.src}:{packet[TCP].sport}"
                info['destination'] = f"{ip_layer.dst}:{packet[TCP].dport}"
            elif UDP in packet:
                info["protocol"] = "(IPv6)UDP"
                info['source'] = f"{ip_layer.src}:{packet[UDP].sport}"
                info['destination'] = f"{ip_layer.dst}:{packet[UDP].dport}"
            else:
                info["protocol"] = "Other(IPv6)"
            # 检查 ARP 包
        elif ARP in packet:
            arp_layer = packet[ARP]
            info["source"] = arp_layer.psrc
            info['destination'] = arp_layer.pdst
            info['protocol'] = "ARP"
        layer = None
        for var,c in self.GetPacketLayers(packet):
            if not isinstance(var, (Padding, Raw)):
                layer = var
        info["protocol"] = layer.name
        return info

    def GetPacketLayers(self,packet):
        counter = 0
        while True:
            layer = packet.getlayer(counter)
            if layer is None:
                break
            yield [layer,counter]
            counter += 1