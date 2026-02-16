class Contact:
    '''
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''
    
    def __init__(self, name, number):
        """Initialize a contact with a name and phone number."""
        self.name = name
        self.number = number
    
    def __str__(self):
        """Return string representation of the contact."""
        return f"{self.name}: {self.number}"

class Node:
    '''
    Node class to represent a single entry in the hash table.
    Attributes:
        key (str): The key (name) of the contact.
        value (Contact): The value (Contact object) associated with the key.
        next (Node): Pointer to the next node in case of a collision.
    '''
   
    def __init__(self, key, value):
        """Initialize a node with a key and value."""
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    '''
    HashTable class to represent a hash table for storing contacts.
    Attributes:
        size (int): The size of the hash table.
        data (list): The underlying array to store linked lists for collision handling.
    Methods:
        hash_function(key): Converts a string key into an array index.
        insert(key, value): Inserts a new contact into the hash table.
        search(key): Searches for a contact by name.
        print_table(): Prints the structure of the hash table.
    '''
    
    def __init__(self, size):
        """Initialize the hash table with a given size."""
        self.size = size
        self.data = [None] * size
    
    def hash_function(self, key):
        """
        Convert a string key into an array index.
        Uses the sum of ASCII values modulo the table size.
        """
        hash_value = 0
        for char in key:
            hash_value += ord(char)
        return hash_value % self.size
    
    def insert(self, key, number):
        """
        Insert a new contact into the hash table.
        If the key already exists, update the contact's number.
        """
        # Create a new Contact object
        contact = Contact(key, number)
        
        # Get the index for this key
        index = self.hash_function(key)
        
        # If the slot is empty, create a new node
        if self.data[index] is None:
            self.data[index] = Node(key, contact)
        else:
            # Traverse the linked list to check if key exists
            current = self.data[index]
            
            # Check if we need to update an existing contact
            while current:
                if current.key == key:
                    # Update the existing contact's number
                    current.value = contact
                    return
                
                # If we're at the end of the list, add new node
                if current.next is None:
                    current.next = Node(key, contact)
                    return
                
                current = current.next
    
    def search(self, key):
        """
        Search for a contact by name.
        Returns the Contact object if found, None otherwise.
        """
        # Get the index for this key
        index = self.hash_function(key)
        
        # Traverse the linked list at this index
        current = self.data[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        
        # Key not found
        return None
    
    def print_table(self):
        """Display the structure of the hash table."""
        for i in range(self.size):
            if self.data[i] is None:
                print(f"Index {i}: Empty")
            else:
                # Build the string for this index
                contacts = []
                current = self.data[i]
                while current:
                    contacts.append(f" - {current.value}")
                    current = current.next
                print(f"Index {i}:{''.join(contacts)}")

# Test your hash table implementation here.
if __name__ == "__main__":
    print("=== Testing Hash Table Implementation ===\n")
    
    # Create a hash table with size 10
    table = HashTable(10)
    
    print("Initial empty table:")
    table.print_table()
    print()
    
    # Add some contacts
    print("Adding John and Rebecca...")
    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")
    table.print_table()
    print()
    
    # Search for a contact
    print("Searching for John:")
    contact = table.search("John")
    print(f"Search result: {contact}")
    print()
    
    # Test collision handling
    print("Testing collision handling with Amy and May...")
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")
    table.print_table()
    print()
    
    # Test duplicate key (should update)
    print("Updating Rebecca's number...")
    table.insert("Rebecca", "999-444-9999")
    table.print_table()
    print()
    
    # Test searching for non-existent contact
    print("Searching for Chris (not in table):")
    print(table.search("Chris"))
    print()
    
    print("=== All Tests Complete ===")

"""
DESIGN MEMO

Why is a hash table the appropriate type of structure to use?

The hash table will provide you with O(1) average time add and a hash table will look up and add stuff on average as well as give you O(1) time which is killer as you need instant information such as a contacts list.
Lists cost you O(n) time to take up everyone but a hash table causes you to invoke a hash function and go directly to the location where the data is stored and therefore you avoid all that walking about.
It is significant in machines with less memories and speed as the secret.

What was your approach towards collisions?

I have taken the separate chaining through linked list.
Each time the two contacts touch on the same hash slot they form some sort of a linked list there.
All Nodes have their contact and next pointer.
You put in a new one and find that you have one there, you walk the chain taking out the old entry or pushing the new entry at the end.
In a search you simply go that chain tapping keys until you strike a match or you strike the end of the nodes.

In which instances may an engineer then opt to use a hash table instead of a list or tree?

Hash tables are tremendously bright when the primary requirement is rapid access of the information by the key and the volume of data does not oscillate dramatically.
When you look up things much more frequently than you do need to simply read them sequentially then use a hash table instead of a list.
Take it instead of a tree when you are not bothered about order or doing range queries.
Contact books it fits well since you need it when you are mostly interested in locating the key (that is mostly by name) rather than by alphabetical or ranges.
"""