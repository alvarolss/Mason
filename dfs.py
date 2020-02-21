class Mason:
    """Building a system using the signal flow diagram. For now, only SISO systems"""

    def __init__(self, *positional_parameters):
        # The information for each node is stored with the same index in the vectors below
        self.node_names = []  # Vector that holds the names of the diagram nodes. Each name is unique
        self.node_conections = []  # Vector that keeps the connections of this node with other nodes
        self.input = None  # Stores the index of the input node
        self.output = None  # Stores the index of the output node
        # Records the system name
        if len(positional_parameters) > 0:
            self.name = positional_parameters[0]
        else:
            self.name = 'Unamed System'

    def create_node(self, *positional_parameters):
        length = len(positional_parameters)  # Number of function parameters
        # Checks whether the user has passed the node name
        if length > 0:
            if isinstance(positional_parameters[0], int):  # If the name is an integer, it is converted to string
                node_name = str(positional_parameters[0])
            elif not isinstance(positional_parameters[0], str):  # The node name must be a string
                raise TypeError('Node name must be string, ' + str(type(1)) + ' given')
            elif positional_parameters[0] in self.node_names:  # If the name is repeated, returns false
                return False
            else:
                node_name = positional_parameters[0]
        else:
            node_name = len(self.node_names)  # Default name
            while 'node'+str(node_name) in self.node_names:  # Ensures an unprecedented name
                node_name += 1
            node_name = 'node'+str(node_name)  # The name must be a string
        node_index = len(self.node_names)
        self.node_names.append(node_name)
        # creates the node connection vector
        self.node_conections.append([])
        # Checks whether the node is input / output
        try:
            if positional_parameters[1].upper() == 'I':
                self.input = node_index
            if positional_parameters[1].upper() == 'O':
                self.output = node_index
        except IndexError:
            pass
        return node_name

    def set_input(self, node_name):
        index = self.name2index(node_name)
        if index >= 0:
            self.input = index
            return True
        return False

    def get_input(self):
        if self.input is None:
            return None
        else:
            return self.node_names[self.input]

    def set_output(self, node_name):
        index = self.name2index(node_name)
        if index >= 0:
            self.output = index
            return True
        return False

    def get_output(self):
        if self.output is None:
            return None
        else:
            return self.node_names[self.output]

    def connect_node(self, from_name_node, to_name_node, *positional_parameters):
        # It treats the name of the input and output nodes. The system performs an internal conversion between index and name,
        #  so that the user uses only the name and the system uses only the index.
        index_from = self.name2index(from_name_node)
        index_to = self.name2index(to_name_node)
        # Checks whether the two indexes exist
        if index_from < 0 or index_to < 0:
            return False
        # Search for a unique connection id
        # Make the connection. If a gain is not reported, it will be 1
        if len(positional_parameters):
            self.node_conections[index_from].append([index_to, positional_parameters[0]])
        else:
            self.node_conections[index_from].append([index_to, 1])
        return True

    def get_sis_tf(self):
        paths = self.get_paths()
        loops = self.get_loops()
        delta = self.get_delta(loops)
        tf = 0
        for path in paths:
            # Calculates the product of all earnings contained in the path
            path_gain = self.get_loop_gain(path)
            # Create a list of all loops that do not touch this path
            loops_path = list(loops)
            for l in loops:
                if self.touching_loops([path, l]):
                    loops_path.remove(l)
            path_delta = self.get_delta(loops_path)
            tf += path_gain*path_delta
        tf /= delta
        return tf

    # ------------------------------------------------------------------------------------------------------------------
    # Functions for internal use only
    # ------------------------------------------------------------------------------------------------------------------

    def name2index(self, name):
        if isinstance(name, int):  # If the name is an integer, it is converted to a string
            name = str(name)
        if name not in self.node_names:
            return -1
        else:
            return self.node_names.index(name)

    def get_paths(self):
        if self.input is None or self.output is None:
            return []
        # Calls the function that calculates all possible paths
        paths = self.compute_path([self.input], self.output)
        # Remove equal paths
        paths = self.remove_duplicate_loops(paths, True)
        return paths

    def compute_path(self, current_path, end):
        paths = []
        last_node = current_path[len(current_path)-1]  # Get the index of the node to be analyzed
        for connection in self.node_conections[last_node]:
            new_path = list(current_path)
            new_path.append(connection[0])
            if connection[0] == end:
                paths.append(new_path)
            elif connection[0] not in current_path:
                paths += self.compute_path(new_path, end)
        return paths

    def get_loops(self):
        # Calls the function of calculating loops. This function removes the need for handling arguments within the
        # function get_loops_args
        loops = self.compute_loops([self.input], self.output)
        # Remove repeated loops
        loops = self.remove_duplicate_loops(loops)
        return loops

    def compute_loops(self, current_path, end):
        loops = []
        last_node = current_path[len(current_path)-1]  # Get the index of the node to be analyzed
        for connection in self.node_conections[last_node]:
            # Variable description: connection = [target node index, connection gain]
            new_path = list(current_path)
            new_path.append(connection[0])
            if connection[0] in current_path:
                while new_path[0] != connection[0]:
                    new_path.remove(new_path[0])
                loops.append(new_path)
            else:
                loops += self.compute_loops(new_path, end)
        return loops

    def remove_duplicate_loops(self, loops, *positional_parameters):
        # It also works for paths. If it is path, you must enter an optional parameter
        rdl = list(loops)
        i = 0
        j = 1
        while i < len(rdl):
            while j < len(rdl):
                if self.compare_loop(rdl[i], rdl[j], *positional_parameters):
                    remove = rdl[j]
                    rdl.reverse()
                    rdl.remove(remove)
                    rdl.reverse()
                else:
                    j += 1
            i += 1
            j = i + 1
        return rdl

    @staticmethod
    def compare_loop(loop1, loop2, *positional_parameters):
        # Returns True if the loops are the same. Returns False in other cases. Valid for paths
        if len(loop1) < 2 or len(loop1) != len(loop2):
            # It's required at least three elements in the vector to build a loop.
            # If one of the vectors is not a loop, then they are considered to be different loops.
            # If the loops are different sizes, they are certainly different loops
            return False
        loop_1 = list(loop1)
        loop_2 = list(loop2)
        # If no optional parameter is entered, there are two loops. Otherwise, there are two paths
        if not len(positional_parameters):
            loop_1.pop()  # Remove the repeated element from loop 1
            loop_2.pop()  # Remove the repeated element from loop 2
        # If all elements of loop 1 are in loop 2, regardless of order, the loops are the same
        for l1 in loop_1:
            if not loop_2.count(l1):
                return False
        return True

    def get_delta(self, loops):
        delta = 1
        for l in range(1, len(loops)+1):
            delta_l = self.compute_delta_l(loops, [], l)
            delta += delta_l*(-1)**l
            # If for a given l there are no independent meshes, for a higher value of l there will also be no independent meshes
            if not delta_l:
                break
        return delta

    def compute_delta_l(self, pool, selected, l):
        # Recursive function. Removes a loop from the pool, until l = 0. When l = 0, check if the loops have any points in
        # common. If so, returns zero. If not, returns the product of the individual mesh gains.
        # The function ensures that no mesh combination is repeated.
        if l:
            delta_l = 0
            pool_recursive = list(pool)
            l_recursive = l - 1
            while len(pool_recursive):
                selected_recursive = list(selected)
                selected_recursive.append(pool_recursive.pop())
                delta_l += self.compute_delta_l(pool_recursive, selected_recursive, l_recursive)
            return delta_l
        elif not self.touching_loops(selected):
            gains = 1
            for s in selected:
                gains *= self.get_loop_gain(s)
            return gains
        else:
            return 0

    def get_loop_gain(self, loop):
        # It also calculates the gain of a path
        gain = 1
        for i in range(0, len(loop)-1):
            connections = self.node_conections[loop[i]]
            # Sum all gains between the two nodes in question
            connection_gain = 0
            for c in connections:
                if c[0] == loop[i+1]:
                    connection_gain += c[1]
            # Multiplies the gains of each loop/path connection
            gain *= connection_gain
        return gain

    @staticmethod
    def touching_loops(vet_loops):
        # Returns True if any of the meshes passed by the argument touch each other. Returns False for other cases
        # Paths can also be passed in arguments
        if len(vet_loops) < 2:
            # Returns False if there are less than two loops
            return False
        for i in range(0, len(vet_loops)):
            for j in range(i+1, len(vet_loops)):
                for l in vet_loops[i]:
                    if vet_loops[j].count(l):
                        return True
        return False
