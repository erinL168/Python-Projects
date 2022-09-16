


"""CSC108/A08: Fall 2021 -- Assignment 2: voting

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Sophia Huynh, Sadia Sharmin,
Elizabeth Patitsas, Anya Tafliovich.

"""

from typing import List

from constants import (COL_RIDING, COL_VOTER, COL_RANK, COL_RANGE,
                       COL_APPROVAL, APPROVAL_TRUE, APPROVAL_FALSE,
                       SEPARATOR)

# In the following docstrings, 'VoteData' refers to a list of 5
# elements of the following types:
#
# at index COL_RIDING: int         (this is the riding number)
# at index COL_VOTER: int         (this is the voter number)
# at index COL_RANK: List[str]   (this is the rank ballot)
# at index COL_RANGE: List[int]   (this is the range ballot)
# at index COL_APPROVAL: List[bool]  (this is the approval ballot)

###############################################################################
# Task 0: Creating example data
###############################################################################

SAMPLE_DATA_1 = [[0, 1, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [1, 4, 2, 3],
                  [False, True, False, False]],
                 [1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
                  [False, False, True, True]],
                 [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
                  [False, True, False, True]],
                 [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
                  [True, False, True, True]]]
SAMPLE_ORDER_1 = ['CPC', 'GREEN', 'LIBERAL', 'NDP']


SAMPLE_DATA_2 = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [5, 4, 0, 0],
                  [True, True, False, False]],
                 [117, 21, ['GREEN', 'LIBERAL', 'NDP', 'CPC'], [5, 5, 5, 4],
                  [True, True, True, True]],
                 [72, 12, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [5, 1, 1, 0],
                  [True, True, True, False]]]
SAMPLE_ORDER_2 = ['CPC', 'GREEN', 'LIBERAL', 'NDP', 'OTHER']


###############################################################################
# Task 1: Data cleaning
###############################################################################

def str_to_int(num_list: List[str]) -> List[int]:
    """Return int list of num_list by changing each item in num_list into an int
    and serves as a helper function for clean_data

    Pre: Each item in num_list is a string

    >>> str_to_int(['1', '2', '3'])
    [1, 2, 3]
    >>> str_to_int(['0', '2', '34'])
    [0, 2, 34]
    """
    num_final = []

    for item in num_list:
        num_final.append(int(item))
    return num_final



def clean_data(data: List[List[str]]) -> None:
    """Modify data so that the applicable string values are converted to
    their appropriate type, making data of type List['VoteType'].

    Pre: Each item in data is in the format
     at index COL_RIDING: a str that can be converted to an integer (riding)
     at index COL_VOTER: a str that can be converted to an integer (voter ID)
     at index COL_RANK: a SEPARATOR-separated non-empty string (rank ballot)
     at index COL_RANGE: a SEPARATOR-separated non-empty string of ints
                         (range ballot)
     at index COL_APPROVAL: a SEPARATOR-separated non-empty string of
                         APPROVAL_TRUE's and APPROVAL_FALSE's (approval ballot)


    >>> data3 = [['0', '1', 'NDP;Liberal', '1;4', 'NO;YES']]
    >>> expected3 = [[0, 1, ['NDP', 'Liberal'], [1, 4],
    ...             [False, True]]]
    >>> clean_data(data3)
    >>> data3 == expected3
    True
    >>> data2 = [['0', '1', 'NDP;LIBERAL;GREEN;CPC', '1;4;2;3', 'NO;YES;NO;NO'],
    ...             ['1', '2', 'LIBERAL;NDP;GREEN;CPC', '2;1;4;2', 'NO;NO;YES;YES']]
    >>> expected2 = [[0, 1, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [1, 4, 2, 3],
    ...             [False, True, False, False]],
    ...             [1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
    ...             [False, False, True, True]]]
    >>> clean_data(data2)
    >>> data2 == expected2
    True
    """
    length = len(data)

    for i in range(0, length):
        data[i][COL_RIDING] = int(data[i][COL_RIDING])
        data[i][COL_VOTER] = int(data[i][COL_VOTER])

        #COL_RANK(parties) COLUMN
        rank_string = data[i][COL_RANK]
        data[i][COL_RANK] = rank_string.split(SEPARATOR)


        #COL_RANGE (1, 2, 3, 4) COLUMN
        range_string = data[i][COL_RANGE]
        range_l = range_string.split(SEPARATOR)


        data[i][COL_RANGE] = str_to_int(range_l)

        #COL_APPROVAL COLUMN
        approval_string = data[i][COL_APPROVAL]

        approval = approval_string.split(SEPARATOR)

        approval_final = []

        for item in approval:
            if item == APPROVAL_FALSE:
                approval_final.append(False)
            else:
                approval_final.append(True)

        data[i][COL_APPROVAL] = approval_final

    #return data


