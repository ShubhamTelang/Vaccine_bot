from telegram.ext import *
import mysql.connector as mcc
import datetime
import time

conn=mcc.connect(host="localhost",user="root",passwd="4444",database="tg_bot")
cursor=conn.cursor()

data={}

stmt = "SHOW TABLES LIKE 'vaccine_details'"
cursor.execute(stmt)
result = cursor.fetchone()
if result:
    print("exists")    
else:
  
    sql="CREATE TABLE vaccine_details (id int NOT NULL AUTO_INCREMENT,name varchar(255),location varchar(255), vacine_date date, vaccine_time varchar(255), is_booked boolean not null default 0, PRIMARY KEY (id))"
    cursor.execute(sql)
    conn.commit()

Token = "5930947072:AAFgAb-xL0ebE2GK84hb3UPy07aJ95VNGRg"

count1 = 0

def response(update):
    global count1
    if count1==0:
        name = str(update.message.text).lower()
        update.message.reply_text('Please enter your location')
        count1 += 1
        return {"name":name}

    elif count1==1:
        location = str(update.message.text).lower()
        update.message.reply_text(' Enter 1 for booking slot \n Enter 2 for viewing slot')
        count1 += 1
        return {"location":location}

    elif count1==2:
        service = str(update.message.text).lower()
        today = datetime.date.today()
        bot_date = f"BOOK DATE FOR VACCINE \n Enter 1 for {today + datetime.timedelta(days=1)} \n Enter 2 for {today + datetime.timedelta(days=2)} \n Enter 3 for {today + datetime.timedelta(days=3)}"
        update.message.reply_text(bot_date)
        count1 += 1
        return {"service":service}

    elif count1==3:
        today = datetime.date.today()
        user_date = str(update.message.text).lower()
        if user_date == "1":
            vaccine_date = today + datetime.timedelta(days=1)
            update.message.reply_text('BOOK TIME FOR VACCINE \n Enter 1 for 11am \n Enter 2 for 2pm \n Enter 3 for 5pm')
            count1 += 1
            return {"vaccine_date":vaccine_date}
        elif user_date == "2":
            vaccine_date = today + datetime.timedelta(days=2)
            
            update.message.reply_text('BOOK TIME FOR VACCINE \n Enter 1 for 11am \n Enter 2 for 2pm \n Enter 3 for 5pm')
            count1 += 1
            return {"vaccine_date":vaccine_date}
        elif user_date == "3":
            vaccine_date = today + datetime.timedelta(days=3) 
            update.message.reply_text('BOOK TIME FOR VACCINE \n Enter 1 for 11am \n Enter 2 for 2pm \n Enter 3 for 5pm')
            count1 += 1
            return {"vaccine_date":vaccine_date}
        else:
            today = datetime.date.today()
            bot_date = f"PLEASE Enter FROM THE OPTIONS BELOW ONLY \n Enter 1 for {today + datetime.timedelta(days=1)} \n Enter 2 for {today + datetime.timedelta(days=2)} \n Enter 3 for {today + datetime.timedelta(days=3)}"
            update.message.reply_text(bot_date)
            vaccine_date = None
            return {"vaccine_date":vaccine_date}
        

    elif count1==4:
        user_time = str(update.message.text).lower()
        if user_time == "1":
            vaccine_time = "11am"
            count1 = 0
            return {"vaccine_time":vaccine_time}
        elif user_time == "2":
            vaccine_time = "2pm"
            
            count1 = 0
            return {"vaccine_time":vaccine_time}
        elif user_time == "3":
            vaccine_time = "5pm"
            
            count1 = 0
            return {"vaccine_time":vaccine_time}
        else:
            update.message.reply_text('PLEASE Enter FROM THE OPTIONS BELOW ONLY \n Enter 1 for 11am \n Enter 2 for 2pm \n Enter 3 for 5pm')
            vaccine_time = None
            print(vaccine_time)
            return {"vaccine_time":vaccine_time}  

print("Bot Started")

def start_command(update, context):
    update.message.reply_text(f"Send \'/book\' or \'/Book\' to start vaccine booking")

def book_command(update, context):
    update.message.reply_text('Please type in Your Name')    
    

def help_command(update, context):
    update.message.reply_text('help')    


def handle_message(update, context):
    text = str(update.message.text).lower() 
    
    y = response(update)  

    data.update(y) 
    data.pop('service', None)
    print(data)
    try:
        if data["vaccine_time"] != None: 
            name = data["name"]
            location = data["location"]
            vaccine_date = data["vaccine_date"]
            vaccine_time = data["vaccine_time"]
            
            sql = f'INSERT INTO vaccine_details (name, location, vacine_date, vaccine_time, is_booked) VALUES (\'{name}\',\'{location}\',\'{vaccine_date}\',\'{vaccine_time}\',True)'
            print(sql)
            cursor.execute(sql)
            conn.commit()

            update.message.reply_text(f"Your vaccine slot has been booked for {vaccine_date} at {vaccine_time} successfully")

            time.sleep(10)
            update.message.reply_text(f"Send \'/book\' or \'/Book\' to book vaccine for another user")
            
            data["vaccine_time"]=None
            print('success')

    except:
        pass    

    
def main():
     
    updater = Updater(Token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("book", book_command))
    dp.add_handler(CommandHandler("Book", book_command))
    dp.add_handler(CommandHandler("help", help_command))

    ot = dp.add_handler(MessageHandler(Filters.text, handle_message))
    print(ot)
    updater.start_polling()    
    updater.idle()

main()    



