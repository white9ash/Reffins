"""
auther:white9ash
"""
import time
from tkinter import messagebox

from scapy.arch.common import compile_filter
from scapy.utils import hexdump
from capture import Capture
from datetime import datetime
from packetParser import Parser
from ui import Win
import threading


class Controller:
    ui: Win

    def __init__(self):
        self.capture = Capture()
        self.parser = Parser()
        self.updateThread = None
        self.selectedIface = None
        self.startBtnStatus = "start"
        self.packetMaxSize = 1024
        self.filterBlank = True

    def init(self, ui):
        """
        get UI instance
        """
        self.ui = ui
        self.InitIfaceCombobox()
        self.InitStartBtn()
        self.InitPacketTreeView()
        self.InitLayerTreeView()
        self.InitHexTextBox()
        self.InitFilterInputBox("Input BPF Expression...")

    # region widget initialize
    def InitIfaceCombobox(self):
        self.ui.tk_select_box_IfaceCombobox["value"] = self.capture.interfaces
        self.ui.tk_select_box_IfaceCombobox.current(0)

    def InitFilterInputBox(self,text):
        self.filterBlank = True
        self.ui.tk_input_FilterTextBox.delete(0, 'end')
        self.ui.tk_input_FilterTextBox.insert(0, text)
        self.ui.tk_input_FilterTextBox.config(foreground='gray')

    def InitPacketTreeView(self):
        columns = {"Protocl": 100, "Source": 150, "Destination": 150, "Time": 160, "Length": 100, "Info": 500}
        self.ui.tk_table_PacketTreeView.config(columns=list(columns), show="headings", selectmode="extended")
        for text, width in columns.items():  # 批量设置列属性
            self.ui.tk_table_PacketTreeView.heading(text, text=text, anchor='center')
            self.ui.tk_table_PacketTreeView.column(text, anchor='center', width=width, stretch=True)

    def InitLayerTreeView(self):
        self.ui.tk_table_LayerTreeView.config(show="tree headings", )
        self.ui.tk_table_LayerTreeView["columns"] = ("Columns 1",)
        self.ui.tk_table_LayerTreeView.heading("#0", text="", anchor="w")
        self.ui.tk_table_LayerTreeView.heading("Columns 1", anchor="w", text="Packet Detail", )
        self.ui.tk_table_LayerTreeView.column("#0", anchor='w', width=20, stretch=False)
        self.ui.tk_table_LayerTreeView.column("Columns 1", anchor='w', width=400, stretch=True, )

    def InitHexTextBox(self):
        self.ui.tk_text_HexTextBox.config(state="normal")
        self.ui.tk_text_HexTextBox.delete(1.0, "end")
        self.ui.tk_text_HexTextBox.config(state="disabled")
        pass

    def InitStartBtn(self):
        self.ui.tk_button_StartTbn.config(text="Start")

    # endregion
    # region event handler functions
    def PacketItemSelected(self, evt):
        selectedItem = self.ui.tk_table_PacketTreeView.selection()
        try:
            selectedpid = self.ui.tk_table_PacketTreeView.item(selectedItem, "tags")[0]
        except:
            return
        self.UpdateHexText(selectedpid)
        self.UpdateLayerTreeView(selectedpid)

    def LayerItemSelected(self, evt):
        selectedPacket = self.ui.tk_table_PacketTreeView.selection()
        selectedLayerItem = self.ui.tk_table_LayerTreeView.selection()
        try:
            selectedpid = self.ui.tk_table_PacketTreeView.item(selectedPacket, "tags")[0]
            counter = self.ui.tk_table_LayerTreeView.item(selectedLayerItem, "tags")[0]
        except:
            return
        selectedLayerParent = self.ui.tk_table_LayerTreeView.parent(selectedLayerItem)
        if selectedLayerParent != '':
            return
        self.UpdateHexText(selectedpid, counter)

    def StartBtnClicked(self, evt):
        if self.startBtnStatus == "start":
            self.Reset()
            if self.StartSniff():
                self.ChangeStartBtn()
        else:
            self.StopSniff()
            self.ChangeStartBtn()

    def FilterTextBoxClicked(self, evt):
        if self.ui.tk_input_FilterTextBox.get() == "Input BPF Expression...":
            self.filterBlank = False
            self.ui.tk_input_FilterTextBox.delete(0, "end")  # 删除提示文本
            self.ui.tk_input_FilterTextBox.config(foreground='black')  # 设置为黑色

    def FilterTextBoxFocusOut(self, evt):
        if self.ui.tk_input_FilterTextBox.get() == "":
            self.ui.tk_input_FilterTextBox.insert(0, "Input BPF Expression...")  # 恢复提示文本
            self.filterBlank = True
            self.ui.tk_input_FilterTextBox.config(foreground='gray')  # 提示文本灰色

    def IfaceItemSelected(self, evt):
        selectedItem = self.ui.tk_select_box_IfaceCombobox.get()
        # print(selectedItem,evt)
        return selectedItem

    def UpdatePacketItem(self):
        while self.capture.running:
            self.capture.semaphore.acquire()
            try:
                packet = self.capture.packetQueue.get()  #
            except self.capture.packetQueue.empty():
                continue  # Retry if no packets are available
            pid = self.parser.UpdateDict(packet)
            info = self.parser.ParsePacket(pid, datetime.now())
            items = self.ui.tk_table_PacketTreeView.get_children()
            if len(items) >= 1024:
                self.ui.tk_table_PacketTreeView.delete(items[0])
            self.ui.tk_table_PacketTreeView.insert("", "end", values=(info["protocol"], info["source"],
                                                                      info["destination"], info['time'], info['length'],
                                                                      info['summary']), tags=(pid,))

    # endregion
    # region control functions
    def ChangeStartBtn(self):
        if self.startBtnStatus == "start":
            self.ui.tk_button_StartTbn.config(text="Stop")
            self.startBtnStatus = "stop"
        else:
            self.ui.tk_button_StartTbn.config(text="Start")
            self.startBtnStatus = "start"

    def UpdateHexText(self, selectedpid, counter=None):
        self.ui.tk_text_HexTextBox.config(state="normal")
        self.ui.tk_text_HexTextBox.delete(1.0, "end")
        if self.parser.packetdict.get(selectedpid) is None:
            self.ui.tk_text_HexTextBox.config(state="disabled")
            return
        if counter is None:
            self.ui.tk_text_HexTextBox.insert('end', hexdump(self.parser.packetdict[selectedpid], dump=True))
        else:
            layer = self.parser.packetdict[selectedpid].getlayer(int(counter))
            self.ui.tk_text_HexTextBox.insert('end', hexdump(layer, dump=True))
        self.ui.tk_text_HexTextBox.config(state="disabled")

    def UpdateLayerTreeView(self, selectedpid):
        for i in self.ui.tk_table_LayerTreeView.get_children():
            self.ui.tk_table_LayerTreeView.delete(i)
        packet = self.parser.packetdict[selectedpid]
        for layer, counter in self.parser.GetPacketLayers(packet):
            item = self.ui.tk_table_LayerTreeView.insert("", "end", values=(layer.name,), tags=(counter,))
            for field, value in layer.fields.items():
                self.ui.tk_table_LayerTreeView.insert(item, "end", values=f"{field}:{value}")

    def StopSniff(self):
        self.capture.running = False

        while not self.capture.packetQueue.empty():
            self.capture.packetQueue.get()
        self.capture.packetNumber = 0
        print("stop!")

    def StartSniff(self):
        self.capture.filter = self.ui.tk_input_FilterTextBox.get()
        if self.filterBlank:
            self.capture.filter = ""
        self.InitHexTextBox()
        try:
            compile_filter(filter_exp=self.capture.filter)
        except:
            messagebox.showerror("Error!", "There is an error in filter syntax, please re-enter!")
            self.InitFilterInputBox("")
            self.capture.filter = ""
            return False
        print("start!", "filterText=", self.capture.filter)
        self.capture.sniffIface = self.ui.tk_select_box_IfaceCombobox.get()
        self.updateThread = threading.Thread(target=self.UpdatePacketItem, daemon=True)
        self.capture.running = True
        self.parser.startTime = time.time()
        self.capture.RunSniff()
        self.updateThread.start()
        return True

    def Reset(self):
        for i in self.ui.tk_table_PacketTreeView.get_children():
            self.ui.tk_table_PacketTreeView.delete(i)
        for i in self.ui.tk_table_LayerTreeView.get_children():
            self.ui.tk_table_LayerTreeView.delete(i)
        self.ui.update()
        while not self.capture.packetQueue.empty():
            self.capture.packetQueue.get()
    # endregion
