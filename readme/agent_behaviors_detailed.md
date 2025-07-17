# CBDC Banking Simulation: Complete Agent Behaviors and References

## Overview
This document provides a comprehensive list of all behaviors for each agent type in the CBDC banking simulation, with detailed explanations and academic references where applicable.

## Central Bank Agent Behaviors

### Core Behavioral Functions

#### 1. **CBDC Introduction (`introduce_cbdc`)**
**Behavior**: Central bank announces CBDC availability with demand-driven supply policy at predetermined time step.
**Implementation**: Notifies all consumers, activates CBDC functionality, starts with zero supply that expands automatically to meet demand.
**Reference**: Meaning, J. et al. (2021). "Broadening narrow money: monetary policy with a central bank digital currency." *Bank of England Working Paper No. 724*.

#### 2. **CBDC Impact Monitoring (`monitor_cbdc_impact`)**
**Behavior**: Continuously tracks CBDC adoption rates and assesses impact on banking system health.
**Implementation**: Calculates adoption metrics, deposit changes, and banking system stability scores (0-1 scale).
**Reference**: Auer, R., & Böhme, R. (2020). "The technology of retail central bank digital currency." *BIS Quarterly Review*.

#### 3. **CBDC Promotion (`promote_cbdc_adoption`)**
**Behavior**: Actively encourages CBDC adoption through policy measures and attractiveness adjustments.
**Implementation**: Increases CBDC attractiveness factor based on adoption momentum and network effects.
**Reference**: Network effects literature - Katz, M. L., & Shapiro, C. (1985). "Network externalities, competition, and compatibility." *American Economic Review*.

#### 4. **Banking System Monitoring (`monitor_banking_system`)**
**Behavior**: Supervises commercial banking sector health and provides support when systemic risk emerges.
**Implementation**: Calculates banking system health score, triggers intervention if >30% of banks show weakness.
**Reference**: Basel Committee on Banking Supervision (2017). "Basel III: Finalising post-crisis reforms."

#### 5. **Systemic Risk Assessment (`calculate_systemic_risk`)**
**Behavior**: Evaluates overall financial system stability considering CBDC adoption and banking sector stress.
**Implementation**: Weighted risk score combining rapid adoption (40%), banking instability (40%), deposit concentration (20%).
**Reference**: Adrian, T., & Brunnermeier, M. K. (2016). "CoVaR." *American Economic Review*, 106(7), 1705-1741.

#### 6. **Deposit Change Tracking (`calculate_deposit_change`)**
**Behavior**: Monitors rate of change in commercial bank deposits to assess CBDC substitution effects.
**Implementation**: Calculates period-over-period deposit growth rates using historical data.
**Reference**: Standard central bank monitoring practices for financial stability assessment.

#### 7. **CBDC Supply Management (`update_cbdc_outstanding`)**
**Behavior**: Expands CBDC supply automatically to meet all consumer demand, ensuring no supply constraints.
**Implementation**: Monitors consumer CBDC holdings and increases supply to exactly match demand, tracks expansion metrics.
**Reference**: Demand-responsive monetary policy and modern central bank digital currency accommodation principles.

## Commercial Bank Agent Behaviors

### Core Behavioral Functions

#### 1. **Deposit Management (`update_deposits`)**
**Behavior**: Continuously tracks and updates total customer deposits from all consumer relationships.
**Implementation**: Aggregates deposits from customer list, updates balance sheet accordingly.
**Reference**: Standard banking operations and balance sheet management.

#### 2. **Lending Operations (`make_loans`)**
**Behavior**: Makes lending decisions based on available liquidity after meeting reserve requirements.
**Implementation**: Lends 80% of available funds (deposits minus 10% reserves), adjusts for CBDC uncertainty.
**Reference**: Banking lending practices and liquidity management (Basel III framework).

#### 3. **Competitive Strategy Adjustment (`adjust_competitive_strategy`)**
**Behavior**: Responds to CBDC competition by adjusting deposit interest rates to retain customers.
**Implementation**: Increases rates based on CBDC adoption pressure, maintains minimum 1% lending spread.
**Reference**: Bank competition literature - Vives, X. (2016). *Competition and stability in banking*. Princeton University Press.

#### 4. **Customer Attrition Handling (`handle_customer_attrition`)**
**Behavior**: Manages customer loss due to CBDC adoption, differentiated by bank size and customer stickiness.
**Implementation**: Large banks retain 70% of customers vs 30% for small banks during CBDC transitions.
**Reference**: Customer loyalty research - Sharma, A., & Foropon, C. (2019). *Journal of Cleaner Production*.

