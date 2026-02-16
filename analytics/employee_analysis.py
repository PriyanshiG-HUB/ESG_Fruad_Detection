# analytics/employee_analysis.py

# from scipy import stats


def sentiment_score_from_reviews(reviews):
    """
    Simple keyword-based sentiment scoring.
    """

    positive_keywords = [
        "great", "excellent", "good", "supportive",
        "inclusive", "positive", "growth", "fair"
    ]

    negative_keywords = [
        "toxic", "poor", "bad", "unfair",
        "discrimination", "stress", "burnout", "bias"
    ]

    text = " ".join(reviews).lower()

    pos_count = sum(text.count(word) for word in positive_keywords)
    neg_count = sum(text.count(word) for word in negative_keywords)

    total = pos_count + neg_count + 1

    return pos_count / total


def employee_esg_correlation(company_name, esg_score, employee_data):
    """
    Compare ESG score vs employee satisfaction.
    """

    overall_rating = employee_data["overall_rating"]
    inclusion_rating = employee_data.get("inclusion_rating", 70)

    # Normalize values
    normalized_esg = esg_score / 100
    normalized_rating = overall_rating / 5

    # Correlation (simplified single-point correlation proxy)
    correlation_strength = 1 - abs(normalized_esg - normalized_rating)

    sentiment_ratio = sentiment_score_from_reviews(employee_data["reviews"])

    # Fraud Logic
    fraud_flag = (
        esg_score > 80 and
        overall_rating < 3.2 and
        correlation_strength < 0.6
    )

    return {
        "company": company_name,
        "claimed_esg_score": esg_score,
        "employee_rating": overall_rating,
        "inclusion_rating": inclusion_rating,
        "correlation_strength": round(correlation_strength, 2),
        "sentiment_ratio": round(sentiment_ratio, 2),
        "employee_esg_mismatch_flag": fraud_flag
    }