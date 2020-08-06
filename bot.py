from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ChosenInlineResultHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import InlineQueryHandler
from uuid import uuid4
import logging
import random

token=''

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
updater = Updater(token=token, use_context=True)

fakedb={'rate':{},'data':{},'query':''}

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="这是一个评价加速等级的bot")

def report(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="@huoju @gokeeper")

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

def top(update, context):
    if len(fakedb['rate'])==0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="目前还没有新闻，请积极贡献")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="当前新闻量为："+str(len(fakedb['rate']))+", 计算数据中。。。")
        maxid=uuid4()
        maxrate=-10
        for i in fakedb['rate'].keys():
            tmp=fakedb['rate'][i][0]-fakedb['rate'][i][2]
            if tmp > maxrate and i in fakedb['data'].keys():
                maxrate=tmp
                maxid=i
        context.bot.send_message(chat_id=update.effective_chat.id, text="加速次数：{}\n{}".format(fakedb['rate'][maxid][0],fakedb['data'][maxid]))
    



def query(update, context):
    callback_query = update.callback_query
    user = callback_query.from_user
    #print(user.id,user.full_name)
    data = callback_query.data.split("|")
    #print("time",time.time())
    #print(callback_query.data)
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
    #print(message_id)
    ret+="|"+message_id
    fakedb['rate'][message_id]=[int(i) for i in count]
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
    #print(query)
    #print("time",time.time())
    #print(update.inline_query.from_user.full_name)
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
        fakedb['query']=[message_id,q2]
    else:
        return

def onsend(update,context):
    #print(fakedb)
    message_id=str(fakedb['query'][0])
    query=fakedb['query'][1]
    fakedb['rate'][message_id]=[0,0,0]
    fakedb['data'][message_id]=query

inline_caps_handler = InlineQueryHandler(inline_caps)
result_hanlder = ChosenInlineResultHandler(onsend)
dispatcher = updater.dispatcher
dispatcher.add_handler(result_hanlder)
dispatcher.add_handler(inline_caps_handler)
dispatcher.add_handler(CallbackQueryHandler(query))

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('acc', acc))
dispatcher.add_handler(CommandHandler('top', top))
dispatcher.add_handler(CommandHandler('report', report))
updater.start_polling()
updater.idle()