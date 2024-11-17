import tkinter as tk
from tkinter import font
import util.util_ventana as util_ventana
from config import constantes as cons
import math

class Calculadora(tk.Tk):

    def __init__(self):
        super().__init__()
        self.config_window()
        self.construir_widget()
        self.construir_widget_toggle()

    def config_window(self):
        self.title('Calculadora Python')
        self.configure(bg=cons.COLOR_DE_FONDO_DARK)
        self.attributes('-alpha', 1.0)
        self.resizable(False, False) 
        w, h = 410, 620
        util_ventana.centrar_ventana(self, w, h)
        for i in range(6):  
            self.grid_rowconfigure(i, weight=1)
        for j in range(4):  
            self.grid_columnconfigure(j, weight=1)

        
    def construir_widget(self):
        
        self.operation_label = tk.Label(self, text="", font=(
            'Arial', 16), fg=cons.COLOR_DE_TEXTO_DARK, bg=cons.COLOR_DE_FONDO_DARK, justify='right')
        self.operation_label.grid(row=0, column=3, padx=10, pady=10,sticky='') 
        
        self.entry = tk.Entry(self, width=12, font=(
            'Arial', 40), bd=0, fg=cons.COLOR_DE_TEXTO_DARK, bg=cons.COLOR_CAJA_TEXTO_DARK, justify='right')
        self.entry.grid(row=1, column=0, columnspan=4, padx=10, pady=10,sticky='nsew')  

        buttons = [
            '√', 'π', '^', '!',
            'AC','<', '%', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.', '=',
        ]

        row_val = 2 
        col_val = 0


        roboto_font = font.Font(family="Roboto", size=16)

        for button in buttons:
            if button in ['=', '*', '/', '-', '+', 'AC', '<', '%','√','π','^','!']:
                color_fondo = cons.COLOR_BOTONES_ESPECIALES_DARK
                button_font = font.Font(size=16, weight='bold')
            else:
                color_fondo = cons.COLOR_BOTONES_DARK
                button_font = roboto_font

            if button == '=':
                tk.Button(self, text=button, width=11, height=2, command=lambda b=button: self.on_button_click(b),
                          bg=color_fondo, fg=cons.COLOR_DE_TEXTO_DARK, relief=tk.FLAT, font=button_font, padx=5, pady=5, bd=0, borderwidth=0, highlightthickness=0,
                          overrelief='flat').grid(row=row_val, column=col_val, columnspan=2, pady=5, padx=5,sticky='nsew') 
                col_val += 1
            else:
                tk.Button(self, text=button, width=5, height=2, command=lambda b=button: self.on_button_click(b),
                          bg=color_fondo, fg=cons.COLOR_DE_TEXTO_DARK, relief=tk.FLAT, font=button_font, padx=5, pady=5, bd=0, borderwidth=0, highlightthickness=0,
                          overrelief='flat').grid(row=row_val, column=col_val, pady=5, padx=5,sticky='nsew')  
                col_val += 1

            if col_val > 3:
                col_val = 0
                row_val += 1
                
    def construir_widget_toggle(self):
        roboto_font = font.Font(family="Roboto", size=12)
        self.dark_theme = True
        self.theme_button = tk.Button(self, text="Modo Claro", width=12,  font=roboto_font, bd=0, borderwidth=0,
                                      highlightthickness=0, relief=tk.FLAT, command=self.toggle_theme, bg=cons.COLOR_BOTONES_DARK,fg=cons.COLOR_DE_TEXTO_DARK)
        self.theme_button.grid(row=0, column=0, columnspan=2,
                               pady=0, padx=0, sticky="nw") 


    def toggle_theme(self):
        if self.dark_theme:
            # Cambiar a tema claro
            self.configure(bg=cons.COLOR_DE_FONDO_LIGHT)
            self.entry.config(fg=cons.COLOR_DE_TEXTO_LIGHT,
                            bg=cons.COLOR_CAJA_TEXTO_LIGHT)
            self.operation_label.config(
                fg=cons.COLOR_DE_TEXTO_LIGHT, bg=cons.COLOR_DE_FONDO_LIGHT)
            self.theme_button.configure(
                text="Modo Oscuro", relief=tk.SUNKEN, bg=cons.COLOR_BOTONES_ESPECIALES_LIGHT)

            # Cambiar colores de botones
            for widget in self.winfo_children():
                if isinstance(widget, tk.Button):
                    if widget.cget("text") in ['=', '*', '/', '-', '+', 'AC', '<', '%', '√', 'π', '^', '!']:
                        widget.config(bg=cons.COLOR_BOTONES_ESPECIALES_LIGHT,
                                    fg=cons.COLOR_DE_TEXTO_LIGHT)
                    else:
                        widget.config(bg=cons.COLOR_BOTONES_LIGHT,
                                    fg=cons.COLOR_DE_TEXTO_LIGHT)
        else:
            # Cambiar a tema oscuro
            self.configure(bg=cons.COLOR_DE_FONDO_DARK)
            self.entry.config(fg=cons.COLOR_DE_TEXTO_DARK,
                            bg=cons.COLOR_CAJA_TEXTO_DARK)
            self.operation_label.config(
                fg=cons.COLOR_DE_TEXTO_DARK, bg=cons.COLOR_DE_FONDO_DARK)
            self.theme_button.configure(
                text="Modo Claro", relief=tk.RAISED, bg=cons.COLOR_BOTONES_ESPECIALES_DARK)

            # Cambiar colores de botones
            for widget in self.winfo_children():
                if isinstance(widget, tk.Button):
                    if widget.cget("text") in ['=', '*', '/', '-', '+', 'AC', '<', '%', '√', 'π', '^', '!']:
                        widget.config(bg=cons.COLOR_BOTONES_ESPECIALES_DARK,
                                    fg=cons.COLOR_DE_TEXTO_DARK)
                    else:
                        widget.config(bg=cons.COLOR_BOTONES_DARK,
                                    fg=cons.COLOR_DE_TEXTO_DARK)

        self.dark_theme = not self.dark_theme


    def on_button_click(self, value):
        if value == '=':
            try:
                expression = self.entry.get().replace('%', '/100')
                result = eval(expression)
                result = f"{result:.10g}"
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
                operation = expression + " " + value
                self.operation_label.config(text=operation)
            except Exception as e:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
                self.operation_label.config(text="")
        elif value == 'AC':
            self.entry.delete(0, tk.END)
            self.operation_label.config(text="")
        elif value == '<':
            current_text = self.entry.get()
            if current_text:
                new_text = current_text[:-1] 
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, new_text)
                self.operation_label.config(text=new_text + " ")
        elif value == '√':
            current_text = self.entry.get()
            if current_text:
                try:
                    result = math.sqrt(float(current_text))
                    self.entry.delete(0, tk.END)
                    self.entry.insert(tk.END, str(result))
                    self.operation_label.config(text="√" + current_text)
                except ValueError:
                    self.entry.delete(0, tk.END)
                    self.entry.insert(tk.END, "Error")
        elif value == 'π':
            self.entry.insert(tk.END, str(round(math.pi,2)))
        elif value == '^':
            current_text = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, current_text + "**")  
        elif value == '!':
            current_text = self.entry.get()
            try:
                result = math.factorial(int(current_text))
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
                self.operation_label.config(text="!" + current_text)
            except ValueError:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
        else:
            current_text = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, current_text + value)
            if value == '=':
                self.operation_label.config(text="")
    
                