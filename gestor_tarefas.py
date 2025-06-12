import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

ARQUIVO = "tarefas.json"

class GerenciadorTarefas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tarefas")
        self.tarefas = self.carregar_tarefas()

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.entrada = tk.Entry(self.frame, width=40, font=('Inter', 12))
        self.entrada.grid(row=0, column=0, padx=5, pady=5)
        self.entrada.bind("<Return>", lambda e: self.adicionar_tarefa())

        self.criar_botoes()

        self.lista = tk.Listbox(root, width=70, height=15, font=('Inter', 12), selectmode=tk.SINGLE)
        self.lista.pack(pady=10)
        
        self.atualizar_lista(self.tarefas)

    def criar_botoes(self):
        buttons_info = [
            ("Adicionar", self.adicionar_tarefa),
            ("Editar", self.editar_tarefa),
            ("Concluir Tarefa", self.concluir_tarefa),
            ("Excluir", self.excluir_tarefa),
            ("Filtrar Concluídas", self.filtrar_concluidas),
            ("Mostrar Todas", self.mostrar_todas)
        ]

        for i, (text, command) in enumerate(buttons_info):
            tk.Button(self.frame, text=text, command=command, font=('Inter', 10), padx=5, pady=2).grid(row=0, column=i+1, padx=5, pady=5)

    def carregar_tarefas(self):
        if os.path.exists(ARQUIVO):
            try:
                with open(ARQUIVO, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                messagebox.showerror("Erro", f"Erro ao carregar tarefas: {e}")
                return []
        return []

    def salvar_tarefas(self):
        try:
            with open(ARQUIVO, "w", encoding="utf-8") as f:
                json.dump(self.tarefas, f, indent=2, ensure_ascii=False)
        except IOError as e:
            messagebox.showerror("Erro", f"Erro ao salvar tarefas: {e}")

    def atualizar_lista(self, tarefas_para_exibir):
        self.lista.delete(0, tk.END)
        for i, tarefa in enumerate(tarefas_para_exibir):
            status_char = "✔" if tarefa["concluida"] else "✘"
            display_text = f"{tarefa['nome']} [{status_char}]"
            self.lista.insert(tk.END, display_text)
            
            if tarefa["concluida"]:
                self.lista.itemconfig(i, fg="gray", overrelief="solid")
                self.lista.itemconfig(i, relief="flat", highlightbackground="gray")
                self.lista.itemconfig(i, font=('Inter', 12, 'overstrike'))
            else:
                self.lista.itemconfig(i, fg="black", font=('Inter', 12))


    def adicionar_tarefa(self):
        nome = self.entrada.get().strip()
        if nome:
            self.tarefas.append({"nome": nome, "concluida": False})
            self.entrada.delete(0, tk.END)
            self.salvar_tarefas()
            self.atualizar_lista(self.tarefas)
        else:
            messagebox.showwarning("Aviso", "O nome da tarefa não pode ser vazio!")

    def editar_tarefa(self):
        selecionado = self.lista.curselection()
        if selecionado:
            idx = selecionado[0]
            novo_nome = simpledialog.askstring("Editar Tarefa", "Novo nome da tarefa:", initialvalue=self.tarefas[idx]["nome"])
            if novo_nome is not None and novo_nome.strip():
                self.tarefas[idx]["nome"] = novo_nome.strip()
                self.salvar_tarefas()
                self.atualizar_lista(self.tarefas)
            elif novo_nome is not None:
                 messagebox.showwarning("Aviso", "O nome da tarefa não pode ser vazio!")
        else:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para editar.")

    def concluir_tarefa(self):
        selecionado = self.lista.curselection()
        if selecionado:
            idx = selecionado[0]
            self.tarefas[idx]["concluida"] = not self.tarefas[idx]["concluida"]
            self.salvar_tarefas()
            self.atualizar_lista(self.tarefas)
        else:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para alternar o status.")

    def excluir_tarefa(self):
        selecionado = self.lista.curselection()
        if selecionado:
            idx = selecionado[0]
            if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir esta tarefa?"):
                del self.tarefas[idx]
                self.salvar_tarefas()
                self.atualizar_lista(self.tarefas)
        else:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para excluir.")

    def filtrar_concluidas(self):
        concluidas = [t for t in self.tarefas if t["concluida"]]
        self.atualizar_lista(concluidas)

    def mostrar_todas(self):
        self.atualizar_lista(self.tarefas)

if __name__ == "__main__":
    root = tk.Tk()
    app = GerenciadorTarefas(root)
    root.mainloop()
