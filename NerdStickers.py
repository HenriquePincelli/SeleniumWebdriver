from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from functions import makeFiles, sendEmail
import pandas
from unidecode import unidecode

#Function to make a report with the requested sticker
def NerdStickers(userEmail):

    #Ask user which sticker they want
    print("=-=" * 24)
    sticker = str(input("Deseja gerar um relatório com qual adesivo?\n"))
    print("=-=" * 24)

    #Open the navigator
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.nerdstickers.com.br/")
    assert "Nerd Stickers" in driver.title
    driver.maximize_window()

    #Searching the product
    pesquisa = driver.find_element(By.ID, "dgwt-wcas-search-input-1")
    pesquisa.send_keys(sticker)
    pesquisa.send_keys(Keys.ENTER)

    #Creating lists with all products founded in the first page
    # products_URL = driver.current_url
    # products_Titles = driver.find_elements(By.CLASS_NAME, "title-wrapper")
    products_Titles = driver.find_elements(By.CLASS_NAME, "woocommerce-loop-product__title")
    # products_Prices = driver.find_elements(By.CLASS_NAME, "price-wrapper")
    products_Prices = driver.find_elements(By.CLASS_NAME, "price")

    #Making a dict list with the products
    # emailList = {"Vegeta Vírus": ["Preço", "URL"], "Henrique Vírus": ["Preço", "URL"]}
    emailList = {}
    for i in range (len(products_Titles)):
        emailList.update({i: [products_Titles[i].text, products_Prices[i].text, ("https://www.nerdstickers.com.br/todos/{}/".format(products_Titles[i].text.replace(" ", "-")))]})

    #Close the driver
    driver.quit()

    #Calling the remaining functions from the process
    df = pandas.DataFrame(emailList).transpose()
    df = df.set_axis(["Adesivo", "Preço", "Link"], axis='columns')
    reportName = makeFiles(0, df)
    print("=-=" * 24)
    print("Relatórios Armazenados!")
    sendEmail(0, sticker, reportName, userEmail)

    #Variable to return success message
    check = "Relatório enviado!!!"

    return check