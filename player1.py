
import collections
import time

class Pathing:
    def __init__(self):
        self.original_position = None
        self.visited_positions = set()
        self.potion_collected = False

    def put_visited_positions(self, self_position):
        self.visited_positions.add(self_position)

    def get_visited_positions(self):
        return self.visited_positions
    
    def get_original_position(self):
        return self.original_position
    
    def set_original_position(self, original_position):
        self.original_position = original_position
        
    def get_potion_collected(self):
        return self.potion_collected
    
    def set_potion_collected(self, collected):
        self.potion_collected = collected

def no_wallsbetween(start, end, dungeon_map, other_agent_position=None):
    x1, y1 = start
    x2, y2 = end
    
    if x1 == x2:
        for y in range(min(y1, y2) + 1, max(y1, y2)):
            if dungeon_map[y][x1] != 'floor':
                return False
    elif y1 == y2:
        for x in range(min(x1, x2) + 1, max(x1, x2)):
            if dungeon_map[y1][x] != 'floor':
                return False
    else:
        return False

    return True

    
def get_potion(potions, dungeon_map, self_position):
    x, y = self_position

    for potion in potions:
        if no_wallsbetween(self_position, potion, dungeon_map):
            if potion[0] > x:
                return 'D', potion
            elif potion[0] < x:
                return 'A', potion
            elif potion[1] > y:
                return 'S', potion
            elif potion[1] < y:
                return 'W', potion
    return None, None

def get_food_radius(foods, dungeon_map, self_position, radius=2):
    x, y = self_position

    for food in foods:
        if abs(food[0] - x) <= radius and abs(food[1] - y) <= radius:
            if no_wallsbetween(self_position, food, dungeon_map):
                return True
    return False

def get_nearby_food(foods, dungeon_map, self_position, radius=2):
    x, y = self_position

    for food in foods:
        if abs(food[0] - x) <= radius and abs(food[1] - y) <= radius:
            if no_wallsbetween(self_position, food, dungeon_map):
                if food[0] > x:
                    return 'D', food
                elif food[0] < x:
                    return 'A', food
                elif food[1] > y:
                    return 'S', food
                elif food[1] < y:
                    return 'W', food
    return None, None


def find_coin_clusters(coins, center, size=5):
    x_center, y_center = center
    cluster = []
    for x in range(x_center - size // 2, x_center + size // 2 + 1):
        for y in range(y_center - size // 2, y_center + size // 2 + 1):
            if (x, y) in coins:
                cluster.append((x, y))
    return cluster

def bfs_to_target(self_position, target_items, directions, dungeon_map, other_agent_position, visited, coins_set):
    queue = collections.deque([(self_position[0], self_position[1], [])])
    visited.add(self_position)

    while queue:
        cx, cy, path = queue.popleft()
        if (cx, cy) in target_items:
            return path[0] if path else 'I'

        for move, (dx, dy) in directions.items():
            nx, ny = cx + dx, cy + dy

            if (nx, ny) in visited or not (0 <= nx < len(dungeon_map[0]) and 0 <= ny < len(dungeon_map)):
                continue

            if dungeon_map[ny][nx] != 'floor' or (other_agent_position is not None and (nx, ny) == other_agent_position):
                continue

            new_path = path + [move]
            visited.add((nx, ny))
            queue.append((nx, ny, new_path))

            if (nx, ny) in coins_set:
                return new_path[0]

    return None


def player1_logic(coins, potions, foods, dungeon_map, self_position, other_agent_position):
    start_time = time.time()
    directions = {'W': (0, -1), 'A': (-1, 0), 'S': (0, 1), 'D': (1, 0)}
    
    pathing = Pathing()
    if pathing.get_original_position() is None:
        pathing.set_original_position(self_position)
    pathing.put_visited_positions(self_position)

    x, y = self_position

    visited = set(pathing.get_visited_positions())
    visited.add((x, y))

    target_items = set(foods + potions)
    coins_set = set(coins)

    if not pathing.get_potion_collected():
        move, potion = get_potion(potions, dungeon_map, self_position)
        if move is not None:
            if potion == self_position:
                pathing.set_potion_collected(True)
            print("--- %s seconds ---" % (time.time() - start_time))
            return move


        if get_food_radius(foods, dungeon_map, self_position):
            move, food = get_nearby_food(foods, dungeon_map, self_position)
            if move is not None:
                print("--- %s seconds ---" % (time.time() - start_time))
                return move
            if pathing.get_potion_collected():
                move, food = get_nearby_food(foods, dungeon_map, self_position, radius=15)
        if move is not None:
            print("--- %s seconds ---" % (time.time() - start_time))
            return move
        

    max_coins = 0
    best_center = None

    for coin in coins:
        cluster = find_coin_clusters(coins, coin)
        if len(cluster) > max_coins:
            max_coins = len(cluster)
            best_center = coin

    if best_center:
        target_items.update(find_coin_clusters(coins, best_center))

    move = bfs_to_target(self_position, target_items, directions, dungeon_map, other_agent_position, visited, coins_set)
    if move:
        print("--- %s seconds ---" % (time.time() - start_time))
        return move
    print("--- %s seconds ---" % (time.time() - start_time))
    return bfs_to_target(self_position, coins_set, directions, dungeon_map, other_agent_position, visited, coins_set)

        
