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
from random import randint

from utils.LoadingClass import Loader


class StartBot:
    def __init__(self, mail="", senha="", extraOpc=False):
        client = MongoClient(config("MONGO_URI"))
        self.db = client.dbAppBotYt
        self.col = self.db.channels

        if not extraOpc:
            self.mail = mail
            self.senha = senha
            self.nav = Chrome(driver_executable_path=ChromeDriverManager().install())
            self.nav.implicitly_wait(1)
            self.channelSend = []

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
        self.nav.get(config("VIDEO"))
        sleep(2.5)
        self.checkCommentsRecent()

        maxChannel = int(config("MAX_CHANNEL_LIMIT", default=100))

        channelSend = []

        while True:
            try:
                canais = self.nav.find_elements(By.ID, 'author-text')

                for canal in canais:
                    try:
                        if not self.col.find_one({"url": canal.get_attribute('href')}):
                            self.col.insert_one({"_id": str(ObjectId()), "url": canal.get_attribute('href')})
                            channelSend.append(canal.get_attribute('href'))
                    except:
                        sleep(0.1)

                if len(channelSend) >= maxChannel:
                    break
                sleep(.8)
                self.toDown()
            except NoSuchElementException:
                sleep(1)

        self.channelSend = channelSend

    def executComment(self, comments):

        sleep(randint(45, 85))

        nScroll = 600
        comment = comments[randint(0, len(comments) - 1)]
        sleep(1.4)
        self.nav.execute_script(f"window.scrollTo(0,{nScroll})")
        """ Esse limite simplemente quando o bt de comentário não existir nos shorts - raro - """
        limt = 5

        while True:

            try:
                self.nav.find_element(By.ID, 'comments-button').click()
                self.nav.find_element(By.XPATH, '//*[@id="contenteditable-root"]').click()
                self.nav.find_element(By.XPATH, '//*[@id="contenteditable-root"]').send_keys(comment)
                self.nav.find_element(By.ID, 'submit-button').click()
                break
            except NoSuchElementException or ElementNotInteractableException:
                try:
                    self.nav.find_element(By.ID, 'simplebox-placeholder').click()
                    sleep(0.5)
                    self.nav.find_element(By.ID, 'contenteditable-root').send_keys(comment)
                    self.nav.find_element(By.ID, 'submit-button').click()
                    break
                except NoSuchElementException or ElementNotInteractableException:
                    """ quando nao tem comentario ativado """
                    try:
                        self.nav.find_element(By.XPATH, '//*[@id="message"]/span')
                        break
                    except NoSuchElementException:
                        try:
                            """ pop up do nada interrompedo clicar '-'"""
                            self.nav.find_element(By.XPATH, '//*[@id="button"]/yt-icon').click()
                        except NoSuchElementException or ElementNotInteractableException:
                            sleep(1.5)
                            nScroll += 50
                            self.nav.execute_script(f"window.scrollTo(0,{nScroll})")

            except ElementNotInteractableException:
                limt -= 1
                if limt < 0:
                    break
                sleep(0.7)
        sleep(3.5)

    def comentInChannels(self):
        """
            Entra no canal clica na aba vídeos e seleciona o primeiro um vídeo
        """
        for channelLink in self.channelSend:
            self.nav.get(channelLink)

            self.verifyXpath('//*[@id="tabsContent"]/tp-yt-paper-tab[2]/div')
            self.nav.find_element(By.XPATH, '//*[@id="tabsContent"]/tp-yt-paper-tab[2]/div').click()

            with open("./percistence/comments.txt", encoding="utf-8") as file_comment:
                comments = file_comment.read().split('/')

            otherLimit = 5

            while True:

                if otherLimit <= 0:
                    break

                try:
                    sleep(1.5)
                    try:
                        self.nav.find_element(By.XPATH, '//*[@id="video-title"]').click()

                        self.executComment(comments)
                        break
                    except Exception as err:
                        otherLimit -= 1
                        sleep(1)

                except NoSuchElementException or ElementNotInteractableException:
                    otherLimit -= 1
                    sleep(1)

    def startAllProcess(self):
        self.loadingScreen(" Iniciando Login", self.startLogin)
        self.loadingScreen(" Buscando canais", self.searchChannels)
        self.loadingScreen(" Comentando nos canais", self.comentInChannels)
