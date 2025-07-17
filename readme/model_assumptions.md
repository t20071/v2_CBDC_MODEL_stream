# CBDC Banking Simulation: Model Assumptions and References

## Overview
This document outlines all assumptions made in the CBDC banking simulation model for each agent type, along with academic references where available.

## General Model Assumptions

### 1. Market Structure
- **Assumption**: Banking market consists of large banks (20% of institutions) and small-medium banks (80%)
- **Rationale**: Reflects real-world banking concentration
- **Reference**: Claessens, S., & Laeven, L. (2004). "What drives bank competition? Some international evidence." *Journal of Money, Credit and Banking*, 36(3), 563-583.

### 2. Network Topology
- **Assumption**: Agent relationships follow Erdős-Rényi random graph with 10% connection probability
- **Rationale**: Standard approach for modeling financial networks with sparse connections
- **Reference**: Erdős, P., & Rényi, A. (1960). "On the evolution of random graphs." *Publications of the Mathematical Institute of the Hungarian Academy of Sciences*, 5(1), 17-60.

### 3. CBDC Introduction
- **Assumption**: CBDC introduced at predetermined time step (default: step 30)
- **Rationale**: Allows analysis of pre/post CBDC dynamics
- **Reference**: Meaning, J., Dyson, B., Barker, J., & Clayton, E. (2021). "Broadening narrow money: monetary policy with a central bank digital currency." *Bank of England Working Paper No. 724*.

### 4. Perfect Information
- **Assumption**: Agents have perfect information about interest rates and CBDC availability
- **Limitation**: Real-world information asymmetries not modeled
- **Reference**: Standard simplification in ABM literature (Farmer & Foley, 2009)

## Central Bank Agent Assumptions

### 1. Monopoly CBDC Issuer
- **Assumption**: Central bank is sole issuer of CBDC
- **Rationale**: Reflects current CBDC proposals
- **Reference**: Auer, R., & Böhme, R. (2020). "The technology of retail central bank digital currency." *BIS Quarterly Review*.

### 2. Dual Mandate
- **Assumption**: Central bank targets both financial stability (0.8 target) and inflation (2% target)
- **Reference**: Federal Reserve dual mandate; ECB price stability mandate

### 3. Passive Monetary Policy
- **Assumption**: Base monetary policy rate remains constant (2%)
- **Limitation**: No dynamic monetary policy response to CBDC effects
- **Potential Reference**: Taylor, J. B. (1993). "Discretion versus policy rules in practice." *Carnegie-Rochester Conference Series on Public Policy*, 39, 195-214.

### 4. CBDC Promotion
- **Assumption**: Central bank actively promotes CBDC adoption
- **Rationale**: Based on current central bank CBDC initiatives
- **Reference**: Boar, C., Holden, H., & Wadsworth, A. (2020). "Impending arrival–a sequel to the survey on central bank digital currency." *BIS Papers No. 107*.

### 5. Demand-Driven CBDC Supply
- **Assumption**: Central bank expands CBDC supply automatically to meet all consumer demand
- **Implementation**: Supply starts at zero and increases exactly to match total consumer CBDC holdings
- **Rationale**: Reflects central bank commitment to satisfy demand without supply constraints
- **Reference**: Modern central bank digital currency proposals emphasize accommodation of legitimate demand

### 5. Systemic Risk Monitoring
- **Assumption**: Central bank monitors banking system health and provides support if >30% of banks are weak
- **Reference**: Basel Committee on Banking Supervision guidelines on systemic risk

## Commercial Bank Agent Assumptions

### 1. Profit Maximization
- **Assumption**: Banks maximize profits through deposits and lending
- **Reference**: Standard microeconomic assumption in banking literature

### 2. Fixed Interest Rate Spread
- **Assumption**: Lending rate = deposit rate + 3% fixed spread
- **Limitation**: No dynamic pricing based on risk or competition
- **Reference**: Typical retail banking spreads (Demirgüç-Kunt & Huizinga, 1999)

### 3. Reserve Requirements
- **Assumption**: 10% reserve requirement, banks hold 20% reserves initially
- **Reference**: Basel III liquidity requirements; central bank regulations

### 4. Size-Based Vulnerability
- **Large Banks**: 40% CBDC vulnerability, 70% customer stickiness
- **Small Banks**: 80% CBDC vulnerability, 30% customer stickiness
- **Rationale**: Larger banks have more resources to compete with CBDC
- **Reference**: Berger, A. N., Klapper, L. F., & Turk-Ariss, R. (2009). "Bank competition and financial stability." *Journal of Financial Services Research*, 35(2), 99-118.

### 5. Network Effects
- **Assumption**: Large banks more connected (60% of network) than small banks (30%)
- **Reference**: Financial network literature on core-periphery structure (Craig & Von Peter, 2014)

### 6. Competitive Response
- **Assumption**: Banks adjust interest rates and strategies in response to CBDC competition
- **Limitation**: No explicit game-theoretic framework
- **Reference**: Competition literature in banking (Vives, 2016)

