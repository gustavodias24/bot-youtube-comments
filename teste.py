from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
from bson.objectid import ObjectId
from time import sleep

'''
    rolando pra baixo e pegando a quantidade escolhida corretamente
'''
def toDown(nav):
    nav.execute_script("window.scrollTo(0,999999)")
    sleep(1.5)


client = MongoClient("mongodb+srv://benicio:84048010233@cluster0.4ujdozl.mongodb.net/?retryWrites=true&w=majority")
db = client.dbAppBotYt
col = db.channels


nav = webdriver.Chrome(executable_path=ChromeDriverManager().install())

nav.get("https://www.youtube.com/watch?v=y-TGsytx91Q")

maxChannel = 100


while True:
    try:
        canais = nav.find_elements(By.ID, 'author-text')
        if len(canais) == maxChannel:
            break
        sleep(2)
        toDown(nav)
    except Exception as erro:
        print(erro)
        sleep(1)

for canal in canais:
    if not col.find_one({"url": canal.get_attribute('href')}):
        col.insert_one({"_id": str(ObjectId()), "url": canal.get_attribute('href')})
        print(canal.get_attribute('href'))
    else:
        print("Já foi tinha")
