# CBDC Banking Simulation: Agent Interaction Mermaid Charts

## Main Agent Interaction Flow

```mermaid
graph TB
    %% Agent Definitions
    CB[Central Bank<br/>💎 CBDC Issuer<br/>Monetary Policy]
    LB[Large Banks<br/>🏛️ 20% of institutions<br/>60% market capital]
    SB[Small-Medium Banks<br/>🏪 80% of institutions<br/>40% market capital]
    C[Consumers<br/>👥 Portfolio Managers<br/>Adoption Decision Makers]
    
    %% Central Bank to Banks
    CB -->|Monetary Policy<br/>Interest Rates<br/>Regulatory Oversight| LB
    CB -->|Monetary Policy<br/>Interest Rates<br/>Regulatory Oversight| SB
    CB -->|CBDC Competition<br/>Market Disruption<br/>Systemic Risk Monitor| LB
    CB -->|CBDC Competition<br/>Market Disruption<br/>Systemic Risk Monitor| SB
    
    %% Central Bank to Consumers
    CB -->|CBDC Issuance<br/>1% Interest Rate<br/>Adoption Incentives| C
    CB -->|Digital Currency<br/>Convenience Features<br/>Network Effects| C
    
    %% Banks to Consumers
    LB -->|Deposit Services 2%<br/>Loan Products 5%<br/>Traditional Banking| C
    SB -->|Deposit Services 2%<br/>Loan Products 5%<br/>Traditional Banking| C
    LB -->|High Customer Stickiness 70%<br/>Brand Loyalty<br/>Service Quality| C
    SB -->|Low Customer Stickiness 30%<br/>Limited Resources<br/>Vulnerability| C
    
    %% Consumer Feedback
    C -->|Deposit Flows $1,850<br/>Customer Attrition<br/>Service Demand| LB
    C -->|Deposit Flows $1,850<br/>Customer Attrition<br/>Service Demand| SB
    C -->|CBDC Adoption 3%<br/>Usage Patterns<br/>Market Response| CB
    
    %% Interbank Relationships
    LB -.->|Interbank Lending<br/>60% Network Connectivity<br/>High Centrality 0.8| SB
    SB -.->|Interbank Borrowing<br/>30% Network Connectivity<br/>Low Centrality 0.3| LB
    
    %% Competitive Dynamics
    LB <-->|Interest Rate Competition<br/>Market Share Battle<br/>CBDC Response| SB
    
    %% Network Effects
    C -.->|Peer Influence<br/>Social Learning<br/>Adoption Pressure| C
    
    %% Styling
    classDef centralBank fill:#FFD700,stroke:#333,stroke-width:3px
    classDef largeBank fill:#87CEEB,stroke:#333,stroke-width:2px
    classDef smallBank fill:#98FB98,stroke:#333,stroke-width:2px
    classDef consumer fill:#FFB6C1,stroke:#333,stroke-width:2px
    
    class CB centralBank
    class LB largeBank
    class SB smallBank
    class C consumer
```

## Detailed Pre-CBDC Phase Interactions

```mermaid
sequenceDiagram
    participant CB as Central Bank
    participant LB as Large Banks
    participant SB as Small Banks
    participant C as Consumers
    
    Note over CB,C: Pre-CBDC Phase (Steps 1-29)
    
    %% Initial Setup
    CB->>LB: Set monetary policy (2% base rate)
    CB->>SB: Set monetary policy (2% base rate)
    CB->>CB: Monitor banking system health
    
    %% Consumer-Bank Relationships
    C->>LB: Random assignment (initial banking)
    C->>SB: Random assignment (initial banking)
    LB->>C: Accept deposits ($1,850 avg per consumer)
    SB->>C: Accept deposits ($1,850 avg per consumer)
    
    %% Banking Operations
    LB->>C: Offer loans (5% interest rate)
    SB->>C: Offer loans (5% interest rate)
    LB->>LB: Build reserves (20% of capital)
    SB->>SB: Build reserves (20% of capital)
    
    %% Interbank Network
    LB<-->SB: Establish interbank connections
    LB->>LB: High connectivity (60% of network)
    SB->>SB: Lower connectivity (30% of network)
    
    %% Market Dynamics
    C->>C: Economic activity (2% income, 1.5% spending)
    LB->>SB: Compete for market share
    CB->>LB: Monitor bank performance
    CB->>SB: Monitor bank performance
```

