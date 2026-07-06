# Using map and filter
def functional_programming_demo():
    scores = [78, 90, 65, 88, 95]
    
    # Give 5 extra marks to all
    bonus = list(map(lambda x: x + 5, scores))
    
    # Find scores above 80
    toppers = list(filter(lambda x: x > 80, scores))
    
    return {"bonus_marks": bonus, "toppers": toppers}
