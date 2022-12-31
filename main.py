from colorama import Fore, Back, Style
from undetected_chromedriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from utils.LoadingClass import Loader
import threading
from time import sleep

print(Style.BRIGHT + Fore.WHITE + Back.RED + " Menu de escolhas: ")
print(Style.RESET_ALL + Fore.YELLOW + " [ 1 ]" + Fore.BLUE + " Fazer login. ")
print(Fore.YELLOW + " [ 2 ]" + Fore.BLUE + " Limpar database. ")
print(Fore.YELLOW + " [ 3 ]" + Fore.BLUE + " Iniciar bot. ")

nav = Chrome(driver_executable_path=ChromeDriverManager().install())
nav.get("https://www.google.com/")


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
