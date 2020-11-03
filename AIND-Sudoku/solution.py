
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#diagonal_units = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],['I1','H2','G3','F4','E5','D6','C7','B8','A9']]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist
# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # For each unit
    nakedPairs = []
    for unit in unitlist:
        # Find values of length 2
        #List of Box (A1 etc) where the length of the value is 2 making it possibly a nakedpair
        possiblePair = [box for box in unit if len(values[box]) == 2]
        # If more than 1 length of 2 in a unit
        if len(possiblePair) > 1:
            listOfPossibles = []
            # Append the values into a list - Not efficient but simple
            for box in possiblePair:
                listOfPossibles.append(values[box])
            # If list loses value when turned into a set then must have duplicates
            if len(listOfPossibles) != len(set(listOfPossibles)):
                # Store the pairs for this unit TODO: WHat happens if multiple pairs in 1 unit?
                paired = [x for x in listOfPossibles if listOfPossibles.count(x) > 1]
                numberOfPairs = len(paired)/2
                uniquePairs = []
                # Find the number of unique pairs (And the values)
                for box in possiblePair:
                    searchToken = values[box]
                    if searchToken in paired and searchToken not in uniquePairs:
                        uniquePairs.append(searchToken)
                # Using unique pairs append a list of pairs
                for x in uniquePairs:
                    foundPair = []
                    for box in possiblePair:
                        if values[box] == x:
                            foundPair.append(box)
                    nakedPairs.append(foundPair)

                #print (paired)
                # TODO: RETURN A LIST of all naked pairs in each unit
                #for box in possiblePair:
                    # If the possible pair is in the paired list
                 #   if values[box] in paired:
                   #     nakedPairs.append(box)
                  #      currentPair = values[box]




    # Peer of both twins - I Need: A list of Pairs (Not a list of boxes)
    # With a list of pairs - Get a list of shared peers, Take values away from the shared peers


    #print (nakedPairs)

    # TODO: FOR EACH naked pair, find all its peers and adjust values accordingly
    # A Naked pair that needs to change
    for pair in nakedPairs:
        # Get the actual values each value in the pair
        pairValue1 = values[pair[0]][0]
        pairValue2 = values[pair[0]][1]
        # Peers for the first box
        box1 = peers[pair[0]]
        box2 = peers[pair[1]]
        matching = []
        # Find the peers that match for this pair
        for x in box1:
            if x in box2:
                matching.append(x)
        for box in matching:
            # Value looking at changing
            boxValue = values[box]
            if len(boxValue) > 1 and box not in pair:
                if pairValue1 in boxValue:
                    boxValue = boxValue.replace(pairValue1, "")
            if len(boxValue) > 1 and box not in pair:
                if pairValue2 in boxValue:
                    boxValue = boxValue.replace(pairValue2, "")
            values[box] = boxValue



    return values

"""
    for box in nakedPairs:
        for peer in peers[box]:
            # Value of a box which has a naked pair
            value = values[box]
            peerValue = values[peer]
            # If the first value in the pair is in the peer value remove it (UNLESS it is a naked pair)
            if len(peerValue) > 1:
                if value[0] in peerValue and peer not in nakedPairs:
                    peerValue = peerValue.replace(value[0], "")
            if len(peerValue) > 1:
                # IF the second value in the pair is in the peer value also remove it (Unless it is a naked pair)
                if value[1] in peerValue and peer not in nakedPairs:
                    peerValue = peerValue.replace(value[1], "")
            values[peer] = peerValue
           # print (values[peer])
"""



def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values

def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        #print("eliminate", values)
        values = only_choice(values)
        #print ("Only Choice values",values)
        values = naked_twins(values)
        #print (values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    # If the value is broken stop iterating
    if values == False:
        return False
    # If everything = 1 then it is solved
    if all(len(values[s]) == 1 for s in boxes):
        return values

    # Now we know that there are unknown answers in this iteration

    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # n = Value to be tested
    # s = box being tested


    for value in values[s]:
        aCopy = values.copy()
        aCopy[s] = value
        attempt = search(aCopy)
        if attempt:
            return attempt
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!

    # If you're stuck, see the solution.py tab!



def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    #values = grid
    values = search(values)
    return values


if __name__ == "__main__":
    dad_sudoku_grid = '.......6....5.3.29834.......43....8....4.....7.5.6..1....8.12..42...65..17.3..6..'
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(dad_sudoku_grid))
    #test1 = {"I9": "9", "E6": "4", "A7": "234568", "E4": "2", "G5": "23456789", "D6": "5", "B8": "3456789", "G4": "345678", "F8": "58", "G7": "2345678", "D9": "47", "C8": "3456789", "B9": "124578", "E3": "56", "I5": "2345678", "I7": "1", "F4": "9", "D4": "1", "D5": "36", "I1": "2345678", "G8": "345678", "I8": "345678", "H3": "1234569", "A8": "345689", "E2": "567", "B6": "236789", "D7": "47", "E7": "9", "G9": "24578", "F2": "24", "F5": "37", "G3": "1234569", "F3": "24", "H6": "1236789", "B2": "1234568", "D1": "36", "I3": "23456", "A5": "1", "H5": "23456789", "I4": "345678", "B3": "1234569", "C4": "345678", "C3": "1234569", "A3": "7", "A2": "234568", "G6": "1236789", "A4": "34568", "F1": "1", "G2": "12345678", "A6": "23689", "B4": "345678", "C1": "2345689", "H1": "23456789", "C9": "124578", "E1": "567", "A1": "2345689", "C6": "236789", "B5": "23456789", "C2": "1234568", "D2": "9", "F7": "58", "B7": "2345678", "H7": "2345678", "E5": "678", "H8": "345678", "C5": "23456789", "I6": "23678", "H2": "12345678", "H4": "345678", "E8": "1", "H9": "24578", "C7": "2345678", "I2": "2345678", "A9": "2458", "G1": "23456789", "E9": "3", "F6": "37", "B1": "2345689", "D3": "8", "F9": "6", "D8": "2"}
    #display(test1)
    result = solve(dad_sudoku_grid)
    display(result)
    #print (result)
    #display(dad_sudoku_grid)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
