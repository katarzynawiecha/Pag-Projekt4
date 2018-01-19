from heapq import heappush, heappop
import klasy


def calc_heuristic(vertex, goal):
    return vertex.distance_to(goal)

def get_neighbour(vertex, edge):
    v1 = edge.vertex_from
    v2 = edge.vertex_to
    if vertex == v1:
        return v2
    else:
        return v1

def reconstruct_path(start, goal):
    v = goal
    path = [v]
    while v != start:
        v = v.came_from
        path.append(v)
    return path

def a_star(start, goal, illegal_edges):
    visited_vertexes = set()
    queued_vertexes = [] #zakolejkowane
    queued_set = set()
    start.g_score = 0 #dlugosc optymalnej trasy
    heappush(queued_vertexes, (0, start))
    queued_set.add(start)

    while True:
        try:
            _, v = heappop(queued_vertexes)
        except IndexError:
            break
        if v in visited_vertexes:
            continue
        if v == goal:
            break
        visited_vertexes.add(v)
        for edge in v.edge_out:
            if edge.id_jezdni in illegal_edges:
                continue
            w = get_neighbour(v, edge)
            if w in visited_vertexes:
                continue
            g_score = v.g_score + edge.weight()
            if w not in queued_set:
                w.h_score = calc_heuristic(w, goal)
                w.g_score = g_score
                w.came_from = v
                heappush(queued_vertexes, (w.g_score + w.h_score, w))
                queued_set.add(w)
            elif g_score < w.g_score:
                w.came_from = v
                w.g_score = g_score
                heappush(queued_vertexes, (w.g_score + w.h_score, w))

    return reconstruct_path(start, goal)
