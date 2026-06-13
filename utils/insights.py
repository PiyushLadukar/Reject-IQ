def pricing_insight(df):

    if "Too Expensive" in df["Reason"].values:
        return "Review product pricing."

    return "Pricing looks acceptable."


def discount_insight(df):

    if "Need Discount" in df["Reason"].values:
        return "Offer seasonal discounts."

    return "Current discounts seem sufficient."


def competitor_insight(df):

    if "Already Using Competitor" in df["Reason"].values:
        return "Improve competitive positioning."

    return "Competition impact is low."


def marketing_insight(df):

    if "Not Interested" in df["Reason"].values:
        return "Improve marketing strategy."

    return "Customer interest looks stable."


def information_insight(df):

    if "Need More Information" in df["Reason"].values:
        return "Improve product awareness."

    return "Product information is sufficient."


def get_all_insights(df):

    return [
        pricing_insight(df),
        discount_insight(df),
        competitor_insight(df),
        marketing_insight(df),
        information_insight(df)
    ]