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

        self.entrada = tk.Entry(self.frame, width=40)
        self.entrada.grid(row=0, column=0, padx=5)
        self.entrada.bind("<Return>", lambda e: self.adicionar_tarefa())

        tk.Button(self.frame, text="Adicionar", command=self.adicionar_tarefa).grid(row=0, column=1, padx=5)
        tk.Button(self.frame, text="Editar", command=self.editar_tarefa).grid(row=0, column=2, padx=5)
        tk.Button(self.frame, text="Concluir", command=self.concluir_tarefa).grid(row=0, column=3, padx=5)
        tk.Button(self.frame, text="Filtrar Concluídas", command=self.filtrar_concluidas).grid(row=0, column=4, padx=5)
        tk.Button(self.frame, text="Mostrar Todas", command=self.mostrar_todas).grid(row=0, column=5, padx=5)

        self.lista = tk.Listbox(root, width=70)
        self.lista.pack()
        self.atualizar_lista(self.tarefas)

    def carregar_tarefas(self):
        if os.path.exists(ARQUIVO):
            with open(ARQUIVO, "r") as f:
                return json.load(f)
        return []

    def salvar_tarefas(self):
        with open(ARQUIVO, "w") as f:
            json.dump(self.tarefas, f, indent=2)

    def atualizar_lista(self, tarefas):
        self.lista.delete(0, tk.END)
        for tarefa in tarefas:
            status = "✔" if tarefa["concluida"] else "✘"
            self.lista.insert(tk.END, f"{tarefa['nome']} [{status}]")

    def adicionar_tarefa(self):
        nome = self.entrada.get().strip()
        if nome:
            self.tarefas.append({"nome": nome, "concluida": False})
            self.entrada.delete(0, tk.END)
            self.salvar_tarefas()
            self.atualizar_lista(self.tarefas)

    def editar_tarefa(self):
        selecionado = self.lista.curselection()
        if selecionado:
            idx = selecionado[0]
            novo_nome = simpledialog.askstring("Editar Tarefa", "Novo nome da tarefa:")
            if novo_nome:
                self.tarefas[idx]["nome"] = novo_nome.strip()
                self.salvar_tarefas()
                self.atualizar_lista(self.tarefas)

    def concluir_tarefa(self):
        selecionado = self.lista.curselection()
        if selecionado:
            idx = selecionado[0]
            self.tarefas[idx]["concluida"] = True
            self.salvar_tarefas()
            self.atualizar_lista(self.tarefas)

    def filtrar_concluidas(self):
        concluidas = [t for t in self.tarefas if t["concluida"]]
        self.atualizar_lista(concluidas)

    def mostrar_todas(self):
        self.atualizar_lista(self.tarefas)

if __name__ == "__main__":
    root = tk.Tk()
    app = GerenciadorTarefas(root)
    root.mainloop()