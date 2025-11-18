import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URL тура РПЛ на Спортэкспрессе (подстроить под актуальный тур)
URL = "https://www.sport-express.ru/football/russia/premier-league/calendar/"

def get_matches():
    response = requests.get(URL)
    if response.status_code != 200:
        print("Не удалось загрузить страницу")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    matches = []

    # Пример, структура сайта может меняться, проверить через inspect
    rows = soup.select('.matches-table__row')
    for row in rows:
        date_el = row.select_one('.matches-table__date')
        home_el = row.select_one('.matches-table__home')
        away_el = row.select_one('.matches-table__away')
        time_el = row.select_one('.matches-table__time')

        if not date_el or not home_el or not away_el or not time_el:
            continue

        date_str = date_el.text.strip()
        home = home_el.text.strip()
        away = away_el.text.strip()
        time_str = time_el.text.strip()

        try:
            # Преобразуем в ISO формат
            dt_obj = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
            iso_date = dt_obj.isoformat()
            matches.append({"date": iso_date, "home": home, "away": away})
        except Exception as e:
            print(f"Ошибка парсинга: {e}")
            continue

    return matches

if __name__ == "__main__":
    data = get_matches()
    with open("matches.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{len(data)} матчей сохранено в matches.json")
