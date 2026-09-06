from datetime import datetime
import sys
import sqlite3
import time
import os

pasta_script = os.path.dirname(os.path.abspath(__file__)) #diretório absoluto/fixo
caminho_db = os.path.join(pasta_script, 'sis_cond_database.db') #localização do arquivo no diretório fixo

conexao = sqlite3.connect(caminho_db)
cursor = conexao.cursor()

soma_valores_pagos = 0

for casa_id in range(1,15): #criar tabela para cada casa no BD (poder ser adaptada para cada uso)
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS casa{casa_id}(
            mes_ano VARCHAR(20) PRIMARY KEY,
            status VARCHAR(20),
            valor_cond FLOAT NOT NULL
            )''') #criar tabelas de cada casa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS casas(
            casa_id INT PRIMARY KEY
            )''') #tabela para todas as casas
    cursor.execute(f'''
        INSERT OR IGNORE INTO casas (casa_id)
        VALUES ({casa_id})''') #inserção das cass na tabela
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS caixa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            motivo VARCHAR(120),
            caixa_valores FLOAT NOT NULL
        )''') #criar tabela caixa
    cursor.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS index_motivo
        ON caixa (motivo)
        WHERE motivo = 'Pagamento do condomínio'
        ''') #criar index para tornar 'Pagamento do condominio' fixo
    cursor.execute(f'''
        SELECT valor_cond
        FROM casa{casa_id}
''')
    valor_pago = cursor.fetchall()
    for valores in valor_pago:
        for valores_pagos in valores:
            soma_valores_pagos += valores_pagos #somando todos os pagamentos de todos os meses das casas

cursor.execute(f'''
    INSERT OR IGNORE INTO caixa (caixa_valores, motivo)
    VALUES (?,?)
    ''', (soma_valores_pagos, 'Pagamento do condomínio')) #inserindo essa linha do total do pagamento

cursor.execute(f'''
    UPDATE caixa
    SET caixa_valores = ?
    WHERE motivo = ?''', (soma_valores_pagos, 'Pagamento do condomínio')) #atualizando a linha do total pagamento

conexao.commit() #salvar a criação

mes_atual = datetime.today().strftime('%m/%y') #mês vigente no padrão MM/AA

cursor.execute('''
    SELECT casa_id 
    FROM casas
    ''') #procurando pelos numeros das casas
casas = cursor.fetchall() #procura em tupla
for casa in casas: #cada elemento da tupla em um array
    for casa_ in casa: #cada elemento do array
            cursor.execute(f'''
                INSERT OR IGNORE INTO casa{casa_} (mes_ano, status, valor_cond)
                VALUES (?,?,?)
                ''', (mes_atual, 'NAO PAGO', 0)) #toda vez que adicionado o mes atual, as casas vêm com status de NAO PAGO
conexao.commit()           

def listar_casas():
    cursor.execute('''
        SELECT casa_id 
        FROM casas
        ''') #procurando pelos numeros das casas
    casas = cursor.fetchall() #procura em tupla
    for casa in casas: #cada elemento da tupla em um array
        for casa_ in casa: #cada elemento do array
            print(f'Casa {casa_}') #exibir a lista 
            time.sleep(0.05)
            
def listar_status_mes():
    while True:
        mes_selecionado = input('Qual é o seu mês de pesquisa? (MM/AA) ')
        valor_achado = False #sem valor achado
        if len(mes_selecionado) == 5 and mes_selecionado[2] == '/': #verifica se está no padrão MM/AA
            cursor.execute('''
                SELECT casa_id 
                FROM casas
                ''')
            casas = cursor.fetchall()
            for casa in casas:
                for casa_ in casa:
                    cursor.execute(f'''
                        SELECT mes_ano
                        FROM casa{casa_}
                        WHERE mes_ano = ?
                        ''', (mes_selecionado,)) #verifica se tem o mẽs
                    mes_db = cursor.fetchall()
                    if mes_db != []: #o mês selecionado foi encontrado
                        valor_achado = True #o valor foi achado
                        break

            if valor_achado == True:
                break
            else:
                print('Selecione um valor válido.')

        else:
            print('Selecione um formato válido.')

    print(f'O período selecionado foi {mes_selecionado}:')

    cursor.execute('''
        SELECT casa_id 
        FROM casas
        ''')
    casas = cursor.fetchall()
    for casa in casas:
        for casa_ in casa:
            cursor.execute(f'''
                SELECT status, valor_cond
                FROM casa{casa_}
                WHERE mes_ano = ?
                ''', (mes_selecionado,)) #procura as colunas referentes ao mês escolhido
            coluna_status_mes = cursor.fetchone() #pega os dados da execução da query

            if coluna_status_mes != None: #pega o que nao está vazio
                status_pag, valor_cond = coluna_status_mes
                time.sleep(0.1)
                print(f'Casa {casa_} - {status_pag} - R$ {valor_cond:.2f}')

