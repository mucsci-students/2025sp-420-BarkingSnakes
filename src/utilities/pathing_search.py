# filename: pathing_search.py
# Authors: Juliana Vinluan, Steven Barnes
# Date: 2025-04-25
# Description: Pathing algorithms to find an optimal path between two points
# while avoiding obstacles.
from __future__ import annotations
import heapq
import math

PVAL = int
P_X = PVAL
P_Y = PVAL
POINT = tuple[P_X, P_Y]
GRID = list[list[PVAL]]
PATH = list[POINT]
F_SCORE = PVAL
G_SCORE = PVAL
DIRECTION  = tuple[P_X, P_Y, str]
ASTAR_DATA = tuple[F_SCORE, G_SCORE, P_X, P_Y, DIRECTION, PATH]

class AStar:
    """A* search by Juliana Vinluan, appended by Steven Barnes."""
    DIRECTIONS:list[DIRECTION] = [
        (-1, 0, 'up'),
        (1, 0, 'down'),
        (0, -1, 'left'),
        (0, 1, 'right')
    ]

    def __init__(self, grid:GRID, start_positions:list[POINT], goal_positions:list[POINT]):
        """"""
        self.grid = grid
        self.start_positions = start_positions
        self.goal_positions = goal_positions
        self.heuristic = self.g_manhattan
    
    def g_manhattan(self, a:POINT, b:POINT):
        # Manhattan distance
        x1, y1 = a
        x2, y2 = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star(self, grid:GRID, start:POINT, goal:POINT) -> PATH:
        # print("Start A*", start, goal)
        rows, cols = len(grid), len(grid[0])
        s_x, s_y = start
        heap:list[ASTAR_DATA] = []
        heapq.heappush(heap, (0, 0, s_x, s_y, None, []))  # (f_score, g_score, x, y, direction, path)
        visited = {}
        count = 0

        while heap:
            count += 1
            f, g, x, y, direction, path = heapq.heappop(heap)

            if (x, y) == goal:
                # print("found goal")
                return path + [(x, y)]  # found path

            if (x, y, direction) in visited and visited[(x, y, direction)] <= g:
                # print("continuing")
                continue
            visited[(x, y, direction)] = g

            for dx, dy, new_direction in self.DIRECTIONS:
                nx, ny = x + dx, y + dy
                # print("searching", (nx, ny), (cols, rows))
                # if 0 <= nx < rows and 0 <= ny < cols:
                if 0 <= nx < cols and 0 <= ny < rows:
                    # if grid[nx][ny] == 0 or (nx, ny) == goal:
                    if grid[ny][nx] == 0 or (nx, ny) == goal:
                        # print("adding to path")
                        turn_penalty = 0 if direction == new_direction or direction is None else 5
                        new_g = g + 1 + turn_penalty
                        new_f = new_g + self.heuristic((nx, ny), goal)
                        heapq.heappush(heap, (new_f, new_g, nx, ny, new_direction, path + [(x, y)]))
        # print("End A*", start, goal, count)
        return None  # no path found
    
    def calc_dist(self, p1, p2) -> int:
        x1,y1 = p1
        x2,y2 = p2
        
        math.dist(p1, p2)
        return math.sqrt((x2 - x1)**2 + ())

    def get_optimal_path(self) -> PATH:
        paths:list[PATH] = []
        for start in self.start_positions:
            for goal in self.goal_positions:
                path = self.a_star(self.grid, start, goal)
                if path:
                    paths.append(path)
        
        lowest_turns = float('inf')
        shortest_distance = float('inf')
        best_path = None
        for path in paths:
            dist = math.dist(path[0], path[-1])
            turns = 0
            x1, y1 = path[0]
            x2, y2 = path[1]
            for (x3, y3) in path[2:]:
                if (x1 == x2) and (x2 != x3) :
                    turns += 1
                elif (y1 == y2) and (y2 != y3) :
                    turns += 1
                x1, y1 = x2, y2
                x2, y2 = x3, y3
            lowest_turns = min(lowest_turns, turns)
            if turns == lowest_turns and dist < shortest_distance:
                best_path = path
            
            shortest_distance = min(dist, shortest_distance)
        
        return best_path