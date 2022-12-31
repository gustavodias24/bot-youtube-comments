from colorama import Fore, Back, Style
from undetected_chromedriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from process.AddLoginClasse import Login
from utils.LoadingClass import Loader
import threading
from time import sleep
import os


def main():
    command = "cls"
    os.system(command)
    print(Style.BRIGHT + Fore.WHITE + Back.RED + " Menu de escolhas: ")
    print(Style.RESET_ALL + Fore.YELLOW + " [ 01 ]" + Fore.BLUE + " Opções de login ")
    print(Fore.YELLOW + " [ 02 ]" + Fore.BLUE + " Limpar database. ")
    print(Fore.YELLOW + " [ 03 ]" + Fore.BLUE + " Iniciar bot. ")
    print(Fore.YELLOW + " [ 00 ]" + Fore.BLUE + " sair. ")

    try:
        response = int(input(Fore.RED + Style.BRIGHT + " Sua opção: "))
    except ValueError:
        print(Fore.BLUE + Back.YELLOW + Style.BRIGHT + " Comando inválido " + Back.RESET)
        sleep(1)
        response = 0
        main()

    if response == 1:

        os.system(command)

        with open("./percistence/config.txt", "r") as file:
            contAtual = file.read()

        print(Style.BRIGHT + Fore.WHITE + Back.RED + " Menu de login: ")
        print(Style.RESET_ALL + Fore.YELLOW + " [ 01 ]" + Fore.BLUE + " Add nova conta. ")
        print(Fore.YELLOW + " [ 02 ]" + Fore.BLUE + f" Selecionar conta atual. ( {contAtual} ) ")
        print(Fore.YELLOW + " [ 00 ]" + Fore.BLUE + " Voltar. ")

        try:
            response = int(input(Fore.RED + Style.BRIGHT + " Sua opção: "))
        except ValueError:
            print(Fore.BLUE + Back.YELLOW + Style.BRIGHT + " Comando inválido " + Back.RESET)
            sleep(1)
            response = 0
            main()
        if response == 1:
            mail = input(Fore.CYAN + " E-MAIL: ")
            senha = input(Fore.CYAN + " SENHA: ")
            lg = Login(mail, senha)
            lg.addNewLogin()
            print(Fore.BLUE + Back.YELLOW + Style.BRIGHT + " Conta adicionada " + Back.RESET)
            sleep(1)
            main()
        elif response == 2:
            os.system(command)
            with open("./percistence/accounts.txt", "r") as accountsFile:
                contSelec = 1
                print(Style.BRIGHT + Fore.WHITE + Back.RED + " Trocar conta? ")
                for cont in accountsFile.readlines():
                    mailSenha = cont.split(",")
                    selecionado = Fore.CYAN + " ( SELECIONADO )" if int(contSelec) == int(contAtual) else ""
                    print(Style.RESET_ALL + Fore.YELLOW + f"[ {contSelec} ] " + Fore.YELLOW + Style.BRIGHT + mailSenha[0] + selecionado)
                    contSelec += 1
                print(Style.RESET_ALL + Fore.YELLOW + f"[ 00 ] " + Fore.YELLOW + Style.BRIGHT + "Sair ")

                try:
                    response = int(input(Fore.RED + Style.BRIGHT + " Sua opção: "))
                except ValueError:
                    print(Fore.BLUE + Back.YELLOW + Style.BRIGHT + " Comando inválido " + Back.RESET)
                    sleep(1)
                    response = 0
                    main()

                if response > (contSelec - 1) or response <= 0:
                    rps = " Saindo... " if response == 0 else " Item inválido "
                    print(Fore.BLUE + Back.YELLOW + Style.BRIGHT + rps + Back.RESET)
                    sleep(1)
                else:
                    with open("./percistence/config.txt", "w") as configFile:
                        configFile.writelines(str(response))
                        print(Fore.BLUE + Back.YELLOW + Style.BRIGHT + " Conta alterada " + Back.RESET)
                        sleep(1)

                main()
        else:
            print(Fore.BLUE + Back.YELLOW + Style.BRIGHT + " Comando inválido " + Back.RESET)
            sleep(1)
            main()

    elif response == 2:
        pass
    elif response == 3:
        pass
    elif response == 0:
        print(Fore.RED + Style.BRIGHT + " bye! ")
    else:
        print(Fore.BLUE + Back.YELLOW + Style.BRIGHT + " Comando inválido " + Back.RESET)
        sleep(1)
        main()

    # nav = Chrome(driver_executable_path=ChromeDriverManager().install())
    #
    # nav.get("https://accounts.google.com/")

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


if __name__ == "__main__":
    main()
