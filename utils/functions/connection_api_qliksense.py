import uuid

import aiohttp
from aiogram import types
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pyautogui
from selenium.webdriver.common.keys import Keys
import time
from urllib3.util.retry import Retry


import requests
import base64
import json



async def fetch_data_from_api(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, verify=False) as response:
            return await response.json()


async def get_data(message: types.Message):
    import requests
    import json

    # Логин и пароль для авторизации
    username = "tattelecom\\qlikdevelop"
    password = "q*4rt8kN%y"

    # URL для страницы авторизации
    login_url = "https://qlik.tattelecom.ru/ttk/internal_forms_authentication/?targetId=47c5ba15-80fc-4e03-9ac4-2a30c5b4197d"

    # Создание сессии для хранения cookies
    session = requests.Session()
    cert = ('client.pem', 'client_key.pem')
    xrf = '1736453957027364'
    # Отправка POST запроса с логином и паролем на страницу авторизации
    response = session.post(login_url, data={"username": username, "password": password}, verify=False, cert=cert)

    if response.status_code == 200:
        # URL для получения JSON данных
        data_url = "https://qlik.tattelecom.ru/api/v1/apps/43ce28ec-a6a2-43bd-9250-786a35bd9198/data/lineage?qlikTicket=rETanRJ3noXYt3Pk"

        # GET запрос для получения JSON данных после успешной авторизации
        response_data = session.get(data_url, verify=False)

        if response_data.status_code == 200:
            try:
                json_data = response_data.json()
                print(json_data)
            except json.decoder.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        else:
            print(f"Error retrieving data. Status code: {response_data.status_code}")
    else:
        print(f"Authentication error. Status code: {response.status_code}")


    # import requests
    # import json
    #
    # qlik_host = 'https://10.19.63.5'
    # app_id = '6c82b08c-e9f4-409d-a32a-e6e83f2f177c'
    # xrf_key = '1234567890123456'  # случайно сгенерированный строковый ключ
    #
    # headers = {
    #     'X-Qlik-Xrfkey': xrf_key,
    #     'Content-Type': 'application/json',
    #     'X-Qlik-User': 'UserDirectory=INTERNAL;UserId=sa_repository'
    # }
    #
    # url = f'{qlik_host}/qrs/app/{app_id}'
    # response = requests.get(url, headers=headers, verify=False)
    #
    # if response.status_code == 200:
    #     script_text = response.text
    #
    #     if script_text:
    #         with open('app_script.qvs', 'w') as file:
    #             file.write(script_text)
    #         print("Скрипт приложения сохранен в файл 'app_script.qvs'")
    #     else:
    #         print("Не удалось получить скрипт приложения.")
    # else:
    #     print(f"Ошибка получения скрипта приложения. Статус ответа: {response.status_code}")

    # import requests
    #
    # # URL для метода GetScript
    # url = 'https://10.19.63.5/api/v1/apps/6c82b08c-e9f4-409d-a32a-e6e83f2f177c/script'
    #
    # headers = {
    #     'Content-Type': 'application/json'
    # }
    #
    # # Параметры для аутентификации, возможно, потребуется использовать сертификат
    # # cert = ('path/to/client.pem', 'path/to/client_key.pem')
    #
    # response = requests.get(url, headers=headers, verify=False)  # cert=cert - если используется сертификат
    #
    # if response.status_code == 200:
    #     script = response.text
    #     print("Скрипт приложения:")
    #     print(script)
    #
    #     # Сохранение скрипта в файл, если это необходимо
    #     with open('app_script.qvs', 'w') as file:
    #         file.write(script)
    #         print("Скрипт сохранен в файл 'app_script.qvs'")
    # else:
    #     print("Ошибка получения скрипта приложения. Статус ответа:", response.status_code)

    # config = {
    #     'host': 'qlik.tattelecom.ru',
    #     'prefix': '/',
    #     'port': 443,
    #     'isSecure': False
    # }
    # app_id = "0417f8ed-6869-42ac-a6ee-540cceb19b40"
    #
    # xrf_key = str(uuid.uuid4())
    #
    # app_url = f"https://{config['host']}:{config['port']}"
    # response = requests.get(app_url, headers={'x-qlik-xrfkey': xrf_key}, verify=False)
    # print(app_url)
    #
    # # Вывод текста ответа от сервера для анализа
    # print(response.json)

    # Инициализация браузера
    # o = Options()
    # o.add_experimental_option("detach", True)
    # driver = webdriver.Chrome(options=o)
    #
    # # Загрузка страницы
    # driver.get("https://qlik.tattelecom.ru/ttk/qmc/")
    #
    # # Ожидание загрузки страницы
    # time.sleep(1)
    #
    # # Вводим логин
    # pyautogui.write(r'tattelecom\qlikdevelop')
    # pyautogui.press('tab')
    # time.sleep(0.5)
    #
    # # Вводим пароль
    # pyautogui.write('q*4rt8kN%y')
    # pyautogui.press('enter')
    #
    # # Подождать загрузки следующей страницы
    # time.sleep(1)
    #
    # # Находим и нажимаем на ссылку "Engines"
    # try:
    #     engines_link = driver.find_element(By.XPATH,
    #                                        "//a[@class='qmc-primary-navigation-item-link'][contains(@href, './engines')]//div[contains(@class, 'qmc-primary-navigation-item-label')]/span[text()='Engines']")
    #     if engines_link:
    #         engines_link.click()
    #         print("Ссылка 'Engines' успешно нажата.")
    #     else:
    #         print("Ссылка 'Engines' не найдена.")
    # except Exception as e:
    #     print(f"Ошибка при попытке нажать на ссылку 'Engines': {e}")
    #
    # # Подождать загрузки следующей страницы
    # time.sleep(1)
    #
    # # Словарь для хранения данных об узлах
    # nodes_data = {}
    # page_source = driver.page_source
    #
    # print(page_source)

    # Извлекаем строки из таблицы
    # rows = table.find_elements(By.TAG_NAME, "tr")
    #
    # # Словарь для хранения данных о статусе узлов
    # status_data = {}
    #
    # for row in rows:
    #     # Находим ячейку со статусом, которая находится во второй колонке каждой строки
    #     status_cell = row.find_element(By.XPATH, ".//td[2]//div[@class='qmc-cell-icon']")
    #     if status_cell:
    #         # Извлекаем текст статуса
    #         status_text = status_cell.text.strip()
    #
    #         # Добавляем статус в словарь, используя ID строки в качестве ключа
    #         status_data[row.get_attribute('id')] = status_text
    #
    # print(status_data)


    # from selenium import webdriver
    # from selenium.webdriver.common.by import By
    # import time
    #
    # # Инициализация браузера
    # driver = webdriver.Chrome()  # Укажите путь к драйверу, если необходимо
    #
    # # Загрузка страницы
    # driver.get("https://qlik.tattelecom.ru")
    #
    # # Ожидание загрузки страницы
    # time.sleep(2)

    # Найти и ввести логин
    # username_input = driver.find_element(By.NAME, "Имя пользователя")
    # username_input.send_keys("tattelecom\qlikdevelop")
    #
    # # Найти и ввести пароль
    # password_input = driver.find_element(By.NAME, "Пароль")
    # password_input.send_keys("q*4rt8kN%y")

    # Нажать кнопку для входа
    # login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    # login_button.click()

    # Подождать загрузки следующей страницы
    # time.sleep(2)
    #
    # # Считываем информацию со страницы
    # data = driver.find_element(By.CSS_SELECTOR, "selector_for_data").text
    # print(data)
    #
    # # Изменяем URL-адрес и считываем новую информацию
    # driver.get("new_url")
    # time.sleep(2)
    # new_data = driver.find_element(By.CSS_SELECTOR, "selector_for_new_data").text
    # print(new_data)
    #
    # # Закрыть браузер
    # driver.quit()

    #////////////////////////////////////////////////////////
    # import requests
    #
    # url = "https://qlik.tattelecom.ru/qrs/task"
    # response = requests.get(url, verify=False)
    #
    # if response.status_code == 200:
    #     print(response.text)  # Вывод содержимого ответа для анализа
    #     try:
    #         json_data = response.json()
    #         print(json_data)
    #     except ValueError as e:
    #         print(f"Error decoding JSON: {e}")
    # else:
    #     print(f"Error: Unable to fetch data. Status code: {response.status_code}")


    # import requests
    # import json
    #
    # # Логин и пароль для авторизации
    # username = "tattelecom\\qlikdevelop"
    # password = "q*4rt8kN%y"
    #
    # # URL для страницы авторизации
    # login_url = "https://qlik.tattelecom.ru/internal_windows_authentication/?targetId=bfbee3d6-bae0-472b-a10c-969c07b67628"
    #
    # # Создание сессии для хранения cookies
    # session = requests.Session()
    #
    # # Отправка POST запроса с логином и паролем на страницу авторизации
    # response = session.post(login_url, data={"username": username, "password": password}, verify=False)
    #
    # if response.status_code == 200:
    #     # URL для получения JSON данных
    #     data_url = "https://qlik.tattelecom.ru/api/v1/apps/43ce28ec-a6a2-43bd-9250-786a35bd9198/data/lineage?qlikTicket=rETanRJ3noXYt3Pk"
    #
    #     # GET запрос для получения JSON данных после успешной авторизации
    #     response_data = session.get(data_url, verify=False)
    #
    #     if response_data.status_code == 200:
    #         try:
    #             json_data = response_data.json()
    #             print(json_data)
    #         except json.decoder.JSONDecodeError as e:
    #             print(f"Error decoding JSON: {e}")
    #     else:
    #         print(f"Error retrieving data. Status code: {response_data.status_code}")
    # else:
    #     print(f"Authentication error. Status code: {response.status_code}")
    # api_url = 'https://qlik.tattelecom.ru:5432/qrs/about'
    # api_url = 'https://qlik.tattelecom.ru:5432/api/v1/apps'
    # data = await fetch_data_from_api(api_url)
    # response_message = f"Data: {data}"
    # await message.reply(response_message)
