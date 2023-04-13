from NerdStickers import NerdStickers
from ClickBus import ClickBus
import os

#Collecting the user email to send the report later
print("=-=" * 24)
userEmail = str(input("Insira o seu email: "))

#Starting the program.
program = 1
while program == 1:

    #Ask user which report they want
    print("=-=" * 24)
    option = str(input("""[1] Adesivos
[2] Passagens de ônibus
[0] Sair do programa\n
Digite o número correspondente ao seu interesse para em seguida gerar um relatório: """))

    #Activate the function of the requested report
    try:
        if int(option) == 1:
            option1 = "Relatório pendente."
            while option1 != "Relatório enviado!!!":
                try:
                    if option1 == "Relatório com erro.":
                        print("=-=" * 24)
                        print("Nenhum resultado encontrado, Tente novamente.")
                        option1 = NerdStickers()
                        if option1 == "Relatório enviado!!!":
                            print("=-=" * 24)
                            print(option1)
                            continue
                    else:
                        option1 = NerdStickers(userEmail)
                        print("=-=" * 24)
                        print(option1)
                        continue
                except:
                    option1 = "Relatório com erro."
        elif int(option) == 2:
            option2 = "Relatório pendente."
            while option2 != "Relatório enviado!!!":
                try:
                    option2 = ClickBus(userEmail)
                    print(option2)
                    continue
                except:
                    option2 = "Relatório pendente."
        elif int(option) == 0:
            print("=-=" * 24)
            print("Obrigado e volte sempre ;)")
            print("=-=" * 24)
            os._exit(0)
        else:
            print("=-=" * 24)
            print("Número inválido. Tente novamente.")
    except:
        print("=-=" * 24)
        print("Entrada inválida. Tente novamente.")
        continue