import customtkinter as ctk
from tkinter import font as tkfont  # IMPORTANTE para registrar a fonte
from PIL import Image
import os
import sys
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except Exception:
        base_path = os.path.abspath(".")  # modo script normal
    return os.path.join(base_path, relative_path)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class Login:
    def __init__(self):
        self.root = ctk.CTk(fg_color="#0d0d0d")

        # Registrar a fonte Nunito manualmente
        self.nome_user = None
        self.salario_user = None
    

        self.window()
        self.elements()
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_sem_dados)

    def window (self):
        self.root.geometry("854x480")
        self.root.title("CA$CALHO")
        self.root.resizable(False, False)
        self.extraframe = ctk.CTkFrame(self.root, fg_color="#0d0d0d", corner_radius=0)
        self.extraframe.place(relx=0, rely=0.5, relwidth=0.6, relheight=1, anchor="w")
        
        self.mainframe = ctk.CTkFrame(self.root, fg_color="#1b1b1b", corner_radius=0)
        self.mainframe.place(relx=1, rely=0.5, relwidth=0.4, relheight=1, anchor="e")


    def fechar(self):

        
        nome = self.nome.get()
        salario = float(self.salario.get())

        if not nome:
            self.caution = ctk.CTkLabel(self.mainframe, text="Por favor insira seus dados",font=("Nunito", 20, "bold"), text_color="#BF1700" )
            self.caution.place(anchor="center", relx=0.5, rely=0.8, )
        elif not salario or salario == 0:
            self.caution = ctk.CTkLabel(self.mainframe, text="Por favor insira seus dados",font=("Nunito", 20, "bold"), text_color="#BF1700" )
            self.caution.place(anchor="center", relx=0.5, rely=0.8, )
        else:
            self.nome_user = nome
            self.salario_user = salario

            self.root.destroy() 

    def elements (self):

##Titulo a ser exibido

        self.logo = ctk.CTkImage(
            light_image=Image.open(resource_path("./images/LOGO.png")),  # imagem no modo claro
            dark_image=Image.open(resource_path("./images/LOGO.png")),   # imagem no modo escuro
            size=(280, 160)  # tamanho desejado
        )
        self.tipografia = ctk.CTkImage(
            light_image=Image.open(resource_path("./images/TIPOGRAFIA.png")),  # imagem no modo claro
            dark_image=Image.open(resource_path("./images/TIPOGRAFIA.png")),   # imagem no modo escuro
            size=(380, 252)  # tamanho desejado
        )
        

        self.enunciado = ctk.CTkLabel(self.mainframe, text="", image=self.logo)
        self.enunciado.place(anchor="center" , relx=0.5, rely=0.125)

        self.art = ctk.CTkLabel(self.extraframe, text="", image=self.tipografia)
        self.art.place(anchor="center" , relx=0.5, rely=0.4)




        self.hello = ctk.CTkLabel(self.mainframe, text="Nome:",font=("Nunito", 20, "bold") )
        self.hello.place(anchor="center", relx=0.2625, rely=0.22, )

        self.saldo = ctk.CTkLabel(self.mainframe, text="Saldo:",font=("Nunito", 20, "bold") )
        self.saldo.place(anchor="center", relx=0.26, rely=0.42, )

        self.nome = ctk.CTkEntry(self.mainframe, height=45,fg_color="#3f3f3f", border_width=0)
        self.nome.place(anchor="n", relx=0.5, rely=0.25, relwidth=0.65)

        # Função para aceitar apenas números e ponto
        def somente_numeros(action, value_if_allowed):
            if action == "1":  # se for inserção
                if value_if_allowed in ("", ".", ","):
                    return True  # permite vazio ou só ponto vírgula temporário
                try:
                    float(value_if_allowed.replace(",", "."))  # permite vírgula como ponto
                    return True
                except ValueError:
                    return False
            return True  # permite deleção

        # Registrar a validação
        vcmd = (self.root.register(somente_numeros), "%d", "%P")

        # Entry com validação
        self.salario = ctk.CTkEntry(self.mainframe, height=45,placeholder_text="Salario, mesada ou saldo atual",fg_color="#3f3f3f", border_width=0, validatecommand=vcmd,validate="key")
        self.salario.place(anchor="n", relx=0.5, rely=0.45, relwidth=0.65)


        self.button = ctk.CTkButton(self.mainframe, fg_color="#00bf63", hover_color="#236A48", text="salvar", height=40, command=self.fechar, font=("Nubito", 20))
        self.button.place(anchor="center", relx=0.5, rely=0.675, relwidth=0.33)

        


    def fechar_sem_dados(self):
        # Quando o usuário fecha a janela pelo X
        self.nome_user = None
        self.salario_user = None
        self.root.destroy()

if __name__ == "__main__":
    app = Login()
    app.root.mainloop()

