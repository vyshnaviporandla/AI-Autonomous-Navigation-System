import heapq


def heuristic(a, b):
    """Manhattan distance, suitable for four-direction grid movement."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    """Find a shortest four-direction path. Return [start, ..., goal], or []."""
    rows, cols = len(grid), len(grid[0])
    for node in (start, goal):
        x, y = node
        if not (0 <= x < cols and 0 <= y < rows) or grid[y][x] != 0:
            return []

    frontier = [(heuristic(start, goal), 0, start)]
    came_from = {}
    cost_so_far = {start: 0}
    counter = 0

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return list(reversed(path))

        x, y = current
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for nxt in neighbors:
            nx, ny = nxt
            if not (0 <= nx < cols and 0 <= ny < rows):
                continue
            if grid[ny][nx] == 1:
                continue

            new_cost = cost_so_far[current] + 1
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                came_from[nxt] = current
                counter += 1
                priority = new_cost + heuristic(nxt, goal)
                heapq.heappush(frontier, (priority, counter, nxt))

    return []