def listar_historico_casa():
    while True:
        try:
            casa_listar_status = int(input('Qual casa gostaria de consultar o histórico de pagamento? (Somente número) '))
            cursor.execute('''
                SELECT casa_id
                FROM casas
                ''') #na tabela casas, vai verificar quais casas existem
            casas = cursor.fetchall()

            list_casas = [] #array vazio
            for casas_id in casas: #pega cada elemento da tupla
                for valor in casas_id: #pega valor de cada elemento da tupla
                    list_casas.append(valor) #adiciona no array

            if casa_listar_status in list_casas: #verifica se a casa solicitada está entre as listadas no BD
                break
            else:
                print('Casa não encontrada. Favor, escolher casa válida.')
            
        except ValueError:
            print('Selecione um valor válido')
        
        
    cursor.execute(f'''
        SELECT mes_ano, status, valor_cond
        FROM casa{casa_listar_status}
        ''')
    status = cursor.fetchall()

    print(f'Para a Casa {casa_listar_status}:')

    for status_um_a_um in status: #passa a tupla para array
        mes_ano_listar_status, status_listar_status, valor_cond_listar_status = status_um_a_um
        time.sleep(0.1)
        print(f'{mes_ano_listar_status} - {status_listar_status} - {valor_cond_listar_status:.2f}')

def alt_pag_casa():
    while True:
        try:
            casa_alt_pag = int(input('Qual casa quer alterar status de pagamento? (Somente número) '))
            cursor.execute('''
                SELECT casa_id
                FROM casas
                ''') #na tabela casas, vai verificar quais casas existem
            casas = cursor.fetchall()

            list_casas = [] #array vazio
            for casas_id in casas: #pega cada elemento da tupla
                for valor in casas_id: #pega valor de cada elemento da tupla
                    list_casas.append(valor) #adiciona no array

            if casa_alt_pag in list_casas:
                break
            else:
                print('Casa não encontrada. Favor, escolher casa válida.')

        except ValueError:
            print('Selecione um valor válido')

    valor_achado = False

    while True:
        try:
            valor_pago = float(input(f'Qual foi o valor pago pela casa {casa_alt_pag}? R$ ').replace(',','.'))

            while True:
                valor_achado = False
                mes_ano = input('Qual foi o período do pagamento? (MM/AA) ')
                if len(mes_ano) == 5 and mes_ano[2] == '/': #verifica se está no padrão MM/AA
                    cursor.execute('''
                        SELECT casa_id 
                        FROM casas
                        ''')
                    casas = cursor.fetchall()
                    for casa in casas:
                        for casa_ in casa:
                            cursor.execute(f'''
                                SELECT mes_ano
                                FROM casa{casa_}
                                WHERE mes_ano = ?
                                ''', (mes_ano,)) #verifica se tem o mẽs
                            mes_db = cursor.fetchall()
                            if mes_db != []: #o mês selecionado foi encontrado
                                valor_achado = True
                                break
        
                    if valor_achado == True:
                        break
                    else:
                        print('Selecione um valor válido.')
        
                else:
                    print('Selecione um formato válido.')

            if valor_pago == 0: #caso 0, NAO PAGO
                cursor.execute(f'''
                    UPDATE OR IGNORE casa{casa_alt_pag}
                    SET valor_cond = ?, status = ?
                    WHERE mes_ano = ?
                    ''', (0, 'NAO PAGO', mes_ano))
                break
            elif valor_pago == 50: #caso 50, PAGO (podendo ser adaptado para cada uso)
                cursor.execute(f'''
                    UPDATE OR IGNORE casa{casa_alt_pag}
                    SET valor_cond = ?, status = ?
                    WHERE mes_ano = ?
                    ''', (50, 'PAGO', mes_ano))
                break
            elif 0 < valor_pago < 50: #maior que 0 e menor que 50, PARCIALMENTE PAGO
                cursor.execute(f'''
                    UPDATE OR IGNORE casa{casa_alt_pag}
                    SET valor_cond = ?, status = ?
                    WHERE mes_ano = ?
                    ''', (valor_pago, 'PARCIALMENTE PAGO', mes_ano))
                break
            elif valor_pago > 50:
                print('O valor pago não pode ser mais do que o valor do condomínio.')
            else:
                print('O valor não pode ser negativo.')

        except ValueError:
            print('Selecione um valor válido')

    print(f'A casa {casa_alt_pag} pagou R$ {valor_pago:.2f} referente ao mês {mes_ano}.')        
    conexao.commit()

