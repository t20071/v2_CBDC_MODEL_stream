# Network Centrality Measures in CBDC Banking Simulation

## Overview

The CBDC Banking Simulation now includes comprehensive network centrality analysis with four key centrality measures that provide different perspectives on agent importance and influence within the financial network.

## Centrality Measures Implemented

### 1. Degree Centrality
**Definition**: Measures the number of direct connections an agent has in the network.

**Implementation**:
- **Commercial Banks**: Based on direct customer relationships and interbank connections
- **Central Bank**: Grows with CBDC adoption as direct consumer relationships increase
- **Range**: 0.0 to 1.0

**Interpretation**:
- **Large Banks**: Start at ~0.85, representing extensive branch networks and customer bases
- **Small Banks**: Start at ~0.35, representing limited customer reach
- **Central Bank**: Starts at 0.05, grows to ~0.85 with widespread CBDC adoption

**CBDC Impact**: Direct connections increase for central bank, decrease for commercial banks as customers switch to CBDC

### 2. Betweenness Centrality
**Definition**: Measures how often an agent acts as a bridge along the shortest path between two other agents.

**Implementation**:
- **Commercial Banks**: Reflects role as intermediaries in financial flows
- **Central Bank**: Becomes the dominant intermediary with CBDC introduction
- **Range**: 0.0 to 1.0

**Interpretation**:
- **Large Banks**: Start at ~0.90, representing key intermediary roles
- **Small Banks**: Start at ~0.25, limited intermediation capacity
- **Central Bank**: Starts at 0.08, grows to ~0.93 with CBDC dominance

**CBDC Impact**: Highest impact measure - CBDC bypasses traditional intermediation, drastically reducing bank betweenness while increasing central bank's

### 3. Closeness Centrality
**Definition**: Measures how close an agent is to all other agents in the network (inverse of average shortest path).

**Implementation**:
- **Commercial Banks**: Proximity to customers and other financial institutions
- **Central Bank**: Benefits from central position in monetary system
- **Range**: 0.0 to 1.0

**Interpretation**:
- **Large Banks**: Start at ~0.80, representing good access to financial network
- **Small Banks**: Start at ~0.45, more peripheral positions
- **Central Bank**: Starts at 0.12, grows to ~0.82 with CBDC network effects

**CBDC Impact**: Moderate impact - central bank gains closeness while commercial banks become more peripheral

### 4. Eigenvector Centrality
**Definition**: Measures influence based on connections to other influential agents (network effects).

**Implementation**:
- **Commercial Banks**: Influence through connections to important customers and institutions
- **Central Bank**: Amplified influence through CBDC network dominance
- **Range**: 0.0 to 1.0

**Interpretation**:
- **Large Banks**: Start at ~0.88, representing high influence in financial system
- **Small Banks**: Start at ~0.30, limited influence networks
- **Central Bank**: Starts at 0.06, grows to ~0.96 with CBDC network effects

**CBDC Impact**: High impact - network effects amplify central bank influence while reducing commercial bank influence

## Network Dynamics and CBDC Impact

### Pre-CBDC Network Structure
- **Large Banks**: Dominant across all centrality measures
- **Small Banks**: Lower centrality, more vulnerable positions
- **Central Bank**: Minimal network presence, regulatory role only

### Post-CBDC Network Evolution
- **Centrality Decay**: Commercial banks lose centrality as CBDC provides alternative pathways
- **Differential Impact**: Small banks lose centrality faster than large banks (2x multiplier)
- **Central Bank Rise**: Central bank becomes dominant network node through direct CBDC relationships

### Critical Thresholds
- **20% CBDC Adoption**: Significant impact on network connectivity begins
- **30% CBDC Adoption**: Central bank gains monopoly position boost
- **50%+ CBDC Adoption**: Network topology fundamentally shifts to central bank-centric

## Hypothesis Testing with Centrality Measures

### H1: Differential Network Centrality Impact
- **Primary Measure**: General network centrality
- **Supporting Measures**: All four centrality types show consistent patterns
- **Evidence**: Increasing centrality gap between large and small banks

### H6: Central Bank Network Dominance
- **Key Indicators**: All centrality measures for central bank
- **Dominance Threshold**: Central bank centrality exceeding commercial bank average
- **Network Transformation**: Shift from distributed to centralized network topology

## Data Collection and Analysis

### Model-Level Tracking
- Average centrality for each measure across commercial banks
- Separate tracking for large vs small banks
- Complete central bank centrality evolution
- Real-time calculation during simulation steps

### Visualization Features
- Individual centrality measure time series
- Comparative analysis between bank types
- Central bank dominance progression
- Multi-measure summary dashboard

## Technical Implementation

### Agent-Level Calculations
```python
# Commercial Bank centrality update
def update_all_centrality_measures(self, cbdc_adoption_rate, customer_loss_rate):
    base_impact = cbdc_adoption_rate * self.cbdc_vulnerability * (1 + customer_loss_rate)
    
    # Different decay rates for different measures
    degree_decay = min(0.08, base_impact * 0.04)
    betweenness_decay = min(0.10, base_impact * 0.05)  # Highest impact
    closeness_decay = min(0.06, base_impact * 0.03)
    eigenvector_decay = min(0.07, base_impact * 0.035)
```

### Central Bank Centrality Growth
```python
# Central bank centrality increase with CBDC
def update_centrality_measures(self):
    adoption_boost = self.cbdc_adoption_rate * 0.8  # Strong growth
    market_boost = cbdc_market_share * 0.4
    monopoly_boost = min(0.2, self.cbdc_adoption_rate * 0.3)
```

## Research Applications

### Academic Contributions
- **Network Theory**: Empirical demonstration of centrality measure evolution during monetary system transition
- **Digital Currency Research**: Quantification of CBDC impact on financial network structure
- **Banking Economics**: Evidence of differential impacts on bank types and systemic importance

### Policy Implications
- **Regulatory Preparedness**: Understanding network changes for supervision frameworks
- **Systemic Risk Assessment**: New centrality-based metrics for financial stability
- **CBDC Design**: Insights for managing network effects and concentration risks

## Future Enhancements

### Potential Extensions
- **Dynamic Network Topology**: Real-time network graph visualization
- **Centrality Correlation Analysis**: Relationships between different measures
- **Stress Testing**: Centrality impacts under extreme CBDC adoption scenarios
- **Comparative Analysis**: Different CBDC design impacts on network structure

### Research Questions
- How do different CBDC interest rates affect centrality evolution?
- What network structures emerge under different adoption speeds?
- How do regulatory interventions modify centrality dynamics?
- What are the long-term equilibrium network configurations?

## Usage in Simulation

The enhanced centrality measures are automatically calculated during simulation and displayed in the "Centrality Analysis" tab, providing comprehensive insights into network evolution during CBDC introduction and adoption.