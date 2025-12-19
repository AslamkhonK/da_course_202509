import requests
from bs4 import BeautifulSoup


def save_page(url, page_num):

    response = requests.get(f"{url}?page={page_num}")
    response.encoding = "utf-8"
    filename = f"page{page_num}.html"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"Страница {page_num} сохранена как {filename}")


def parse_page(filename):

    with open(filename, "r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, "lxml")

    price_tags = soup.find_all("a", class_="advert__content-price _not-title")
    title_tags = soup.find_all("a", class_="advert__content-title")

    cars = []
    for title_tag, price_tag in zip(title_tags, price_tags):
        parts = title_tag.text.strip().split(", ")
        car_model = parts[0]
        year = parts[1] if len(parts) > 1 else "-"
        price_text = price_tag.text.split("c.")[0].strip().replace(" ", "")
        price = int(price_text) if price_text.isdigit() else None

        cars.append({"Модель": car_model, "Год": year, "Цена (TJS)": price})

    return cars


def create_car_dict(cars):

    return {
        "Модель": [c["Модель"] for c in cars],
        "Год": [c["Год"] for c in cars],
        "Цена автомобиля": [c["Цена (TJS)"] for c in cars if c["Цена (TJS)"] is not None]
    }



url = "https://somon.tj/transport/legkovyie-avtomobili/dushanbe/"
page_num = 20


save_page(url, page_num)


cars = parse_page(f"page{page_num}.html")


car_data = create_car_dict(cars)


print("{:<30} {:<12} {:<10}".format("Модель", "Год", "Цена (TJS)"))
print("-" * 55)
for car in cars:
    print("{:<30} {:<12} {:<10}".format(car["Модель"], car["Год"], car["Цена (TJS)"] or "-"))

print("\n📊 Словарь данных:")
print(car_data)
