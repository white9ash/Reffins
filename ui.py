import random
from tkinter import *
from tkinter.ttk import *
from ttkbootstrap import *
from PIL import Image, ImageTk
class WinGUI(Window):
    def __init__(self):
        super().__init__(themename="simplex", hdpi=True)
        self.__win()
        self.tk_frame_Container1 = self.__tk_frame_Container1(self)
        self.tk_table_PacketTreeView = self.__tk_table_PacketTreeView( self.tk_frame_Container1)
        self.tk_input_FilterTextBox = self.__tk_input_FilterTextBox(self)
        self.tk_select_box_IfaceCombobox = self.__tk_select_box_IfaceCombobox(self)
        self.tk_button_StartTbn = self.__tk_button_StartTbn(self)
        self.tk_frame_Container2 = self.__tk_frame_Container2(self)
        self.tk_table_LayerTreeView = self.__tk_table_LayerTreeView( self.tk_frame_Container2)
        self.tk_label_FilterLabel = self.__tk_label_FilterLabel(self)
        self.tk_label_IfaceLabel = self.__tk_label_IfaceLabel(self)
        self.tk_frame_container3 = self.__tk_frame_container3(self)
        self.tk_text_HexTextBox = self.__tk_text_HexTextBox( self.tk_frame_container3)
    def __win(self):
        self.title("Reffins")
        width = 1000
        height = 650
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    def scrollbar_autohide(self,vbar, hbar, widget):
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def new_style(self,widget):
        ctl = widget.cget('style')
        ctl = "".join(random.sample('0123456789',5)) + "." + ctl
        widget.configure(style=ctl)
        return ctl
    def __tk_frame_Container1(self,parent):
        frame = Frame(parent,bootstyle="default")
        frame.place(x=19, y=60, width=958, height=160)
        return frame
    def __tk_table_PacketTreeView(self,parent):

        columns = {"ID":185,"字段#1":278,"字段#2":464}
        tk_table = Treeview(parent, show="headings", columns=list(columns),bootstyle="default")
        for text, width in columns.items():
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)

        tk_table.place(x=0, y=0, width=929, height=160)
        self.create_bar(parent, tk_table,True, True,0, 0, 929,160,958,160)
        return tk_table
    def __tk_input_FilterTextBox(self,parent):
        ipt = Entry(parent, bootstyle="default")
        ipt.place(x=603, y=15, width=237, height=30)
        return ipt
    def __tk_select_box_IfaceCombobox(self,parent):
        cb = Combobox(parent, state="readonly", bootstyle="default")
        cb['values'] = ("")
        cb.place(x=191, y=16, width=301, height=30)
        return cb
    def __tk_button_StartTbn(self,parent):
        btn = Button(parent, text="Start", takefocus=False,bootstyle="default")
        btn.place(x=878, y=11, width=50, height=30)
        return btn
    def __tk_frame_Container2(self,parent):
        frame = Frame(parent,bootstyle="default")
        frame.place(x=21, y=226, width=490, height=183)
        return frame
    def __tk_table_LayerTreeView(self,parent):
        columns = {}
        tk_table = Treeview(parent, show="headings", columns=list(columns),bootstyle="default")
        for text, width in columns.items():
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)

        tk_table.place(x=0, y=0, width=466, height=183)
        return tk_table
    def __tk_label_FilterLabel(self,parent):
        label = Label(parent,text="Fillter:",anchor="center", bootstyle="default")
        label.place(x=520, y=16, width=70, height=30)
        return label
    def __tk_label_IfaceLabel(self,parent):
        label = Label(parent,text="Interfaces:",anchor="center", bootstyle="default")
        label.place(x=69, y=13, width=111, height=30)
        return label
    def __tk_frame_container3(self,parent):
        frame = Frame(parent,bootstyle="default")
        frame.place(x=20, y=424, width=957, height=215)
        return frame
    def __tk_text_HexTextBox(self,parent):
        text = Text(parent)
        text.place(x=0, y=2, width=750, height=213)
        self.create_bar(parent, text,True, True, 0, 2, 750,213,957,215)
        return text
class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
    def __event_bind(self):
        self.tk_table_PacketTreeView.bind('<<TreeviewSelect>>',self.ctl.PacketItemSelected)
        self.tk_select_box_IfaceCombobox.bind('<<ComboboxSelected>>',self.ctl.IfaceItemSelected)
        self.tk_button_StartTbn.bind('<Button-1>',self.ctl.StartBtnClicked)
        self.tk_table_LayerTreeView.bind('<<TreeviewSelect>>',self.ctl.LayerItemSelected)
        self.tk_input_FilterTextBox.bind('<FocusIn>',self.ctl.FilterTextBoxClicked)
        self.tk_input_FilterTextBox.bind('<FocusOut>',self.ctl.FilterTextBoxFocusOut)
        pass
    def __style_config(self):
        sty = Style()
        sty.configure(self.new_style(self.tk_button_StartTbn),font=("微软雅黑",-12))
        sty.configure(self.new_style(self.tk_label_FilterLabel),font=("微软雅黑",-16))
        sty.configure(self.new_style(self.tk_label_IfaceLabel),font=("微软雅黑",-16))
        pass
if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()