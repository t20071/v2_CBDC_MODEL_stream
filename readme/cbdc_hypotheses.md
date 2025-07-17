# CBDC Banking Simulation: Complete Hypothesis Framework

## Overview
This document presents all hypotheses being tested in the CBDC banking simulation, with their theoretical foundations, operational definitions, and measurement approaches.

## Hypothesis H1: Differential Network Centrality Impact

### **Statement**
CBDC introduction disproportionately reduces network centrality for small-medium banks compared to large banks, creating a more concentrated banking network structure.

### **Theoretical Foundation**
- Large banks have superior resources and customer loyalty to compete with CBDC
- Small banks face higher vulnerability due to limited competitive capabilities
- Network effects amplify advantages for systemically important institutions

### **Operational Definition**
- **Large Banks**: 20% of institutions holding 60% of market capital, initial centrality 0.8
- **Small-Medium Banks**: 80% of institutions holding 40% of market capital, initial centrality 0.3
- **Centrality Loss**: Economic centrality based on market position and customer relationships

### **Measurement Approach**
```python
# Large bank centrality tracking
large_bank_centrality = sum(bank.network_centrality for bank in large_banks) / len(large_banks)

# Small bank centrality tracking  
small_bank_centrality = sum(bank.network_centrality for bank in small_banks) / len(small_banks)

# Differential impact measurement
centrality_gap = large_bank_centrality - small_bank_centrality
```

### **Expected Results**
- Large banks maintain higher centrality (0.6-0.8 range)
- Small banks experience steeper centrality decline (0.3 → 0.1-0.2 range)
- Increasing centrality gap over time post-CBDC introduction

### **Policy Implications**
Market concentration, systemic risk from "too big to fail" institutions, potential need for regulatory intervention

---

## Hypothesis H3: Systemic Liquidity Stress

### **Statement**
Rapid CBDC adoption creates systemic liquidity stress in the commercial banking sector, particularly during periods of accelerated consumer switching.

### **Theoretical Foundation**
- Bank runs and deposit flight amplified by digital currency convenience
- Liquidity stress concentrates in vulnerable institutions
- Network effects accelerate stress contagion across banking system

### **Operational Definition**
- **Liquidity Stress**: Composite measure of deposit volatility, reserve adequacy, and competitive pressure
- **Systemic Risk Threshold**: >30% of banks showing high stress levels
- **Crisis Periods**: Sustained stress levels above 0.7 threshold

### **Measurement Approach**
```python
# Bank-level stress calculation
customer_loss_rate = 1 - self.customer_retention_rate
deposit_volatility = abs(recent_deposits - previous_deposits) / previous_deposits
competitive_pressure = cbdc_adoption_rate * self.cbdc_vulnerability
liquidity_stress = (customer_loss_rate + deposit_volatility + competitive_pressure) / 3

# System-wide stress aggregation
average_liquidity_stress = sum(bank.liquidity_stress_level) / len(banks)
```

### **Expected Results**
- Stress levels spike during rapid CBDC adoption phases (>20% adoption)
- Small banks show higher and more persistent stress
- Potential stress-induced central bank intervention

### **Policy Implications**
Need for enhanced liquidity monitoring, potential lender-of-last-resort facilities, stress testing requirements

---

## Hypothesis H4: Banking Network Connectivity Decline

### **Statement**
CBDC weakens traditional interbank network connections as direct central bank-consumer relationships reduce intermediation needs.

### **Theoretical Foundation**
- CBDC provides alternative to traditional interbank settlement
- Direct central bank relationships bypass commercial banking networks
- Reduced intermediation decreases interbank dependency

### **Operational Definition**
- **Network Density**: Ratio of actual interbank connections to maximum possible connections
- **Connection Baseline**: Large banks 60% connected, small banks 30% connected initially
- **CBDC Threshold**: Significant decline when adoption exceeds 20%

### **Measurement Approach**
```python
# Network density calculation
total_connections = sum(bank.interbank_connections for bank in banks)
max_possible = len(banks) * (len(banks) - 1)
network_density = total_connections / max_possible

# Dynamic connection reduction
if cbdc_adoption_rate > 0.2:
    connection_impact = (cbdc_adoption_rate - 0.2) * 0.15
    connection_loss = connection_impact * 0.1
    bank.interbank_connections = max(0, bank.interbank_connections - connection_loss)
```

### **Expected Results**
- Steady network density decline post-CBDC introduction
- Accelerated decline when CBDC adoption exceeds 20%
- Small banks lose connections faster than large banks

### **Policy Implications**
Changes in payment system infrastructure, potential for network fragmentation, implications for monetary policy transmission

---

## Hypothesis H6: Central Bank Network Dominance

### **Statement**
CBDC transforms the central bank from a peripheral regulatory entity into the dominant node in the financial network through direct consumer relationships.

