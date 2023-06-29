from twilio.rest import Client
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import gspread
import time
import re

# (Gustavo) - Registro de mensagens enviadas
n_ola = 0
n_td_bem = 0
n_auditoria = 0
mens_auto = 0
# (Arthur) - Registro de mensagens enviadas
n_ola2 = 0
n_td_bem2 = 0
n_auditoria2 = 0
mens_auto2 = 0

while True:
    time.sleep(1)
    hora_init = str(datetime.datetime.now())[14:16]

    # Comunicação com API Twilio e protocolo de autorização
    class Config():
        # Substitua as informações abaixo pelas suas credenciais de autenticação e número do WhatsApp registrado na conta Twilio
        account_sid = 'xxxxxxxxxxxxxxxxx'
        auth_token = 'xxxxxxxxxxxxxxxxxx'
        whatsapp_number = 'whatsapp:+xxxxxxxxxxxxxxx'
        from_whatsapp_number = 'whatsapp:+14155238886'
        to_whatsapp_number = 'whatsapp:+xxxxxxxxxxx'

        # cria uma instância do objeto Client com suas credenciais de autenticação
        client = Client(account_sid, auth_token)

        # lista as mensagens recebidas pelo número do WhatsApp registrado em sua conta Twilio
        messages = client.messages.list(from_=whatsapp_number)
    class Config2():
        # Substitua as informações abaixo pelas suas credenciais de autenticação e número do WhatsApp registrado na conta Twilio
        account_sid = 'xxxxxxxxxxxxx'
        auth_token = 'xxxxxxxxxxxxxx'
        whatsapp_number = 'whatsapp:+5521977199199'
        from_whatsapp_number = 'whatsapp:+14155238886'
        to_whatsapp_number = 'whatsapp:+5521977199199'

        # cria uma instância do objeto Client com suas credenciais de autenticação
        client = Client(account_sid, auth_token)

        # lista as mensagens recebidas pelo número do WhatsApp registrado em sua conta Twilio
        messages = client.messages.list(from_=whatsapp_number)
    # Comunicação com API Google e protocolo de autorização
    class Config_sheets():
        # API Google Sheets - Definindo as credenciais e escopo da API
        scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

        # Autorizando a conta com as credenciais
        client = gspread.authorize(creds)
    # Escrever em células no Google Sheets
    class Write_sheets:
        def __init__(self, url, aba, cell, txt):
            self.url = url
            self.aba = aba
            self.cell = cell
            self.txt = txt

            # Referenciar a planilha
            sheet = Config_sheets.client.open_by_url(url)
            # Selecionando uma guia da planilha
            worksheet = sheet.worksheet(aba)
            # Escrevendo dados em uma célula específica
            worksheet.update(cell, txt)
    # Encontrar a linha de um dado no Google Sheets e atualizar colunas correspondentes
    class Match_sheets:
        def __init__(self, url, aba, txt):
            self.url = url
            self.aba = aba
            self.txt = txt

            # Referenciar a planilha
            sheet = Config_sheets.client.open_by_url(url)
            # Selecionando uma guia da planilha
            worksheet = sheet.worksheet(aba)
            # Buscando dados em células específicas
            global ref
            ref = worksheet.findall(txt, None, in_column=7)

            global cell
            cell = []
            itens = 0
            while itens <= len(ref) - 1:
                txt = str(ref[itens])
                coluna = txt.find("C", 2)
                linha = txt.find("R")
                cell.append(str(ref[itens])[coluna] + str(ref[itens])[linha + 1:coluna])
                itens += 1

            global results
            results = []
            for i in cell:
                if worksheet.acell(str(i).replace("C", "AH")).value is not None:
                    if (int(worksheet.acell(str(i).replace("C", "AH")).value[0:2]) >= int(data[6:8])-5) and (int(worksheet.acell(str(i).replace("C", "AH")).value[3:5]) == int(data[9:11])):
                        results.append("Cliente: " + worksheet.acell(str(i).replace("C", "B")).value + "\nUnidade: " + worksheet.acell(i).value)

    # Tratar textos recebidos via Whatsapp e identificar o autor, conteúdo, data e hora
    def tratamento_dados():

        global dict
        dict = {"Conteúdo: ": message.body, "Remetente: ": message.from_, "Data e hora: ": str(message.date_sent)[:19]}
        global data_hoje
        data_hoje = str(datetime.datetime.today())[:10]
        global tempo
        tempo = str(datetime.datetime.today())[11:16]
        global dict_data
        dict_data = str(dict.get("Data e hora: "))[:10]
        global hora
        hora = int(str(dict.get("Data e hora: "))[11:13]) - 3
        global new_hour

        if hora < 10:
            new_hour = "0" + str(hora) + ":" + str(dict.get("Data e hora: "))[14:16]
        else:
            new_hour = str(hora) + ":" + str(dict.get("Data e hora: "))[14:16]
    # Script de resposta ao receber um "Olá" no Whatsapp
    def apresentacao():
        client = Config.client
        message = client.messages.create(body="Olá! Sou o Chatbot da Diel Energia, prazer te conhecer...",
                                         from_=Config.from_whatsapp_number,
                                         to=Config.to_whatsapp_number)
        print("Mensagem enviada: " + str(message.body))
    # Script de resposta ao ser questionado se "Está tudo bem?" no Whatsapp
    def tudo_bem():
        client = Config.client
        message = client.messages.create(body="Obrigado por perguntar, eu estou ótimo e você? Como está?",
                                         from_=Config.from_whatsapp_number,
                                         to=Config.to_whatsapp_number)
        print("Mensagem enviada: " + str(message.body))
    # Script de resposta ao ser solicitado para verificar unidades aprovadas no Google Sheets
    def auditoria_ok():
        client = Config.client
        Match_sheets("https://docs.google.com/spreadsheets/d/1WrIbUS1-9R4JmGm0O6-MGkqZPMERcHimmp-AKlrAgFs/", "Controle de Auditoria", "Concluída")
        dia_init = int(data[6:8]) - 5
        rest = data[8:]

        if len(results) != 0:
            message = client.messages.create(body=f"O(s) supervisor(es) aprovou/aprovaram a(s) unidades(s):\nDe: {dia_init}{rest} até {data[6:]}",
                                             from_=Config.from_whatsapp_number,
                                             to=Config.to_whatsapp_number)
        else:
            message = client.messages.create(
                body=f"Nenhuma unidade foi aprovada, de {dia_init}{rest} até {data[6:]}",
                from_=Config.from_whatsapp_number,
                to=Config.to_whatsapp_number)
        itens = 0
        while itens <= len(results)-1 and len(results) != 0:
            message = client.messages.create(body="\n" + str(results[itens]),
                                             from_=Config.from_whatsapp_number,
                                             to=Config.to_whatsapp_number)
            itens += 1
    # Script de resposta ao receber um "Olá" no Whatsapp
    def apresentacao2():
        client = Config2.client
        message = client.messages.create(body="Olá! Sou o Chatbot da Diel Energia, prazer te conhecer...",
                                         from_=Config.from_whatsapp_number,
                                         to=Config.to_whatsapp_number)
        print("Mensagem enviada: " + str(message.body))
    # Script de resposta ao ser questionado se "Está tudo bem?" no Whatsapp
    def tudo_bem2():
        client = Config2.client
        message = client.messages.create(body="Obrigado por perguntar, eu estou ótimo e você? Como está?",
                                         from_=Config.from_whatsapp_number,
                                         to=Config.to_whatsapp_number)
        print("Mensagem enviada: " + str(message.body))
    # Script de resposta ao ser solicitado para verificar unidades aprovadas no Google Sheets
    def auditoria_ok2():
        client = Config2.client
        Match_sheets("https://docs.google.com/spreadsheets/d/1WrIbUS1-9R4JmGm0O6-MGkqZPMERcHimmp-AKlrAgFs/", "Controle de Auditoria", "Concluída")
        dia_init = int(data[6:8]) - 5
        rest = data[8:]

        if len(results) != 0:
            message = client.messages.create(body=f"O(s) supervisor(es) aprovou/aprovaram a(s) unidades(s):\nDe: {dia_init}{rest} até {data[6:]}",
                                             from_=Config.from_whatsapp_number,
                                             to=Config.to_whatsapp_number)
        else:
            message = client.messages.create(
                body=f"Nenhuma unidade foi aprovada, de {dia_init}{rest} até {data[6:]}",
                from_=Config.from_whatsapp_number,
                to=Config.to_whatsapp_number)
        itens = 0
        while itens <= len(results)-1 and len(results) != 0:
            message = client.messages.create(body="\n" + str(results[itens]),
                                             from_=Config.from_whatsapp_number,
                                             to=Config.to_whatsapp_number)
            itens += 1
    # Realiza uma varredura nas mensagens recebidas e seleciona a mensagem do dia, hora e minuto atuais

    # Número do Arthur
    for message in Config2.messages:
        tratamento_dados()

        # Ler e responder mensagens recebidas instantaneamente
        if (tempo == new_hour) and (data_hoje == dict_data):
            acess = 0

            global mensagem
            mensagem = dict.get("Conteúdo: ")
            recebida = "\nMensagem: " + mensagem + "\n" + "-------------------------"
            remetente = "N° Remetente: " + dict.get("Remetente: ")[12:]
            data = "Data: " + data_hoje[8:10] + "/" + data_hoje[5:7] + "/" + data_hoje[0:4]
            hora = "Hora: " + tempo
            print(recebida + "\n" + remetente + "\n" + data + "\n" + hora)
            print("-------------------------------------")

            if "olá" in mensagem.lower() and n_ola2 == 0:
                apresentacao()
                n_ola2 = 1

            elif "tudo bem" in mensagem.lower() and n_td_bem2 == 0:
                tudo_bem()
                n_td_bem2 = 1

            elif ("auditoria" or "aprovação" or "unidade" or "auditada") in mensagem.lower() and n_auditoria2 == 0:
                auditoria_ok()
                n_auditoria2 = 1

            elif ("encerrar" and "atividade" and "hoje") in mensagem.lower() or ("desligar" and "serviço") in mensagem.lower():
                exit()

    # Mensagens automáticas por horário do dia (Arthur)
    if tempo == "17:37" and mens_auto2 == 0:
        data = "Data: " + data_hoje[8:10] + "/" + data_hoje[5:7] + "/" + data_hoje[0:4]
        auditoria_ok2()
        mens_auto2 = 1

    # Mensagens automáticas por horário do dia (Gustavo)
    if tempo == "17:44" and mens_auto == 0:
        data = "Data: " + data_hoje[8:10] + "/" + data_hoje[5:7] + "/" + data_hoje[0:4]
        auditoria_ok()
        mens_auto = 1

    # Número do Gustavo
    for message in Config.messages:

        tratamento_dados()

        # Ler e responder mensagens recebidas instantaneamente
        if (tempo == new_hour) and (data_hoje == dict_data):
            acess = 0

            global mensagem2
            mensagem2 = dict.get("Conteúdo: ")
            recebida = "\nMensagem: " + mensagem2 + "\n" + "-------------------------"
            remetente = "N° Remetente: " + dict.get("Remetente: ")[12:]
            data = "Data: " + data_hoje[8:10] + "/" + data_hoje[5:7] + "/" + data_hoje[0:4]
            hora = "Hora: " + tempo
            print(recebida + "\n" + remetente + "\n" + data + "\n" + hora)
            print("-------------------------------------")

            if "olá" in mensagem2.lower() and n_ola == 0:
                apresentacao()
                n_ola = 1

            elif "tudo bem" in mensagem2.lower() and n_td_bem == 0:
                tudo_bem()
                n_td_bem = 1

            elif ("auditoria" or "aprovação" or "unidade" or "auditada") in mensagem2.lower() and n_auditoria == 0:
                auditoria_ok()
                n_auditoria = 1

            elif ("encerrar" and "atividade" and "hoje") in mensagem2.lower() or ("desligar" and "serviço") in mensagem2.lower():
                exit()

    hora_fim = str(datetime.datetime.now())[14:16]

    if hora_init != hora_fim:
        n_ola = 0
        n_td_bem = 0
        n_auditoria = 0
        mens_auto = 0

        n_ola2 = 0
        n_td_bem2 = 0
        n_auditoria2 = 0
        mens_auto2 = 0
