# CBDC Banking Simulation: Initial Conditions and References

## Overview
This document provides comprehensive documentation of all initial conditions for the CBDC banking simulation model, including specific parameter values, distributions, and academic references that justify these choices.

## Model-Level Initial Conditions

### 1. Simulation Parameters
| Parameter | Default Value | Range | Reference |
|-----------|---------------|-------|-----------|
| Number of Consumers | 200 | 50-500 | Typical ABM population size (Epstein, 2006) |
| Number of Commercial Banks | 8 | 3-15 | US banking market structure (FDIC, 2023) |
| Simulation Steps | 200 | 50-500 | Monthly time steps for 16+ years analysis |
| CBDC Introduction Step | 30 | 10-100 | Allows pre-CBDC baseline establishment |

**References:**
- Epstein, J. M. (2006). *Generative social science: Studies in agent-based computational modeling*. Princeton University Press.
- FDIC (2023). "Banking Market Share Statistics." Federal Deposit Insurance Corporation.

### 2. Economic Environment
| Parameter | Value | Justification | Reference |
|-----------|-------|---------------|-----------|
| Initial Consumer Wealth | $5,000 | Median liquid assets for middle-income households | SCF (2022) |
| Bank Interest Rate | 2.0% | Post-GFC low interest rate environment | Federal Reserve (2020-2024) |
| CBDC Interest Rate | 1.0% | Competitive but lower than bank deposits | Meaning et al. (2021) |
| CBDC Adoption Rate | 3.0% | Conservative adoption assumption | Auer & Böhme (2020) |
| CBDC Attractiveness | 1.5 | Network effects multiplier | Kahn et al. (2021) |

**References:**
- Survey of Consumer Finances (SCF) (2022). Federal Reserve Board.
- Meaning, J., et al. (2021). "Broadening narrow money: monetary policy with a central bank digital currency." *Bank of England Working Paper No. 724*.
- Auer, R., & Böhme, R. (2020). "The technology of retail central bank digital currency." *BIS Quarterly Review*.
- Kahn, C. M., Rivadeneyra, F., & Wong, T. N. (2021). "Should the central bank issue e-money?" *Journal of Economic Theory*, 194, 105244.

### 3. Network Structure
| Parameter | Value | Rationale | Reference |
|-----------|-------|-----------|-----------|
| Network Type | Erdős-Rényi | Standard for financial networks | Erdős & Rényi (1960) |
| Connection Probability | 10% | Sparse but connected network | Newman (2010) |
| Total Network Nodes | n_consumers + n_banks + 1 | All agents + central bank | ABM standard |

**References:**
- Erdős, P., & Rényi, A. (1960). "On the evolution of random graphs." *Publications of the Mathematical Institute of the Hungarian Academy of Sciences*.
- Newman, M. (2010). *Networks: an introduction*. Oxford University Press.

## Central Bank Initial Conditions

### Core Parameters
| Attribute | Initial Value | Source/Reference |
|-----------|---------------|------------------|
| Unique ID | 0 | Model convention |
| CBDC Interest Rate | 1.0% (configurable) | Central bank CBDC proposals |
| CBDC Supply | 0 | No CBDC pre-introduction |
| CBDC Outstanding | 0 | No circulation initially |
| CBDC Introduced | False | Introduction at specified step |

### Policy Framework
| Parameter | Value | Justification | Reference |
|-----------|-------|---------------|-----------|
| Monetary Policy Rate | 2.0% | Federal funds rate approximation | FOMC (2020-2024) |
| CBDC Attractiveness | 1.0 | Baseline, grows with adoption | Network effects literature |
| Financial Stability Target | 0.8 (80%) | Basel III stability metrics | Basel Committee (2017) |
| Inflation Target | 2.0% | Standard central bank mandate | Taylor (1993) |

