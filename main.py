import os
import sys
import subprocess


def instalar_fonte():
    """
    Instala a fonte Nunito no Windows copiando para a pasta Fonts.
    Só tenta instalar se não encontrar a fonte já registrada.
    """
    try:
        # Verifica se já está instalada (apenas Windows)
        result = subprocess.run(['reg', 'query',
                                 r'HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts',
                                 '/v', 'Nunito (TrueType)'],
                                capture_output=True, text=True)
        if "Nunito" in result.stdout:
            print("✅ Fonte Nunito já está instalada.")
            return

        # Caminho da fonte embutida no executável
        if getattr(sys, 'frozen', False):
            # Quando empacotado com PyInstaller
            pasta_base = sys._MEIPASS
        else:
            pasta_base = os.path.dirname(os.path.abspath(__file__))

        caminho_fonte = os.path.join(pasta_base, "fonts", "Nunito.ttf")

        # Copia a fonte para a pasta do Windows
        subprocess.run(['powershell', '-Command',
                        f'Copy-Item "{caminho_fonte}" "$env:windir\\Fonts" ; ' +
                        f'Reg Add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" /v "Nunito (TrueType)" /t REG_SZ /d "Nunito.ttf" /f'],
                        check=True)
        print("✅ Fonte Nunito instalada com sucesso!")

    except Exception as e:
        print("⚠️ Erro ao instalar a fonte:", e)

# Chama a função no início
instalar_fonte()

def resource_path(relative_path):
    """ Retorna o caminho absoluto para um recurso, funciona no Python e no PyInstaller """
    try:
        base_path = sys._MEIPASS  # Se estiver rodando no exe PyInstaller
    except Exception:
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)  # exe
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))  # script
    return os.path.join(base_path, relative_path)



import customtkinter as ctk
from Login import Login
import math, requests
from tkcalendar import DateEntry
from tkinter import font
from PIL import Image
from data.database import Usuario_cascalho, Movimentacao
from datetime import datetime


def cotacao_dolar():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data['USDBRL']['bid'])
    except Exception as e:
        return 5.4  # fallback

converter = cotacao_dolar()


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def get_font_path(font_name="Nunito.ttf"):
    """
    Retorna o caminho absoluto para a fonte, seja rodando no Python ou no executável.
    """
    if getattr(sys, 'frozen', False):
        # Rodando no executável
        base_path = sys._MEIPASS
    else:
        # Rodando no Python normal
        base_path = os.path.abspath(".")
    return os.path.join(base_path, "fonts", font_name)

# Registra a fonte Nunito embutida
try:
    ctk.CTkFont(family=get_font_path(), size=16)
except Exception as e:
    print("⚠️ Erro ao carregar a fonte embutida:", e)
# ===============================================
from tkinter import font as tkFont

def load_embedded_font():
    """
    Registra a fonte Nunito para funcionar no customtkinter,
    mesmo sem estar instalada no Windows.
    """
    try:
        # Caminho do .ttf (dentro do projeto ou embutido no .exe)
        nunito_path = get_font_path("Nunito.ttf")

        # Cria a fonte com tkinter e dá o nome "Nunito"
        tkFont.Font(name="Nunito", file=nunito_path, size=16)
        print("✅ Fonte Nunito carregada com sucesso!")
    except Exception as e:
        print("⚠️ Erro ao carregar fonte Nunito:", e)

load_embedded_font()


usuario_definido = Usuario_cascalho.select().first()


if usuario_definido is None:
    app_login = Login()
    app_login.root.mainloop()

    user = getattr(app_login, 'nome_user', None)
    salario = getattr(app_login, 'salario_user', None)
    if user is None or salario is None:
        exit()
    usuario_definido = Usuario_cascalho.create(
        nome=user,
        salario=float(salario),
        maximo_valor=float(salario),
        moeda_atual="R$"  
    )