### **Theoretical Foundation**
- CBDC creates direct central bank-consumer connections bypassing commercial banks
- Monopoly CBDC issuer position provides structural network advantage
- Market share growth translates to network centrality dominance

### **Operational Definition**
- **Initial Centrality**: Central bank starts at 0.1 (minimal regulatory role)
- **CBDC-Driven Growth**: Centrality increases with adoption rate and market share
- **Dominance Threshold**: Central bank centrality exceeds average commercial bank centrality

### **Measurement Approach**
```python
# Central bank centrality calculation
base_centrality = 0.1
adoption_boost = cbdc_adoption * 0.6      # Up to 60% from adoption
market_boost = cbdc_market_share * 0.4    # Up to 40% from market share  
monopoly_boost = min(0.2, cbdc_adoption * 0.3) if cbdc_adoption > 0.3 else 0

central_bank_centrality = base_centrality + adoption_boost + market_boost + monopoly_boost

# Dominance ratio measurement
dominance_ratio = central_bank_centrality / average_commercial_bank_centrality
```

### **Expected Results**
- Central bank centrality grows from 0.1 to 0.8+ with high CBDC adoption
- Dominance ratio exceeds 2x-3x commercial bank average
- Network topology shift from bank-centric to central bank-centric

### **Policy Implications**
Fundamental change in monetary system architecture, central bank operational responsibilities, financial stability oversight requirements

---

## Hypotheses H2 and H5: Implementation Notes

### **H2: Small Bank Vulnerability**
- **Embedded in H1**: Small banks modeled with 80% CBDC vulnerability vs 40% for large banks
- **Customer Stickiness**: 30% retention for small banks vs 70% for large banks
- **Resource Constraints**: Limited ability to compete on rates and service quality

### **H5: Systemic Importance Integration**
- **Network Effects**: Bank centrality influences systemic importance scoring
- **Stress Propagation**: Highly connected banks can amplify or contain systemic stress
- **Regulatory Response**: Central bank intervention triggered by systemic importance metrics

---

## Hypothesis Testing Framework

### **Experimental Design**
- **Baseline Period**: 30 steps (2.5 years) pre-CBDC to establish market structure
- **Intervention**: CBDC introduction at step 30 with demand-driven supply
- **Observation Period**: 90-120 steps (7.5-10 years) post-introduction
- **Controls**: Traditional banking parameters held constant

### **Statistical Measures**
- **Trend Analysis**: Time series of key metrics before/after CBDC
- **Comparative Analysis**: Large vs small bank performance differentials
- **Threshold Effects**: Behavioral changes at critical adoption levels
- **Correlation Analysis**: Relationships between adoption, stress, and network metrics

### **Validation Criteria**
- **H1 Support**: Increasing centrality gap between large and small banks
- **H3 Support**: Stress peaks during rapid adoption phases, recovery patterns
- **H4 Support**: Monotonic decline in network density post-CBDC
- **H6 Support**: Central bank centrality exceeding commercial bank average

### **Robustness Checks**
- **Parameter Sensitivity**: Testing different CBDC attractiveness levels
- **Adoption Scenarios**: Slow vs rapid adoption pathways
- **Market Structure**: Alternative bank size distributions
- **Policy Interventions**: Central bank support mechanisms

---

## Academic Foundations

### **Network Theory Literature**
- **Financial Networks**: Acemoglu et al. (2015) on network effects in banking
- **Centrality Measures**: Bonacich (1987) on power centrality in social networks
- **Contagion Models**: Allen & Gale (2000) on financial contagion mechanisms

### **Banking Competition Studies**
- **Size Effects**: Berger et al. (2009) on competition and bank size
- **Digital Disruption**: Vives (2019) on fintech and banking competition
- **Market Structure**: Claessens & Laeven (2004) on banking concentration

### **CBDC Research**
- **Intermediation Effects**: Fernández-Villaverde et al. (2020) on CBDC competition
- **Network Implications**: Meaning et al. (2021) on CBDC system design
- **Stability Concerns**: Kumhof & Noone (2018) on CBDC risks

### **Monetary Policy Framework**
- **Transmission Mechanisms**: Bernanke & Gertler (1995) on credit channels
- **Network Effects**: Adrian & Shin (2010) on monetary policy and financial networks
- **Central Bank Operations**: Bindseil (2004) on monetary policy implementation

---

## Expected Research Contributions

### **Theoretical Insights**
- Quantification of CBDC impact on banking network structure
- Identification of critical adoption thresholds for systemic effects
- Framework for analyzing central bank network dominance

### **Policy Applications**
- Stress testing scenarios for CBDC implementation
- Regulatory preparedness for network structure changes
- Central bank operational readiness assessment

### **Methodological Advances**
- Agent-based modeling of monetary system transformation
- Network analysis techniques for financial system evolution
- Integration of behavioral and structural economic factors

---

*This hypothesis framework provides the foundation for comprehensive testing of CBDC impacts on commercial banking intermediation through agent-based simulation modeling.*