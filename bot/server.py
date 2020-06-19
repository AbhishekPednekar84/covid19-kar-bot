import requests
from kar_covid_bot import TelegramBot
from functools import reduce

# Create the bot
bot = TelegramBot()


def make_reply(msg, name):
    reply = None
    name = name if name else "there"

    if msg in ["/karcovid", "/karcorona"]:
        reply = get_kar_stats()
    elif msg == "/start":
        reply = f"Hi {name}! 👋. Use the /karcovid or /karcorona commands for the latest COVID 19 counts from Karnataka."
    else:
        reply = "Oops! I don't recognize that command 😕. Try using /karcovid or /karcorona."
    return reply


def get_dist_data():
    r = requests.get("https://api.covid19india.org/v2/state_district_wise.json")

    for item in r.json():
        if item["state"] == "Karnataka":
            dist_data = item["districtData"]

    return dist_data


def get_deltas():
    dist_data = get_dist_data()

    deltas = [dist_data[j]["delta"] for j in range(len(dist_data))]

    confirmed_delta = reduce(lambda x, y: x + y["confirmed"], deltas, 0)
    recovered_delta = reduce(lambda x, y: x + y["recovered"], deltas, 0)
    deceased_delta = reduce(lambda x, y: x + y["deceased"], deltas, 0)

    return {"confirmed": confirmed_delta,
            "recovered": recovered_delta,
            "deceased": deceased_delta}


def get_kar_stats():
    dist_cases = []
    dist_item = ""

    r = requests.get("https://api.covid19india.org/v3/data.json")
    kar_total = r.json()["KA"]["total"]

    delta_info = get_deltas()

    dist_counts = get_dist_data()
    

    for count in range(len(dist_counts)):
        if dist_counts[count]['district'] != "Unknown" and dist_counts[count]['district'] != "Other State":
            dist_cases.append(f"\n👉  <strong>{dist_counts[count]['district']}</strong> ❗ C: {dist_counts[count]['confirmed']} ❗ R: {dist_counts[count]['recovered']} ❗ D: {dist_counts[count]['deceased']}")

    for item in dist_cases:
        dist_item += item    

    return f"📊 <strong><u>Current COVID 19 Counts for Karnataka</u></strong>: \
                \n\n🔸 Confirmed:  <strong>{kar_total['confirmed']}</strong>  [↑ {delta_info['confirmed']}] \
                \n🔸 Recovered:  <strong>{kar_total['recovered']}</strong>  [↑ {delta_info['recovered']}] \
                \n🔸 Deceased:  <strong>{kar_total['deceased']}</strong>  [↑ {delta_info['deceased']}] \
                \n🔸 Tested:  <strong>{kar_total['tested']}</strong> \
                \n\n\n🔢 <strong><u>District-wise Counts</u></strong> (<strong>C</strong>onfirmed - <strong>R</strong>ecovered - <strong>D</strong>eceased): \
                \n{dist_item} \
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

                #If the message is edited, the "message" key changes
                if "message" in item.keys():
                    message = str(item["message"]["text"])
                    name = item["message"]["from"]["first_name"]
                    from_user = item["message"]["from"]["id"]
                    reply = make_reply(message, name)

                elif "edited_message" in item.keys():
                    edited_message = str(item["edited_message"]["text"])
                    name = item["edited_message"]["from"]["first_name"]
                    from_user = item["edited_message"]["from"]["id"]
                    reply = make_reply(edited_message, name)

                bot.send_message(reply, from_user)


if __name__ == "__main__":
    main()