#### 5. **Performance Metrics Calculation (`calculate_metrics`)**
**Behavior**: Computes key financial ratios including liquidity, loan-to-deposit, profitability, and market share.
**Implementation**: Standard banking ratios with real-time updates based on customer and lending activity.
**Reference**: Banking performance measurement literature and regulatory reporting standards.

#### 6. **Network Metrics Updates (`update_network_metrics`)**
**Behavior**: Maintains network centrality scores and interbank connectivity measures for systemic risk analysis.
**Implementation**: Large banks maintain 0.8 centrality vs 0.3 for small banks, tracks interbank connections.
**Reference**: Financial network analysis - Craig, B., & Von Peter, G. (2014). *Journal of Financial Intermediation*.

#### 7. **Liquidity Stress Calculation (`calculate_liquidity_stress`)**
**Behavior**: Assesses bank-specific liquidity stress levels for hypothesis H3 testing.
**Implementation**: Combines deposit volatility, reserve ratios, and CBDC competitive pressure into stress indicator.
**Reference**: Liquidity risk management - Basel Committee guidelines on liquidity coverage ratios.

### Size-Differentiated Behaviors

#### **Large Banks**
- **Higher Customer Stickiness**: 70% retention rate during CBDC adoption
- **Lower CBDC Vulnerability**: 40% susceptibility to customer loss
- **High Network Centrality**: 0.8 connectivity score in banking network
- **Resource Advantages**: Better able to compete with CBDC through service quality

#### **Small-Medium Banks**
- **Lower Customer Stickiness**: 30% retention rate during CBDC adoption
- **Higher CBDC Vulnerability**: 80% susceptibility to customer loss
- **Low Network Centrality**: 0.3 connectivity score, peripheral position
- **Resource Constraints**: Limited ability to compete with CBDC offerings

**Reference**: Bank size effects - Berger, A. N. et al. (2009). "Bank competition and financial stability." *Journal of Financial Services Research*.

## Consumer Agent Behaviors

### Core Behavioral Functions

#### 1. **Economic Activity (`economic_activity`)**
**Behavior**: Handles regular income generation and spending patterns that affect financial portfolio.
**Implementation**: Monthly income of 2%±0.5% of wealth, spending of 1.5%±0.5%, proportional allocation.
**Reference**: Household finance literature - Federal Reserve Survey of Consumer Finances (2022).

#### 2. **CBDC Adoption Decision (`consider_cbdc_adoption`)**
**Behavior**: Complex multi-factor decision process weighing financial and social factors for CBDC adoption.
**Implementation**: Base 3% probability adjusted by interest rates, social influence, convenience, risk aversion.
**Reference**: Technology adoption models - Davis, F. D. (1989). "Technology Acceptance Model." *MIS Quarterly*.

#### 3. **Portfolio Rebalancing (`rebalance_portfolio`)**
**Behavior**: Adjusts allocation between bank deposits and CBDC based on personal preferences and market conditions.
**Implementation**: Dynamic rebalancing using CBDC preference ratio, influenced by peer behavior and interest rates.
**Reference**: Portfolio theory - Markowitz, H. (1952). "Portfolio selection." *Journal of Finance*.

#### 4. **Banking Relationship Management (`update_banking_relationship`)**
**Behavior**: Maintains and updates primary banking relationships, handles bank switching decisions.
**Implementation**: Tracks primary bank assignment, updates customer lists, manages service relationships.
**Reference**: Customer relationship management in banking - relationship banking literature.

#### 5. **CBDC Adoption Process (`adopt_cbdc`)**
**Behavior**: Executes the transition to CBDC user status with initial portfolio allocation.
**Implementation**: Sets adopter flag, records adoption timing, initiates portfolio rebalancing.
**Reference**: Innovation diffusion theory - Rogers, E. M. (2003). *Diffusion of innovations*.

### Decision-Making Factors

#### **Interest Rate Sensitivity**
**Behavior**: Consumers respond to interest rate differentials between bank deposits (2%) and CBDC (1%).
**Parameter**: Interest sensitivity ~ Normal(0.5, 0.2), multiplied by rate advantage.
**Reference**: Interest rate elasticity studies - Hutchison, D. E., & Pennacchi, G. G. (1996). *Journal of Financial and Quantitative Analysis*.

#### **Social Influence Effects**
**Behavior**: Adoption decisions influenced by peer adoption rates with network effects and momentum.
**Parameter**: Social weight ~ Normal(0.3, 0.1), amplified by adoption momentum over time.
**Reference**: Social learning - Banerjee, A. V. (1992). "A simple model of herd behavior." *Quarterly Journal of Economics*.

#### **Risk Aversion Impact**
**Behavior**: Higher risk aversion reduces CBDC adoption probability, moderated by banking system stress.
**Parameter**: Risk aversion ~ Normal(0.5, 0.2), constrained [0.1, 0.9].
**Reference**: Risk preferences - Holt, C. A., & Laury, S. K. (2002). "Risk aversion and incentive effects." *American Economic Review*.

