import hashlib

class Node:
    # no previous hash supplied if this is the first node
    def __init__(self, value, previous_hash='head'):
        # this node's value
        self.value = value
        # hash from the previous node
        self.previous_hash = previous_hash
        # a reference to the next node
        self.next = None
        # sha256(self.value + self.previous_hash)
        self.hash = Node.make_hash(self.value, self.previous_hash)

    def __str__(self):
        return f'{self.hash} ▶︎ {self.value}'

    @staticmethod # decorator
    def make_hash(value, previous_hash):
        # creates the hash for the node
        history = str(value) + previous_hash
        # print('Making new node ⦿→ the history is ⑆ ', history)
        return hashlib.sha256(history.encode()).hexdigest()

    @staticmethod
    def validate(prev_node, current_node):
        # check to see if the nodes have valid hashes
        if current_node.hash == Node.make_hash(current_node.value, prev_node.hash):
            # we are valid!
            return True
        else:
            return False

    @staticmethod
    def consensus(head):
        # if the head is the only node in the list, the list is valid
        if not head.next:
            return True
        # loop over a list to see if all nodes are valid
        current_node = head
        while current_node.next:
            # if two nodes fail validation, we will return false
            if not Node.validate(current_node, current_node.next):
                return False
            current_node = current_node.next
        # return True after checking the entire list
        return True

# hashlist testing area
head = Node(0)
# print('The Head Node: ', head)

one = Node(1, head.hash)
head.next = one
# print('Node one:', one)

two = Node(2, one.hash)
one.next = two
# print('Node two: ', two)

three = Node(3, two.hash)
two.next = three

# print(Node.validate(one, two)) # true
# print(Node.validate(one, three)) # false
# two.value = 100
# print(Node.validate(one, two))
# print(three)

# test consensus
print(Node.consensus(head)) # true
print(Node.consensus(Node(10)))
two.value = 15 # false
print(Node.consensus(head)) 