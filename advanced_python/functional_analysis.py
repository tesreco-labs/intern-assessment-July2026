from functools import reduce


def analyze_scores(scores):
    increased_scores = list(map(lambda score: score + 5, scores))
    high_scores = list(filter(lambda score: score >= 85, scores))
    total_score = reduce(lambda total, score: total + score, scores, 0)
    average_score = total_score / len(scores) if scores else 0

    return {
        "increased_scores": increased_scores,
        "high_scores": high_scores,
        "total_score": total_score,
        "average_score": round(average_score, 2),
    }
