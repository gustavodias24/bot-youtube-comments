from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome
from time import sleep
from utils.LoadingClass import Loader
from pymongo import MongoClient
import threading


# def processo():
#     finalizar = False
#     while not finalizar:
#         finalizar = input("finalizar? ")
#     nav.close()
#
#
# the_process = threading.Thread(name='process', target=processo)
#
# the_process.start()
#
# while the_process.is_alive():
#     Loader().animated_loading()

class StartBot:
    def __init__(self, mail="", senha="", extraOpc=False):
        client = MongoClient(
            "mongodb+srv://benicio:84048010233@cluster0.4ujdozl.mongodb.net/?retryWrites=true&w=majority")
        self.db = client.dbAppBotYt
        self.col = self.db.channels

        if not extraOpc:
            self.mail = mail
            self.senha = senha
            self.nav = Chrome(driver_executable_path=ChromeDriverManager().install())

    def verifyXpath(self, xpath, needLimit=False):
        """
            Tem certeza que o xpath vai estar presente na página!
        """

        limit = 0

        while True:
            try:
                self.nav.find_element(By.XPATH, xpath)
                return True
            except NoSuchElementException:
                sleep(1.5)
                if needLimit:
                    limit += 1
                    if limit == 2:
                        break

    def verify2Xpath(self, xpathVery, xpathBtn):
        """
            Quando a página varia de acordo com o email
        """
        while True:
            try:
                self.nav.find_element(By.XPATH, xpathVery)
                break
            except NoSuchElementException:
                try:
                    self.nav.find_element(By.XPATH, xpathBtn).click()
                    break
                except NoSuchElementException:
                    sleep(1.5)

    def loadingScreen(self, text, process, args=()):
        the_process = threading.Thread(name='process', target=process, args=args)
        the_process.start()

        while the_process.is_alive():
            Loader(text).animated_loading()

    def startLogin(self):

        self.nav.implicitly_wait(.7)
        self.nav.get("https://accounts.google.com/")

        if self.verifyXpath('//*[@id="af-error-container"]/p[1]/b', True):
            self.startAllProcess()

        self.verifyXpath('//*[@id="identifierId"]')
        edtEmail = self.nav.find_element(By.XPATH, '//*[@id="identifierId"]')
        edtEmail.click()
        edtEmail.send_keys(self.mail + Keys.ENTER)

        self.verifyXpath('//*[@id="password"]/div[1]/div/div[1]/input')
        edtSenha = self.nav.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
        edtSenha.click()
        edtSenha.send_keys(self.senha + Keys.ENTER)

        self.verify2Xpath(
            '//*[@id="headingText"]/span',
            '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[4]/div[1]/button/div[3]')

        self.verifyXpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/header/h1')

    def clearDB(self):
        self.col.delete_many({})

    def searchChannels(self):
        with open("./percistence/videoExtract.txt", "r") as fileExtract:
            for videoUrl in fileExtract.readlines():
                self.nav.get(videoUrl)
                pass

    def startAllProcess(self):
        self.loadingScreen(" Iniciando Login ", self.startLogin)
        self.loadingScreen(" Buscando canais ", self.searchChannels)
