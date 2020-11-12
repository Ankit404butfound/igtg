from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import os
import time
from telegram.utils.helpers import mention_markdown
from telegram import Bot
import threading
import time
import re
import requests

TOKEN = "1193425272:AAEM41GhNs1wZ7Yn762pK8uSL-J1D9icoY8"
user_fields = ["State", "Region", "Province", "City", "Photographic Style"]

mybot = Bot(TOKEN)

interval = [1, 40, 11]
user_with_no_uname = []
id_name = {}

PORT = int(os.environ.get('PORT', 5000))
username = os.environ.get("username")
password = os.environ.get("password")
##url = "https://www.instagram.com/p/CHNKZVdg_Wd/?igshid=g5qmsw600bfd"
##url = "https://www.instagram.com/accounts/login/?next=%2Fp%2FCGr21kOsXM2%2F&source=desktop_nav"
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("user/data/dir=selenium")
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
            driver.get(url)
        
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
                
              
def has_username(chat_id):
    global user_with_no_uname
    try:
        data = mybot.get_chat(chat_id)
        if data["username"] is None:
            return False
        else:
            if chat_id in user_with_no_uname:
                user_with_no_uname.remove(chat_id)
            return True
    except Exception as e:
        print(e)
        return "Not started"

def no_username(group_id,chat_id_lst,name):
    global user_with_no_uname
    
    for inter in interval:
        time.sleep(inter) 
        for i in chat_id_lst:
            has_username(i)
        users =  ", ".join(str(mention_markdown(int(user),id_name[user])) for user in user_with_no_uname)
        print(user_with_no_uname)
        
        if len(user_with_no_uname) > 0:
            if inter==interval[0]:
                mybot.sendMessage(group_id, f"Hello {users} Please add a username or I will have to remove you from the group",parse_mode="Markdown")

            elif inter==interval[1]:
                mybot.sendMessage(group_id, f"Hello {users} last warning for you to add username or I will have to remove you from the group",parse_mode="Markdown")
            
            elif inter == interval[2]:
                for i in chat_id_lst:
                    has_username(i)
                for user in user_with_no_uname:
                    mybot.kickChatMember(group_id,user)
                    user_with_no_uname.remove(user)
        users = ""
     
def start(bot,update):
    code = update.message.text.replace("/start ","")
    


def new_member(bot,update):
    member = update.message.new_chat_members
    for member in update.message.new_chat_members:
        uname = member.username
        memid = member.id
        name = member.first_name
        print(uname)
        print(memid)
        if not uname:
            id_name[memid] = name
            user_with_no_uname.append(memid)
    if len(user_with_no_uname) >= 1:
        threading.Thread(target=lambda:no_username(update.message.chat_id,user_with_no_uname,name)).start()

def form(bot,update):
    update.message.reply_text("*Please copy the following form (including '/f: Qww323df') and fill out the fields and send it in the group*\n\n/f: Qww323df\nState:\nRegion:\nProvince:\nCity:\nPhotographic Style:\n\n_Note: Do not remove_ '/f: Qww323df' or your response will not be recorded.",parse_mode="Markdown")

def update_form(bot,update):
    temp_lst = []
    missing_fields = []
    message = update.message.text.replace("/f","")
    chat_id = update.message.from_user.id
    temp_lst.append(chat_id)
    try:
        for field in user_fields:
            print(field,end=" ")
            info = re.search(f'{field}:(.+)',message).group(1).strip()
            print(info)
            temp_lst.append(info)
            if info == "":
                missing_fields.append(info)
        if len(missing_fields) > 0:
            mis_fld = ", ".join(i for i in user_with_no_uname)
            update.message.reply_text(f"Fields {misfld} are missing")
        
        else:
            status = requests.get("""http://mydatabase.pythonanywhere.com/update?id=%s&data={"state":"%s","region":"%s","province":"%s","city":"%s","photo_style":"%s"}"""%tuple(temp_lst)).text
            print(status)
            if status == "success":
                update.message.reply_text("Your response has been updated")

            elif status == "not_exists":
                update.message.reply_text("You do not already exist in the database, replace '/u' with '/f' in your form and send again")
        
    except Exception as e:
        print(e)
        update.message.reply_text("Your response could not be updated")
        
def empty_lst(bot,update):
    global user_with_no_uname
    user_with_no_uname = []

def get_form(bot,update):
    temp_lst = []
    missing_fields = []
    message = update.message.text.replace("/f","")
    chat_id = update.message.from_user.id
    temp_lst.append(chat_id)
    temp_lst.append(chat_id)
    try:
        for field in user_fields:
            print(field,end=" ")
            info = re.search(f'{field}:(.+)',message).group(1).strip()
            print(info)
            temp_lst.append(info)
            if info == "":
                missing_fields.append(info)
        if len(missing_fields) > 0:
            mis_fld = ", ".join(i for i in user_with_no_uname)
            update.message.reply_text(f"Fields {misfld} are missing")
        
        else:
            status = requests.get("""http://mydatabase.pythonanywhere.com/addinfo?id=%s&data=,"%s":[{"state":"%s","region":"%s","province":"%s","city":"%s","photo_style":"%s"}]"""%tuple(temp_lst)).text
            if status == "success":
                update.message.reply_text("Your response has been recorded")
            elif status == "exists":
                update.message.reply_text("Your response has already been recorded, To update:\n*Please copy the following form (including '/u: Qww323df') and fill out the fields and send it in the group*\n\n/u: Qwrt45df\nState:\nRegion:\nProvince:\nCity:\nPhotographic Style:\n\n_Note: Do not remove_ '/u: Qwrt45df' or your response will not be recorded.",parse_mode="Markdown")
            else:
                update.message.reply_text("Something went wrong")
    except:
        update.message.reply_text("Your response could not be added")

updater = Updater(TOKEN)

updater.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
updater.dispatcher.add_handler(CommandHandler("start",start))
updater.dispatcher.add_handler(CommandHandler("form",form))
updater.dispatcher.add_handler(CommandHandler("f",get_form))
updater.dispatcher.add_handler(CommandHandler("u",update_form))  
updater.dispatcher.add_handler(CommandHandler("empty",empty_lst))  


dp = updater.dispatcher
dp.add_handler(CommandHandler("g", post))
dp.add_handler(CommandHandler("q", quit))
updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
updater.bot.setWebhook('https://igtg.herokuapp.com/' + TOKEN)
updater.idle()
#dp.add_handler(MessageHandler(Filters.text, fix))
##updater.start_polling()
##updater.idle()

