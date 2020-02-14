#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source #starting airport
        self.destination = destination #next airport

def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = []

    #insert the array of tickets into the hashtable
    for ticket in tickets:
        hash_table_insert(hashtable, ticket.source, ticket.destination)

    #retrieve the the ticket for your first destination with a `source` of `NONE`
    ticket_destination = hash_table_retrieve(hashtable, 'NONE')

    #find the other tickets and add them to the route array
    while ticket_destination is not 'NONE':
        route.append(ticket_destination)

        #find a ticket with a source that is the same as the destination of the preceding ticket         
        ticket_destination = hash_table_retrieve(hashtable, ticket_destination)
   
    return route


    