## Consumer Agent Assumptions

### 1. Wealth Allocation
- **Assumption**: Initial allocation: 37% bank deposits, 63% other assets
- **Reference**: Federal Reserve Survey of Consumer Finances data on household liquid assets

### 2. Rational Choice with Behavioral Elements
- **Assumption**: Consumers optimize based on interest rates, convenience, and social influence
- **Reference**: Behavioral finance literature (Kahneman & Tversky, 1979)

### 3. Risk Aversion Distribution
- **Assumption**: Risk aversion ~ Normal(0.5, 0.2), constrained [0.1, 0.9]
- **Reference**: Experimental economics literature on risk preferences (Holt & Laury, 2002)

### 4. Social Influence
- **Assumption**: CBDC adoption influenced by peer adoption rates
- **Weight**: Social influence weight ~ Normal(0.3, 0.1)
- **Reference**: Social learning and network effects literature (Banerjee, 1992)

### 5. Interest Sensitivity
- **Assumption**: Interest sensitivity ~ Normal(0.5, 0.2), affects CBDC adoption
- **Reference**: Interest rate elasticity studies in banking (Hutchison & Pennacchi, 1996)

### 6. Portfolio Rebalancing
- **Assumption**: Consumers rebalance between bank deposits and CBDC based on preferences
- **Frequency**: Every simulation step (monthly)
- **Reference**: Portfolio theory (Markowitz, 1952)

### 7. Economic Activity
- **Income Growth**: ~ Normal(2%, 0.5%) monthly
- **Spending Rate**: ~ Normal(1.5%, 0.5%) monthly
- **Assumption**: Regular income and spending affect financial holdings
- **Reference**: Household consumption literature (Campbell & Mankiw, 1989)

### 8. Bank Loyalty
- **Assumption**: Bank loyalty ~ Normal(0.7, 0.2), affects switching behavior
- **Reference**: Customer loyalty literature in banking (Sharma & Foropon, 2019)

## Key Limitations and Assumptions Not Modeled

### 1. Regulatory Response
- **Missing**: Dynamic regulatory changes in response to CBDC
- **Impact**: May underestimate policy interventions

### 2. International Effects
- **Missing**: Cross-border flows, international banking
- **Impact**: Closed economy assumption

### 3. Technology Adoption Costs
- **Missing**: Implementation costs for CBDC infrastructure
- **Impact**: May overestimate adoption speed

### 4. Macroeconomic Feedback
- **Missing**: GDP, employment, inflation dynamics
- **Impact**: Partial equilibrium analysis only

### 5. Bank Heterogeneity
- **Limited**: Only size-based differentiation
- **Missing**: Specialization, geographic differences

## Academic References

1. Banerjee, A. V. (1992). A simple model of herd behavior. *The Quarterly Journal of Economics*, 107(3), 797-817.

2. Berger, A. N., Klapper, L. F., & Turk-Ariss, R. (2009). Bank competition and financial stability. *Journal of Financial Services Research*, 35(2), 99-118.

3. Campbell, J. Y., & Mankiw, N. G. (1989). Consumption, income, and interest rates: Reinterpreting the time series evidence. *NBER Macroeconomics Annual*, 4, 185-216.

4. Claessens, S., & Laeven, L. (2004). What drives bank competition? Some international evidence. *Journal of Money, Credit and Banking*, 36(3), 563-583.

5. Craig, B., & Von Peter, G. (2014). Interbank tiering and money center banks. *Journal of Financial Intermediation*, 23(3), 322-347.

6. Demirgüç-Kunt, A., & Huizinga, H. (1999). Determinants of commercial bank interest margins and profitability: some international evidence. *The World Bank Economic Review*, 13(2), 379-408.

7. Farmer, J. D., & Foley, D. (2009). The economy needs agent-based modelling. *Nature*, 460(7256), 685-686.

8. Holt, C. A., & Laury, S. K. (2002). Risk aversion and incentive effects. *American Economic Review*, 92(5), 1644-1655.

9. Hutchison, D. E., & Pennacchi, G. G. (1996). Measuring rents and interest rate risk in imperfect financial markets: The case of retail bank deposits. *Journal of Financial and Quantitative Analysis*, 31(3), 399-417.

10. Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263-291.

11. Markowitz, H. (1952). Portfolio selection. *The Journal of Finance*, 7(1), 77-91.

12. Meaning, J., Dyson, B., Barker, J., & Clayton, E. (2021). Broadening narrow money: monetary policy with a central bank digital currency. *Bank of England Working Paper No. 724*.

13. Sharma, A., & Foropon, C. (2019). Green product attributes and green purchase behavior: A theory of planned behavior perspective with the moderating effect of consumer knowledge. *Journal of Cleaner Production*, 219, 849-874.

14. Vives, X. (2016). *Competition and stability in banking: The role of regulation and competition policy*. Princeton University Press.