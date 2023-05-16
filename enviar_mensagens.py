from twilio.rest import Client
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Comunicação com API Twilio e protocolo de autorização
class Config():
    # Substitua as informações abaixo pelas suas credenciais de autenticação e número do WhatsApp registrado na conta Twilio
    account_sid = 'AC91c36db3513971ff70473a25d5ced9db'
    auth_token = '69f3613c42544aefd60ef7c59c3b7030'
    whatsapp_number = 'whatsapp:+5511945805551'
    from_whatsapp_number = 'whatsapp:+14155238886'
    to_whatsapp_number = 'whatsapp:+5511945805551'

    # cria uma instância do objeto Client com suas credenciais de autenticação
    client = Client(account_sid, auth_token)

    # lista as mensagens recebidas pelo número do WhatsApp registrado em sua conta Twilio
    messages = client.messages.list(from_=whatsapp_number)

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
# Comunicação entre WhatsApp e Google Sheets
def write_sheets():
    # API Google Sheets
    # Definindo as credenciais e escopo da API
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

    # autorizando a conta com as credenciais
    client = gspread.authorize(creds)

    # Referenciar planilha
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1WrIbUS1-9R4JmGm0O6-MGkqZPMERcHimmp-AKlrAgFs/')
    # selecionando uma guia da planilha
    worksheet = sheet.worksheet('Painel validação geral')
    # lendo dados de uma célula específica
    cell_value = worksheet.acell('A2').value
    # escrevendo dados em uma célula específica
    worksheet.update('A2', 'Arthur')
write_sheets()

# Realiza uma varredura nas mensagens recebidas e seleciona a mensagem do dia, hora e minuto atuais
for message in Config.messages:

    tratamento_dados()

    # Ler e responder mensagens recebidas instantaneamente
    if (tempo == new_hour) and (data_hoje == dict_data):

        global mensagem
        mensagem = dict.get("Conteúdo: ")
        recebida = "\nMensagem: " + mensagem + "\n" + "-------------------------"
        remetente = "N° Remetente: " + dict.get("Remetente: ")[12:]
        data = "Data: " + data_hoje[8:10] + "/" + data_hoje[5:7] + "/" + data_hoje[0:4]
        hora = "Hora: " + tempo
        print(recebida + "\n" + remetente + "\n" + data + "\n" + hora)
        print("-------------------------------------")

        if "Olá" in mensagem:
            apresentacao()

        elif "Tudo bem" in mensagem:
            tudo_bem()
