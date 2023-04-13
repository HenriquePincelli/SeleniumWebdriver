from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from functions import makeFiles, sendEmail
import pandas
from unidecode import unidecode

#Function to update and send a report with trip data
def ClickBus(userEmail):

    #Loop to guarantee that the program will return a report
    searchSuccess = 0
    while searchSuccess != 1:
        #Ask user which report trip they want
        tripBeginDay = 0
        while tripBeginDay not in ["01", "1", "02", "2", "03", "3", "04", "4", "05", "5", "06", "6", "07", "7", "08", "8", "09", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]:
            print("=-=" * 24)
            tripBeginDay = str(input("""Dia de partida: """))
            if tripBeginDay not in ["01", "1", "02", "2", "03", "3", "04", "4", "05", "5", "06", "6", "07", "7", "08", "8", "09", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]:
                print("=-=" * 24)
                print("Dia inválido, tente novamente.")
                print("=-=" * 24)
                continue
            continue
        tripBeginMonth = 0
        while tripBeginMonth not in ["01", "1", "02", "2", "03", "3", "04", "4", "05", "5", "06", "6", "07", "7", "08", "8", "09", "9", "10", "11", "12"]:
            tripBeginMonth = str(input("""Mês de partida: """))
            if tripBeginMonth not in ["01", "1", "02", "2", "03", "3", "04", "4", "05", "5", "06", "6", "07", "7", "08", "8", "09", "9", "10", "11", "12"]:
                print("=-=" * 24)
                print("Mês inválido, tente novamente.")
                print("=-=" * 24)
                continue
            continue
        time = datetime.now()
        tripBeginYear = 0
        while tripBeginYear < int(time.strftime("%Y")):
            tripBeginYear = int(input("""Ano de partida: """))
            if tripBeginYear < int(time.strftime("%Y")):
                print("=-=" * 24)
                print("Ano inválido, tente novamente.")
                print("=-=" * 24)
                continue        
        tripDestination = unidecode(str(input("Insira o destino desejado: ")))
        print("=-=" * 24)

        #Open the navigator in the trip page
        driver = webdriver.Chrome(ChromeDriverManager().install())
        listEstados = ["sp", "rj", "am", "rr", "pa", "ap", "to", "ma", "pi", "ce", "rn", "pb", "pe", "al", "se", "ba", "mg", "es", "ac", "ro", "pr", "sc", "rs", "df", "mt", "go", "ms"]
        cont = 0
        for h in listEstados:
            driver.get("https://www.clickbus.com.br/onibus/sao-paulo-sp-todos/" + str(tripDestination.replace(" ", "-").lower()) + "-" + h + "-todos?departureDate=" + str(tripBeginYear) + "-" + str(tripBeginMonth) + "-" + str(tripBeginDay))
            driver.maximize_window()
            if "ClickBus" in driver.title:
                #Making a dict list with all data collected
                list_Hour = driver.find_elements(By.CLASS_NAME, "hour")
                listBusStations = driver.find_elements(By.CLASS_NAME, "bus-stations")
                listRouteType = driver.find_elements(By.CLASS_NAME, "route-type")
                # listDuration = driver.find_elements(By.CLASS_NAME, "duration")
                listServiceClass = driver.find_elements(By.CLASS_NAME, "service-class")
                list_Price = driver.find_elements(By.CLASS_NAME, "price")
                if len(list_Hour) - 1 == len(listBusStations) and len(listBusStations) == len(listRouteType) and len(listRouteType) == len(listServiceClass) and len(listServiceClass) == len(list_Price) - 1:
                    tripsList = {}
                    for p in range(len(list_Hour) - 1):
                        tripsList.update({p + 1: [list_Hour[p + 1].text.split("\n")[0], list_Hour[p + 1].text.split("\n")[1], listBusStations[p].text.split("\n")[0], listBusStations[p].text.split("\n")[1], listRouteType[p].text, listServiceClass[p].text, list_Price[p + 1].text.replace("\n", " - ")]})
                    df = pandas.DataFrame(tripsList).transpose()
                    df = df.set_axis(["Horário de Partida", "Horário de Chegada", "De", "Para", "Duração da viagem", "Tipo de Serviço", "Preço da passagem"], axis='columns')
                    #Calling the functions to make and send the report
                    reportName = makeFiles(1, df)
                    print("Relatórios Armazenados!")
                    print("=-=" * 24)
                    sendEmail(1, tripDestination, reportName, userEmail)
                    searchSuccess = 1
                    driver.quit()
                    break
            elif "Página não encontrada" in driver.title:
                driver.get("https://www.clickbus.com.br/onibus/sao-paulo-sp-todos/" + str(tripDestination.replace(" ", "-").lower()) + "-" + h + "?departureDate=" + str(tripBeginYear) + "-" + str(tripBeginMonth) + "-" + str(tripBeginDay))
                if "ClickBus" in driver.title:
                    #Making a dict list with all data collected
                    list_Hour = driver.find_elements(By.CLASS_NAME, "hour")
                    listBusStations = driver.find_elements(By.CLASS_NAME, "bus-stations")
                    listRouteType = driver.find_elements(By.CLASS_NAME, "route-type")
                    # listDuration = driver.find_elements(By.CLASS_NAME, "duration")
                    listServiceClass = driver.find_elements(By.CLASS_NAME, "service-class")
                    list_Price = driver.find_elements(By.CLASS_NAME, "price")
                    if len(list_Hour) - 1 == len(listBusStations) and len(listBusStations) == len(listRouteType) and len(listRouteType) == len(listServiceClass) and len(listServiceClass) == len(list_Price) - 1:
                        tripsList = {}
                        for h in range(len(list_Hour) - 1):
                            tripsList.update({h + 1: [list_Hour[h + 1].text.split("\n")[0], list_Hour[h + 1].text.split("\n")[1], listBusStations[h].text.split("\n")[0], listBusStations[h].text.split("\n")[1], listRouteType[h].text, listServiceClass[h].text, list_Price[h + 1].text.replace("\n", " - ")]})
                        df = pandas.DataFrame(tripsList).transpose()
                        df = df.set_axis(["Horário de Partida", "Horário de Chegada", "De", "Para", "Duração da viagem", "Tipo de Serviço", "Preço da passagem"], axis='columns')
                        #Calling the functions to make and send the report
                        reportName = makeFiles(1, df)
                        print("Relatórios Armazenados!")
                        print("=-=" * 24)
                        sendEmail(1, tripDestination, reportName, userEmail)
                        searchSuccess = 1
                        driver.quit()
                        break
                elif "Página não encontrada" in driver.title:
                    cont += 1
                    if cont == 27:
                        print("Não foi possível encontrar nenhum resultado correspondente a sua pesquisa, por gentileza, insira os parâmetros de busca novamente.")
                        driver.quit()
                        continue
                    print(h.upper())
                    print("=-=" * 24)
            else:
                print("Erro ao realizar operação, por gentileza, tente novamente.")
                return

    #Variable to return success message
    check = "Relatório enviado!!!"

    return check