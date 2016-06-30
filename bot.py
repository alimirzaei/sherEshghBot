#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.

"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

"""

from telegram import Updater
import logging
import MySQLdb
import json
import telegram
from datetime import datetime
import urllib2
import urllib
import time
from threading import Thread
import testPic
from PIL import Image
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

telegram.ReplyKeyboardMarkup

db = MySQLdb.connect("localhost",
                       "root",
                       "database1456",
                       "sher_eshgh",
                       charset='utf8',
                       init_command='SET NAMES UTF8')
                       
cur = db.cursor()

cur.execute("set names utf8;")
db.set_character_set('utf8') 
cur.execute('SET NAMES utf8;') 
cur.execute('SET CHARACTER SET utf8;') 
cur.execute('SET character_set_connection=utf8;')
db.commit();
                         
# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

# Create the EventHandler and pass it your bot's token.
Token = "167654974:AAGT2kRX7fJQCXjfSlx4g_-BKMMIYbNqY4k"
myBot = telegram.Bot(Token)
updater = Updater(Token)

BASE_URL = "https://api.telegram.org/bot{}/".format(Token)
options = [['خوشم اومد'],['ای بدک نیست'],['اصلا حال نکردم'],['بسه رای دادم']];
reply_markup = {'keyboard': options, 'resize_keyboard': True, 'one_time_keyboard': True}
reply_markup = json.dumps(reply_markup)

read_options = [['بعدی'],['بسه دیگه']];
read_reply_markup = {'keyboard': read_options, 'resize_keyboard': True, 'one_time_keyboard': True}
read_reply_markup = json.dumps(read_reply_markup)


# Get the dispatcher to register handlers
dp = updater.dispatcher




# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

    
def help(bot,update):
    bot.sendMessage(update.message.chat_id,"/vote            رای دادن به شعرهای موجود\n/sher             وارد کردن شعر \n/count          تعداد شعرهای موجود\n/read            خواندن اشعار\n/help             راهنمایی\n")


    
def start(bot, update):    
    db.commit()
    firstName = update.message.from_user.first_name;
    lastName = update.message.from_user.last_name;
    userID = update.message.from_user.id;
    userName = update.message.from_user.username;
    statement = "'%ld','%s','%s','%s','%s'"%(userID , userName , firstName.encode('utf-8'),lastName.encode('utf-8'),str(datetime.now()));    
    command = 'INSERT INTO Users(userID, userName, firstName, lastName,time) VALUES ('+statement+');'
   # pdb.set_trace()    
    
    try:
        cur.execute(command)
        db.commit()
    except MySQLdb.Error, e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
            print "MySQL Error: %s" % str(e)
    bot.sendMessage(update.message.chat_id, text='سلام به ادمین کانال شعر عشق خوش آمدید')
    help(bot, update)



def deleteSher(sherID):
    cur.execute('delete from Shers where ID = %d'%sherID )
    db.commit()
    
votedSherID = -1    

def saveVote(bot, update):
    global votedSherID
    dp.removeTelegramMessageHandler(saveVote)    
    text = update.message.text    
    if (text == options[0][0]):
        voteValue=2
    elif(text == options[1][0]):
        voteValue=1
    elif(text == options[2][0]):
        voteValue = 0
    else:
        voteValue=-2
                
    if (voteValue == 1 or voteValue==0 or voteValue == 2):
        
        statement = '\''+str(votedSherID)+'\', \''+str(update.message.from_user.id)+'\',\''+str(voteValue)+'\',\''+str(datetime.now())+'\''
        command = 'INSERT INTO Votes (sherID,personID,vote,time) VALUES (' +statement +');'       
        cur.execute(command)
        db.commit()
        bot.sendMessage(update.message.chat_id,'رای شما ثبت شد.')
       
        cur.execute('select votes,numVisited from NotSentVotes where ID = %d'%votedSherID)
        result = cur.fetchall()
                
        if(100*result[0][0]/(1+2*result[0][1]) < 15 and result[0][1]>3):
            deleteSher(votedSherID)
            bot.sendMessage(update.message.chat_id,'شعر مورد نظر به علت کم بودن محبوبیت حذف گردید')
        vote(bot,update)
            

    elif (text == 'حذف' and update.message.from_user.name == '@Ali_Mirzaei'):
        deleteSher(votedSherID)
        bot.sendMessage(update.message.chat_id,'شعر مورد نظر حذف گردید')
        vote(bot,update)
        
    else:
        votedSherID = -1
        bot.sendMessage(update.message.chat_id,'شما از قسمت رای دهی خارج شدید')
        
            
def vote(bot, update):
    db.commit()
    global votedSherID,cur
    #import pdb
    #pdb.set_trace()
    if(votedSherID == -1):
        bot.sendMessage(update.message.chat_id, text='به قسمت رای دهی به اشعار خوش آمدید')

    cur.execute('CALL PoemHasToVote(%ld)' %update.message.from_user.id)
    result = cur.fetchall()
    cur.close()
    cur = db.cursor() 
    
    if(len(result)==1):
        votedSherID = result[0][0]
        poem = result[0][1] 
        #beyts = poem.split('\n')
        #for m in beyts:
        #    if(len(m)<3):
        #        beyts.remove(m)
        #splitted = poem.split('#')
        #Poems = beyts[0:2]
        #Poet = splitted[-1]
        #out = testPic.getPicture(Poems,Poet)
        #out.save('temp.jpg')
        #myBot.sendPhoto(update.message.chat_id,open('temp.jpg'),'@sher_eshgh')
        #if(len(beyts)>3):
        bot.sendMessage(update.message.chat_id,poem);
        msg= "نظرتون چیه؟"
        params = urllib.urlencode({'chat_id': str(update.message.chat_id),
        'text': msg.encode('utf-8'),
        'reply_markup': reply_markup,
        'disable_web_page_preview': 'true',
        # 'reply_to_message_id': str(message_id),
        })
        urllib2.urlopen(BASE_URL + 'sendMessage', params).read()
        dp.addTelegramMessageHandler(saveVote)
    else:
        bot.sendMessage(update.message.chat_id,'شما به همه ی شعر های موجود رای داده اید');
        
        

def isAllowedToSave(bot,update):
    from datetime import timedelta
    q = "SELECT count(sher) FROM `Shers` WHERE time BETWEEN '%s' AND '%s' AND sender=%ld"%(str(datetime.now()-timedelta(days=1)),str(datetime.now()),update.message.from_user.id)
    cur.execute(q)
    count = cur.fetchall()
    c = int(count[0][0])
    if(c<3):
        return True;
    else:
        return False;
                
        

def saveSher(bot, update):
    dp.removeTelegramMessageHandler(saveSher)
    text = update.message.text
    splitted = text.split('#')
    if(text[0] == '/'):
        a = 5            
    elif(len(splitted) == 2):
        q = "INSERT INTO Shers (sher, sender,poet,time) VALUES ('%s','%ld','%s','%s')" % \
        (text, update.message.from_user.id, splitted[-1].encode('utf8'),str(datetime.now()))    
        try:
            cur.execute(q)
            db.commit()
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)
       
       
        bot.sendMessage(update.message.chat_id, 'شعر شما با موفقیت ذخیره شد')
    else:
        bot.sendMessage(update.message.chat_id, 'فرمت شعر را رعایت ننموده اید. نوشتن نام شاعر با هشتک (#) الزامی است. دوباره دستور /sher را فراخوانی کنید')

        
        
def sher(bot, update):
    db.commit()
    if( isAllowedToSave(bot,update)):
        bot.sendMessage(update.message.chat_id, "لطفا شعر خود را وارد نمایید:")
        dp.addTelegramMessageHandler(saveSher)
    else:
        bot.sendMessage(update.message.chat_id, 'در هر ۲۴ ساعت بیش از سه شعر نمی توانید قرار دهید')
        

    
def count(bot,update):
    db.commit()
    cur.execute('select count(sher) from NotSentShers')
    result = cur.fetchall()
    text = ' در حال حاضر ' + str(result[0][0]) + ' شعر کاندید برای ارسال به کانال شعرعشق موجود است '
    bot.sendMessage(update.message.chat_id,text)
   
readIndex = 1
def readNext(bot,update):
    global readIndex,cur
    dp.removeTelegramMessageHandler(readNext)
    text = update.message.text
    if (text == read_options[0][0]):
        cur.execute('CALL GetPoemForReading(%d)'%readIndex)
        result = cur.fetchall()
        cur.close()
        cur = db.cursor() 
        if(len(result) != 0):
            readIndex = readIndex+1
            text = "\n محبوبیت %d درصد||%d امتیاز از %d رای \n"%(int(result[0][4]*100) ,int(result[0][2]), int(result[0][3]) )
            bot.sendMessage(update.message.chat_id,result[0][1] + text)
            msg = "ادامه میدی؟"
            params = urllib.urlencode({'chat_id': str(update.message.chat_id),
            'text': msg.encode('utf-8'),
            'reply_markup': read_reply_markup,
            'disable_web_page_preview': 'true',
            # 'reply_to_message_id': str(message_id),
            })
            urllib2.urlopen(BASE_URL + 'sendMessage', params).read()
            dp.addTelegramMessageHandler(readNext)    
        else:
            bot.sendMessage(update.message.chat_id,'اشعار تمام شده است')
            
    else:
        bot.sendMessage(update.message.chat_id,'شما از بخش خواندن اشعار خارج شدید')
        dp.removeTelegramMessageHandler(readNext)
        help(bot,update)
         
def read(bot,update):
    global cur,readIndex
    db.commit()
    readIndex=1
    text = ' به بخش خواندن و مشاهده رای ها و فرستنده های اشعار خوش آمدید. شما به ترتیب محبوبیت شعر ها را خواهید خواند'
        
    bot.sendMessage(update.message.chat_id,text)
    
    cur.execute('CALL GetPoemForReading(0)')
    result = cur.fetchall()
    cur.close()
    cur = db.cursor() 
    import pdb
    if(len(result) != 0):
        
        text = "\n محبوبیت %d درصد||%d امتیاز از %d رای \n"%(int(result[0][4]*100) ,int(result[0][2]), int(result[0][3]) )
        bot.sendMessage(update.message.chat_id,result[0][1] + text)
        msg = "ادامه میدی؟"
        params = urllib.urlencode({'chat_id': str(update.message.chat_id),
        'text': msg.encode('utf-8'),
        'reply_markup': read_reply_markup,
        'disable_web_page_preview': 'true',
        # 'reply_to_message_id': str(message_id),
        })
        urllib2.urlopen(BASE_URL + 'sendMessage', params).read()
        
        dp.addTelegramMessageHandler(readNext)
    else:
        bot.sendMessage(update.message.chat_id,'شعری وجود ندارد')
        
        


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))



import glob
from random import randint
def sendSher():
    global cur    
    while(1):
        #allPics = glob.glob('/home/toranado/Pictures/sher_eshgh/*.*')
        #selected = randint(0,len(allPics)-1)
        #pic = allPics[selected]
        cur.execute('CALL GetPoemForReading(0)')
        result = cur.fetchall()
        cur.close()
        cur = db.cursor()
        
        signiture = '\n\n به شعر عشق بپیوندید و یکی از ادمین های کانال باشید \n @sher_eshgh'
        if(len(result)!=0):
            pop = "\n محبوبیت این شعر %d درصد است "%(int(result[0][4]*100) )
            cur.execute("insert into SentShers(sherID,time) Values ('%d','%s')"%(result[0][0],str(datetime.now())))
            db.commit()
            
            poem = result[0][1] 
            #beyts = poem.split('\n')
            #for m in beyts:
            #    if(len(m)<3):
            #        beyts.remove(m)
            #splitted = poem.split('#')
            #Poems = beyts[0:2]
            #Poet = splitted[-1]
            #print Poet
            #import pdb
            #pdb.set_trace()
            #Poet = Poet.replace('ـ',' ')
            
            #Poet = Poet.replace('ـ',' ')
            #out = testPic.getPicture(Poems,Poet)
            #out.save('temp.jpg')
            #myBot.sendPhoto(104729667,open('temp.jpg'),'@sher_eshgh')
            #if(len(beyts)>3):
            myBot.sendMessage(104729667,poem+pop+signiture)
            time.sleep(3600*24*2)

            
            
def main():
    thread = Thread(target = sendSher)
    thread.start()

#    #thread.join()


#    t = threading.Timer(30, sendSher)
#    t.start() 
    
    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("vote", vote)
    dp.addTelegramCommandHandler("sher", sher)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("count", count)
    dp.addTelegramCommandHandler("read", read)
    # on noncommand i.e message - echo the message on Telegram
    # dp.addTelegramMessageHandler(echo)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    

if __name__ == '__main__':
    main()