## CBDC Introduction and Impact Phase

```mermaid
sequenceDiagram
    participant CB as Central Bank
    participant LB as Large Banks
    participant SB as Small Banks
    participant C as Consumers
    
    Note over CB,C: CBDC Introduction Phase (Step 30+)
    
    %% CBDC Launch
    CB->>C: Introduce CBDC (1% interest rate)
    CB->>CB: Begin CBDC promotion campaign
    CB->>LB: Create competitive pressure
    CB->>SB: Create competitive pressure
    
    %% Consumer Decision Making
    C->>C: Evaluate CBDC vs bank deposits
    C->>C: Apply social influence (peer adoption)
    C->>C: Consider interest rates (1% vs 2%)
    C->>C: Factor in convenience preferences
    
    %% Consumer Adoption
    alt Consumer adopts CBDC
        C->>CB: Transfer funds to CBDC
        C->>LB: Reduce bank deposits
        C->>SB: Reduce bank deposits
        C->>C: Rebalance portfolio (CBDC + deposits)
    else Consumer stays with banks
        C->>LB: Maintain traditional banking
        C->>SB: Maintain traditional banking
    end
    
    %% Bank Response
    LB->>LB: Adjust competitive strategy
    SB->>SB: Struggle with higher vulnerability (80%)
    LB->>C: Leverage customer stickiness (70%)
    SB->>C: Lose customers due to low stickiness (30%)
    
    %% Market Evolution
    CB->>CB: Monitor CBDC adoption rate
    CB->>CB: Track systemic risk levels
    CB->>LB: Assess banking system health
    CB->>SB: Assess banking system health
    
    %% Network Changes
    CB->>CB: Increase network centrality
    LB->>LB: Maintain network position
    SB->>SB: Lose network connectivity
    C->>C: Amplify social influence effects
```

## Consumer Decision Process Detail

```mermaid
flowchart TD
    Start([Consumer Decision Cycle])
    
    %% Economic Activity
    Start --> Income[Receive Monthly Income<br/>2% ± 0.5% of wealth]
    Income --> Spend[Monthly Spending<br/>1.5% ± 0.5% of wealth]
    
    %% CBDC Evaluation
    Spend --> CBDCAvail{CBDC Available?}
    CBDCAvail -->|No| BankOnly[All funds to bank deposits<br/>37% wealth allocation]
    CBDCAvail -->|Yes| Evaluate[Evaluate CBDC Adoption]
    
    %% Decision Factors
    Evaluate --> Interest[Interest Rate Comparison<br/>CBDC 1% vs Bank 2%]
    Evaluate --> Social[Social Influence<br/>Peer adoption rate × 0.3]
    Evaluate --> Convenience[Convenience Factor<br/>Personal preference weight]
    Evaluate --> Risk[Risk Aversion<br/>μ=0.5, σ=0.2]
    Evaluate --> Loyalty[Bank Loyalty<br/>μ=0.7, σ=0.2]
    
    %% Adoption Decision
    Interest --> Decide{Adopt CBDC?}
    Social --> Decide
    Convenience --> Decide
    Risk --> Decide
    Loyalty --> Decide
    
    %% Outcomes
    Decide -->|Yes| Adopt[Become CBDC Adopter<br/>Rebalance portfolio]
    Decide -->|No| StayBank[Maintain bank relationship]
    
    %% Portfolio Management
    Adopt --> Rebalance[Portfolio Rebalancing<br/>Bank deposits ↔ CBDC]
    StayBank --> BankRelation[Update banking relationship]
    BankOnly --> BankRelation
    
    %% Loop Back
    Rebalance --> UpdateBank[Update primary bank<br/>Customer lists]
    BankRelation --> UpdateBank
    UpdateBank --> Start
    
    %% Styling
    classDef decision fill:#FFE4B5,stroke:#333,stroke-width:2px
    classDef action fill:#E0E0E0,stroke:#333,stroke-width:1px
    classDef outcome fill:#98FB98,stroke:#333,stroke-width:2px
    
    class CBDCAvail,Decide decision
    class Income,Spend,Evaluate,Interest,Social,Convenience,Risk,Loyalty,Rebalance,UpdateBank action
    class BankOnly,Adopt,StayBank,BankRelation outcome
```