#### **Bank Loyalty Factor**
**Behavior**: Loyalty to traditional banking reduces CBDC adoption, weakened during banking stress periods.
**Parameter**: Bank loyalty ~ Normal(0.7, 0.2), reduced by bank liquidity stress.
**Reference**: Customer loyalty literature - brand attachment and switching costs.

#### **Convenience Preference**
**Behavior**: Preference for convenient payment methods increases CBDC adoption likelihood.
**Parameter**: Convenience preference ~ Normal(0.5, 0.2), provides adoption boost.
**Reference**: Technology acceptance and ease-of-use factors.

#### **Banking System Stress Response**
**Behavior**: Consumers switch to CBDC when their primary bank shows signs of liquidity stress.
**Implementation**: Bank stress level directly increases adoption probability by up to 15%.
**Reference**: Flight-to-quality behavior during financial stress periods.

### Wealth Management Behaviors

#### **Initial Wealth Allocation**
- **Bank Deposits**: 37% of $5,000 initial wealth ($1,850)
- **Other Assets**: 63% of wealth ($3,150) in savings, investments, cash
- **CBDC Holdings**: 0% initially, grows with adoption
**Reference**: Federal Reserve Survey of Consumer Finances - household liquid asset allocation.

#### **Income Allocation Rules**
**Pre-CBDC**: All new income flows to bank deposits
**Post-CBDC Adoption**: Income split between bank deposits and CBDC based on preference ratio
**Reference**: Household cash management literature.

#### **Spending Patterns**
**Behavior**: Proportional spending reduces both bank deposits and CBDC holdings equally.
**Implementation**: Spending rate affects all liquid holdings proportionally to maintain allocation preferences.
**Reference**: Consumption smoothing theory.

## Model-Level Coordination Behaviors

### **Network Effects Amplification**
**Behavior**: CBDC attractiveness increases with adoption rate creating positive feedback loops.
**Implementation**: Network effect factor = 1 + (adoption_rate × 0.5).
**Reference**: Network externalities literature - increasing returns to adoption.

### **Market Condition Adjustments**
**Behavior**: Model adjusts market-wide conditions based on CBDC adoption and banking sector response.
**Implementation**: Banks collectively adjust interest rates, central bank monitors systemic metrics.
**Reference**: General equilibrium effects in financial markets.

### **Systemic Risk Threshold Management**
**Behavior**: Central bank intervention triggers when banking system health falls below 30% threshold.
**Implementation**: Automatic support mechanisms activate to prevent banking system collapse.
**Reference**: Central bank crisis management and lender-of-last-resort functions.

## Behavioral Assumptions and Limitations

### **Perfect Information Assumption**
**Assumption**: All agents have complete information about interest rates and CBDC availability.
**Limitation**: Real-world information asymmetries and search costs not modeled.
**Reference**: Information economics literature on market efficiency.

### **Rational Choice with Behavioral Elements**
**Assumption**: Agents optimize decisions but include behavioral factors like social influence and risk aversion.
**Implementation**: Combines utility maximization with psychological and social factors.
**Reference**: Behavioral economics - Kahneman, D., & Tversky, A. (1979). "Prospect theory." *Econometrica*.

### **Static Preference Parameters**
**Assumption**: Individual preference parameters (risk aversion, social influence) remain constant over time.
**Limitation**: Preference evolution and learning effects not captured.
**Reference**: Preference stability assumptions in economic modeling.

### **Simplified Banking Operations**
**Assumption**: Banking operations reduced to deposit-taking and lending with fixed spreads.
**Limitation**: Complex banking products, fee income, and operational costs not modeled.
**Reference**: Banking theory simplifications for tractability.

## Academic Foundation Summary

### **Primary Literature Streams**
1. **CBDC Economic Impact**: Central bank research on digital currency effects
2. **Agent-Based Financial Modeling**: Multi-agent systems in finance
3. **Banking Competition**: Industrial organization in banking markets
4. **Technology Adoption**: Diffusion of innovations and network effects
5. **Behavioral Finance**: Psychology in financial decision-making
6. **Systemic Risk**: Financial stability and interconnectedness

### **Empirical Calibration Sources**
- **Federal Reserve Survey of Consumer Finances**: Household wealth data
- **Basel III Guidelines**: Banking regulatory parameters
- **Central Bank CBDC Research**: Policy proposals and pilot studies
- **Banking Industry Data**: Market structure and performance metrics
- **Experimental Economics**: Risk preferences and social learning

---

*This document provides the complete behavioral specification for all agents in the CBDC banking simulation, grounded in academic literature and empirical evidence where available.*