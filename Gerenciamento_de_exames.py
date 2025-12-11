from datetime import datetime, timedelta
import json

# Dados

# --------------------------------------------------------------------------------------------------------------------------------------


informaçoes = [] # lista que armazena os exames 

arquivo = "exames.json" # nome do arquivo onde os exames serão salvos

def salvar(lista): # salvar arquivos no .json
    dados = [] 
    for p in lista:
        item = {
            "nome": p["nome"],
            "exame": p["exame"],
            "local": p["local"],
            "data": p["data"],
            "entrega": p["entrega"],
            "recebido": p["recebido"]
        }
        dados.append(item)
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def carregar(): # carrega os exames do arquivo .json para a lista
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            for p in dados:
                data_obj = datetime.strptime(p["data"], "%d/%m/%Y")
                informaçoes.append({
                    "nome": p["nome"],
                    "exame": p["exame"],
                    "local": p["local"],
                    "data": p["data"],
                    "data1": data_obj,
                    "entrega": p["entrega"],
                    "recebido": p["recebido"],
                    "data_obj": data_obj
                })
    except FileNotFoundError:
        pass

carregar()


# -------------------------------------------------------------------------------------------------------------------------------------

# Funções principais

# -------------------------------------------------------------------------------------------------------------------------------------

def cadastro_exame(lista): # Função para cadastrar novo exame
    nome=input('📝 Qual nome do paciente: ').lower().strip()
    exame=input('🧪 Digite qual é o exame: ').strip()
    local=input('🏥 Digite o local do exame: ').strip()
    data_exame_str=input('📅 Para quando é o exame (D/M/A): ').strip()
    data_entrega=input('📦 Digite a data da entrega (D/M/A): ').strip()
    recebido=input('👤 Quem recebeu: ').strip()
    data_exame=datetime.strptime(data_exame_str, "%d/%m/%Y") # converte string de data para obj datetime para manipular
    info={
        'nome':nome,
        'exame':exame,
        'local':local,
        'data':data_exame_str,
        'data1':data_exame,
        'entrega':data_entrega,
        'recebido':recebido,
        'data_obj':data_exame  
    }
    lista.append(info)
    salvar(lista)
    print("✅ Exame cadastrado com sucesso!\n")

def listar(): # Função para listar todos exames
    if len(informaçoes)==0:
        print('⚠️ Não há exames cadastrados!!\n')
    for indice, paciente in enumerate(informaçoes):
        print(f"\n🔢 Número: {indice}\n👤 Nome: {paciente['nome'].title()}\n🧪 Exame: {paciente['exame'].title()}\n🏥 Local do exame: {paciente['local'].upper()}\n📅 Data do exame: {paciente['data']}\n📦 Data da entrega: {paciente['entrega']}\n👤 Recebido por: {paciente['recebido'].title()}")

def listar_com_dias_para_vencer(lista): # Função que nós da todos exames e quantos dias eles tem p vencer
    if len(lista) == 0:
        print("⚠️ Não há exames cadastrados.\n")
        return
    
    hoje = datetime.now()
    print("\n📋 Lista de exames com dias restantes para vencer:\n")
    for p in lista:
        dias_restantes = (p['data_obj'] - hoje).days
        if dias_restantes >= 0:
            print(f"- 👤 {p['nome'].title()} | 🧪 Exame: {p['exame']} | ⏳ Faltam {dias_restantes} dias")
        else:
            print(f"- 👤 {p['nome'].title()} | 🧪 Exame: {p['exame']} | ⚠️ Já venceu")

def busca(): # Tipo uma barra de pesquisa
    if len(informaçoes)==0:
        print('⚠️ Não há exames cadastrados!!\n')
    paciente=input('🔍 Digite o nome do paciente para busca: ').strip().lower()
    paciente_encontrado=False

    for pacientes in informaçoes:
        if pacientes['nome'].lower()==paciente:
            print(f"\n👤 Nome: {pacientes['nome'].title()}\n🧪 Exame: {pacientes['exame'].title()}\n🏥 Local do exame: {pacientes['local'].upper()}\n📅 Data do exame: {pacientes['data']}\n📦 Data da entrega: {pacientes['entrega']}\n👤 Recebido por: {pacientes['recebido'].title()}")
            paciente_encontrado=True
            break
    if not paciente_encontrado:
        print(f'❌ Não foi encontrado o(a) paciente {paciente.capitalize()}')