def listar_pendencias():
    print('Listando pendências...')
    time.sleep(0.1)
    cursor.execute('''
        SELECT casa_id 
        FROM casas
        ''')
    casas = cursor.fetchall()
    listar_casas_pendecias = []
    for casa in casas:
        for casa_ in casa:
            listar_casas_pendecias.append(casa_)

    for casa_id in listar_casas_pendecias:
        cursor.execute(f'''
            SELECT mes_ano, status, valor_cond
            FROM casa{casa_id}
            ''')
        status_pendencia = cursor.fetchall()
        for listar_status in status_pendencia:
            mes_ano, status, valor_cond = listar_status
            if status in ['NAO PAGO','PARCIALMENTE PAGO']: #filtra os status para 'NAO PAGO' E 'PARCIALMENTE PAGO'
                time.sleep(0.05)
                print(f'Casa {casa_id} - {mes_ano} - {status} - R$ {valor_cond:.2f}')

def valor_total():

    cursor.execute('''
        SELECT caixa_valores, motivo
        FROM caixa''')
    resultado = cursor.fetchall()

    soma_caixa_valores = 0

    for resultado_valores_motivo in resultado:
        caixa_valores, motivo = resultado_valores_motivo
        print(f'R$ {caixa_valores:.2f} | {motivo}')
        time.sleep(0.05)
        soma_caixa_valores += caixa_valores #faz a soma dos pagamentos das casas
    print(40*'-')
    print(f'O valor no caixa do condomínio é R$ {soma_caixa_valores:.2f}.')

    conexao.commit()


def add_ret_acres():
    cursor.execute('''
        SELECT caixa_valores
        FROM caixa''')
    resultado = cursor.fetchall()

    soma_caixa_valores = 0

    for resultado_valores in resultado:
        for resultado_valores_cada in resultado_valores:
            soma_caixa_valores += resultado_valores_cada

    while True:
        pergunta_ret_acres = input('Deseja fazer um acréscimo ou uma retirada no caixa? (+ ou -) ')
        if pergunta_ret_acres == '+':
            while True:
                try:
                    valor_acres = float(input('Qual valor deseja acrescentar? (Somente número) ').replace(',','.'))
                    if type(valor_acres) == float:
                        break
                    
                except ValueError:
                    print('Selecione um valor válido')

            while True:
                motivo = input('Qual motivo do acréscimo? ')
                if motivo == '':
                    print('Deve relatar o motivo.')
                else:
                    break

            cursor.execute(f'''
                INSERT INTO caixa (caixa_valores, motivo)
                VALUES (?,?)
                ''', (valor_acres, motivo))

            time.sleep(0.05)
            
            print(f'O valor de R${valor_acres:.2f} foi acresentado no caixa e seu motivo é "{motivo}".')

            break
        
        elif pergunta_ret_acres == '-':
            while True:
                try:
                    valor_ret = float(input('Qual valor deseja retirar? (Somente número) ').replace(',','.'))
                    if type(valor_ret) == float:
                        if valor_ret > soma_caixa_valores:
                            print('O valor não pode ultrapassar o valor do caixa.')
                        else:
                            break
                        
                except ValueError:
                    print('Selecione um valor válido')

            while True:
                motivo = input('Qual motivo da retirada? ')
                if motivo == '':
                    print('Deve relatar o motivo.')
                else:
                    break

            cursor.execute(f'''
                INSERT INTO caixa (caixa_valores, motivo)
                VALUES (?,?)
                ''', (-valor_ret, motivo))

            time.sleep(0.05)

            print(f'O valor de R${valor_ret:.2f} foi retirado do caixa e seu motivo é "{motivo}".')

            break

        else:
            print('Selecione uma resposta válida')


    conexao.commit()



def apresentacao():
    print('='*5,' Seja bem-vindo(a) ao Sistema do Condomínio!','='*5)

    while True:
        print('\nEscolha o que quer fazer:\n(0) Sair do sistema; \n(1) Listar casas; \n(2) Listar status de pagamento em um determinado mês; \n(3) Listar histórico de pagamento de uma determinada casa; \n(4) Alterar status de pagamento de uma determinada casa; \n(5) Listar pendências de pagamento; \n(6) Exibir valor total do caixa; \n(7) Adicionar retirada/acréscimo pontual.')

        try:
            escolha_inicial = int(input('(Somente o número): '))
            print('')
            if escolha_inicial == 0:
                sys.exit()
            elif escolha_inicial == 1:
                listar_casas()
                time.sleep(0.5)
            elif escolha_inicial == 2:
                listar_status_mes()
                time.sleep(0.5)
            elif escolha_inicial == 3:
                listar_historico_casa()
                time.sleep(0.5)
            elif escolha_inicial == 4:
                alt_pag_casa()
                time.sleep(0.5)
            elif escolha_inicial == 5:
                listar_pendencias()
                time.sleep(0.5)
            elif escolha_inicial == 6:
                valor_total()
                time.sleep(0.5)
            elif escolha_inicial == 7:
                add_ret_acres()
                time.sleep(0.5)
            else:    
                print('Selecione um valor válido.')

        except ValueError:
            print('\nSelecione um valor válido.')

apresentacao()

conexao.close()