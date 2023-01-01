import threading
from time import sleep

from pymongo import MongoClient
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from undetected_chromedriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from decouple import config
from bson.objectid import ObjectId

from utils.LoadingClass import Loader


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
        client = MongoClient(config("MONGO_URI"))
        self.db = client.dbAppBotYt
        self.col = self.db.channels

        if not extraOpc:
            self.mail = mail
            self.senha = senha
            self.nav = Chrome(driver_executable_path=ChromeDriverManager().install())
            self.nav.implicitly_wait(0.8)

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

    def checkCommentsRecent(self):
        nScroll = 600
        self.nav.execute_script(f"window.scrollTo(0,{nScroll})")
        while True:
            try:
                self.nav.find_element(By.XPATH, '//*[@id="icon-label"]').click()
                self.nav.find_element(By.XPATH,
                                      '//*[@id="menu"]/a[2]/tp-yt-paper-item/tp-yt-paper-item-body/div[1]').click()
                break
            except NoSuchElementException:
                sleep(1.5)
                nScroll += 100
                self.nav.execute_script(f"window.scrollTo(0,{nScroll})")
            except ElementNotInteractableException:
                sleep(1.5)

    def toDown(self):
        self.nav.execute_script("window.scrollTo(0,999999)")
        sleep(1.5)

    def searchChannels(self):
        with open("./percistence/videoExtract.txt", "r") as fileExtract:
            self.nav.get(fileExtract.read())

            self.verifyXpath('//*[@id="icon-label"]')
            self.checkCommentsRecent()

            maxChannel = config("MAX_CHANNEL_LIMIT", default=100)

            while True:
                try:
                    canais = self.nav.find_elements(By.ID, 'author-text')
                    if len(canais) == maxChannel:
                        break
                    sleep(2)
                    self.toDown()
                except NoSuchElementException:
                    sleep(1)

            for canal in canais:
                if not self.col.find_one({"url": canal.get_attribute('href')}):
                    self.col.insert_one({"_id": str(ObjectId()), "url": canal.get_attribute('href')})
                    print(canal.get_attribute('href'))

    def startAllProcess(self):
        self.loadingScreen(" Iniciando Login ", self.startLogin)
        self.loadingScreen(" Buscando canais ", self.searchChannels)
