from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackQueryHandler, ChosenInlineResultHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import InlineQueryHandler
from telegram.ext.filters import Filters
from telegram.ext.dispatcher import run_async
#from telegram.constants import MARKDOWN_V2
from uuid import uuid4
import logging
from datetime import datetime
import random
import sqlite3
import os
import requests


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
updater = Updater(token='YOUR_TOKEN_HERE', use_context=True)

querydata=['','']
flag=['特朗普','特没谱','奥巴马']
if not os.path.exists('data.db'):
    with sqlite3.connect('data.db') as conn:
        conn.execute('create table data (id varchar(20) primary key, url verchar(20), voteup int, votedown int, voteno int, posttime timestamp)',[])
        conn.commit()

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="这是一个评价加速等级的bot")

def report(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="ADMIN_HERE")


def acc(update,context):
    stickerset=context.bot.get_sticker_set(name="UPINTHEAIR").stickers
    ids=['CAACAgEAAxUAAV8Y1_mQ7xmszCJW6fltxNffFPPzAAJvAAP5BdMCZ_A5kDalAX4aBA',
    'CAACAgEAAxUAAV8Y1_kzSYg8yqM69zJiMSJ3OEMNAAJ9AAP5BdMCOOD4LVAcE8gaBA',
    'CAACAgEAAxUAAV8Y1_m0T440xcsxM9seSMtmQ1-RAAJ_AAP5BdMCG9cpUFhkOcQaBA',
    'CAACAgEAAxUAAV8Y1_kODIawUF8I1dnfNeZcWd0GAAJwAAP5BdMCumTFzdZJj-YaBA',
    'CAACAgEAAxUAAV8Y1_meVaKdMiE9qxAm2rexiFhjAAJxAAP5BdMCKa8a7B5-0CsaBA',
    'CAACAgEAAxUAAV8Y1_k-55B7UrbgKZd-1hI18Es9AAJ7AAP5BdMCe3aIUGck9FIaBA']
    '''for i in stickerset:
        if i.emoji in ['🚗','🚄','🚀','🚙','🏎','⚓️']:
            context.bot.send_message(chat_id=update.effective_chat.id, text=i.emoji+i.file_id)'''
    idx = random.randint(0, 200) % len(ids)
    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=ids[idx])

def lick(update,context):
    print(context.args)
    print(update.message.reply_to_message)
    if len(context.args)>0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="{}舔了一下{}".format(update.message.from_user.full_name,context.args[0]))
    elif update.message.reply_to_message:
        context.bot.send_message(chat_id=update.effective_chat.id, text="{}舔了一下{}".format(update.message.from_user.full_name,update.message.reply_to_message.from_user.full_name))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="{}舔了一下{}".format(update.message.from_user.full_name,"空气"))

def top(update, context):
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("select * from data")
        data=cursor.fetchall()
        cursor.execute("SELECT url, max(voteup), posttime from data")
        top=cursor.fetchall()
        cursor.close()

    if len(data)==0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="目前还没有新闻，请积极贡献")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="当前新闻量为：{}, 计算数据中。。。".format(len(data)))
        context.bot.send_message(chat_id=update.effective_chat.id, text="加速次数：{}\n提交日期：{}\n{}".format(top[0][1],top[0][2],top[0][0]))
def topbrake(update, context):
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("select * from data")
        data=cursor.fetchall()
        cursor.execute("SELECT url, max(votedown), posttime from data")
        top=cursor.fetchall()
        cursor.close()

    if len(data)==0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="目前还没有新闻，请积极贡献")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="当前新闻量为：{}, 计算数据中。。。".format(len(data)))
        context.bot.send_message(chat_id=update.effective_chat.id, text="减速次数：{}\n提交日期：{}\n{}".format(top[0][1],top[0][2],top[0][0]))
    
def topweek(update, context):
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("select * from data")
        data=cursor.fetchall()
        cursor.execute("select url,max(voteup),posttime from data where posttime>=(select datetime('now','-7 day'))")
        top=cursor.fetchall()
        cursor.close()
    if len(data)==0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="目前还没有新闻，请积极贡献")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="当前新闻量为：{}, 计算数据中。。。".format(len(data)))
        context.bot.send_message(chat_id=update.effective_chat.id, text="加速次数：{}\n提交日期：{}\n{}".format(top[0][1],top[0][2],top[0][0]))

def tops(date_range):
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("select * from data")
        data=cursor.fetchall()
        cursor.execute("select url,max(voteup),posttime from data where posttime>=(select datetime('now','{}'))".format(date_range))
        top=cursor.fetchall()
        cursor.close()
    return data,top

def toptoday(update, context):
    data,top=tops('-1 day')
    if len(data)==0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="目前还没有新闻，请积极贡献")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="当前新闻量为：{}, 计算数据中。。。".format(len(data)))
        context.bot.send_message(chat_id=update.effective_chat.id, text="加速次数：{}\n提交日期：{}\n{}".format(top[0][1],top[0][2],top[0][0]))