### Monitoring Metrics
| Metric | Initial Value | Reference |
|--------|---------------|-----------|
| Banking System Health | 1.0 (100%) | Perfect initial state |
| CBDC Adoption Rate | 0% | Pre-introduction |
| Systemic Risk Level | 0% | Stable initial conditions |

**References:**
- FOMC (2020-2024). Federal Open Market Committee meeting minutes.
- Basel Committee on Banking Supervision (2017). "Basel III: Finalising post-crisis reforms."
- Taylor, J. B. (1993). "Discretion versus policy rules in practice." *Carnegie-Rochester Conference Series on Public Policy*.

## Commercial Bank Initial Conditions

### Bank Size Distribution
**Market Structure Assumption:** 80/20 rule reflecting banking concentration

| Bank Type | Proportion | Market Capital Share | Reference |
|-----------|------------|---------------------|-----------|
| Large Banks | 20% of institutions | 60% of total capital | Banking concentration studies |
| Small-Medium Banks | 80% of institutions | 40% of total capital | Berger et al. (2009) |

**Reference:** Berger, A. N., Klapper, L. F., & Turk-Ariss, R. (2009). "Bank competition and financial stability." *Journal of Financial Services Research*.

### Large Banks Initial Conditions
| Attribute | Value | Calculation | Reference |
|-----------|-------|-------------|-----------|
| Bank Type | "large" | Classification | Industry standard |
| Initial Capital | 60% market ÷ large banks | $480,000 per bank (8 banks) | Market concentration data |
| Network Centrality | 0.8 | High connectivity | Financial network analysis |
| Interest Rate | 2.0% | Market rate | Deposit rate surveys |
| Lending Rate | 5.0% | Deposit rate + 3% | Banking spread literature |
| Reserve Requirement | 10% | Regulatory standard | Basel III |
| Initial Reserves | 20% of capital | Conservative liquidity | Bank management practices |
| CBDC Vulnerability | 0.4 (40%) | Lower due to resources | Competitive advantage |
| Customer Stickiness | 0.7 (70%) | Brand loyalty | Customer retention studies |

### Small-Medium Banks Initial Conditions
| Attribute | Value | Calculation | Reference |
|-----------|-------|-------------|-----------|
| Bank Type | "small_medium" | Classification | Size-based categorization |
| Initial Capital | 40% market ÷ small banks | $120,000 per bank (6 banks) | Market structure |
| Network Centrality | 0.3 | Lower connectivity | Periphery position |
| Interest Rate | 2.0% | Market rate | Rate parity assumption |
| Lending Rate | 5.0% | Deposit rate + 3% | Standard spread |
| Reserve Requirement | 10% | Same regulation | Regulatory uniformity |
| Initial Reserves | 20% of capital | Conservative approach | Risk management |
| CBDC Vulnerability | 0.8 (80%) | Higher due to limited resources | Competitive disadvantage |
| Customer Stickiness | 0.3 (30%) | Lower loyalty | Size effect on retention |

### Common Bank Attributes
| Attribute | Initial Value | Rationale |
|-----------|---------------|-----------|
| Total Deposits | 0 | No customers initially |
| Total Loans | 0 | No lending activity |
| Liquidity Ratio | 1.0 | Perfect liquidity |
| Loan-to-Deposit Ratio | 0.0 | No deposits yet |
| Market Share | 0% | Calculated dynamically |
| Customer Retention Rate | 100% | No attrition initially |
| Interbank Connections | Size-dependent | Network topology |

**References:**
- Demirgüç-Kunt, A., & Huizinga, H. (1999). "Determinants of commercial bank interest margins and profitability." *The World Bank Economic Review*.
- Stiroh, K. J., & Rumble, A. (2006). "The dark side of diversification: The case of US financial holding companies." *Journal of Banking & Finance*.

## Consumer Initial Conditions