###############################################################################
# Task 2: Data extraction
###############################################################################

def extract_column(data: List[list], column: int) -> list:
    """Return a list containing only the elements at index column for each
    sublist in data.

    Pre: each sublist of data has an item at index column.

    >>> extract_column([[1, 2, 3], [4, 5, 6]], 2)
    [3, 6]
    >>> extract_column([[1, 0], [1, 0], [1, 2]], 1)
    [0, 0, 2]
    >>> extract_column([[0]], 0)
    [0]

    """
    final = []
    for item in data:
        final.append(item[column])


    return final


def extract_single_ballots(data: List['VoteData']) -> List[str]:
    """Return a list containing only the highest ranked candidate from
    each rank ballot in voting data data.

    Pre: data is a list of valid 'VoteData's
         The rank ballot is at index COL_RANK for each voter.

    >>> extract_single_ballots(SAMPLE_DATA_1)
    ['NDP', 'LIBERAL', 'GREEN', 'LIBERAL']
    >>> extract_single_ballots(SAMPLE_DATA_2)
    ['LIBERAL', 'GREEN', 'NDP']
    >>> extract_single_ballots(SAMPLE_DATA_2)
    ['LIBERAL', 'GREEN', 'NDP']
    """
    final = []
    for item in data:
        final.append(item[COL_RANK][0])

    return final


def get_votes_in_riding(data: List['VoteData'],
                        riding: int) -> List['VoteData']:
    """Return a list containing only voting data for riding riding from
    voting data data.

    Pre: data is a list of valid 'VoteData's

    >>> expected = [[1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
    ...              [False, False, True, True]],
    ...             [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
    ...              [False, True, False, True]],
    ...             [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
    ...              [True, False, True, True]]]
    >>> get_votes_in_riding(SAMPLE_DATA_1, 1) == expected
    True
    >>> exp_2 = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [5, 4, 0, 0],
    ...              [True, True, False, False]],
    ...             [117, 21, ['GREEN', 'LIBERAL', 'NDP', 'CPC'], [5, 5, 5, 4],
    ...              [True, True, True, True]]]
    """

    final = []
    i = 0
    for item in data:
        if item[COL_RIDING] == riding:
            final.append(data[i])
        i += 1
    return final





###############################################################################
# Task 3.1: Plurality Voting System
###############################################################################

def voting_plurality(single_ballots: List[str],
                     party_order: List[str]) -> List[int]:
    """Return the total number of ballots cast for each party in
    single-candidate ballots single_ballots, in the order specified in
    party_order.

    Pre: each item in single_ballots appears in party_order

    >>> voting_plurality(['GREEN', 'GREEN', 'NDP', 'GREEN', 'CPC'],
    ...                  SAMPLE_ORDER_1)
    [1, 3, 0, 1]
    >>> voting_plurality(['NDP', 'GREEN', 'GREEN', 'GREEN'], SAMPLE_ORDER_2)
    [0, 3, 0, 1, 0]
    """
    ballots_list = []

    for party in party_order:
        counter = 0
        for votes in single_ballots:
            if party == votes:
                counter += 1
        ballots_list.append(counter)

    return ballots_list




###############################################################################
# Task 3.2: Approval Voting System
###############################################################################

