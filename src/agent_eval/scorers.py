def exact_match(expected, actual) -> float:
    return 1.0 if expected == actual else 0.0

SCORERS = {
    "exact_match": exact_match,
}