### Wealth Allocation (Empirically Grounded)
| Asset Category | Initial Allocation | Dollar Amount | Reference |
|----------------|-------------------|---------------|-----------|
| Bank Deposits | 37% | $1,850 | Federal Reserve SCF data |
| CBDC Holdings | 0% | $0 | Not available initially |
| Other Assets | 63% | $3,150 | Savings, investments, cash |
| **Total Wealth** | **100%** | **$5,000** | **Median liquid assets** |

**Reference:** Federal Reserve (2022). "Survey of Consumer Finances." Board of Governors of the Federal Reserve System.

### Demographic and Behavioral Parameters

#### Core Characteristics
| Attribute | Distribution | Parameters | Range | Reference |
|-----------|-------------|------------|--------|-----------|
| Initial Wealth | Fixed | $5,000 | Constant | SCF median |
| Risk Aversion | Normal | μ=0.5, σ=0.2 | [0.1, 0.9] | Holt & Laury (2002) |
| CBDC Adoption Probability | Fixed | 3% | Base rate | Technology adoption literature |

#### Decision-Making Parameters
| Parameter | Distribution | Mean | Std Dev | Range | Reference |
|-----------|-------------|------|---------|--------|-----------|
| Interest Sensitivity | Normal | 0.5 | 0.2 | [0.1, 0.9] | Interest elasticity studies |
| Convenience Preference | Normal | 0.5 | 0.2 | [0.1, 0.9] | Technology acceptance model |
| Bank Loyalty | Normal | 0.7 | 0.2 | [0.1, 0.95] | Customer loyalty research |
| Social Influence Weight | Normal | 0.3 | 0.1 | [0.0, 0.6] | Social learning literature |

#### Economic Activity
| Parameter | Distribution | Mean | Std Dev | Range | Unit |
|-----------|-------------|------|---------|--------|------|
| Income Rate | Normal | 2% | 0.5% | [1%, 5%] | Monthly |
| Spending Rate | Normal | 1.5% | 0.5% | [0.5%, 3%] | Monthly |

**References:**
- Holt, C. A., & Laury, S. K. (2002). "Risk aversion and incentive effects." *American Economic Review*, 92(5), 1644-1655.
- Davis, F. D. (1989). "Perceived usefulness, perceived ease of use, and user acceptance of information technology." *MIS Quarterly*, 13(3), 319-340.
- Sharma, A., & Foropon, C. (2019). "Green product attributes and green purchase behavior." *Journal of Cleaner Production*, 219, 849-874.

### Banking Relationships
| Attribute | Initial Value | Assignment Method | Reference |
|-----------|---------------|-------------------|-----------|
| Primary Bank | Random assignment | Uniform distribution | Market entry modeling |
| CBDC Adopter | False | Pre-introduction | Technology lifecycle |
| CBDC Available | False | Not introduced yet | Sequential adoption |
| Adoption Step | None | Future determination | Diffusion timing |

### Network and Social Factors
| Factor | Modeling Approach | Reference |
|--------|-------------------|-----------|
| Peer Influence | Global adoption rate | Simplified social network |
| Social Learning | Adoption rate momentum | Banerjee (1992) |
| Network Effects | Increasing returns to adoption | Katz & Shapiro (1985) |

**References:**
- Banerjee, A. V. (1992). "A simple model of herd behavior." *The Quarterly Journal of Economics*, 107(3), 797-817.
- Katz, M. L., & Shapiro, C. (1985). "Network externalities, competition, and compatibility." *The American Economic Review*, 75(3), 424-440.

## Inter-Agent Connections and Relationships

### Consumer-Bank Assignment
| Assignment Rule | Method | Rationale |
|-----------------|--------|-----------|
| Initial Bank Selection | Random uniform | No initial preferences |
| Customer Lists | Maintained by banks | Relationship tracking |
| Switching Mechanism | Preference-based | Market dynamics |

### Banking Network (H4 Analysis)
| Bank Type | Target Connections | Percentage | Reference |
|-----------|-------------------|------------|-----------|
| Large Banks | 60% of all banks | High connectivity | Core-periphery structure |
| Small Banks | 30% of all banks | Lower connectivity | Network periphery |

