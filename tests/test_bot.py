import os
import requests
import dotenv
import requests_mock
import pytest

import server


dotenv.load_dotenv()

token = os.getenv("TELEGRAM_TOKEN")

def test_telegram_get_updates(requests_mock):
    requests_mock.get(f"https://api.telegram.org/bot{token}/getUpdates", json={"kw": "flask"})
    assert {"kw": "flask"} == requests.get(f"https://api.telegram.org/bot{token}/getUpdates").json()

def test_covid_state_district_wise_api(requests_mock):
    requests_mock.get(f"https://api.covid19india.org/v2/state_district_wise.json", text="Karnataka")
    assert "Karnataka" == requests.get(f"https://api.covid19india.org/v2/state_district_wise.json").text

def test_covid_data_api(requests_mock):
    requests_mock.get(f"https://api.covid19india.org/v3/data.json", text="Karnataka")
    assert "Karnataka" == requests.get(f"https://api.covid19india.org/v3/data.json").text

def test_make_reply():
    result = server.make_reply("test", "test")
    assert result == "Oops! I don't recognize that command 😕. Try using /karcovid or /karcorona."