# Show initially empty trie
trie-cli display

# Insert some nodes
trie-cli display
trie-cli insert mathur
trie-cli display

trie-cli insert MATH
trie-cli insert mAthEmaticIaN
trie-cli display

trie-cli insert pranav
trie-cli insert pro
trie-cli insert prometheus
trie-cli display

trie-cli insert slingshot
trie-cli insert sling
trie-cli insert shot
trie-cli insert shot
trie-cli display

trie-cli insert chocolate
trie-cli display

# Invalid input commands
trie-cli insert
trie-cli insert "python<3"
trie-cli insert 143

# Delete some nodes
trie-cli delete mathur
trie-cli display

trie-cli delete pro
trie-cli display

trie-cli delete chocolate
trie-cli display

# Invalid delete commands
trie-cli delete mathur 
trie-cli delete frappucino
trie-cli delete pran

# Search for some nodes
trie-cli search math
trie-cli search mathematician
trie-cli search java
trie-cli search slin
trie-cli search hot

# Generate autocomplete results
trie-cli insert mathur
trie-cli insert madripoor
trie-cli insert muffin
trie-cli insert madagascar

trie-cli autocomplete m
trie-cli autocomplete mad
trie-cli autocomplete p
trie-cli autocomplete z