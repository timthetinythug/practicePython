map0 = ["..+..++", "++.B..+", ".....++", "++.....", ".T....+"]


class Node:

    def __init__(self, navigable, grid_x, grid_y):
        self.navigable = navigable
        self.grid_x = grid_x
        self.grid_y = grid_y

map = []
width = 7

def map_maker(lomap):
    for i in range(width):
        x_map = []
        counter_y = 0
        for k in lomap:
            x = list(k).pop(i)
            if x == "+":
                x = Node(False, i, counter_y)
            else:
                x = Node(True, i, counter_y)
            x_map.append(x)
            counter_y += 1
        map.append(x_map)

map_maker(map0)
print(map[1][1].navigable == True)
