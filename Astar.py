import heapq

class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0

def is_valid(grid, row, col):
    ROW, COL = len(grid), len(grid[0])
    return 0 <= row < ROW and 0 <= col < COL

def is_unblocked(grid, row, col):
    return grid[row][col] == 1

def is_destination(row, col, destination):
    return row == destination[0] and col == destination[1]

def manhattan(row, col, destination):
    return abs(row - destination[0]) + abs(col - destination[1])

def trace_path(cell_details, destination):
    path = []
    row, col = destination

    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        row, col = cell_details[row][col].parent_i, cell_details[row][col].parent_j

    path.append((row, col))
    path.reverse()
    return path

def a_star(grid, start, destination):
    if not is_valid(grid, start[0], start[1]) or not is_valid(grid, destination[0], destination[1]):
        print("Source or destination is invalid")
        return None

    if not is_unblocked(grid, start[0], start[1]) or not is_unblocked(grid, destination[0], destination[1]):
        print("Source or destination is blocked")
        return None

    if is_destination(start[0], start[1], destination):
        return [start]

    ROW, COL = len(grid), len(grid[0])

    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    i, j = start
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    open_list = []
    heapq.heappush(open_list, (0, 0, i, j))  # (f, g, row, col)

    while open_list:
        _, g, i, j = heapq.heappop(open_list)

        if closed_list[i][j]:
            continue
        closed_list[i][j] = True

        for move in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_i, new_j = i + move[0], j + move[1]

            if is_valid(grid, new_i, new_j) and is_unblocked(grid, new_i, new_j):
                if is_destination(new_i, new_j, destination):
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    return trace_path(cell_details, destination)  # Nå returnerer den ruten

                if not closed_list[new_i][new_j]:
                    g_new = g + 1
                    h_new = manhattan(new_i, new_j, destination)
                    f_new = g_new + h_new

                    if cell_details[new_i][new_j].f > f_new:
                        heapq.heappush(open_list, (f_new, g_new, new_i, new_j))
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    print("Failed to find the destination")
    return None

def simplify_path(path):
    simplified_path = [path[0]]  # Startpunktet beholdes
    for i in range(1, len(path) - 1):
        prev_x, prev_y = path[i - 1]
        curr_x, curr_y = path[i]
        next_x, next_y = path[i + 1]

        # Sjekk om punktene ligger på en rett linje (samme x eller samme y)
        if not ((prev_x == curr_x == next_x) or (prev_y == curr_y == next_y)):
            simplified_path.append(path[i])

    simplified_path.append(path[-1])  # Sluttpunktet beholdes
    return simplified_path