# Note: even though the only thing we need from party_order in this
# function is its length, we still design all voting functions to
# receive party_order, for consistency and readability.
def voting_approval(approval_ballots: List[List[bool]],
                    party_order: List[str]) -> List[int]:
    """Return the total number of approvals for each party in approval
    ballots approval_ballots, in the order specified in party_order.

    Pre: len of each sublist of approval_ballots is len(party_order)
         the approvals in each ballot are specified in the order of party_order

    >>> voting_approval([[True, True, False, False],
    ...                  [False, False, False, True],
    ...                  [False, True, False, False]], SAMPLE_ORDER_1)
    [1, 2, 0, 1]

    >>> voting_approval([[True, True, False],
    ...                  [False, False, False],
    ...                  [False, True, False]], ['CPC', 'NDP', 'GREEN'])
    [1, 2, 0]
    """
    approval_list = []


    for item in party_order:
        counter = 0
        for ballots in approval_ballots:
            if ballots[party_order.index(item)]:
                counter += 1
        approval_list.append(counter)


    return approval_list



###############################################################################
# Task 3.3: Range Voting System
###############################################################################

def voting_range(range_ballots: List[List[int]],
                 party_order: List[str]) -> List[int]:
    """Return the total score for each party in range ballots
    range_ballots, in the order specified in party_order.

    Pre: len of each sublist of range_ballots is len(party_order)
         the scores in each ballot are specified in the order of party_order

    >>> voting_range([[1, 3, 4, 5], [5, 5, 1, 2], [1, 4, 1, 1]],
    ...              SAMPLE_ORDER_1)
    [7, 12, 6, 8]
    """
    voting_list = []

    for item in party_order:
        counter = 0
        for ballots in range_ballots:
            counter += ballots[party_order.index(item)]
        voting_list.append(counter)
    return voting_list






###############################################################################
# Task 3.4: Borda Count Voting System
###############################################################################
def equiv_items(item1: str, item2: str, value: int)-> int:
    #Work on equiv items doc string
    """Returns the new value of counter, if item1 equivalent to item2, value is
    added to counter, if not equivalent, returns counter, serves as a helper
    function for voting_borda and voting_irv WORK ON THIS**

    Pre: item1 and item2 are both strings, counter and value are both int

    equiv_items('hello', 'hello', 3, 1)
    4
    equiv_items('hello', helo', 3, 1)
    3
    """


    if item1 == item2:
        return value
    return 0


def voting_borda(rank_ballots: List[List[str]],
                 party_order: List[str]) -> List[int]:
    """Return the Borda count for each party in rank ballots rank_ballots,
    in the order specified in party_order.

    Pre: each ballot contains all and only elements of party_order

    >>> voting_borda([['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...               ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
    ...               ['LIBERAL', 'NDP', 'GREEN', 'CPC']], SAMPLE_ORDER_1)
    [4, 4, 8, 2]
    >>> voting_borda([['LIBERAL', 'GREEN', 'CPC', 'NDP','OTHER'],
    ...               ['CPC', 'LIBERAL', 'GREEN', 'NDP','OTHER'],
    ...               ['LIBERAL', 'NDP', 'GREEN', 'CPC','OTHER']],
    ...               SAMPLE_ORDER_2)
    [7, 7, 11, 5, 0]
    """

    borda_list = []
    party = 0
    borda = len(party_order) - 1



    while party < len(party_order):
        borda = len(party_order) - 1
        count = 0
        for i in range(len(party_order)):
            for ballots in rank_ballots:
                row = rank_ballots.index(ballots)
                rank_t = rank_ballots[row][i]
                count += equiv_items(party_order[party], rank_t, borda)
            if borda > 0:
                borda -= 1
        borda_list.append(count)
        party += 1

    return borda_list

###############################################################################
# Task 3.5: Instant Run-off Voting System
###############################################################################

def remove_party(rank_ballots: List[List[str]], party_to_remove: str) -> None:
    """Change rank ballots rank_ballots by removing the party
    party_to_remove from each ballot.

    Pre: party_to_remove is in all of the ballots in rank_ballots.

    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> remove_party(ballots, 'NDP')
    >>> ballots == [['LIBERAL', 'GREEN', 'CPC'],
    ...             ['CPC', 'LIBERAL', 'GREEN'],
    ...             ['CPC', 'GREEN', 'LIBERAL']]
    True
    """

    for item in rank_ballots:
        for party in item:
            if party == party_to_remove:
                item.remove(party)
            else:
                continue

