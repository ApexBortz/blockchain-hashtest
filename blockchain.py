from base64 import encode
import hashlib
import json # python's json module
from time import time # data module similar to new Date()
from pprint import pprint # make that shit pretty (the output - so that its more readable)

class Blockchain:
    def __init__(self):
        # list of blocks in the blockchain
        self.chain = []
        # the list of transactions that have not been added to a block yet
        self.pending_transactions = []
        # seed the blockchain with a new block
        self.new_block(previous_hash="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.", proof=100)

    def __len__(self):
        return len(self.chain)

    @property # another decorator
    def last_block(self):
        # return last block of the chain
        # blockchainInstance.last_block
        return self.chain[-1] # the last index of our chain

    @staticmethod
    def proof_algorithm(prev_proof, new_proof):
        # little algorithm that might produce the right amount of zeros
        return hashlib.sha256(str(new_proof ** 2 - prev_proof ** 2).encode()).hexdigest()

    @staticmethod
    # *args = variable amount of arguments 'variadic argument functions'
    def consensus(*args):
        # filter out all chains that do not pass validation
        valid_chains = []
        for chain in args:
            if chain.validate_chain():
                valid_chains.append(chain)
        # if there are no valid chains return false
        if len(valid_chains) == 0:
            return False
        # find the longest valid chain and return it
        longest_valid = valid_chains[0]
        for chain in valid_chains:
            if len(chain) > len(longest_valid):
                longest_valid = chain

        return longest_valid

    # verifiable computational work
    def proof_of_work(self, verbose=False):
        # get the previous proof from the last block
        previous_proof = self.last_block['proof']
        # start calculating the 'nonce' or 'proof'
        # basically the guess or arbitrary number to find the right proof
        nonce = 1
        # loop until our proof algorithm returns the right proof
        check_proof = False
        while check_proof is False:
            # use our proof algorithm to check the nonce
            proof_guess = Blockchain.proof_algorithm(previous_proof, nonce)
            # if we are in verbose mode - print out what is happening
            if verbose:
                # expression if condition else expression
                print(nonce, 'matches!' if proof_guess[:4] == '0000' else 'does not match')
            # if the proof we guess starts with '0000' - we have a match (break the loop)
            if proof_guess[:4] == '0000':
                check_proof = True
            # otherwise - increment nonce and start again
            else:
                nonce += 1
        # return the correct proof we found 
        return nonce

    def new_block(self, proof, previous_hash=None):
        # create a new block based on the pending transaction
        # create a new block
        block = {
            'index': len(self)+1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof, # provided by the miner
            'previous_hash': previous_hash or self.hash(self.last_block)
        }
        # clear out the pending transaction
        self.pending_transactions = []
        # append the new block to our blockchain
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        # add a new transaction to the list of pending transactions
        # create new transaction
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        # add the transaction to the list of pending transactions
        self.pending_transactions.append(transaction)
        # return transaction that was added on success
        return transaction

    def hash(self, block):
        # hash blocks
        # order the keys of the block so that they are predictable, then encode
        string_block = json.dumps(block, sort_keys=True).encode()
        # return the hexdigest
        return hashlib.sha256(string_block).hexdigest()

    def validate_chain(self):
        # we need to self validate the chain
        i = 0
        # loop over the chain
        while i < len(self) - 2:
            # check if the hashes line up
            # compare in groups of 2
            prev_block = self.chain[i]
            next_block = self.chain[i+1]
            # verify the data integrity
            if next_block['previous_hash'] != self.hash(prev_block):
                return False
            # validate that the hashes start with '0000' (do they have a correct proof of work)
            # verify the computational work
            work_check = Blockchain.proof_algorithm(prev_block['proof'], next_block['proof'])
            # work_check should return a valid '0000' hash string
            if work_check[:4] != '0000':
                return False

            i += 1

        return True


bc = Blockchain()
bc.new_transaction('Alyssa', 'Nicholas', 20)
bc.new_transaction('Nicholas', 'Lola', 10)
bc.new_transaction('Nicholas', 'Suki', 10)
# chain will be the same

bc.new_block(bc.proof_of_work(verbose=True))
# bc.new_block(1000)
# pprint(bc.pending_transactions)
# pprint(bc.chain)
bc.new_transaction('Jaleel', 'Andy', 100)
bc.new_transaction('Des', 'James', 50)
bc.new_transaction('Andy', 'Lola', 25)
bc.new_block(bc.proof_of_work(verbose=True))
# bc.new_block(7000)
pprint(bc.pending_transactions)
pprint(bc.chain)
print(bc.validate_chain())

not_valid = Blockchain()
not_valid.new_transaction('Nicholas', 'Alyssa', 500)
not_valid.new_block(2345768)

old_chain = Blockchain()
old_chain.chain = bc.chain[:len(bc)-2]

current_chain = Blockchain.consensus(bc, not_valid, old_chain)
pprint(current_chain.chain)