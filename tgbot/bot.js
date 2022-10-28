const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');

const mongo = require("./mongoTools.js");
const config = require('./config.json'); 

const bot = new TelegramBot(config.token, { polling: true });

var ids = {};


mongo.init() // connect to db on startup

var options = {
    reply_markup: JSON.stringify({
      inline_keyboard: [
        [{ text: 'not depressed', callback_data: '1' }],
        [{ text: 'depressed', callback_data: '2' }]        
      ]
    })
  };

bot.onText(/\/echo (.+)/, 
  (msg, match) => 
  {
	  const chatId = msg.chat.id;
	  const resp = match[1];

	  bot.sendMessage(chatId, resp);
  }
)

bot.onText( /\/start/, 
  async (msg, match) => 
  {	
    var document = await mongo.get();
    var newMsg = document.text;
    
    if (newMsg.length > 4096)
      newMsg = newMsg.substring(0,4000)+'...';
      
    bot.sendMessage(msg.chat.id, newMsg, options);

    ids[msg.chat.id] = document;
  }
)
bot.onText( /(.+)/, 
  (msg, match) =>
  { 
    for (comm_idx in comms_list)
    {
        if(comms_list[comm_idx].name.indexOf(msg.text.toLowerCase()) > -1)            
          return;
    }     

    bot.sendMessage(msg.chat.id,"Для начала интеракции отправьте команду /start")
  }
)

bot.on('callback_query', 
  async function onCallbackQuery(callbackQuery) 
  {
    const action = callbackQuery.data;
    const msg = callbackQuery.message;
    
    const opts = {
      chat_id: msg.chat.id,
      message_id: msg.message_id,
    };
    
    try
    {
      var answer = '';
      if (action === '1') 
      { // not sad
        answer = 'not depressed';
        mongo.update(ids[msg.chat.id].id, 0)
      }

      if (action === '2') 
      { //sad
        answer = 'depressed';
        mongo.update(ids[msg.chat.id].id, 1)
      }  
    }
    catch(err)
    {
      bot.sendMessage(msg.chat.id, "Произошла ошибка, начните со /start");  
    }
    
    var divider = new Array(30).join('-');
    bot.editMessageText(`${msg.text}\n\n${divider}\n${answer}`, opts);
    
    //bot.deleteMessage(msg.chat.id, msg.message_id, form={})
    
    var document = await mongo.get();
    var newMsg = document.text;
    
    if (newMsg.length > 4096)
      newMsg = newMsg.substring(0,4000)+'...';
        
    bot.sendMessage(msg.chat.id, newMsg, options);
    
    ids[msg.chat.id] = document;
  }
);

var comms_list = [
  {
      name: ["/start"],      
      about: "Start"
  }
]
