import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("Searching for next proof")
    proof = 0
    #  TODO: Your code here
    #encode the last proof
    encoded_last_proof = f'{last_proof}'.encode()

    #hash and convert the encoded proof to hexadigest
    hashed_last_proof = hashlib.sha256(encoded_last_proof).hexadigest

    #this will run until it finds one that works
    while valid_proof(hashed_last_proof, proof) is False:
        #increments the proof value until the hash with the required difficulty has been generated.        
        proof += random.randint(1,000)

    #after we find one that works, we return proof
    return proof


    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """

    # TODO: Your code here!
    #encode the proof passed in from proof_of_work
    encoded_new_proof = f'{proof}'.encode()

    #hashes and converts guess to hexadecimal format (readable format that we can compare)
    hashed_new_proof = hashlib.sha256(encoded_new_proof).hexdigest()

    #return hashed_new_proof if the last 6 digits of last_hash is the first 6 digits of hashed_new_proof
    return hashed_new_proof[:6] == last_hash[-6:]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # open text file and read id
    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        # by visiting the endpoint that is in node + last_proof 
        r = requests.get(url=node + "/last_proof")

        #use .json to get the json encoded content of a response
        data = r.json()

        #sends the proof returned from the last_proof endpoint to the proof_of_work method 
        new_proof = proof_of_work(data.get('proof'))

        #data object to be send to mine endpoint
        post_data = {"proof": new_proof,
                     "id": id}

        #post the data object with proof and id to the mine endpoint and stores the response in r
        r = requests.post(url=node + "/mine", json=post_data)

        #use .json to get the json encoded content of the response from the server
        data = r.json()

        #if a success message is returned from the mine endpoint
        #increment the number of coins mined
        #else print the error message that is sent back from the mine endpoint
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