def remover(): # Função que remove algum exame cadastrado
    if len(informaçoes)!=0:
        listar()
        try:
            indice=int(input('🗑️ Digite o número do paciente que você deseja remover: '))
            if 0<=indice<len(informaçoes):
                removido = informaçoes.pop(indice)
                salvar(informaçoes)
                print(f"✅ Paciente {removido['nome'].title()} removido com sucesso\n")
            else:
                print('❌ Número inválido')
        except ValueError:
            print('⚠️ Digite apenas números')
    else:
        print('⚠️ Não há nada cadastrado\n')

def editar(): # Função que edita um exame já cadastrado
    if len(informaçoes) == 0:
        print("⚠️ Não há exames cadastrados!\n")
        return
    
    listar()
    
    try:
        indice = int(input("✏️ Digite o número do paciente que deseja editar: "))
        if indice < 0 or indice >= len(informaçoes):
            print("❌ Índice inválido!")
            return

        paciente = informaçoes[indice]

        print("\nDeixe em branco para manter o valor atual.\n")

        novo_nome = input(f"👤 Nome ({paciente['nome']}): ").strip()
        novo_exame = input(f"🧪 Exame ({paciente['exame']}): ").strip()
        novo_local = input(f"🏥 Local ({paciente['local']}): ").strip()
        nova_data = input(f"📅 Data do exame ({paciente['data']}): ").strip()
        nova_entrega = input(f"📦 Data da entrega ({paciente['entrega']}): ").strip()
        novo_recebido = input(f"👤 Recebido por ({paciente['recebido']}): ").strip()
        
        if novo_nome: paciente['nome'] = novo_nome
        if novo_exame: paciente['exame'] = novo_exame
        if novo_local: paciente['local'] = novo_local
        if nova_data:
            paciente['data'] = nova_data
            paciente['data_obj'] = datetime.strptime(nova_data, "%d/%m/%Y")
        if nova_entrega: paciente['entrega'] = nova_entrega
        if novo_recebido: paciente['recebido'] = novo_recebido

        salvar(informaçoes)

        print("\n✔ Cadastro atualizado com sucesso!\n")
    except ValueError:
        print("⚠️ Digite apenas números!")

def exames_prestes_vencer(lista, dias=3): # Exames que vencerão logo, ENTREGAAAAAAA
    if len(lista) == 0:
        print("⚠️ Não há exames cadastrados.\n")
        return
    
    hoje = datetime.now()
    limite = hoje + timedelta(days=dias)

    print(f"\n⏳ Exames que vão vencer nos próximos {dias} dias:\n")

    achou = False
    for p in lista:
        if 'data_obj' not in p:
            continue
        if hoje <= p['data_obj'] <= limite:
            achou = True
            print(f"- 👤 {p['nome'].title()} | 🧪 Exame: {p['exame']} | 📅 Data: {p['data']}")
    if not achou:
        print("⚠️ Nenhum exame prestes a vencer.")

# -------------------------------------------------------------------------------------------------------------------------------------

# Menu principal

while True:
    print(f"""
{'='*10} 🧪 GERENCIAMENTO DE EXAMES {'='*10}

1 - ➕  Cadastrar exame
2 - 🔍  Buscar exames
3 - 📋  Listar exames
4 - ✏️  Editar exame
5 - 🗑️  Remover exame
6 - ⏳  Exames vencendo
7 - ⏱️  Listar todos prazos de exames
0 - 🚪  Sair
""")
    try:
        opc=int(input('Digite sua opção: '))
    except ValueError:
        print('⚠️  Digite apenas números!!')
        continue
    match opc:
        case 1:
            cadastro_exame(informaçoes)
        case 2:
            busca()
        case 3:
            listar()
        case 4:
            editar()
        case 5:
            remover()
        case 6:
            exames_prestes_vencer(informaçoes, dias=3)
        case 7:
            listar_com_dias_para_vencer(informaçoes)
        case 0:
            print('👋 Saindo...')
            break
        case _:
            print('❌ Opção inválida, tente novamente')