class APP:
    def __init__(self):
        self.item_count = 0
        self.root = ctk.CTk()
        self.usuario_definido = usuario_definido


        self.usuario = usuario_definido.nome
        self.main_valor = usuario_definido.salario
        self.max_valor = usuario_definido.maximo_valor
        self.cotacao = usuario_definido.moeda_atual  

        if not self.max_valor or self.max_valor <= 0:
            self.max_valor = max(self.main_valor, 1)

        self.new_window = None
        self.settings_window = None


        self.window()
        self.windows_frames()
        self.button()
        self.texto()
        self.progress_bar()
        self.scroll_list()
        self.root.mainloop()

    def window(self):
        self.root.title("CA$CALHO")
        self.root.geometry("854x480")
        self.root.resizable(False, False)

    def windows_frames(self):
        self.frame_1 = ctk.CTkFrame(self.root, fg_color="#1A1A1A", corner_radius=0)
        self.frame_1.place(relx=0, rely=0, relwidth=1, relheight=0.4)

        self.frame_3 = ctk.CTkFrame(self.root, fg_color="transparent", corner_radius=0, border_width=1, border_color="white")
        self.frame_3.place(relx=0.5, rely=1, relwidth=0.425, relheight=0.45, anchor="s")

        self.frame_2 = ctk.CTkFrame(self.root, fg_color="transparent", corner_radius=0, border_width=0, border_color="white")
        self.frame_2.place(anchor="n", relx=0.5, rely=0.38, relwidth=0.66, relheight=0.15)

    def button(self):
        self.config_image = ctk.CTkImage(
            light_image=Image.open(resource_path("images/CONFIG.png")),
            dark_image=Image.open(resource_path("images/CONFIG.png")),
            size=(35, 35)
        )

        self.bt_add = ctk.CTkButton(self.frame_2, text="adicionar", font=("Nunito", 15, "bold"), text_color="#FFFFFF",
                                    fg_color="#00bf63", height=35, hover_color="#236A48", command=self.add_window, corner_radius=5)
        self.bt_add.place(relx=0.425, rely=0.4, relwidth=0.15)

        self.bt_conf = ctk.CTkButton(self.frame_1, text="", fg_color="transparent", hover_color="#1A1A1A",
                                     width=50, height=50, bg_color="transparent", image=self.config_image, command=self.add_window2)
        self.bt_conf.place(relx=0.995, rely=0.025, anchor="ne")

    def salvar_saldo(self):
        self.usuario_definido.salario = self.main_valor
        self.usuario_definido.maximo_valor = self.max_valor
        self.usuario_definido.moeda_atual = self.cotacao  
        self.usuario_definido.save()

    def converter_moeda(self):
        tipo_moeda = self.moeda.get()
        if tipo_moeda == "Real" and self.cotacao == "$":
            self.cotacao = "R$"
            self.main_valor *= converter
            self.max_valor *= converter
            self.salvar_saldo()
            self.texto()
        elif tipo_moeda == "Dolar" and self.cotacao == "R$":
            self.cotacao = "$"
            self.main_valor /= converter
            self.max_valor /= converter
            self.salvar_saldo()
            self.texto()

    def alterar(self):
        novo_salario_str = self.mudar_salario.get().replace(",", ".")
        novo_nome_str = self.mudar_nome.get()

        if novo_salario_str != "":
            try:
                novo_salario = float(novo_salario_str)
                self.main_valor = novo_salario
                self.max_valor = max(novo_salario, 1)
                self.salvar_saldo()
                self.atualizar_progress()
                self.texto()
            except ValueError:
                ctk.CTkLabel(self.frame_settings, text="Dados inválidos", font=("Nunito", 20, "bold"),
                            text_color="#BF1700").place(anchor="center", relx=0.5, rely=0.8)
                return  
        if novo_nome_str != "" and novo_nome_str != self.usuario:
            self.usuario = novo_nome_str
            self.usuario_definido.nome = novo_nome_str
            self.usuario_definido.save()
            self.texto()

        if self.moeda.get() != ("Real" if self.cotacao == "R$" else "Dolar"):
            self.converter_moeda()

        self.settings_window.destroy()
    def atualizar_progress(self):
        progresso = max(0, min(self.main_valor / self.max_valor, 1))
        self.progress.set(progresso)

    def progress_bar(self):
        self.progress = ctk.CTkProgressBar(self.frame_2, width=450, height=10, progress_color="#00bf63")
        self.progress.place(relx=0.5, rely=0.125, anchor="center")
        self.atualizar_progress()

    def texto(self):
        self.valores()
        if hasattr(self, "valor"):
            self.valor.destroy()
            self.cent.destroy()
            self.rs.destroy()
            self.username.destroy()

        self.valor = ctk.CTkLabel(self.frame_1, text=int(self.reais), font=("Nunito", 110), text_color=self.cor_texto)
        self.valor.place(relx=0.5, rely=0.675, anchor="center")
        self.cent = ctk.CTkLabel(self.frame_1, text=f"{self.centavos:02}", font=("Nunito", 33), text_color=self.cor_texto)
        self.cent.place(relx=self.position_cent, rely=0.57, anchor="center")
        self.rs = ctk.CTkLabel(self.frame_1, text=self.cotacao, font=("Nunito", 50), text_color=self.cor_texto)
        self.rs.place(relx=self.position_rs, rely=0.6, anchor="center")
        self.username = ctk.CTkLabel(self.frame_1, text=f"Olá, {self.usuario}", font=("Nunito", 40), text_color="#FFFFFF")
        self.username.place(relx=0.5, rely=0.25, anchor="center")

    def valores(self):
        self.centavos, self.reais = math.modf(self.main_valor)
        self.centavos = int(round(self.centavos * 100))
        self.reais = int(self.reais)
        self.cor_texto = "#BF1700" if self.main_valor < 0 else "#FFFFFF"

    def delete(self):
        self.root.destroy()
        Usuario_cascalho.delete().execute()
        Movimentacao.delete().execute()

    def verificar(self):
        tamanho = len(str(int(self.main_valor)))
        self.position_cent = 0.03425 * tamanho + 0.545
        self.position_rs = -0.034 * tamanho + 0.44
        self.cor_texto = "#BF1700" if self.main_valor < 0 else "#FFFFFF"

    def atualizar_progress(self):
        progresso = max(0, min(self.main_valor / self.max_valor, 1))
        self.progress.set(progresso)

    def progress_bar(self):
        self.progress = ctk.CTkProgressBar(self.frame_2, width=450, height=10, progress_color="#00bf63")
        self.progress.place(relx=0.5, rely=0.125, anchor="center")
        self.atualizar_progress()

    def texto(self):
        self.verificar()
        self.valores()

        if hasattr(self, "valor"):
            self.valor.destroy()
            self.cent.destroy()
            self.rs.destroy()
            self.username.destroy()

        self.valor = ctk.CTkLabel(self.frame_1, text=int(self.reais), font=("Nunito", 110), text_color=self.cor_texto)
        self.valor.place(relx=0.5, rely=0.675, anchor="center")
        self.cent = ctk.CTkLabel(self.frame_1, text=f"{self.centavos:02}", font=("Nunito", 33), text_color=self.cor_texto)
        self.cent.place(relx=self.position_cent, rely=0.57, anchor="center")
        self.rs = ctk.CTkLabel(self.frame_1, text=self.cotacao, font=("Nunito", 50), text_color=self.cor_texto)
        self.rs.place(relx=self.position_rs, rely=0.6, anchor="center")
        self.username = ctk.CTkLabel(self.frame_1, text=f"Olá, {self.usuario}", font=("Nunito", 40), text_color="#FFFFFF")
        self.username.place(relx=0.5, rely=0.25, anchor="center")


    def certificar(self, janela):
        try:
            return janela.winfo_exists()
        except:
            return False

    def selecionar_categoria(self):
        if not hasattr(self, "movimen") or not self.movimen.winfo_exists():
            self.movimen = ctk.CTkOptionMenu(
                self.frame_card_add1,
                width=120,
                values=("Selecione", "Contas", "Transporte","Cartão", "Alimentação", "Lazer"),
                fg_color="#00bf63",button_color="#00bf63",button_hover_color="#236A48"
            )
            self.movimen.set("Selecione")   
            self.movimen.place(relx=0.56, rely=0.5, anchor="w")
        else:
            self.movimen.place(relx=0.56, rely=0.5, anchor="w")


    def esconder_teste(self):
        if hasattr(self, "movimen"):
            self.movimen.place_forget()

    def atualizar_radio(self):
        self.escolha = self.selecionado.get()
        if self.escolha == "gasto":
            self.selecionar_categoria()
        else:
            self.esconder_teste()

    def add_window(self):
        if self.new_window is None or not self.certificar(self.new_window):
            self.new_window = ctk.CTkToplevel(self.root)
            self.new_window.title("Adicionar movimentação")
            self.new_window.geometry("854x480")
            self.new_window.resizable(False, False)
            self.new_window.configure(fg_color="#1b1b1b")
                        
            self.new_window.protocol("WM_DELETE_WINDOW", self.on_close_window1)
            self.new_window.lift()
            self.new_window.grab_set()
            self.new_window.focus_force()

        self.frame_window = ctk.CTkFrame(self.new_window, fg_color="transparent")
        self.frame_window.place(relx=0.5, rely=0.5, relheight=0.9, relwidth=0.9, anchor="center")

        self.frame_card_add1 = ctk.CTkFrame(self.frame_window, fg_color="#242424", corner_radius=10)
        self.frame_card_add1.place(relx=1, rely=0.10, relwidth=0.4,relheight=0.15, anchor="ne")

        self.frame_card_add2 = ctk.CTkFrame(self.frame_window, fg_color="#242424", corner_radius=10)
        self.frame_card_add2.place(relx=1, rely=0.27, relwidth=0.4,relheight=0.15, anchor="ne")

        self.frame_card_add3 = ctk.CTkFrame(self.frame_window, fg_color="#242424", corner_radius=10)
        self.frame_card_add3.place(relx=1, rely=0.44, relwidth=0.4,relheight=0.15, anchor="ne")

        self.frame_card_add4 = ctk.CTkFrame(self.frame_window, fg_color="#242424", corner_radius=10)
        self.frame_card_add4.place(relx=1, rely=0.61, relwidth=0.4,relheight=0.15, anchor="ne")

        self.text_adicionar = ctk.CTkLabel(self.frame_window, text="Adicionar",font=("Nunito", 50,"bold"))
        self.text_adicionar.place(relx=0.2, rely=0.05, anchor="center")

        self.explain_desc = ctk.CTkImage(
            light_image=Image.open(resource_path("./images/DESC.png")), 
            dark_image=Image.open(resource_path("./images/DESC.png")),   
        size=(300, 200)  
        )
        self.explain_text = ctk.CTkLabel(self.new_window, image=self.explain_desc, text="")
        self.explain_text.place(relx=0.27, rely=0.375, anchor="center")


        self.nome_mov = ctk.CTkLabel(self.frame_card_add2, text="Descrição:", font=("Nunito", 25, "bold"))
        self.nome_mov.place(relx=0.05, rely=0.45, anchor="w")

        self.valor_mov = ctk.CTkEntry(self.frame_card_add2, width=120, height=40, border_width=0)
        self.valor_mov.place(relx=0.95, rely=0.45, anchor="e")

        self.nome_valor = ctk.CTkLabel(self.frame_card_add3, text="Valor:", font=("Nunito", 25, "bold"))
        self.nome_valor.place(relx=0.05, rely=0.45, anchor="w")

        self.valor_valor = ctk.CTkEntry(self.frame_card_add3, width=120, height=40, border_width=0)
        self.valor_valor.place(relx=0.95, rely=0.45, anchor="e")

        self.tipo_mov = ctk.CTkLabel(self.frame_card_add1, text="Tipo:", font=("Nunito", 25, "bold"))
        self.tipo_mov.place(relx=0.05, rely=0.45, anchor="w")

        self.selecionado = ctk.StringVar(value="")

        self.tipo_gasto = ctk.CTkRadioButton(
            self.frame_card_add1,
            text="Gasto",
            font=("Nunito", 15),
            variable=self.selecionado,
            value="gasto",
            fg_color="#00bf63",
            hover_color="#236A48",
            command=self.atualizar_radio)
        self.tipo_gasto.place(relx=0.3, rely=0.5, anchor="w")

        self.tipo_receita = ctk.CTkRadioButton(
            self.frame_card_add1,
            text="Receita",
            font=("Nunito", 15),
            fg_color="#00bf63",
            hover_color="#236A48",
            variable=self.selecionado,
            value="receita",
            command=self.atualizar_radio)
        self.tipo_receita.place(relx=0.6, rely=0.5, anchor="w")

        self.nome_data = ctk.CTkLabel(self.frame_card_add4, text="Data:", font=("Nunito", 25, "bold"))
        self.nome_data.place(relx=0.05, rely=0.45, anchor="w")

        self.cal = DateEntry(self.frame_card_add4, locale="pt_BR", firstweekday="sunday",selectbackground="#00bf63", date_pattern="dd/mm/yyyy", width=10, font=("Nunito", 25))
        self.cal.place(relx=0.95, rely=0.45, anchor="e")

        self.buton = ctk.CTkButton(self.frame_window, fg_color="#00bf63", text="salvar", width=100, command=self.exemplo, hover_color="#236A48")
        self.buton.place(relx=0.5, rely=0.9, anchor="center")

    def exemplo(self):
        self.nome_adicionar = self.valor_mov.get()
        self.valor_adicionar = self.valor_valor.get()
        self.data = self.cal.get()
        self.tipo = self.escolha
        self.categoria = None

        if hasattr(self, "movimen"):
            self.categoria = self.movimen.get()
            if self.categoria == "Selecione":
                self.categoria = None

        if self.nome_adicionar == "":
            self.explain = ctk.CTkLabel(self.frame_window, text="Insira um nome", font=("Nunito", 20), text_color="#00bf63")
            self.explain.place(relx=0.5, rely=0.7, anchor="center")
        else:
            try:
                self.valor_adicionar = float(self.valor_adicionar)
                data_formatada = datetime.strptime(self.data, "%d/%m/%Y").date()


                Movimentacao.create(
                    usuario=self.usuario_definido,
                    descricao=self.nome_adicionar,
                    valor=self.valor_adicionar,
                    data=data_formatada,
                    tipo=self.tipo,
                    categoria=self.categoria
                )


                if self.tipo == "receita":
                    self.main_valor += self.valor_adicionar
                else:
                    self.main_valor -= self.valor_adicionar

                self.salvar_saldo()
                self.texto()
                self.atualizar_progress()

                self.carregar_movimentacoes()

                self.new_window.destroy()

            except ValueError:
                self.explain = ctk.CTkLabel(self.frame_window, text="Insira um valor válido", font=("Nunito", 20), text_color="#FC6E20")
                self.explain.place(relx=0.5, rely=0.7, anchor="center")    

    def scroll_list(self):
        self.listagem = ctk.CTkScrollableFrame(self.frame_3, fg_color="transparent",scrollbar_button_color="#1A1A1A", scrollbar_button_hover_color="#1A1A1A")
        self.listagem.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.listagem.grid_columnconfigure(0, weight=1)
        self.linha_atual = 0
        self.carregar_movimentacoes()
    def carregar_movimentacoes(self):
        for widget in self.listagem.winfo_children():
            widget.destroy()


        movimentacoes = Movimentacao.select().where(
            Movimentacao.usuario == self.usuario_definido
        ).order_by(Movimentacao.data.desc())

        for mov in movimentacoes:
            self.adicionar_item(
                texto=mov.descricao,
                valor=mov.valor,
                data=mov.data.strftime("%d/%m/%Y"),
                tipo=mov.tipo,  
                categoria=mov.categoria  
            )

    def adicionar_item(self, texto, valor, data, tipo, categoria=None):
        for widget in self.listagem.winfo_children():
            current_row = widget.grid_info()['row']
            widget.grid(row=current_row + 1, column=0, pady=5)

        cedula = ctk.CTkFrame(self.listagem, fg_color="#2b2b2b", corner_radius=10)
        cedula.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
        cedula.grid_columnconfigure(1, weight=1)  


        label_nome = ctk.CTkLabel(cedula, text=texto, font=("Nunito", 16, "bold"))
        label_nome.grid(row=0, column=0, padx=10, sticky="w")

        label_data = ctk.CTkLabel(cedula, text=f"📅 {data}", font=("Nunito", 12))
        label_data.grid(row=1, column=0, padx=10, sticky="w")


        if tipo == "receita":
            cor_dinheiro = "#00bf63"
            cor = "#00bf63"
            catego_image = ctk.CTkImage(
                light_image=Image.open(resource_path("./images/CATEGO/DOLAR.png")),
                dark_image=Image.open(resource_path("./images/CATEGO/DOLAR.png")),
                size=(16, 16)
            )
        else:
            cor_dinheiro = "#BF1700"
            cor = "#BF1700"

            if categoria == "Contas":
                catego_image = ctk.CTkImage(light_image=Image.open(resource_path("./images/CATEGO/HOUSE.png")),
                                            dark_image=Image.open(resource_path("./images/CATEGO/HOUSE.png")), size=(16, 16))
            elif categoria == "Alimentação":
                catego_image = ctk.CTkImage(light_image=Image.open(resource_path("./images/CATEGO/FOOD.png")),
                                            dark_image=Image.open(resource_path("./images/CATEGO/FOOD.png")), size=(16, 16))
            elif categoria == "Transporte":
                catego_image = ctk.CTkImage(light_image=Image.open(resource_path("./images/CATEGO/CAR.png")),
                                            dark_image=Image.open(resource_path("./images/CATEGO/CAR.png")), size=(16, 16))
            elif categoria == "Lazer":
                catego_image = ctk.CTkImage(light_image=Image.open(resource_path("./images/CATEGO/LEISURE.png")),
                                            dark_image=Image.open(resource_path("./images/CATEGO/LEISURE.png")), size=(16, 16))
            elif categoria == "Cartão":
                catego_image = ctk.CTkImage(light_image=Image.open(resource_path("./images/CATEGO/CARD.png")),
                                            dark_image=Image.open(resource_path("./images/CATEGO/CARD.png")), size=(16, 16))
            else:
                catego_image = ctk.CTkImage(light_image=Image.open(resource_path("./images/CATEGO/DOLAR.png")),
                                            dark_image=Image.open(resource_path("./images/CATEGO/DOLAR.png")), size=(16, 16))

        label_valor = ctk.CTkLabel(cedula, text=f"{self.cotacao} {valor:.2f}",
                                font=("Nunito", 16, "bold"), text_color=cor_dinheiro)
        label_valor.grid(row=0, column=1, rowspan=2, padx=10, sticky="e")

        btn_excluir = ctk.CTkButton(cedula, text="", image=catego_image, text_color="white",
                                    font=("Nunito", 18), width=30, height=30,
                                    fg_color=cor, hover_color=cor)
        btn_excluir.grid(row=0, column=2, rowspan=2, padx=5)

    def adicionar(self):
        self.item_count += 1
        self.adicionar_item(
            texto = self.nome_adicionar,
            valor = self.valor_adicionar,
            data=self.data
            
        )







    def add_window2(self):
        if self.settings_window is None or not self.certificar(self.settings_window):
            self.settings_window = ctk.CTkToplevel(self.root)
        self.settings_window.title("Configurações")
        self.settings_window.geometry("854x480")
        self.settings_window.resizable(False, False)
        self.settings_window.configure(fg_color="#1b1b1b")

        self.frame_settings = ctk.CTkFrame(self.settings_window, fg_color="transparent", border_color="white", border_width=0, corner_radius=0)
        self.frame_settings.place(relx=0.5, rely=0.5, relheight=0.9, relwidth=0.8, anchor="center")
        
        self.frame_card1 = ctk.CTkFrame(self.frame_settings, fg_color="#242424", corner_radius=10)
        self.frame_card1.place(relx=0.5, rely=0.10, relwidth=1,relheight=0.15, anchor="n")

        self.frame_card2 = ctk.CTkFrame(self.frame_settings, fg_color="#242424", corner_radius=10)
        self.frame_card2.place(relx=0.5, rely=0.27, relwidth=1,relheight=0.15, anchor="n")

        self.frame_card3 = ctk.CTkFrame(self.frame_settings, fg_color="#242424", corner_radius=10)
        self.frame_card3.place(relx=0.5, rely=0.44, relwidth=1,relheight=0.15, anchor="n")

        self.frame_card4 = ctk.CTkFrame(self.frame_settings, fg_color="#242424", corner_radius=10)
        self.frame_card4.place(relx=0.5, rely=0.61, relwidth=1,relheight=0.15, anchor="n")

        self.text_config = ctk.CTkLabel(self.settings_window, text="Configurações",font=("Nunito", 35))
        self.text_config.place(relx=0.1, rely=0.025, anchor="nw")

        self.mudar_nome_txt = ctk.CTkLabel(self.frame_card1, text="Alterar nome:",font=("Nunito", 25), fg_color="#242424",)
        self.mudar_nome_txt.place(relx=0.015, rely=0.01,anchor="nw")
        self.mudar_nome = ctk.CTkEntry(self.frame_card1, width=100, height=37, placeholder_text=self.usuario)
        self.mudar_nome.place(relx=0.975, rely=0.5, anchor="e")
        self.explain_mudar_nome_txt = ctk.CTkLabel(self.frame_card1, text="Escolha um nome, apelido ou Nick.",font=("Nunito", 15), fg_color="#242424",)
        self.explain_mudar_nome_txt.place(relx=0.015, rely=0.45,anchor="nw")

        self.mudar_salario_txt = ctk.CTkLabel(self.frame_card2, text="Alterar salario:",font=("Nunito", 25), fg_color="#242424",)
        self.mudar_salario_txt.place(relx=0.015, rely=0.01,anchor="nw")
        self.explain_mudar_salario_txt = ctk.CTkLabel(self.frame_card2, text="Qual valor do seu saldo?",font=("Nunito", 15), fg_color="#242424",)
        self.explain_mudar_salario_txt.place(relx=0.015, rely=0.45,anchor="nw")
        self.mudar_salario = ctk.CTkEntry(self.frame_card2, width=100, height=37, placeholder_text=self.main_valor)
        self.mudar_salario.place(relx=0.975, rely=0.5, anchor="e")


        self.moeda_txt = ctk.CTkLabel(self.frame_card3, text="Alterar moeda:",font=("Nunito", 25), fg_color="#242424",)
        self.moeda_txt.place(relx=0.015, rely=0.01,anchor="nw")
        self.moeda = ctk.CTkOptionMenu(self.frame_card3,width=100, values=("Real", "Dolar"), fg_color="#00bf63",button_color="#00bf63",button_hover_color="#236A48")
        self.moeda.place(relx=0.975, rely=0.5, anchor="e")
        self.explain_moeda = ctk.CTkLabel(self.frame_card3, text="Escolha a moeda dos seu saldo.",font=("Nunito", 15), fg_color="#242424",)
        self.explain_moeda.place(relx=0.015, rely=0.45,anchor="nw")

        self.apagar_dados = ctk.CTkLabel(self.frame_card4, text="Excluir dados",font=("Nunito", 25), fg_color="#242424",)
        self.apagar_dados.place(relx=0.015, rely=0.01,anchor="nw")
        self.apagar_dados_txt = ctk.CTkLabel(self.frame_card4, text="Apaga todos os dados e historico. Ação permanente!",font=("Nunito", 15), fg_color="#242424",)
        self.apagar_dados_txt.place(relx=0.015, rely=0.45,anchor="nw")
        
        self.buton_delet = ctk.CTkButton(self.frame_card4, fg_color="#BF1700",hover_color="#780F01", text="Apagar", width=100,height=30, command=self.advert_screen)
        self.buton_delet.place(relx=0.975, rely=0.5, anchor="e")

        self.buton = ctk.CTkButton(self.frame_settings, fg_color="#00bf63",hover_color="#236A48", text="salvar", width=120,height=37, command=self.alterar)
        self.buton.place(relx=0.5, rely=0.9, anchor="center")

        if self.cotacao == "R$":
            self.moeda.set("Real")
        else:
            self.moeda.set("Dolar")

        self.settings_window.lift()
        self.settings_window.focus_force()
        self.settings_window.grab_set()

        self.settings_window.protocol("WM_DELETE_WINDOW", self.on_close_window2)

    def on_close_window1(self):
        self.new_window.destroy()
        self.new_window = None

    def on_close_window2(self):
        self.settings_window.destroy()
        self.settings_window = None
    
    def advert_screen(self):
        self.advert_window = ctk.CTkToplevel(self.root)
        self.advert_window.title("Escluir Dados")
        self.advert_window.geometry("320x180")
        self.advert_window.resizable(False, False)
        self.advert_txt = ctk.CTkLabel(self.advert_window, text="Apagar dados é uma ação ",font=("Nunito", 18, "bold"), fg_color="#1b1b1b",)
        self.advert_txt.place(relx=0.5, rely=0.3,anchor="center")
        self.advert_txt = ctk.CTkLabel(self.advert_window, text="permanente, tem certeza?",font=("Nunito", 18, "bold"), fg_color="#1b1b1b",)
        self.advert_txt.place(relx=0.5, rely=0.45,anchor="center")

        buton = ctk.CTkButton(self.advert_window,fg_color="#BF1700",hover_color="#780F01", text="Apagar", width=100,height=30, command=self.delete)
        buton.place(relx=0.5, rely=0.8, anchor="center")

        self.advert_window.configure(fg_color="#1b1b1b")
        self.advert_window.lift()
        self.advert_window.focus_force()
        self.advert_window.grab_set()
    


APP()
