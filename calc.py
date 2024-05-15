import math
import random
import requests
from bs4 import BeautifulSoup

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def two_opt(points, iterations=100):
    # Создаем начальный маршрут
    route = list(range(len(points)))
    random.shuffle(route)

    # Выполняем указанное количество итераций
    for i in range(iterations):
        # Выбираем случайные два ребра маршрута
        edge1 = random.randint(0, len(route) - 1)
        edge2 = random.randint(0, len(route) - 1)

        # Проверяем, не пересекаются ли эти ребра
        if (edge1 + 1) % len(route) == edge2 or (edge2 + 1) % len(route) == edge1:
            continue

        # Вычисляем координаты точек, соответствующих этим ребрам
        p1 = points[route[edge1]]['coordinate']
        p2 = points[route[(edge1 + 1) % len(route)]]['coordinate']
        p3 = points[route[edge2]]['coordinate']
        p4 = points[route[(edge2 + 1) % len(route)]]['coordinate']

        # Вычисляем расстояния между этими точками
        d1 = distance(p1, p2)
        d2 = distance(p3, p4)
        d3 = distance(p1, p3)
        d4 = distance(p2, p4)

        # Проверяем, не улучшится ли маршрут при перестановке этих ребер
        if d3 + d4 < d1 + d2:
            # Переставляем ребра
            if edge1 < edge2:
                route[edge1 + 1:edge2 + 1] = route[edge2:edge1:-1]
            else:
                route[edge2 + 1:edge1 + 1] = route[edge1:edge2:-1]

    # Возвращаем полученный маршрут
    return [points[i] for i in route]

# postamats = [
#     '26960',
#     '3023',
#     '25859',
#     '45444',
#     '26773'
# ]

# coordinates = []

# for number in postamats:
#     url = f'http://new-post.orilider.com/Kyivska_region/Kyiv_city/packstation_{number}.shtml'
#     response = requests.get(url)

#     if response.status_code == 200:
#         html_code = response.text
#         soup = BeautifulSoup(html_code, 'html.parser')

#         meta_latitude = soup.find('meta', {'itemprop': 'latitude'})
#         meta_longitude = soup.find('meta', {'itemprop': 'longitude'})

#         latitude = float(meta_latitude['content']) if meta_latitude else None
#         longitude = float(meta_longitude['content']) if meta_longitude else None

#         if latitude and longitude:
#             coordinates.append({
#                 'number': number,
#                 'latitude': latitude,
#                 'longitude': longitude
#             })
#         else:
#             print(f'Failed to get coordinates for postamat {number}')
#     else:
#         print(f'Failed to get the page for postamat {number}. Status code: {response.status_code}')

# # Формируем список координат почтоматов
# points = [{'number': coordinate['number'], 'coordinate': (coordinate['latitude'], coordinate['longitude'])} for coordinate in coordinates]


# # Получаем кратчайший маршрут
# route = two_opt(points)

# # Выводим результат

