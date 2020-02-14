#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    """
    YOUR CODE HERE
    """
    #insert values into hashtable
    for i in range (length):
        #stores the weights or values in the list as keys and the indices as values
        hash_table_insert(ht, weights[i], i)

    for i in range (length):
        #subtract each number in the hashtable and check if the difference/number needed is in the hash table
        difference = limit - weights[i]

        #check hash_table for difference/number needed
        #hash_table_retrieve will return the index of the number given for retrieval
        index_needed = hash_table_retrieve(ht, difference)

        #if index was found
        if index_needed is not None:
            #check if it is greater than the current index where the other number is found
            #place the index_needed in the zeroth index
            if index_needed > i:
                 return (index_needed, i)
            #if the returned index is less than the current index
            #place the current index in the zeroth index
            else:
                return (i, index_needed)

    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
