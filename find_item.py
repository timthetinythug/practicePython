'''height = 5
width = 7
boat_trace = []
def find_boat(lomap):
    """
#    >>> find_boat(map1)
#    >>> find_boat(map2)
#    >>> find_boat(map3)
#    >>> boat_trace
    [[5, 4], [0, 0], [6, 3]]
    """
    boat_point = []
    boat = False
    counter_y = 0
    counter_x = 0
    while boat == False:
        row = lomap.pop(0)
        lofrow = list(row)
        while boat == False and counter_x < width:
            point = lofrow.pop(0)
            if point == "B":
                boat_point.append(counter_x)
                boat_point.append(counter_y)
                boat = True
            else:
                counter_x += 1
        counter_y += 1
        counter_x = 0
    boat_trace.append(boat_point)
'''

map0 = ["..+..++", "++.B..+", ".....++", "++.....", ".T....+"]
map1 = ["T.+..++", "++....+", ".....++", "++.....", ".....B+"]
map2 = ["B.+..++", "++..T.+", ".....++", "++.....", "......+"]
map3 = ["..+..++", "++....+", "T....++", "++....B", "......B"]

map00 = ["..+..++", "++.B..+", ".....++", "++.....", ".T....+"]
map10 = ["T.+..++", "++....+", ".....++", "++.....", ".....B+"]
map20 = ["B.+..++", "++..T.+", ".....++", "++.....", "......+"]
map30 = ["..+..++", "++....+", "T....++", "++....B", "......B"]


width = 7
height = 5
treasure = []
boat = []

def find_item(lomap, item):
    """
    >>> find_item(map0, "B")
    >>> find_item(map1, "B")
    >>> find_item(map2, "B")
    >>> find_item(map3, "B")
    >>> print(boat)
    [[3, 1], [5, 4], [0, 0], [6, 3]]
    >>> find_item(map00, "T")
    >>> find_item(map10, "T")
    >>> find_item(map20, "T")
    >>> find_item(map30, "T")
    >>> print(treasure)
    [[1, 4], [0, 0], [4, 1], [0, 2]]
    """
    coordinates = []
    found = False
    counter_y = 0
    counter_x = 0
    while found is False:
        row = lomap.pop(0)
        lofrow = list(row)
        while found is False and counter_x < width:
            point = lofrow.pop(0)
            if point == item:
                coordinates.append(counter_x)
                coordinates.append(counter_y)
                found = True
            else:
                counter_x += 1
        counter_y += 1
        counter_x = 0
    if item == "T":
        treasure.append(coordinates)
    else:
        boat.append(coordinates)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
