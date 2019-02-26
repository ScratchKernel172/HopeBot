import os
import time
import random

# Import selenium modules
from selenium import webdriver

# For Element Selection
from selenium.webdriver.common.by import By

# For Waiting for Elements
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




# For Proxy Grabber
from bs4 import BeautifulSoup
import requests
import lxml



# Data and Variables Here

driver_path = os.environ.get('CHROMEDRIVER_PATH')
binary_path = os.environ.get('GOOGLE_CHROME_BIN')

goorm_email = os.environ.get('G_EMAIL')
goorm_pass = os.environ.get('G_PASS')
goorm_containername = os.environ.get('G_WORK')

bot_token = os.environ.get('BOT_TOKEN')
to_chat = os.environ.get('BOT_CHAT_ID')

driver_UA = """Mozilla/5.0 (Series40; Nokia200/11.56; Profile/MIDP-2.1 Configuration/CLDC-1.1) Gecko/20100401 S40OviBrowser/2.0.1.62.6"""

def send_msg(msgtext):
    parms = {'chat_id': to_chat,'text': msgtext}
    response = requests.post("https://api.telegram.org/bot"+ bot_token + "/" + "sendMessage" , data=parms)
    return response








send_msg("[#] Starting...")

send_msg("[#] Fetching Proxies...")





def adress_proxy():
    target_url = 'https://www.ip-adress.com/proxy-list'
    result = requests.get(target_url)
    soup = BeautifulSoup(result.text, "lxml")
    pars_result = soup.find('tbody').find_all('tr')
    proxy_list = []
    for elem in pars_result:
        elem = elem.get_text().split()[:2]
        if elem[1] != 'transparent':
            proxy_list.append(elem[0])
    return proxy_list

def check_proxy(proxy):
    proxy = 'http://' + proxy
    time.sleep(1)
    try:
        result = requests.get('http://ip-api.com/json', proxies={'http': proxy}, timeout=2)
        if result.status_code == 200:
            try:
                if result.json()['status'] == 'success':
                    return True
            except IndexError:
                return False
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.ReadTimeout:
        return False
    except requests.exceptions.ChunkedEncodingError:
        return False
    except requests.exceptions.TooManyRedirects:
        return False


list = adress_proxy()
working_proxies = []
for proxy in list:
    if check_proxy(proxy)==True:
        working_proxies.append(proxy)

new_proxy = working_proxies[0]

send_msg("[#] Using New Proxy: " + new_proxy)


options = webdriver.ChromeOptions()
options.binary_location = binary_path
options.add_argument('--headless')
options.add_argument('--proxy-server=' + new_proxy)
options.add_argument("--user-agent="+driver_UA)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("--blink-settings=imagesEnabled=false")
#options.add_argument("default_content_settings.images=2")
options.add_argument('--disable-logging')
desired_cap = options.to_capabilities()





send_msg("[#] Loading Page...")
pbrowser = webdriver.Chrome(executable_path=driver_path,desired_capabilities=desired_cap,service_log_path="chromedriver_logs.log")

pbrowser.maximize_window()

pbrowser.get("https://ide.goorm.io/my/")
send_msg("[#] Success... ")
email_field = pbrowser.find_element_by_id("emailInput")
pass_field = pbrowser.find_element_by_id("passwordInput")
submit_btn = pbrowser.find_element_by_css_selector("""._2N5VJFocxBhsyYl-czZIZB""")
send_msg("[#] Filling Up Login Form...")
WebDriverWait(pbrowser, 10).until(EC.element_to_be_clickable((By.ID, "emailInput")))
email_field.send_keys(goorm_email)
WebDriverWait(pbrowser, 10).until(EC.element_to_be_clickable((By.ID, "passwordInput")))
pass_field.send_keys(goorm_pass)
send_msg("[#] Logging In....")

WebDriverWait(pbrowser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "._2N5VJFocxBhsyYl-czZIZB")))
submit_btn.click()



send_msg("[#] Logged In Successfully...")
send_msg("[#] Starting VM...")

pbrowser.get("https://ide-run.goorm.io/terminal/" + goorm_containername)
while not("Terminal" in pbrowser.title):
    time.sleep(25)
    pbrowser.get("https://ide-run.goorm.io/terminal/" + goorm_containername)
send_msg("[#] VM Started Successfully...")
send_msg("[#] Waiting for VM [#]")
while True:
    send_msg("""[>>] Recurring [<<]""")
    time.sleep(10)
    pbrowser.get("https://ide-run.goorm.io/terminal/" + goorm_containername)
