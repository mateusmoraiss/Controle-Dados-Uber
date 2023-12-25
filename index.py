import sqlite3
from datetime import datetime
import calendar
import os

# Conectando ao banco de dados SQLite
conn = sqlite3.connect('uber_ganhos.db')
c = conn.cursor()

# Criando a tabela se não existir
c.execute('''
          CREATE TABLE IF NOT EXISTS ganhos (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              data TEXT,
              dia_semana INTEGER,
              km_rodados REAL,
              lucro_bruto REAL
          )
          ''')

# Dicionário para mapear número do dia da semana para nome
dias_semana = {1: "Segunda-feira", 2: "Terça-feira", 3: "Quarta-feira", 4: "Quinta-feira", 5: "Sexta-feira", 6: "Sábado"}

# Função para continuar o mês
def continuar_mes():
    print("Escolha o dia da semana:")
    print("1. Segunda-feira")
    print("2. Terça-feira")
    print("3. Quarta-feira")
    print("4. Quinta-feira")
    print("5. Sexta-feira")
    print("6. Sábado")

    dia_semana = int(input("Digite o número correspondente ao dia da semana: "))
    km_rodados = float(input("Informe os quilômetros rodados: "))
    lucro_bruto = float(input("Informe o lucro bruto: "))

    # Obtendo a data atual
    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Inserindo dados na tabela
    c.execute('INSERT INTO ganhos (data, dia_semana, km_rodados, lucro_bruto) VALUES (?, ?, ?, ?)',
              (data_atual, dia_semana, km_rodados, lucro_bruto))
    conn.commit()

# Função para abrir um novo mês
def abrir_mes():
    c.execute('DELETE FROM ganhos')
    print("Novo mês iniciado!")

# Função para fechar o mês
def fechar_mes():
    # Selecione os dados do mês
    c.execute('SELECT * FROM ganhos')
    dados_mes = c.fetchall()

    # Inicializar dicionários para armazenar total de lucro e número de dias para cada dia da semana
    total_lucro = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    dias_contados = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    # Calcular total de lucro e dias para cada dia da semana
    for dado in dados_mes:
        dia = dado[2]  # dia da semana
        total_lucro[dia] += dado[4]  # lucro bruto
        dias_contados[dia] += 1

    # Calcular a média de lucro para cada dia da semana
    media_lucro = {dia: total_lucro[dia] / dias_contados[dia] if dias_contados[dia] > 0 else 0 for dia in total_lucro}

    # Exiba os resultados
    print(f"Lucro Líquido: {sum(total_lucro.values())}")
    print(f"KM Total: {sum(dado[3] for dado in dados_mes)}")
    print(f"N Dias trabalhados: {len(dados_mes)}")
    print(f"Melhor Dia: {dias_semana[max(media_lucro, key=media_lucro.get)]} - Média Lucro Bruto: {max(media_lucro.values())}")
   

    # Criar relatório em bloco de notas
    criar_relatorio(dados_mes, total_lucro, media_lucro)

# Função para criar um relatório em bloco de notas
def criar_relatorio(dados, total_lucro, media_lucro):
    with open('relatorio.txt', 'w') as file:
        file.write("Relatório de Ganhos\n")
        file.write(f"Lucro Bruto: {sum(total_lucro.values())}\n")
        file.write(f"KM Total: {sum(dado[3] for dado in dados)}\n")
        file.write("\nDetalhes por dia:\n")
        for dado in dados:
            file.write(f"{formatar_data(dado)} - KM: {dado[3]}, Lucro Bruto: {dado[4]}\n")
        file.write(f"\n\nMelhor Dia: {dias_semana[max(media_lucro, key=media_lucro.get)]} - Média Lucro Bruto: {max(media_lucro.values())}\n")
        file.write("\n\n\nCom carinho, Mateus Morais")
        
        

# Função para formatar a data
def formatar_data(dado):
    data = datetime.strptime(dado[1], '%Y-%m-%d %H:%M:%S')
    dia_semana = dias_semana[dado[2]]
    return f"{dia_semana}, {data.strftime('%d/%m/%Y')}"

# Menu de opções
while True:

    print("\nEscolha uma opção:")
    print("1. Continuar Mês")
    print("2. Abrir Mês")
    print("3. Fechar Mês")
    print("4. Sair")

    opcao = input("Digite o número da opção desejada: ")

    if opcao == "1":
        continuar_mes()
    elif opcao == "2":
        abrir_mes()
    elif opcao == "3":
        fechar_mes()
    elif opcao == "4":
        print("Saindo do programa. Até mais!\n\n Com carinho, Mateus!")
        break
    else:
        print("Opção inválida. Tente novamente.")