def get_lowest(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the lowest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_lowest([16, 100, 4, 200], SAMPLE_ORDER_1)
    'LIBERAL'

    """

    low = min(party_tallies)
    for item in party_tallies:
        if item == low:
            return party_order[party_tallies.index(item)]
    return None


def get_winner(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the highest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_winner([16, 100, 4, 200], SAMPLE_ORDER_1)
    'NDP'
    """

    high = max(party_tallies)
    for item in party_tallies:
        if item == high:
            return party_order[party_tallies.index(item)]
    return None

def party_order_remove(party_order: List[str], party: str)-> List[str]:
    """ Returns modified list of party_order after removing party from
    party_order

    >>> party_order_remove(['GREEN', 'CPC'], 'CPC')
    ['GREEN']
    >>> party_order_remove(['GREEN', 'CPC', 'NDP'], 'CPC')
    ['GREEN', 'NDP']
    """
    for item in party_order:
        if item == party:
            party_order.remove(party)
    return party_order

def voting_irv(rank_ballots: List[List[str]], party_order: List[str]) -> str:
    """Return the party which wins when IRV is performed on the list of
    rank ballots rank_ballots. Change rank_ballots and party_order as
    needed in IRV, removing parties that are eliminated in the
    process. Each ballot in rank_ballots is ordered by party_order.

    Pre: each ballot contains all and only elements of party_order
         len(rank_ballots) > 0
    >>> order2 = ['CPC', 'GREEN', 'LIBERAL', 'NDP']
    >>> ballots2 = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
    ...            ['CPC', 'GREEN', 'LIBERAL', 'NDP']]
    >>> voting_irv(ballots2, order2)
    'CPC'
    >>> ballots2 == [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
    ...            ['CPC', 'GREEN', 'LIBERAL', 'NDP']]
    True
    >>> order2
    ['CPC', 'GREEN', 'LIBERAL']
    """



    winner = ''
    temp_list = []
    counter = 0
    majority = (len(rank_ballots) //2) + 1

    while counter < majority:
        temp_list = []
        majority = (len(rank_ballots) //2) + 1
        for item in party_order:
            winner = item
            #print (winner)
            counter = 0
            for ballots in rank_ballots:
                counter += equiv_items(item, ballots[0], 1)
            temp_list.append(counter)

            if counter >= majority:
                return winner



        lowest = get_lowest(temp_list, party_order)
        remove_party(rank_ballots, lowest)
        party_order = party_order_remove(party_order, lowest)


    return winner













if __name__ == '__main__':
    import doctest
    doctest.testmod()
'''
#data = [['0', '1', 'NDP;Liberal;Green;CPC', '1;4;2;3', 'NO;YES;NO;NO']]


data = [['0', '1', 'NDP;LIBERAL;GREEN;CPC', '1;4;2;3', 'NO;YES;NO;NO'],
 ['1', '2', 'LIBERAL;NDP;GREEN;CPC', '2;1;4;2', 'NO;NO;YES;YES'],
 ['1', '3', 'GREEN;NDP;CPC;LIBERAL', '1;5;1;2', 'NO;YES;NO;YES']]

clean_data(data)

print(data)

#If columns became different numbers if we move it around:
#Ex. [[[1, 4, 2, 3], 0, 1, [...]]

print (voting_borda([['LIBERAL', 'GREEN', 'CPC', 'NDP','OTHER'], ['CPC', 'LIBERAL', 'GREEN', 'NDP','OTHER'], ['LIBERAL', 'NDP', 'GREEN', 'CPC','OTHER']], SAMPLE_ORDER_2))

#order = ['LIBERAL', 'NDP']
#ballots = [['LIBERAL', 'NDP'], ['NDP', 'LIBERAL'], ['NDP', 'LIBERAL']]
ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'], ['CPC', 'NDP', 'LIBERAL', 'GREEN'], ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
order = ['CPC','GREEN', 'LIBERAL', 'NDP']

print (voting_irv(ballots, order))
print (order)

'''