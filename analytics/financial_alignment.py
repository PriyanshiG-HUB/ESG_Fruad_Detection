# analytics/financial_alignment.py

import re


def extract_capex(text):
    """
    Extract CAPEX values from 10-K text.
    Looks for patterns like:
    'Capital expenditures were $3.2 billion'
    """

    patterns = [
        r"capital expenditures[^$]*\$?([\d\.,]+)\s*(billion|million)?",
        r"capex[^$]*\$?([\d\.,]+)\s*(billion|million)?"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            value, scale = matches[0]
            value = float(value.replace(",", ""))

            if scale.lower() == "billion":
                value *= 1_000_000_000
            elif scale.lower() == "million":
                value *= 1_000_000

            return value

    return 0.0


def extract_esg_spend(text):
    """
    Extract explicitly mentioned sustainability / ESG investments.
    """

    patterns = [
        r"\$([\d\.,]+)\s*(billion|million)?[^\.]{0,50}(sustainability|climate|renewable|environmental)",
        r"(sustainability|climate|renewable)[^\.]{0,50}\$([\d\.,]+)\s*(billion|million)?"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            match = matches[0]

            # Handle both pattern formats
            if len(match) == 3:
                value, scale, _ = match
            else:
                _, value, scale = match

            value = float(value.replace(",", ""))

            if scale and scale.lower() == "billion":
                value *= 1_000_000_000
            elif scale and scale.lower() == "million":
                value *= 1_000_000

            return value

    return 0.0


def count_esg_mentions(text):
    keywords = [
        "sustainability",
        "climate",
        "environmental",
        "carbon",
        "renewable",
        "diversity",
        "inclusion",
        "governance",
        "ethics",
        "social"
    ]

    text_lower = text.lower()
    return sum(text_lower.count(word) for word in keywords)


def financial_esg_alignment(company_name, industry, filing_text):

    capex = extract_capex(filing_text)
    claimed_esg_spend = extract_esg_spend(filing_text)
    esg_mentions = count_esg_mentions(filing_text)

    # If explicit ESG spend not found, estimate based on narrative density
    if claimed_esg_spend == 0 and capex > 0:
        narrative_intensity = min(esg_mentions / 200, 1)
        claimed_esg_spend = capex * narrative_intensity * 0.05

    esg_percent = (claimed_esg_spend / capex * 100) if capex > 0 else 0

    industry_benchmarks = {
        "manufacturing": 6.7,
        "finance": 4.2,
        "healthcare": 5.8
    }

    benchmark = industry_benchmarks.get(industry, 5.0)
    deviation = esg_percent - benchmark

    # Stronger fraud logic
    overclaim_flag = (
        esg_percent > benchmark * 2
        or (esg_mentions > 150 and esg_percent < benchmark / 2)
    )

    return {
        "company": company_name,
        "capex": round(capex, 2),
        "claimed_esg_spend": round(claimed_esg_spend, 2),
        "esg_mentions": esg_mentions,
        "esg_percent_of_capex": round(esg_percent, 2),
        "industry_benchmark": benchmark,
        "deviation_from_benchmark": round(deviation, 2),
        "financial_esg_red_flag": overclaim_flag
    }