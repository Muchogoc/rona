import math

from .helpers import normalise_duration


def compute_currently_infected(reportedCases, numeral):

    return reportedCases * numeral


def compute_infections_by_requested_time(currentlyInfected, timeToElapse):

    # timeToElapse in days
    factorial = math.trunc(timeToElapse / 3)

    return currentlyInfected * (2 ** factorial)


def compute_severe_cases_by_requested_time(infectionsByRequestedTime):

    return math.trunc(0.15 * infectionsByRequestedTime)


def compute_available_beds(severeCasesByRequestedTime, totalHospitalBeds):

    available = math.trunc(0.35 * totalHospitalBeds)

    beds = available - severeCasesByRequestedTime

    if beds > 0:
        return beds
    else:
        return beds + 1


def compute_severe_positive_cases(infectionsByRequestedTime):

    icu_care = math.trunc(0.05 * infectionsByRequestedTime)
    ventilators = math.trunc(0.02 * infectionsByRequestedTime)

    return icu_care, ventilators


def compute_dollars_in_flight(
    infectionsByRequestedTime,
    avgDailyIncomePopulation,
    avgDailyIncomeInUSD,
    period,
):

    amount = math.trunc(
        infectionsByRequestedTime
        * avgDailyIncomePopulation
        * avgDailyIncomeInUSD
        / period
    )
    return round(amount, 2)


def compute_estimate(case, data):
    """Compute the estimate.

    cases, days, totalBeds, avgPopulation, avgIncome
    """
    days = normalise_duration(data["periodType"], data["timeToElapse"])

    currentlyInfected = compute_currently_infected(data["reportedCases"], case)

    infectionsByRequestedTime = compute_infections_by_requested_time(
        currentlyInfected, days
    )

    severeCasesByRequestedTime = compute_severe_cases_by_requested_time(
        infectionsByRequestedTime
    )

    hospitalBedsByRequestedTime = compute_available_beds(
        severeCasesByRequestedTime, data["totalHospitalBeds"]
    )

    (
        ICUByRequestedTime,
        VentilatorsByRequestedTime,
    ) = compute_severe_positive_cases(infectionsByRequestedTime)

    dollarsInFlight = compute_dollars_in_flight(
        infectionsByRequestedTime,
        data["region"]["avgDailyIncomePopulation"],
        data["region"]["avgDailyIncomeInUSD"],
        days,
    )

    data = {
        "currentlyInfected": currentlyInfected,
        "infectionsByRequestedTime": infectionsByRequestedTime,
        "severeCasesByRequestedTime": severeCasesByRequestedTime,
        "hospitalBedsByRequestedTime": hospitalBedsByRequestedTime,
        "casesForICUByRequestedTime": ICUByRequestedTime,
        "casesForVentilatorsByRequestedTime": VentilatorsByRequestedTime,
        "dollarsInFlight": dollarsInFlight,
    }

    return data
