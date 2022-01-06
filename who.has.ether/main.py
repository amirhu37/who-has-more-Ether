from selenium import webdriver
from selenium.webdriver.firefox import options
from selenium.webdriver.firefox.options import Options
import regex
wallets = list()
datas = dict()
opt = Options()
opt.headless = True



def addres_finder():
    driver = webdriver.Firefox(options=opt)
    driver.get("https://etherscan.io/accounts")
    driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_ddlRecordsPerPage"]/option[3]').click()
    flag = 1
    while True:
        try:
            if temp := driver.find_element_by_xpath(f'//*[@id="ContentPlaceHolder1_divTable"]/table/tbody/tr[{flag}]/td[2]/span/a').get_attribute('innerHTML'):
                wallets.append(temp)
                flag += 1
        except:
            try:
                if temp := driver.find_element_by_xpath(f'//*[@id="ContentPlaceHolder1_divTable"]/table/tbody/tr[{flag}]/td[2]/a').get_attribute('innerHTML'):
                    wallets.append(temp)
                    flag += 1
            except:
                break
    driver.close()



def who_has_what():
    
    driver = webdriver.Firefox(options=opt)
    #driver.find_element_by_xpath('//*[@id="mytable_length"]/label/select/option[2]').click()
    for i in range(1, len(wallets)):
        temp_list = list()
        driver.get(f'https://etherscan.io/tokenholdings?a={wallets[i]}')
        j = 1
        while True:
            
            try:
                assets = driver.find_element_by_xpath(f'//*[@id="mytable"]/tbody/tr[{j}]/td[2]').get_attribute('innerHTML')
                temp_list.append(assets)
                j +=1
            except:
                 
                datas[wallets[i][-10:]] = [regex.sub(r"<[^>]*>", "", i) for i in temp_list]
                break
        
        del temp_list
    driver.close()


def writer():
    with open('results.csv', 'w', newline='\n') as file:
        for i in range(len(datas)):
            file.writelines(f'{i+1},{list(datas.keys())[i]},{",".join(list(datas.values())[i])}\n')

        file.close()
    print("Done")


def shudown():
    import os
    os.system("shutdown /s /t 1")

def csv_to_xl():
    import pandas as pd

    df = pd.read_csv('..\\who.has.ether\\results.csv')
    df.to_excel('..\\who.has.ether\\results.xlsx',index=False , header=False)



addres_finder()
who_has_what()
writer()
csv_to_xl()

