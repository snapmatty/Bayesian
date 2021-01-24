from pomegranate import *
#************************************
#
#   AI&CV 249109
#
#*************************************

# First node
# this node is independent from the other, thus we are using DiscreteDistribution class
income = Node(DiscreteDistribution({
    "high_income": 0.3,
    "low_income": 0.7
}), name="income")

housing = Node(DiscreteDistribution({
    "real_estate": 0.35,
    "tenant": 0.65,
}), name="housing")
###########################################################################################

# Deposit is dependant from income
deposit = Node(ConditionalProbabilityTable([
    ["high_income", "large_deposit", 0.1],
    ["low_income", "large_deposit", 0.6],
    ["high_income", "small_deposit", 0.9],
    ["low_income", "small_deposit", 0.4]
], [income.distribution]), name="deposit")

# Payment node is dependant from both income and deposit
payment = Node(ConditionalProbabilityTable([
    ["high_income", "large_deposit", "default", 0.05],
    ["high_income", "large_deposit", "payback", 0.95],
    ["high_income", "small_deposit", "default", 0.5],
    ["high_income", "small_deposit", "payback", 0.5],
    ["low_income", "large_deposit", "default", 0.45],
    ["low_income", "large_deposit", "payback", 0.55],
    ["low_income", "small_deposit", "default", 0.6],
    ["low_income", "small_deposit", "payback", 0.4]
], [income.distribution, deposit.distribution]), name="payment")

# Security is dependant from housing and payment
security = Node(ConditionalProbabilityTable([
    ["default", "real_estate", "security_given", 0.01],
    ["default", "real_estate", "no_security", 0.99],
    ["default", "tenant", "security_given", 0.5],
    ["default", "tenant", "no_security", 0.5],
    ["payback", "real_estate", "security_given", 0.75],
    ["payback", "real_estate", "no_security", 0.25],
    ["payback", "tenant", "security_given", 0.31],
    ["payback", "tenant", "no_security", 0.69]
], [payment.distribution, housing.distribution]), name="security")

# Create a Bayesian Network and add states
universe = BayesianNetwork()
universe.add_states(income, housing, deposit, payment, security)

# Add edges connecting nodes
universe.add_edge(income, deposit)
universe.add_edge(income, payment)
universe.add_edge(deposit, payment)
universe.add_edge(payment, security)
universe.add_edge(housing, security)

# Finalize model
universe.bake()