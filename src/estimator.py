from .utils import compute_estimate


def compute_impact(data):
    return compute_estimate(10, data)


def compute_severe_impact(data):
    return compute_estimate(50, data)


def estimator(data):

    impact = compute_impact(data)
    severe_impact = compute_severe_impact(data)

    data = {
        "data": data,
        "impact": impact,
        "severeImpact": severe_impact,
    }

    return data
