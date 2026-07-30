from itertools import permutations

# Get input from the user
word1 = input("Enter first word: ").upper()
word2 = input("Enter second word: ").upper()
result = input("Enter result word: ").upper()

# Find all unique letters
letters = []

for ch in word1 + word2 + result:
    if ch not in letters:
        letters.append(ch)

# Check if there are too many unique letters
if len(letters) > 10:
    print("More than 10 unique letters. No solution possible.")
    exit()

# First letters cannot be zero
first_letters = {word1[0], word2[0], result[0]}

# Try every possible digit assignment
for perm in permutations(range(10), len(letters)):
# Dict= dictionary , zip=(key,value)=> set of pairs 

    mapping = dict(zip(letters, perm))

    # Check leading zero condition
    valid = True
    for ch in first_letters:
        if mapping[ch] == 0:
            valid = False
            break

    if not valid:
        continue

    # Convert a word into a number
    def word_to_number(word):
        number = ""
        for ch in word:
            number += str(mapping[ch])
        return int(number)

    num1 = word_to_number(word1)
    num2 = word_to_number(word2)
    num3 = word_to_number(result)

    if num1 + num2 == num3:
        print("\nSolution Found!")
        print(num1, "+", num2, "=", num3)

        print("\nLetter Assignments:")
        for letter in sorted(mapping):
            print(letter, "=", mapping[letter])
        break
else:
    print("No solution found.")





