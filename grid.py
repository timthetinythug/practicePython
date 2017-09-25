"""Assignment 1 - Node and Grid

This module contains the Node and Grid classes.

Your only task here is to implement the methods
where indicated, according to their docstring.
Also complete the missing doctests.
"""

import functools
import sys
from container import PriorityQueue


@functools.total_ordering
class Node:
    """
    Represents a node in the grid. A node can be navigable 
    (that is located in water)
    or it may belong to an obstacle (island).

    === Attributes: ===
    @type navigable: bool
       navigable is true if and only if this node represents a 
       grid element located in the sea
       else navigable is false
    @type grid_x: int
       represents the x-coordinate (counted horizontally, left to right) 
       of the node
    @type grid_y: int
       represents the y-coordinate (counted vertically, top to bottom) 
       of the node
    @type parent: Node
       represents the parent node of the current node in a path
       for example, consider the grid below:
        012345
       0..+T..
       1.++.++
       2..B..+
       the navigable nodes are indicated by dots (.)
       the obstacles (islands) are indicated by pluses (+)
       the boat (indicated by B) is in the node with 
       x-coordinate 2 and y-coordinate 2
       the treasure (indicated by T) is in the node with 
       x-coordinate 3 and y-coordinate 0
       the path from the boat to the treasure if composed of the sequence 
       of nodes with coordinates:
       (2, 2), (3,1), (3, 0)
       the parent of (3, 0) is (3, 1)
       the parent of (3, 1) is (2, 2)
       the parent of (2, 2) is of course None
    @type in_path: bool
       True if and only if the node belongs to the path plotted by A-star 
       path search
       in the example above, in_path is True for nodes with coordinates 
       (2, 2), (3,1), (3, 0)
       and False for all other nodes
    @type gcost: float
       gcost of the node, as described in the handout
       initially, we set it to the largest possible float
    @type hcost: float
       hcost of the node, as described in the handout
       initially, we set it to the largest possible float
    """
    def __init__(self, navigable, grid_x, grid_y):
        """
        Initialize a new node

        @type self: Node
        @type navigable: bool
        @type grid_x: int
        @type grid_y: int
        @rtype: None

        Preconditions: grid_x, grid_y are non-negative

        >>> n = Node(True, 2, 3)
        >>> n.grid_x
        2
        >>> n.grid_y
        3
        >>> n.navigable
        True
        """
        self.navigable = navigable
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.in_path = False
        self.parent = None
        self.gcost = sys.float_info.max
        self.hcost = sys.float_info.max

    def set_gcost(self, gcost):
        """
        Set gcost to a given value

        @type gcost: float
        @rtype: None

        Precondition: gcost is non-negative

        >>> n = Node(True, 1, 2)
        >>> n.set_gcost(12.0)
        >>> n.gcost
        12.0
        """
        self.gcost = gcost

    def set_hcost(self, hcost):
        """
        Set hcost to a given value

        @type hcost: float
        @rtype: None

        Precondition: gcost is non-negative

        >>> n = Node(True, 1, 2)
        >>> n.set_hcost(12.0)
        >>> n.hcost
        12.0
        """
        self.hcost = hcost

    def fcost(self):
        """
        Compute the fcost of this node according to the handout

        @type self: Node
        @rtype: float
        """
        return self.gcost + self.hcost

    def set_parent(self, parent):
        """
        Set the parent to self
        @type self: Node
        @type parent: Node
        @rtype: None
        """
        self.parent = parent

    def distance(self, other):
        """
        Compute the distance from self to other
        @self: Node
        @other: Node
        @rtype: int
        """
        dstx = abs(self.grid_x - other.grid_x)
        dsty = abs(self.grid_y - other.grid_y)
        if dstx > dsty:
            return 14 * dsty + 10 * (dstx - dsty)
        return 14 * dstx + 10 * (dsty - dstx)

    def __eq__(self, other):
        """
        Return True if self equals other, and false otherwise.

        @type self: Node
        @type other: Node
        @rtype: bool
        """
        if type(self) == type(other) and self.navigable == other.navigable and \
            self.grid_x == other.grid_x and self.grid_y == self.grid_y:
            return True
        else:
            return False

    def __lt__(self, other):
        """
        Return True if self less than other, and false otherwise.

        @type self: Node
        @type other: Node
        @rtype: bool
        """
        if self.fcost() < other.fcost():
            return True
        else:
            return False

    def __str__(self):
        """
        Return a string representation.

        @type self: Node
        @rtype: str
        """
        return "{} {} {}".format(self.navigable, self.grid_x, self.grid_y)


