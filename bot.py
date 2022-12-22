from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from googletrans import Translator, LANGCODES
import random


app = Flask(__name__)


def gtranslate(tr_text):
    translator = Translator(service_urls=['translate.google.co.in'])
    d = LANGCODES
    l = list(d.items())
    r = random.choice(l)
    lang, lang_cd = r[0], r[1]
    t_text = translator.translate(tr_text, dest=lang_cd).text
    msg = f"_{lang.title()}_\n{t_text}"
    return msg


@app.route('/bot', methods=['POST'])
def bot():
    # add webhook logic here and return a response
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    # msg = resp.message()
    responded = False

    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        # msg.body(quote)``
        msg = resp.message(quote)
        responded = True

    if 'good' in incoming_msg:
        daytime = None
        for dy in ['morning', 'afternoon', 'evening', 'night']:
            if dy in incoming_msg:
                daytime = dy.title()
        if daytime is not None:
            text_ = f"Good {daytime}"
            gm_t = gtranslate(text_)
            # msg.body(gm_t)
            msg = resp.message(gm_t)
            responded = True

    if not responded:
        # msg.body('I only know about famous quotes and cats, sorry!')
        # pass
        msg = resp.message("Nope!")
    return str(resp)


if __name__ == '__main__':
    app.run(port=4000)
