from functools import reduce

# List of intern scores
intern_score = [78, 90, 65, 88, 95]

# Using map() to square each score
def square(numbers):
    return numbers*numbers

map_used = list(map(square, intern_score))
print(map_used)

# Using filter() to get even scores
def even(num):
    if num%2==0:
        return True

filter_used = list(filter(even, intern_score))
print(filter_used)

# Using reduce() to get total sum of scores
reduce_used = reduce(lambda x, y: x+y, intern_score)
print(reduce_used)