class Grid:
    """
    Represents the world where the action of the game takes place.
    You may define helper methods as you see fit.

    === Attributes: ===
    @type width: int
       represents the width of the game map in characters
       the x-coordinate runs along width
       the leftmost node has x-coordinate zero
    @type height: int
       represents the height of the game map in lines
       the y-coordinate runs along height; the topmost
       line contains nodes with y-coordinate 0
    @type map: List[List[Node]]
       map[x][y] is a Node with x-coordinate equal to x
       running from 0 to width-1
       and y-coordinate running from 0 to height-1
    @type treasure: Node
       a navigable node in the map, the location of the treasure
    @type boat: Node
       a navigable node in the map, the current location of the boat

    === Representation invariants ===
    - width and height are positive integers
    - map has dimensions width, height
    """

    def __init__(self, file_path, text_grid=None):
        """
        If text_grid is None, initialize a new Grid assuming file_path
        contains pathname to a text file with the following format:
        ..+..++
        ++.B..+
        .....++
        ++.....
        .T....+
        where a dot indicates a navigable Node, a plus indicates a
        non-navigable Node, B indicates the boat, and T the treasure.
        The width of this grid is 7 and height is 5.
        If text_grid is not None, it should be a list of strings
        representing a Grid. One string element of the list represents
        one row of the Grid. For example the grid above, should be
        stored in text_grid as follows:
        ["..+..++", "++.B..+", ".....++", "++.....", ".T....+"]

        @type file_path: str
           - a file pathname. See the above for the file format.
           - it should be ignored if text_grid is not None.
           - the file specified by file_path should exists, so there
             is no need for error handling
           Please call open_grid to open the file
        @type text_grid: List[str]
        @rtype: None
        """
        if file_path == "":
            self.text_grid = text_grid
        else:
            final_list = []
            file = open(file_path)
            for line in file.read().splitlines():
                if line != "":
                    final_list.append(line)
                    self.text_grid = final_list
        self.width = len(text_grid[0])
        self.height = len(text_grid)

        empty_map = []
        for i in range(self.width):
            x_map = []
            counter_y = 0
            for k in text_grid:
                z = list(k)
                x = z[i]
                if x == "+":
                    node = Node(False, i, counter_y)
                else:
                    node = Node(True, i, counter_y)
                x_map.append(node)
                counter_y += 1
            empty_map.append(x_map)
        self.map = empty_map

        found_tresure = False
        found_boat = False
        counter_y = 0
        counter_x = 0

        while found_tresure is False or found_boat is False:
            row = text_grid[counter_y]
            lofrow = list(row)
            while (found_tresure is False or found_boat is False) and counter_x < \
                    self.width:
                point = lofrow[counter_x]
                if point == "T":
                    self.treasure = Node(True, counter_x, counter_y)
                    found_tresure = True
                    counter_x += 1
                elif point == "B":
                    self.boat = Node(True, counter_x, counter_y)
                    found_boat = True
                    counter_x += 1
                else:
                    counter_x += 1
            counter_y += 1
            counter_x = 0

    @classmethod
    def open_grid(cls, file_path):
        """
        @rtype TextIOWrapper: 
        """
        return open(file_path)

    def __str__(self):
        """
        Return a string representation.

        @type self: Grid
        @rtype: str

        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> print(g)
        B.++
        .+..
        ...T
        """
        final = ""
        for text in self.text_grid:
            final += str(text) + "\n"
        return final.rstrip()

    def move_helper(self, x, y):
        a = self.boat.grid_x
        a_ = a + x
        b = self.boat.grid_y
        b_ = b - y
        if self.map[a_][b_].navigable is True \
                and self.width >= a_ >= 0 \
                and self.height >= b_ >= 0:
            self.boat = Node(True, a_, b_)
            row = self.text_grid[b]
            row = list(row)
            other_row = self.text_grid[b_]
            other_row = list(other_row)
            other_row[a_], row[a] = row[a], other_row[a_]
            new_row = "".join(row)
            new_other_row = "".join(other_row)
            self.text_grid[b] = new_row
            self.text_grid[b_] = new_other_row
        else:
            raise ValueError("sorry m8, path cannot be manuevered")

    def move(self, direction):
        """
        Move the boat in a specific direction, if the node
        corresponding to the direction is navigable
        Else do nothing

        @type self: Grid
        @type direction: str
        @rtype: None

        direction may be one of the following:
        N, S, E, W, NW, NE, SW, SE
        (north, south, ...)
        123
        4B5
        678
        1=NW, 2=N, 3=NE, 4=W, 5=E, 6=SW, 7=S, 8=SE
        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> g.move("S")
        >>> print(g)
        ..++
        B+..
        ...T
        """
        if direction == "NW":
            self.move_helper(-1, 1)
        elif direction == "N":
            self.move_helper(0, 1)
        elif direction == "NE":
            self.move_helper(1, 1)
        elif direction == "W":
            self.move_helper(-1, 0)
        elif direction == "E":
            self.move_helper(1, 0)
        elif direction == "SW":
            self.move_helper(-1, -1)
        elif direction == "S":
            self.move_helper(0, -1)
        elif direction == "SE":
            self.move_helper(1, -1)

    def neighbourhood(self, node):
        """
        lists each neighbouring node of current node
        """
        a = node.grid_x
        b = node.grid_y
        community = []
        for x in [-1, 0, 1]:
            a_ = a + x
            for y in [-1, 0, 1]:
                b_ = b - y
                if x == 0 and y == 0:
                    pass
                elif a_ >= 0 and a_ < self.width and b_ >= 0 and b_ < self.height:
                    neighbour = self.map[a_][b_]
                    community.append(neighbour)
                else:
                    pass
        return community

    def find_path(self, start_node, target_node):
        """
        Implement the A-star path search algorithm
        If you will add a new node to the path, don't forget to set the parent.
        You can find an example in the docstring of Node class
        Please note the shortest path between two nodes may not be unique.
        However all of them have same length!

        @type self: Grid
        @type start_node: Node
           The starting node of the path
        @type target_node: Node
           The target node of the path
        @rtype: None
        """
        open_list = []
        closed_list = []
        start_node.set_gcost(0)
        start_node.set_hcost(0)
        open_list.append(start_node)
        treasure = False

        while treasure is False:
            current_node = open_list[0]
            for i in open_list:
                if (i.fcost() < current_node.fcost()) or (i.fcost() == current_node.fcost() and i.hcost < current_node.hcost):
                    current_node = i
                else:
                    pass
            closed_list.append(current_node)
            open_list.remove(current_node)

            if current_node == target_node:
                treasure = True
                target_node.parent = current_node.parent
            else:
                for neighbour in self.neighbourhood(current_node):
                    if (neighbour.navigable is False) or (neighbour in closed_list):
                        pass
                    else:
                        moving_fee = current_node.gcost + current_node.distance(neighbour)
                        if moving_fee < neighbour.gcost or neighbour in closed_list:
                            neighbour.gcost = moving_fee
                            neighbour.hcost = current_node.distance(neighbour)
                            neighbour.parent = current_node
                            if neighbour not in open_list:
                                open_list.append(neighbour)
                            else:
                                pass
                        else:
                            pass

    def retrace_path(self, start_node, target_node):
        """
        Return a list of Nodes, starting from start_node,
        ending at target_node, tracing the parent
        Namely, start from target_node, and add its parent
        to the list. Keep going until you reach the start_node.
        If the chain breaks before reaching the start_node,
        return and empty list.

        @type self: Grid
        @type start_node: Node
        @type target_node: Node
        @rtype: list[Node]
        """
        empty_path = []
        current_node = target_node

        while current_node != start_node:
            empty_path.append(current_node)
            current_node = current_node.parent
        empty_path.reverse()
        return empty_path

    def get_treasure(self, s_range):
        """
        Return treasure node if it is located at a distance s_range or
        less from the boat, else return None
        @type s_range: int
        @rtype: Node, None
        """
        if self.boat.distance(self.treasure) < s_range:
            return self.treasure
        else:
            return None

    def plot_path(self, start_node, target_node):
        """
        Return a string representation of the grid map,
        plotting the shortest path from start_node to target_node
        computed by find_path using "*" characters to show the path
        @type self: Grid
        @type start_node: Node
        @type target_node: Node["B.++", ".+..", "...T"]
        @rtype: str
        >>> g = Grid("", ["B.++", ".+..", "...T"])
        >>> print(g.plot_path(g.boat, g.treasure))
        B*++
        .+*.
        ...T
        """
        self.find_path(self.boat, self.treasure)
        traced_path = self.retrace_path(self.boat, self.treasure)
        traced_path.pop()
        for i in traced_path:
            x = i.grid_x
            y = i.grid_y
            a = self.boat.grid_x
            b = self.boat.grid_y
            a_ = a + x
            b_ = b + y
            other_row = self.text_grid[b_]
            other_row = list(other_row)
            other_row[a_] = "*"
            new_other_row = "".join(other_row)
            self.text_grid[b_] = new_other_row
        return self

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config='pylintrc.txt')
