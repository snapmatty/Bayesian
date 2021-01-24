from model import universe

getProbability = universe.probability([["high_income", "real_estate", "large_deposit", "default", "no_security"]])

print(getProbability)


getProbability = universe.probability([["low_income", "tenant", "small_deposit", "payback", "security_given"]])

print(getProbability)