## Banking System Network Structure

```mermaid
graph LR
    %% Central Bank
    CB((Central Bank<br/>Network Hub))
    
    %% Large Banks
    LB1[Large Bank 1<br/>High Centrality 0.8]
    LB2[Large Bank 2<br/>High Centrality 0.8]
    
    %% Small-Medium Banks
    SB1[Small Bank 1<br/>Low Centrality 0.3]
    SB2[Small Bank 2<br/>Low Centrality 0.3]
    SB3[Small Bank 3<br/>Low Centrality 0.3]
    SB4[Small Bank 4<br/>Low Centrality 0.3]
    SB5[Small Bank 5<br/>Low Centrality 0.3]
    SB6[Small Bank 6<br/>Low Centrality 0.3]
    
    %% Consumer Groups
    C1[Consumer Group 1<br/>25 consumers]
    C2[Consumer Group 2<br/>25 consumers]
    C3[Consumer Group 3<br/>25 consumers]
    C4[Consumer Group 4<br/>25 consumers]
    C5[Consumer Group 5<br/>25 consumers]
    C6[Consumer Group 6<br/>25 consumers]
    C7[Consumer Group 7<br/>25 consumers]
    C8[Consumer Group 8<br/>25 consumers]
    
    %% Central Bank Connections (Post-CBDC)
    CB -.->|CBDC Direct<br/>Relationship| C1
    CB -.->|CBDC Direct<br/>Relationship| C2
    CB -.->|CBDC Direct<br/>Relationship| C3
    CB -.->|CBDC Direct<br/>Relationship| C4
    CB -.->|CBDC Direct<br/>Relationship| C5
    CB -.->|CBDC Direct<br/>Relationship| C6
    CB -.->|CBDC Direct<br/>Relationship| C7
    CB -.->|CBDC Direct<br/>Relationship| C8
    
    %% Banking Network (Dense Large Bank Connections)
    LB1 <--> LB2
    LB1 <--> SB1
    LB1 <--> SB2
    LB1 <--> SB3
    LB1 <--> SB4
    LB2 <--> SB3
    LB2 <--> SB4
    LB2 <--> SB5
    LB2 <--> SB6
    
    %% Sparse Small Bank Connections
    SB1 <--> SB2
    SB3 <--> SB4
    SB5 <--> SB6
    
    %% Consumer-Bank Assignments
    LB1 --> C1
    LB1 --> C2
    LB2 --> C3
    LB2 --> C4
    SB1 --> C5
    SB2 --> C5
    SB3 --> C6
    SB4 --> C6
    SB5 --> C7
    SB6 --> C8
    
    %% Regulatory Oversight
    CB -->|Regulatory<br/>Oversight| LB1
    CB -->|Regulatory<br/>Oversight| LB2
    CB -->|Regulatory<br/>Oversight| SB1
    CB -->|Regulatory<br/>Oversight| SB2
    CB -->|Regulatory<br/>Oversight| SB3
    CB -->|Regulatory<br/>Oversight| SB4
    CB -->|Regulatory<br/>Oversight| SB5
    CB -->|Regulatory<br/>Oversight| SB6
    
    %% Styling
    classDef centralBank fill:#FFD700,stroke:#333,stroke-width:3px
    classDef largeBank fill:#87CEEB,stroke:#333,stroke-width:2px
    classDef smallBank fill:#98FB98,stroke:#333,stroke-width:2px
    classDef consumers fill:#FFB6C1,stroke:#333,stroke-width:1px
    
    class CB centralBank
    class LB1,LB2 largeBank
    class SB1,SB2,SB3,SB4,SB5,SB6 smallBank
    class C1,C2,C3,C4,C5,C6,C7,C8 consumers
```