**Reference:** Craig, B., & Von Peter, G. (2014). "Interbank tiering and money center banks." *Journal of Financial Intermediation*.

### Central Bank Network Position
| Connection Type | Initial State | Post-CBDC | Reference |
|-----------------|---------------|-----------|-----------|
| To Commercial Banks | Regulatory oversight | Competition monitor | Central bank functions |
| To Consumers | None | Direct CBDC relationship | Digital currency literature |
| Network Centrality | 0.1 (minimal) | Dynamic growth | Network dominance |

## Data Collection and Validation

### Model-Level Metrics
| Metric | Initial Value | Purpose |
|--------|---------------|---------|
| CBDC Adoption Rate | 0% | Track diffusion |
| Total CBDC Holdings | $0 | Market penetration |
| Total Bank Deposits | 37% × total wealth | Baseline measurement |
| Banking Network Density | Calculated | H4 hypothesis testing |

### Agent-Level Tracking
| Agent Type | Key Metrics | Initial States |
|------------|-------------|----------------|
| Central Bank | Policy rates, CBDC supply | Stable, inactive |
| Commercial Banks | Deposits, loans, liquidity | Empty, liquid |
| Consumers | Wealth allocation, adoption | Bank-focused |

## Sensitivity Analysis Parameters

### Critical Assumptions for Testing
1. **37% Bank Deposit Allocation** - Test range: 25-50%
2. **3% CBDC Adoption Rate** - Test range: 1-10%
3. **80/20 Bank Size Distribution** - Test alternative structures
4. **Interest Rate Differentials** - Test various spreads
5. **Social Influence Weights** - Test network effects

### Robustness Checks
| Parameter | Base Value | Test Range | Sensitivity Impact |
|-----------|------------|------------|-------------------|
| Consumer Wealth | $5,000 | $1,000-$20,000 | Scale effects |
| Bank Capital | Market-based | ±50% variation | Concentration effects |
| Network Density | 10% | 5-25% | Connectivity impact |
| CBDC Introduction Timing | Step 30 | Steps 10-60 | Timing effects |

## Academic Foundation Summary

### Key Literature Streams
1. **Agent-Based Financial Modeling**: Farmer & Foley (2009), Delli Gatti et al. (2011)
2. **CBDC Economic Impact**: Meaning et al. (2021), Fernández-Villaverde et al. (2020)
3. **Banking Market Structure**: Berger et al. (2009), Claessens & Laeven (2004)
4. **Consumer Finance**: Federal Reserve SCF, ECB HFCS
5. **Network Economics**: Erdős & Rényi (1960), Katz & Shapiro (1985)
6. **Behavioral Finance**: Kahneman & Tversky (1979), Holt & Laury (2002)

### Validation Data Sources
- **Federal Reserve Survey of Consumer Finances** (household wealth)
- **FDIC Banking Statistics** (market structure)
- **Basel Committee Guidelines** (regulatory parameters)
- **Central Bank Research** (CBDC proposals)
- **Academic Literature** (behavioral parameters)

## Model Calibration Notes

### Empirically Grounded Parameters
- Consumer wealth allocation (37% deposits)
- Interest rate environment (2% deposit, 1% CBDC)
- Banking market concentration (80/20 rule)
- Reserve requirements (10% regulatory)

### Stylized Parameters
- Network connection probabilities
- Behavioral parameter distributions
- CBDC attractiveness factors
- Social influence weights

### Future Calibration Opportunities
1. **Real CBDC pilot data** when available
2. **Updated household finance surveys**
3. **Central bank policy announcements**
4. **Banking industry responses to digital currencies**

---

*This document provides the academic foundation for all initial conditions in the CBDC banking simulation model. Parameters are based on empirical data where available and established literature for behavioral and network assumptions.*