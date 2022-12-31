class Login:

    def __init__(self, email, senha):
        self.email = email
        self.senha = senha

    def addNewLogin(self):
        with open("./percistence/accounts.txt", "a") as file:
            file.write(f"{self.email},{self.senha}\n")
