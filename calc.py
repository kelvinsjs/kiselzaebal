import math
import random

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def total_distance(route):
    return sum(distance(route[i]['coordinate'], route[i + 1]['coordinate']) for i in range(len(route) - 1))

def two_opt(points, iterations=2):
    def greedy_route(start_point, points):
        route = [start_point]
        unvisited_points = points.copy()
        unvisited_points.remove(start_point)

        while unvisited_points:
            nearest_point = min(unvisited_points, key=lambda i: distance(route[-1]['coordinate'], i['coordinate']))
            route.append(nearest_point)
            unvisited_points.remove(nearest_point)
        
        return route

    def two_opt_swap(route, i, k):
        return route[:i] + route[i:k + 1][::-1] + route[k + 1:]

    def optimize_route(route):
        improved = True
        while improved:
            improved = False
            for i in range(1, len(route) - 1):
                for k in range(i + 1, len(route)):
                    new_route = two_opt_swap(route, i, k)
                    if total_distance(new_route) < total_distance(route):
                        route = new_route
                        improved = True
        return route

    best_route = None
    best_distance = float('inf')

    for _ in range(iterations):
        start_point = random.choice(points)
        initial_route = greedy_route(start_point, points)
        optimized_route = optimize_route(initial_route)

        current_distance = total_distance(optimized_route)
        if current_distance < best_distance:
            best_distance = current_distance
            best_route = optimized_route

    return best_route
