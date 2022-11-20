from logging import Filter
from re import A
import string
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import *
import json
import logging


#token
Token = "5529993642:AAFJkMvsan_Iusk14f7JwmUTcb1AlkcqSWw"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
user_anno = 0

ANNO, MATERIA, INFORMAZIONI = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inizia la conversazione e chiede all'utente che anno frequenta."""
    reply_keyboard = [["Primo", "Secondo", "Terzo"]]

    await update.message.reply_text(
        "Benvenuto! Io sono il Bot che ti permette di prenotare il posto a Lezione."
        "Invia /cancel per smettere di parlare con me.\n\n"
        "Che anno frequenti?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Primo, Secondo o Terzo ?"
        ),
    )
    return ANNO


async def anno(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """" Chiede all'utente quale materia vuole prenotare """
    global user_anno
    user = update.message.from_user
    logger.info("Anno di corso di %s: %s", user.full_name, update.message.text)
    testo = update.message.text.lower()
    
    f = open('tabelle.json')
    data = json.load(f)

    if  "primo" in testo :
        user_anno = 1
        reply_keyboard = [["Analisi Matematica 1", "Matematica Discreta 1", "Programmazione 1", "Logica e Reti Logiche"]]
        await update.message.reply_text(
            "Fai il Primo Anno."
            "Scegli la materia che vuoi seguire.",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Analisi Matematica,Matematica Discreta,Programmazione 1,Logica e Reti Logiche"
            ),
        )
        for i in data['orario_1']:
            await update.message.reply_text(json.dumps(i, indent=4))

    if "secondo" in testo:
        user_anno = 2
        reply_keyboard = [["Algoritmi e Strutture Dati", "Calcolo delle Probabilita'","Calcolo Numerico"]]
        await update.message.reply_text(
            "Fai il Secondo Anno."
            "Scegli la materia che vuoi seguire.",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Algoritmi e Strutture Dati,Calcolo delle Probabilita', Calcolo Numerico"
            ),
        )
        for i in data['orario_2']:
            await update.message.reply_text(json.dumps(i, indent=4))

    if "terzo" in testo:
        user_anno = 3
        reply_keyboard = [["Archittetura Reti", "Base di Dati"]]
        await update.message.reply_text(
            "Fai il Terzo Anno."
            "Scegli la materia che vuoi seguire.",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Archittetura Reti,Base di Dati"
            ),
        ) 
        for i in data['orario_3']:
            await update.message.reply_text(json.dumps(i, indent=4))

    
    return MATERIA


async def prenotazione(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """"" Qui verra' salvata la prenotazione dell'utente per la materia scelta """
    user = update.message.from_user
    logger.info("%s vuole prenotare: %s",user.full_name, update.message.text)
    user_materia = update.message.text
    
    with open('tabelle.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    if user_anno == 1:
        for i in data["orario_1"]:
            if user_materia in i["Nome"]:
                if i["posti"] > 0 :
                    await update.message.reply_text("C'e' ancora posto...")
                    i["posti"] = i["posti"]-1
                    break
                else:
                    await update.message.reply_text("Non ci sono posti disponibili ...\nRiprova settimana prossima per questa materia o prenotane un'altra.")
                    return
    
    if user_anno == 2:
        for i in data["orario_2"]:
            if user_materia in i["Nome"]:
                if i["posti"] > 0 :
                    await update.message.reply_text("C'e' ancora posto...")
                    i["posti"] = i["posti"]-1
                    break
                else:
                    await update.message.reply_text("Non ci sono posti disponibili ...\nRiprova settimana prossima per questa materia o prenotane un'altra.")
                    return

    if user_anno == 3:
        for i in data["orario_3"]:
            if user_materia in i["Nome"]:
                if i["posti"] > 0 :
                    await update.message.reply_text("C'e' ancora posto...")
                    i["posti"] = i["posti"]-1
                    break
                else:
                    await update.message.reply_text("Non ci sono posti disponibili ...\nRiprova settimana prossima per questa materia o prenotane un'altra.")
                    return

    lunghezza = len ( data[user_materia])
    for pos in range(lunghezza): 
        if "vuoto" in data[user_materia][pos]["Nome"]:
            await update.message.reply_text("Hai prenotto il tuo posto in aula.\n\nAprendo la KEYBOARD delle materie potrai prenotare un'altra materia.")
            data[user_materia][pos]["Nome"] = user.full_name
            data[user_materia][pos]["posto"] = pos + 1 
            with open('tabelle.json', 'w', encoding='utf-8') as g:
                json.dump(data, g, ensure_ascii=False, indent=4)
            file = open(user_materia,"a")
            file.write(user.full_name + "   " +  str(user.id) +  '\n')
            file.close()
            break
        elif user.full_name in data[user_materia][pos]["Nome"]:
            await update.message.reply_text("Hai gia prenotato il tuo posto in aula per questa materia.")
            break
    
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancella la conversazione."""
    user = update.message.from_user
    logger.info("Utente: %s ha cancellato la conversazione.", user.first_name)
    await update.message.reply_text(
    "Bye! Ci sentiamo un altro giorno.", reply_markup=ReplyKeyboardRemove()
    )

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(Token).build()
    
    application.add_handler(ConversationHandler( entry_points=[CommandHandler("start", start)],
        states={
            ANNO: [MessageHandler(filters.Regex("^(Primo|Secondo|Terzo)$"), anno)], 
            MATERIA: [MessageHandler(filters.Regex("^(Analisi Matematica 1|Matematica Discreta 1|Programmazione 1|Logica e Reti Logiche|Algoritmi e Strutture Dati|Calcolo delle Probabilita'|Calcolo Numerico|Archittetura Reti|Base di Dati)$"), prenotazione)],
        }, 
        fallbacks=[CommandHandler('cancel', cancel)]))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
