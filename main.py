from tkinter import *
from tkinter import ttk

root = Tk()

class APP():
    def __init__(self):
        self.root = root
        self.new_window = None
        self.window()
        self.windows_frames()
        self.button()
        self.texto()


        root.mainloop()
        
    def window(self):
        self.root.title("Financer")
        self.root.configure(background="#1b1b1b")
        self.root.geometry("960x620")
        self.root.resizable(False, False)
        
    def windows_frames(self):
        
        self.frame_1 = Frame(self.root, bd=0, bg="#1b1b1b")
        self.frame_1.place(relx=0 , rely=0, relwidth=1, relheight=0.4)

        self.frame_2 = Frame(self.root, bg="#1b1b1b")
        self.frame_2.place(relx=0.17 , rely=0.4, relwidth=0.66, relheight=0.123)
        
        self.frame_3 = Frame(self.root, bg="#1b1b1b")
        self.frame_3.place(relx=0.17 , rely=0.525, relwidth=0.66, relheight=0.475)
        
        
        
    def button(self):
        self.bt_conf = Button(self.frame_1, background="#FC6E20")
        self.bt_conf.place(relx=0.945, rely=0, relwidth=0.055, relheight=0.2)

        self.bt_prof = Button(self.frame_1, background="#FC6E20", command=self.change_valor)
        self.bt_prof.place(relx=0, rely=0, relwidth=0.055, relheight=0.2)
        
        self.bt_add = Button(self.frame_2, background="#FC6E20", command=self.add_window)
        self.bt_add.place(relx=0.425, rely=0.6, relwidth=0.15, relheight=0.4)

    def texto(self):
        main_valor = 1000
        laranja = 0
        if main_valor > 9999:
            laranja = 0.7255    
        elif main_valor < 1000:
            laranja = 0.65

        else:
            laranja = 0.685


        self.valor = Label(self.frame_1, text=main_valor,justify="center", font=("Roboto", 100, ),fg="#FFE7D0", bg="#1b1b1b")
        self.valor.place(relx=0.5, rely=0.7, anchor="center")
        
        self.cent = Label(self.frame_1, text=".09", font=("Roboto", 33),fg="#FFE7D0", bg="#1b1b1b")
        self.cent.place(relx=laranja, rely=0.57, anchor="center")

      

        self.rs = Label(self.frame_1, text="R$", font=("Roboto", 50),fg="#FFE7D0", bg="#1b1b1b")
        self.rs.place(relx=0.25, rely=0.6, anchor="center")

    def verificar(self, janela):
            try:
                return janela.winfo_exists()
            except:
                return False

    def add_window(self):
        if self.new_window is None or not self.verificar(self.new_window):
            self.new_window = Toplevel(self.root)
            self.new_window.title("teste")
            self.new_window.geometry("600x400")
            self.new_window.resizable(False,False)
            self.new_window.configure(background="#1b1b1b")


            self.new_window.protocol("WM_DELETE_WINDOW", self.on_close)
        else:
            pass
    def on_close(self):
        self.new_window.destroy()
        self.new_window = None

APP()