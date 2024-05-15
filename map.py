import math
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
from PIL import Image
from calc import two_opt

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_coordinates(texts):
    coordinates = []

    for text in texts:
        number = text.split()[-1]
        if "почтомат" in text.lower():
            url = f'http://new-post.orilider.com/Kyivska_region/Kyiv_city/packstation_{number}.shtml'
        elif "отделение" in text.lower():
            url = f'http://new-post.orilider.com/Kyivska_region/Kyiv_city/office_{number}.shtml'
        else:
            print(f"Unsupported text: {text}")
            continue
        
        response = requests.get(url)

        if response.status_code == 200:
            html_code = response.text
            soup = BeautifulSoup(html_code, 'html.parser')

            meta_latitude = soup.find('meta', {'itemprop': 'latitude'})
            meta_longitude = soup.find('meta', {'itemprop': 'longitude'})

            latitude = float(meta_latitude['content']) if meta_latitude else None
            longitude = float(meta_longitude['content']) if meta_longitude else None

            if latitude and longitude:
                coordinates.append({
                    'number': number,
                    'latitude': latitude,
                    'longitude': longitude
                })
            else:
                print(f'Failed to get coordinates for {text}')
        else:
            print(f'Failed to get the page for {text}. Status code: {response.status_code}')

    return coordinates

def text_of_route(route):
    route_text = ''
    for i in range(len(route) - 1):
        route_text += f'{route[i]["number"]} -> {route[i + 1]["number"]}\n'
    route_text += f'{route[-1]["number"]} -> {route[0]["number"]}'
    return route_text

def plot_map(texts, filename):
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