## Hypothesis Testing Framework

```mermaid
mindmap
  root((CBDC Impact<br/>Hypotheses))
    H1[H1: Network Centrality]
      Large Banks
        Maintain centrality 0.8
        Strong network position
        Resource advantages
      Small Banks
        Lose centrality 0.3→lower
        Peripheral position
        Higher vulnerability 80%
    H3[H3: Liquidity Stress]
      Systemic Risk
        Banking system health
        Deposit outflows
        Liquidity ratios
      Stress Indicators
        >30% weak banks threshold
        Central bank intervention
        Crisis periods
    H4[H4: Network Connectivity]
      Interbank Density
        Large banks 60% connected
        Small banks 30% connected
        Network fragmentation
      Connection Changes
        CBDC disruption
        Reduced intermediation
        Direct relationships
    H6[H6: Central Bank Dominance]
      Network Position
        Minimal initially 0.1
        Growth with CBDC adoption
        Direct consumer relationships
      Dominance Metrics
        Adoption rate boost 60%
        Market share boost 40%
        Monopoly position 20%
```

## Key Model Metrics and Data Flow

```mermaid
graph TD
    %% Data Collection Points
    ModelData[Model Data Collector]
    AgentData[Agent Data Collector]
    
    %% Central Bank Metrics
    ModelData --> CBDCAdopt[CBDC Adoption Rate]
    ModelData --> CBDCHold[Total CBDC Holdings]
    ModelData --> CBCent[Central Bank Centrality]
    
    %% Banking Metrics
    ModelData --> BankDep[Total Bank Deposits]
    ModelData --> BankLoans[Total Bank Loans]
    ModelData --> AvgLiq[Average Bank Liquidity]
    ModelData --> NetDens[Banking Network Density]
    ModelData --> LiqStress[Average Liquidity Stress]
    
    %% Bank Size Metrics
    ModelData --> LargeCent[Large Bank Centrality]
    ModelData --> SmallCent[Small Bank Centrality]
    
    %% Agent Level Tracking
    AgentData --> AgentID[Agent Identification]
    AgentData --> Wealth[Individual Wealth]
    AgentData --> CBDCHold2[CBDC Holdings per Agent]
    AgentData --> BankDep2[Bank Deposits per Agent]
    AgentData --> AdopterFlag[CBDC Adopter Status]
    
    %% Visualization Outputs
    CBDCAdopt --> SubTab[Substitution Analysis Tab]
    LargeCent --> H1Tab[H1: Network Centrality Tab]
    SmallCent --> H1Tab
    LiqStress --> H3Tab[H3: Liquidity Stress Tab]
    NetDens --> H4Tab[H4: Network Connectivity Tab]
    CBCent --> H6Tab[H6: Central Bank Dominance Tab]
    
    %% Flow Chart Integration
    AgentID --> FlowTab[Agent Flow Chart Tab]
    
    %% Styling
    classDef data fill:#E6E6FA,stroke:#333,stroke-width:2px
    classDef metrics fill:#F0F8FF,stroke:#333,stroke-width:1px
    classDef tabs fill:#F5F5DC,stroke:#333,stroke-width:2px
    
    class ModelData,AgentData data
    class CBDCAdopt,CBDCHold,CBCent,BankDep,BankLoans,AvgLiq,NetDens,LiqStress,LargeCent,SmallCent,AgentID,Wealth,CBDCHold2,BankDep2,AdopterFlag metrics
    class SubTab,H1Tab,H3Tab,H4Tab,H6Tab,FlowTab tabs
```

## Usage Instructions

### For Documentation
1. Copy the Mermaid code blocks into any Markdown viewer that supports Mermaid
2. Use in GitHub README files or documentation platforms
3. Export as images for presentations or papers

### For Development
1. Use these charts to understand interaction patterns
2. Reference when debugging agent behaviors
3. Validate model implementation against these specifications

### For Analysis
1. Compare actual simulation results against these interaction patterns
2. Use for hypothesis validation
3. Identify unexpected behaviors or missing connections