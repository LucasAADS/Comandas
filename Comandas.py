import sqlite3

class Comanda:
    def __init__(self, cliente):
        self.cliente = cliente
        self.cpf = None
        self.data = None
        self.itens = []
    
    def adicionar_item(self, item):
        self.itens.append(item)
    
    def remover_item(self, item):
        self.itens.remove(item)
    
    def calcular_total(self):
        total = 0
        for item in self.itens:
            total += item.preco
        return total


class Item:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

def criar_tabela():
    conn = sqlite3.connect('comandas.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comandas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            cpf TEXT,
            data TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comanda_id INTEGER,
            nome TEXT,
            preco REAL,
            FOREIGN KEY (comanda_id) REFERENCES comandas(id)
        )
    ''')

    conn.commit()
    conn.close()

def inserir_comanda(comanda):
    conn = sqlite3.connect('comandas.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO comandas (cliente, cpf, data)
        VALUES (?, ?, ?)
    ''', (comanda.cliente, comanda.cpf, comanda.data))

    comanda_id = cursor.lastrowid

    for item in comanda.itens:
        cursor.execute('''
            INSERT INTO itens (comanda_id, nome, preco)
            VALUES (?, ?, ?)
        ''', (comanda_id, item.nome, item.preco))

    conn.commit()
    conn.close()

def main():
    criar_tabela()

    comandas = []

    while True:
        print("\nBem-vindo à bicicletaria!")
        print("1. Nova comanda")
        print("2. Adicionar item à comanda")
        print("3. Remover item da comanda")
        print("4. Calcular total da comanda")
        print("5. Visualizar todas as comandas existentes")
        print("6. Pesquisar comandas por cliente ou CPF")
        print("7. Atualizar informações de uma comanda existente")
        print("8. Gerar relatórios de vendas")
        print("9. Sair")
        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            cliente = input("Digite o nome do cliente: ")
            cpf = input("Digite o CPF do cliente: ")
            comanda = Comanda(cliente)
            comanda.cpf = cpf
            comandas.append(comanda)
            inserir_comanda(comanda)
            print(f"Comanda criada para o cliente {cliente} com CPF {cpf}.")

        elif opcao == "2":
            if not comandas:
                print("Não há comandas disponíveis.")
                continue

            print("Selecione uma comanda:")
            for i, comanda in enumerate(comandas):
                print(f"{i + 1}. {comanda.cliente}")

            indice = int(input("Digite o número da comanda: ")) - 1
            comanda = comandas[indice]

            nome_item = input("Digite o nome do item: ")
            preco_item = float(input("Digite o preço do item: "))
            item = Item(nome_item, preco_item)
            comanda.adicionar_item(item)
            print(f"Item {item.nome} adicionado à comanda do cliente {comanda.cliente}.")

        elif opcao == "3":
            if not comandas:
                print("Não há comandas disponíveis.")
                continue

            print("Selecione uma comanda:")
            for i, comanda in enumerate(comandas):
                print(f"{i + 1}. {comanda.cliente}")

            indice = int(input("Digite o número da comanda: ")) - 1
            comanda = comandas[indice]

            print("Selecione um item para remover:")
            for i, item in enumerate(comanda.itens):
                print(f"{i + 1}. {item.nome}")

            indice_item = int(input("Digite o número do item: ")) - 1
            item = comanda.itens[indice_item]
            comanda.remover_item(item)
            print(f"Item {item.nome} removido da comanda do cliente {comanda.cliente}.")

        elif opcao == "4":
            if not comandas:
                print("Não há comandas disponíveis.")
                continue

            print("Selecione uma comanda:")
            for i, comanda in enumerate(comandas):
                print(f"{i + 1}. {comanda.cliente}")

            indice = int(input("Digite o número da comanda: ")) - 1
            comanda = comandas[indice]
            total = comanda.calcular_total()
            print(f"Total da comanda do cliente {comanda.cliente}: R${total:.2f}")

        elif opcao == "5":
            if not comandas:
                print("Não há comandas disponíveis.")
                continue

            print("Comandas existentes:")
            for i, comanda in enumerate(comandas):
                print(f"{i + 1}. {comanda.cliente}")

        elif opcao == "6":
            if not comandas:
                print("Não há comandas disponíveis.")
                continue

            termo = input("Digite o nome do cliente ou CPF para pesquisar: ")
            resultados = []
            for comanda in comandas:
                if termo in [comanda.cliente, comanda.cpf]:
                    resultados.append(comanda)

            if not resultados:
                print("Nenhuma comanda encontrada.")
            else:
                print("Comandas encontradas:")
                for i, comanda in enumerate(resultados):
                    print(f"{i + 1}. {comanda.cliente}")

        elif opcao == "7":
            if not comandas:
                print("Não há comandas disponíveis.")
                continue

            print("Selecione uma comanda:")
            for i, comanda in enumerate(comandas):
                print(f"{i + 1}. {comanda.cliente}")

            indice = int(input("Digite o número da comanda: ")) - 1
            comanda = comandas[indice]

            novo_cliente = input("Digite o novo nome do cliente (deixe em branco para manter o mesmo): ")
            novo_cpf = input("Digite o novo CPF do cliente (deixe em branco para manter o mesmo): ")

            if novo_cliente:
                comanda.cliente = novo_cliente
            if novo_cpf:
                comanda.cpf = novo_cpf

            print("Informações da comanda atualizadas.")

        elif opcao == "8":
            print("Opção não implementada.")

        elif opcao == "9":
            print("Encerrando o programa...")
            break

        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")

if __name__ == "__main__":
    main()