def topmonth(update, context):
    data,top=tops('-1 month')
    if len(data)==0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="目前还没有新闻，请积极贡献")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="当前新闻量为：{}, 计算数据中。。。".format(len(data)))
        context.bot.send_message(chat_id=update.effective_chat.id, text="加速次数：{}\n提交日期：{}\n{}".format(top[0][1],top[0][2],top[0][0]))

def topyear(update, context):
    data,top=tops('-1 year')
    if len(data)==0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="目前还没有新闻，请积极贡献")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="当前新闻量为：{}, 计算数据中。。。".format(len(data)))
        context.bot.send_message(chat_id=update.effective_chat.id, text="加速次数：{}\n提交日期：{}\n{}".format(top[0][1],top[0][2],top[0][0]))


def query(update, context):
    callback_query = update.callback_query
    user = callback_query.from_user
    print(user.id,user.full_name)
    data = callback_query.data.split("|")
    #print("time",time.time())
    print(callback_query.data)
    count = data[2].split(",")
    count[int(data[1])] = str(int(count[int(data[1])])+1)
    text = ["⏩", "⏸", "⏪"]
    for i in range(3):
        if count[i]!="0":
            text[i] += " ("+count[i]+")"
    ret = ",".join(count)
    if len(data)==4:
        message_id=data[3]     
    else:
        message_id=uuid4().hex
    print(message_id)
    ret+="|"+message_id
    sqlupdate('update data set voteup=?, voteno=?, votedown=? where id=?',[int(i) for i in count]+[message_id])
    message = callback_query.message
    callback_query.answer(
        text="你觉得这个"+data[0], show_alert=True,
    )
    keyboard = [
        [InlineKeyboardButton(
            text[0], callback_data="加速了！|0|"+ret
        ),
        InlineKeyboardButton(
            text[1], callback_data="速度不太行|1|"+ret
        ),
        InlineKeyboardButton(
            text[2], callback_data="减速了|2|"+ret
        )]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    callback_query.edit_message_reply_markup(
        reply_markup=markup
    )


def inline_caps(update, context):
    message_id=uuid4().hex
    query = update.inline_query.query
    q2 = "#acc "+query
    print(query)
    #print("time",time.time())
    print(update.inline_query.from_user.full_name)
    #print(message_id)
    results = list()
    keyboard = [
        [InlineKeyboardButton(
            "⏩",callback_data="加速了！|0|0,0,0|"+str(message_id)
        ),
        InlineKeyboardButton(
            "⏸", callback_data="速度不太行|1|0,0,0|"+str(message_id)
        ),
        InlineKeyboardButton(
            "⏪", callback_data="减速了|2|0,0,0|"+str(message_id)
        )]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    results.append(
        InlineQueryResultArticle(
            id=message_id,
            title="开始评价",
            description="开搞开搞",
            input_message_content=InputTextMessageContent(q2),
            reply_markup=markup
        )
    )
    if query:
        context.bot.answer_inline_query(update.inline_query.id, results, cache_time=5)
        querydata[0]=message_id
        querydata[1]=q2
    else:
        return

def onsend(update,context):
    message_id=str(querydata[0])
    url=querydata[1]
    sqlupdate('insert into data (id, url, voteup, votedown, voteno, posttime) values (?, ?, 0, 0, 0, ?)', [message_id, url, datetime.now()])

def sqlupdate(command,data):
    with sqlite3.connect('data.db',detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        cursor = conn.cursor()
        cursor.execute(command,data)
        cursor.close()
        conn.commit()

def tests(update, context):
    if update.message.from_user.id == 47384057:
        #context.bot.delete_message(chat_id=-1001289980771, message_id=202693)
        buttons = [
            [
                InlineKeyboardButton(
                    "测试一下",
                    callback_data=f"checkin",
                )
            ]
        ]
        context.bot.send_message(chat_id=update.effective_chat.id,
            text = "测试一下，点一下", 
            reply_markup=InlineKeyboardMarkup(buttons)
        )

def checkin(update, context):
    print(update.callback_query.from_user)
    update.callback_query.answer(
            text="ok了，成功了", show_alert=True,
        )



def msg(update, context):
    print(update.message)
    print(update.edited_message)
    message = update.message
    chat = message.chat
    for user in message.new_chat_members:
        if user.is_bot:
            continue
        buttons = [
            [
                InlineKeyboardButton(
                    t,
                    callback_data=f"challenge|{user.id}|{t}",
                )
            ]
            for t in flag
        ]
        buttons.append(
            [
                InlineKeyboardButton(
                    '拜登',
                    callback_data=f"challenge|{user.id}|{'拜登'}",
                )
            ]
        )
        question_message = message.reply_text(
            "您好，我是本群的加速小助手。请在30秒内选择美国现任总统的名字", 
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        context.job_queue.run_once(
            kick_queue,
            30,
            context={"chat_id": chat.id, "user_id": user.id,},
            name=f"{chat.id}|{user.id}|kick",
        )
        context.job_queue.run_once(
            clean_queue,
            30,
            context={
                "chat_id": chat.id,
                "user_id": user.id,
                "message_id": message.message_id,
            },
            name=f"{chat.id}|{user.id}|clean_join",
        )
        context.job_queue.run_once(
            clean_queue,
            30,
            context={
                "chat_id": chat.id,
                "user_id": user.id,
                "message_id": question_message.message_id,
            },
            name=f"{chat.id}|{user.id}|clean_question",
        )

@run_async
def kick_queue(context):
    job = context.job
    kick(context, job.context.get("chat_id"), job.context.get("user_id"))

def kick(context, chat_id, user_id):
    if context.bot.kick_chat_member(
        chat_id=chat_id,
        user_id=user_id,
    ):
        #logger.info(f"Job kick: Successfully kicked user {user_id} at group {chat_id}")
        return True
    else:
        '''logger.warning(
            f"Job kick: No enough permissions to kick user {user_id} at group {chat_id}"
        )'''
        return False

@run_async
def clean_queue(context):
    job = context.job

    def clean(context, chat_id, user_id, message_id):
        if context.bot.delete_message(chat_id=chat_id, message_id=message_id):
            '''logger.info(
                f"Job clean: Successfully delete message {message_id} from {user_id} at group {chat_id}"
            )'''
            return True
        else:
            '''logger.warning(
                f"Job clean: No enough permissions to delete message {message_id} from {user_id} at group {chat_id}"
            )'''
            return False

    clean(
        context,
        job.context.get("chat_id"),
        job.context.get("user_id"),
        job.context.get("message_id"),
    )
@run_async
def query2(update, context):
    callback_query = update.callback_query
    user = callback_query.from_user
    message = callback_query.message
    chat = message.chat
    data = callback_query.data.split('|')
    print(data)
    user_id = int(data[1])
    result = data[2] == '拜登'
    if user.id != user_id:
        callback_query.answer(
            text="没问你，别瞎点", show_alert=True,
        )
        return
    cqconf = "恭喜你回答正确" if result else "答错了，拜拜"
    callback_query.answer(
        text=cqconf, show_alert=False if result else True,
    )
    if result:
        conf = "恭喜你回答正确，欢迎来到马车热爱者群"
        for job in context.job_queue.get_jobs_by_name(
            f"{chat.id}|{user.id}|clean_join"
        ):
            job.schedule_removal()
        for job in context.job_queue.get_jobs_by_name(f"{chat.id}|{user.id}|kick"):
            job.schedule_removal()
    else:
        if kick(context, chat.id, user_id):
            conf = "他永远的离开了我们"
        else:
            conf = "踢人失败，请求管理员手动处理 @huoju @gokeeper"
    message.edit_text(conf)
    for job in context.job_queue.get_jobs_by_name(f"{chat.id}|{user.id}|kick"):
        job.schedule_removal()


def check(update, context):
    if update.message.reply_to_message:
        ori = update.message.reply_to_message
        #print(ori)
        if len(ori.photo) > 0:
            #print(ori.photo)
            #print(ori.photo[-1].get_file().file_path)
            path = ori.photo[-1].get_file().file_path
            print(ori.photo[-1].get_file().file_path)
            r = requests.post("http://localhost:9999", data={"url": path})
            if float(r.text) > 0.7:
                context.bot.send_message(chat_id=update.effective_chat.id, text=str(r.text)+" 🔞", reply_to_message_id=update.message.message_id)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=str(r.text)+" ✅", reply_to_message_id=update.message.message_id)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="请回复一条带有图片的消息", reply_to_message_id=update.message.message_id)


msg_hanlder = MessageHandler(~Filters.command, msg)
result_hanlder = ChosenInlineResultHandler(onsend)
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher = updater.dispatcher
dispatcher.add_handler(CallbackQueryHandler(query2, pattern=r"^challenge\|"))
dispatcher.add_handler(CallbackQueryHandler(checkin, pattern=r"^checkin"))
dispatcher.add_handler(msg_hanlder)
dispatcher.add_handler(result_hanlder)
dispatcher.add_handler(inline_caps_handler)
dispatcher.add_handler(CallbackQueryHandler(query))
dispatcher.add_handler(CommandHandler('check', check))
dispatcher.add_handler(CommandHandler('lick', lick))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('acc', acc))
dispatcher.add_handler(CommandHandler('top', top))
dispatcher.add_handler(CommandHandler('topweek', topweek))
dispatcher.add_handler(CommandHandler('topmonth', topmonth))
dispatcher.add_handler(CommandHandler('topyear', topyear))
dispatcher.add_handler(CommandHandler('toptoday', toptoday))
dispatcher.add_handler(CommandHandler('topbrake', topbrake))
dispatcher.add_handler(CommandHandler('report', report))
#dispatcher.add_handler(CommandHandler('test', test))
updater.start_polling()
updater.idle()