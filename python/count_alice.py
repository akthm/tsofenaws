file = open("Alice.txt", "r")
dictionary = {}
for sentence in file:
    for word in sentence.split():
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
mx = max(dictionary.keys(), key=lambda x: dictionary[x])
print(mx, dictionary[mx])
