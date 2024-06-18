from icecream import ic
import heapq
from PIL import Image, ImageDraw, ImageFont
import re
from functools import partial, reduce
from operator import or_


class Grid:
    def __init__(self, grid):
        self._grid = tuple(tuple(row) for row in grid)
        self._rows = len(grid)
        self._cols = len(grid[0]) if grid else 0

    def __getitem__(self, index):
        row, col = index
        return self._grid[row][col]

    def __setitem__(self, row, col, value):
        new_grid = [list(row) for row in self._grid]
        new_grid[row][col] = value
        return Grid(new_grid)

    def __iter__(self):
        """Iterator over grid positions."""
        for i in range(self._rows):
            for j in range(self._cols):
                yield (i, j)

    def __repr__(self):
        return f"Grid({[list(row) for row in self._grid]})"

    # necessary for using Grid as a dict key
    def __hash__(self):
        return hash(tuple(self[i, j] for (i, j) in iter(self)) + (self.rows, self.cols))

    # looks odd but we'll see why it's necessary later
    def __lt__(self, other):
        return False

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    def set_mul(self, positions, value):
        """Change multiple grid positions."""
        new_grid = [list(row) for row in self._grid]
        for row, col in positions:
            new_grid[row][col] = value
        return Grid(new_grid)

    def is_valid(self, pos):
        """Check if position is on grid."""
        row, col = pos
        return (0 <= row < self._rows) and (0 <= col < self._cols)


easy = "puzzles/easy_5.txt"
medi = "puzzles/medium_5.txt"
hard = "puzzles/hard_5.txt"


def parse_header(header):
    p = re.compile(r"(?P<width>\d{1,2}) by (?P<height>\d{1,2}) -> (?P<mmoves>\d{1,2})")
    if m := re.match(p, header):
        return {k: int(v) for k, v in m.groupdict().items()}


def parse_puzzles(file):
    puzzles = []
    with open(file, "r") as fp:
        while line := fp.readline():
            if line.strip():
                meta = parse_header(line.strip())
                board = []
                for _ in range(meta["height"]):
                    r = list(map(int, iter(fp.readline().strip())))
                    board.append(r)
                puzzles.append(meta | {"board": Grid(board)})
    return puzzles


peasy = parse_puzzles(easy)
pmedi = parse_puzzles(medi)
phard = parse_puzzles(hard)

peb0 = peasy[0]["board"]


color_map = ["red", "yellow", "green", "blue", "orange", "purple"]


def show_puzzle(board, highlight=None, cell_width=40, debug=False):
    width = board.cols
    height = board.rows
    image = Image.new("RGB", (cell_width * width, cell_width * height), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    fnt = ImageFont.truetype("/usr/share/fonts/TTF/FiraCode-Bold.ttf", size=16)
    y0 = 0
    y1 = cell_width
    x0 = 0
    x1 = cell_width
    for i, j in board:
        x0 = cell_width * j
        y0 = cell_width * i
        x1 = cell_width * (j + 1)
        y1 = cell_width * (i + 1)
        if highlight is not None and (i, j) in highlight:
            draw.rectangle(
                [x0, y0, x1, y1],
                fill=color_map[board[i, j]],
                outline="white",
                width=4,
            )
        else:
            draw.rectangle(
                [x0, y0, x1, y1],
                fill=color_map[board[i, j]],
                outline="black",
                width=2,
            )
        if debug:
            draw.text(
                (x0 + cell_width // 2, y0 + cell_width // 2),
                f"{i}, {j}",
                anchor="mm",
                fill=(0, 0, 0, 255),
            )
    return image


def find_neighbours(position, board):
    neighbourhood = [
        (0, -1),
        (-1, 0),
        (+1, 0),
        (0, +1),
    ]
    return set(
        filter(
            lambda x: board.is_valid(x),
            [(i[0] + position[0], i[1] + position[1]) for i in neighbourhood],
        )
    )


def find_cluster_containing(position, board):
    cluster = {position}
    color_matches = lambda p: board[p] == board[position]
    neighbours = find_neighbours(position, board)
    while neighbours:
        n = neighbours.pop()
        if color_matches(n):
            cluster.add(n)
            neighbours |= find_neighbours(n, board) - cluster
    return cluster


def find_cluster_neighbours(cluster, board):
    return (
        set(reduce(or_, map(partial(find_neighbours, board=board), cluster))) - cluster
    )


c1 = find_cluster_containing((7, 9), peb0)
i1 = show_puzzle(peb0, debug=True, highlight=find_cluster_neighbours(c1, peb0))


def move(color, board):
    main_cluster = find_cluster_containing((0, 0), board)
    color = color_map.index(color) if isinstance(color, str) else color
    cluster_neighbours = set()
    for i in main_cluster:
        cluster_neighbours |= find_neighbours(i, board)
    if any([board[i] == color for i in cluster_neighbours]):
        return board.set_mul(main_cluster, color)
    return board


peb00 = move("red", peb0)
i2 = show_puzzle(peb00)


def find_color(c):
    return next(i for i in color_map if i[0] == c)


def play(board):
    while not is_solved(board):
        i = show_puzzle(board)
        i.show()
        choices = [i[0] for i in color_map]
        color = input(f"pick a color {' '.join(choices)}> ")
        if color in choices:
            board = move(board, find_color(color))
        else:
            return board
    return


def find_all_clusters(board):
    positions = set(iter(board))
    while positions:
        pos = positions.pop()
        c = find_cluster_containing(pos, board)
        positions -= c
        yield c


def cluster_count(board):
    main = find_cluster_containing((0, 0), board)
    count = 0
    for c in find_all_clusters(board):
        if c == main:
            continue
        count += 1
    return count


def a_star_solve(initial_board, heuristic=cluster_count):
    open_set = []
    heapq.heappush(open_set, (0, initial_board))
    came_from = {}
    g_score = {initial_board: 0}
    f_score = {initial_board: heuristic(initial_board)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if is_solved(current):
            return reconstruct_path(came_from, current)

        cluster = find_cluster_containing((0, 0), current)
        # valid moves
        maybe_colors = {current[x] for x in find_cluster_neighbours(cluster, current)}
        for next_board in [move(c, current) for c in maybe_colors]:
            tentative_g_score = g_score[current] + 1
            if next_board not in g_score or tentative_g_score < g_score[next_board]:
                came_from[next_board] = current
                g_score[next_board] = tentative_g_score
                f_score[next_board] = tentative_g_score + heuristic(next_board)
                e = (f_score[next_board], next_board)
                if e not in open_set:
                    heapq.heappush(open_set, e)
    return None


def reconstruct_path(came_from, current):
    cluster = find_cluster_containing((0, 0), current)
    color = current[cluster.pop()]
    total_path = [color]
    while current in came_from.keys():
        current = came_from[current]
        cluster = find_cluster_containing((0, 0), current)
        color = current[cluster.pop()]
        total_path.append(color)
    return total_path[::-1][1:]


def is_solved(board):
    return len(set(board[i, j] for (i, j) in board)) == 1
