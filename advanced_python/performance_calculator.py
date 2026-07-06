# Simple function to calculate marks
def calculate_performance(scores):
    if not scores:
        return {"average": 0, "grade": "F"}
        
    avg = sum(scores) / len(scores)
    
    # Add grace marks
    if avg > 85:
        avg += 5
        
    # Check grade
    if avg >= 90:
        grade = "A+"
    elif avg >= 80:
        grade = "A"
    else:
        grade = "B"
        
    return {"average": avg, "grade": grade}
