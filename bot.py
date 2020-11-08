from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import os
import time

TOKEN = "1193425272:AAEM41GhNs1wZ7Yn762pK8uSL-J1D9icoY8"
PORT = int(os.environ.get('PORT', 5000))
username = os.environ.get("username")
password = os.environ.get("password")
##url = "https://www.instagram.com/p/CHNKZVdg_Wd/?igshid=g5qmsw600bfd"
##url = "https://www.instagram.com/accounts/login/?next=%2Fp%2FCGr21kOsXM2%2F&source=desktop_nav"
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

print("Started")
def quit(bot,update):
    driver.quit()

def post(bot,update):
    url = update.message.text.replace("/g ","")
    update.message.reply_text("Processing your request, please wait a few seconds.")
    driver.get(url)
    count = 0
    while count<10:
        try:
            driver.find_element_by_xpath("//*[@aria-label='Phone number, username, or email']").send_keys(username)
            driver.find_element_by_xpath("//*[@aria-label='Password']").send_keys(password)
            driver.find_element_by_xpath("//*[@type='submit']").click()
            time.sleep(2)
            driver.find_element_by_xpath("//*[@type='button']").click()
            count = 11
        
        except:
            count+=1
            time.sleep(1)
            
    nameele = driver.find_element_by_xpath("//*[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']")
    name = nameele.text

    img = driver.find_element_by_xpath("//*[@class='FFVAD']").get_attribute("src")
    print(img)
    elelst = driver.find_elements_by_xpath("//*[@class='C4VMK']")
    string = ""
    hass = ""
    for ele in elelst:
        if name in ele.text:
            post = ele.text.split("\n")
            for i in post[1:len(post)-1]:
                if len(i) > 0 and "#" in i[0]:
                    hass = hass + i
                if "#" in i and i[0] != "#":
                    rep = i.split("#")[0]
                    string = string+rep
                    hass = hass + i.replace(rep,"")
                else:
                    string = string+i+"\n"

        else:
            break

    curr = time.localtime()
    day = curr.tm_mday
    month = curr.tm_mon
    year = curr.tm_year

    if day < 10:
        day = "0"+str(day)

    if month < 10:
        month = "0"+str(month)

    msg = f"""{day}.{month}.{year}
@IG_FotografiaItalia
\U0001F30E {string}
\U0001F4F8 Grazie a @{name} per la foto \U0001F609
\U0001F441 Visitate la sua galleria
\U0001F504 È gradito il Repost
__
Per scoprire altri scenari ricchi di fascino, seguite la nostra community @IG_FotografiaItalia
__
Volete anche voi entrare a far parte della nostra gallery?
Utilizzate il nostro hashtag ufficiale #IG_FotografiaItalia
__
Non dimenticatevi di iscrivervi nel gruppo ufficiale su Telegram, trovate il link all’interno del nostro profilo!
__
{hass}"""
    try:
        bot.send_photo(chat_id=update.message.chat_id,photo=img,caption=msg)
    except:

        try:
            bot.send_photo(chat_id=update.message.chat_id,photo=img)
            bot.send_message(chat_id=update.message.chat_id,text=msg)

        except:
            try:
                bot.send_message(chat_id=update.message.chat_id,text=msg)
            except:
                bot.send_message(chat_id=update.message.chat_id,text="ERROR! Post is too long, Telegram is not allowing me to send it.")

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("g", post))
dp.add_handler(CommandHandler("q", quit))
updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
updater.bot.setWebhook('https://igtg.herokuapp.com/' + TOKEN)
updater.idle()
#dp.add_handler(MessageHandler(Filters.text, fix))
##updater.start_polling()
##updater.idle()

