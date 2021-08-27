from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from datetime import datetime
from constants import *
from time import sleep
import requests
import schedule
import os

# - DEFININDO FUNÇÕES - 
# x é y porcento de z
def percent(x, z): # Ex. 585 dias é quanto porcento de 1440 dias? | percent(585, 1440) | output = 40.6 
    y = (x*100)/z
    #print(str(x) + " é {:.1f}% de ".format(r) + str(z))
    return "{:.1f}".format(y) # retorna o valor formatado para mostrar apenas uma casa após a vírgula

# quantos dias já foram
def dateToDays():
    hoje = datetime.now()
    diaAtual = hoje.strftime("%d")
    mesAtual = hoje.strftime("%m")
    anoAtual = hoje.strftime("%Y")
    diasRestantes = (int(diaAtual)-1) # comecei no dia 01/01/2020
    mesesRestantes =(int(mesAtual)-1)*30 # convertendo para dias
    anosRestantes = (int(anoAtual)-2020)*360 # convertendo para dias
    jaPassaram = (diasRestantes + mesesRestantes + anosRestantes)
    return jaPassaram

# editar bio instagram
def editarBio():
    os.system('cls' if os.name == 'nt' else 'clear') # limpa o terminal (cls se for windows e clear se for qualquer outro)
    options = Options()
    options.headless = True # abrir navegador em background
    driver = webdriver.Firefox(options=options)
    print("Entrando no instagram")
    driver.get("https://www.instagram.com/") # entrar no instagram
    sleep(3)
    print("Enviando login...")
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(login) # login
    sleep(3)
    print("Enviando senha...")
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(senha) # senha
    sleep(3)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click() # botão de login
    print("Logado como", login)
    sleep(8)
    print("Editando informações...")
    driver.get("https://www.instagram.com/accounts/edit/") # editar informações
    sleep(8)
    driver.find_element_by_xpath('//*[@id="pepBio"]').clear() # limpar textarea da bio
    driver.find_element_by_xpath('//*[@id="pepBio"]').send_keys(texto) # colar texto na textarea
    sleep(3)
    print("Salvando...")
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/form/div[10]/div/div/button').click() # confirmar alteração da bio
    sleep(10)
    print("Salvo, deslogando...")
    driver.get("https://www.instagram.com/accounts/logout") # sair da conta
    sleep(8)
    print("Deslogado.")
    driver.close() # fechar navegador
    print("Finalizado com sucesso.")
    checarConcluido()

# enviar mensagem telegram
def telegramBotSendtext(message):
    send_text = 'https://api.telegram.org/bot' + telegramApiKey + '/sendMessage?chat_id=' + telegramChatId + '&parse_mode=Markdown&text=' + message
    response = requests.get(send_text)
    return response.json()

# documentar erro
def documentarErro(err):
    hoje = datetime.now()
    diaAtual = hoje.strftime("%d/%m/%Y - %H:%M")
    mensagem = ("{}\nErro em Alterar bio Instagram\n{}".format(diaAtual, err))
    telegramBotSendtext(mensagem)

# verificar se chegamos em 100%
def checarConcluido():
    if (percent(dateToDays(), 1440) == "100.0"):
        print("Chegamos em 100%")
        print("Finalizando...")
        telegramBotSendtext("Chegamos em 100%\nFinalizando...")
        erros += 1

# - DEFININDO VARIÁVEIS -
texto = ("•FAG - Eng. Software {}%\n•Toledo/Cascavel - PR\n•19y".format(percent(dateToDays(), 1440)))
erros = 0

# - DEFININDO ROTINA -
schedule.every().day.at("00:00").do(editarBio) # todo dia executa editarBio() em horário específico

# - LOOP -
while True:
    if erros == 0:
        try:
            schedule.run_pending()
            sleep(1)
        except Exception as err:
            documentarErro(err)
            erros += 1
    else: break
