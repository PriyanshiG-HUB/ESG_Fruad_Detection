from analytics.employee_analysis import employee_esg_correlation


# Example mock employee data (replace with scraped later)
employee_data = {
    "overall_rating": 2.9,
    "inclusion_rating": 65,
    "reviews": [
        "Management is toxic and stressful.",
        "Good pay but poor work-life balance.",
        "Some inclusive policies but burnout culture."
    ]
}

result = employee_esg_correlation(
    company_name="Ford Motor Company",
    esg_score=85,
    employee_data=employee_data
)

print("\nEmployee–ESG Analysis Result:\n")
print(result)