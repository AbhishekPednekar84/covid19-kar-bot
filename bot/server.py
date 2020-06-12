import requests
from kar_covid_bot import TelegramBot

# Create the bot
bot = TelegramBot()


def make_reply(msg):
    reply = None
    if msg in ["/karcovid", "/karcorona"]:
        reply = get_kar_stats()
    elif msg == "/start":
        reply = "Hi there 👋"
    else:
        reply = "Oops! I don't recognize that command 😕. Try using /karcovid or /karcorona."
    return reply


def get_kar_stats():
    r = requests.get("https://api.covid19india.org/v3/data.json")
    kar_total = r.json()["KA"]["total"]

    return f"📊 <strong>Current COVID 19 stats for Karnataka</strong>: \
                \n\nConfirmed:  <b>{kar_total['confirmed']}</b> \
                \nRecovered:  <b>{kar_total['recovered']}</b> \
                \nDeceased:  <b>{kar_total['deceased']}</b> \
                \nTested:  <b>{kar_total['tested']}</b> \
                \n\nFor more details, check out the <a href='https://kar.covid19-info.website'>Karnataka COVID 19 Tracker</a>."


def main():
    update_id = None
    from_user = None
    reply = None

    while True:
        print("Firing up the bot...")
        updates = bot.get_updates(offset=update_id)
        updates = updates["result"]
        if updates:

            for item in updates:
                update_id = item["update_id"]

                # If the message is edited, the "message" key changes
                try:
                    if item["message"]:
                        message = str(item["message"]["text"])
                        from_user = item["message"]["from"]["id"]
                        reply = make_reply(message)
                    else:
                        edited_message = str(item["edited_message"]["text"])
                        from_user = item["edited_message"]["from"]["id"]
                        reply = make_reply(edited_message)
                except:
                    if item["message"]:
                        message = None
                    else:
                        edited_message = None

                bot.send_message(reply, from_user)


if __name__ == "__main__":
    main()
