import math
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
from PIL import Image
from calc import two_opt
import json


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_coordinates(texts, filename='new_post_offices.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    coordinates = []

    for text in texts:
        number = text.split()[-1]
        type_text = text.split()[0].lower()

        if "почтомат" in type_text:
            office_type = "Поштомат"
        elif "отделение" in type_text:
            office_type = "Відділення"
        else:
            print(f"Unsupported text type: {text}")
            continue

        office = next((item for item in data if item['number'] == number and item['type'] == office_type), None)
        
        if office:
            latitude = float(office['coordinates']['latitude'])
            longitude = float(office['coordinates']['longitude'])
            coordinates.append({
                'number': number,
                'latitude': latitude,
                'longitude': longitude
            })
        else:
            print(f"Failed to find office for {text}")

    return coordinates

def remove_duplicates(texts):
    unique_texts = list(dict.fromkeys(texts))
    return unique_texts

def text_of_route(route):
    route_text = ''
    for i in range(len(route) - 1):
        route_text += f'{route[i]["number"]} -> {route[i + 1]["number"]}\n'
    route_text += f'{route[-1]["number"]} -> {route[0]["number"]}'
    return route_text

def plot_map(texts, filename):
    # Удаляем дублирующиеся элементы
    texts = remove_duplicates(texts)
    
    # Получаем координаты
    points = [{'number': coordinate['number'], 'coordinate': (coordinate['latitude'], coordinate['longitude'])} for coordinate in get_coordinates(texts)]

    # Получаем кратчайший маршрут
    route = two_opt(points)
    
    # Загрузить картинку с помощью библиотеки PIL
    img = Image.open('brovary.png')

    # Преобразовать изображение в массив
    img_array = np.array(img)

    # Создать проекцию карты
    map_proj = ccrs.PlateCarree()

    # Создать фигуру и осевую сетку
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=map_proj)

    # Установить пределы осей
    ax.set_extent([30.465336, 30.536577, 50.486015, 50.532129], crs=ccrs.PlateCarree())

    # Отобразить изображение на карте
    ax.imshow(img_array, extent=[30.465336, 30.536577, 50.486015, 50.532129], transform=ccrs.PlateCarree())

    # Отметить точки почтоматов на карте с номерами
    for point in points:
        ax.plot(point['coordinate'][1], point['coordinate'][0], 'ro', transform=ccrs.PlateCarree())
        ax.text(point['coordinate'][1], point['coordinate'][0], point['number'], color='black', fontsize=8, ha='right')

    # Нарисовать маршрут
    for i in range(len(route)):
        start = route[i]['coordinate']
        end = route[(i + 1) % len(route)]['coordinate']
        ax.plot([start[1], end[1]], [start[0], end[0]], 'b-', transform=ccrs.PlateCarree())

    plt.savefig(filename)

def plot_map_to_file(texts, filename='map.png'):
    plot_map(texts, filename)


addresses123 = ['Почтомат 5245', 'Почтомат 45553', 'Почтомат 36482', 'Почтомат 25351', 'Почтомат 35220', 'Почтомат 36563']

plot_map_to_file(addresses123)