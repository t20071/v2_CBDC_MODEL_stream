# CBDC Banking Simulation: Complete Model Flow Analysis

## Current Model Architecture

### Agent Types (Current)
1. **Central Bank** - Issues CBDC, manages monetary policy
2. **Commercial Banks** - Accept deposits, provide loans, compete with CBDC  
3. **Consumers** - Make financial decisions between bank deposits and CBDC

### Model Flow (Current Implementation)

#### Initialization Phase
1. **Agent Creation**
   - 1 Central Bank with regulatory role
   - 8 Commercial Banks (20% large, 80% small/medium)
   - 200 Consumers with initial wealth of $8,400
   
2. **Network Setup**
   - Random customer-bank assignments
   - Interbank network connections initialized
   - Balance sheets calibrated to 2025 banking standards
   
3. **Initial Conditions**
   - Consumers allocate 37% wealth to bank deposits
   - Banks start with realistic loan/deposit ratios
   - Central bank has minimal network centrality

#### Simulation Steps (30 steps = ~2.5 years)

**Pre-CBDC Period (Steps 1-29)**
- Consumers: Regular economic activity (income, spending)
- Banks: Accept deposits, make loans, calculate metrics
- Central Bank: Monitor system, prepare for CBDC

**CBDC Introduction (Step 30)**
- Central bank launches CBDC with 4.5% interest rate
- CBDC becomes available to consumers
- Network effects begin

**Post-CBDC Period (Steps 31+)**
- **Consumer Behavior**:
  - Evaluate CBDC vs bank deposits
  - Portfolio rebalancing based on rates and convenience
  - Social influence affects adoption decisions
  
- **Bank Response**:
  - Competitive rate adjustments
  - Customer retention strategies
  - Network centrality degradation
  
- **Central Bank Actions**:
  - CBDC supply management
  - System stability monitoring
  - Network dominance growth

### Key Interactions (Current)

1. **Consumer ↔ Banks**: Deposit/loan relationships, rate sensitivity
2. **Consumer ↔ Central Bank**: CBDC adoption and holdings
3. **Banks ↔ Central Bank**: Regulatory oversight, CBDC competition
4. **Bank ↔ Bank**: Interbank lending and network effects

## Real-World Scenarios Missing

### Economic Realism Gaps
1. **No Merchant Economy**: No retail transactions or payment flows
2. **Limited Payment Methods**: Only deposits and CBDC, no cash/cards
3. **Simplified Transactions**: No real economic activity beyond transfers
4. **Missing Intermediaries**: No payment processors, fintech, or merchants

### Real-World Use Cases Needed
1. **Retail Payments**: Groceries, utilities, services
2. **E-commerce**: Online shopping with different payment preferences
3. **Business Payments**: B2B transactions, supply chain finance
4. **Cross-border**: International payments and remittances

## Enhanced Model Flow with Real-World Scenarios

### New Agent: Merchant
**Purpose**: Represent real economy transaction endpoints
- Grocery stores, restaurants, online retailers
- Different payment method preferences and costs
- Revenue generation and business banking needs

### Enhanced Interactions

#### Consumer Daily Life Scenarios
1. **Morning Coffee Shop**
   - Small transaction ($5-15)
   - Payment method choice: Cash, Card, Bank transfer, CBDC
   - Merchant preferences affect adoption

2. **Grocery Shopping**
   - Medium transaction ($50-200)
   - Bulk purchases, recurring needs
   - Loyalty programs and payment incentives

3. **Online Shopping**
   - Variable transactions ($20-500)
   - Security concerns, convenience factors
   - Cross-merchant payment patterns

4. **Utility Bills**
   - Fixed recurring payments
   - Automated payment preferences
   - Large value, predictable timing

#### Business-to-Business Scenarios
1. **Supply Chain Payments**
   - Large value transactions ($1,000-100,000)
   - Payment terms and financing needs
   - Bank intermediation vs direct CBDC

2. **Employee Salaries**
   - Recurring, medium-large payments
   - Direct deposit vs CBDC distribution
   - Payroll service provider roles

#### Merchant Business Operations
1. **Payment Processing Costs**
   - Credit card fees (2-3%)
   - Bank transfer costs
   - CBDC transaction costs (potentially lower)

2. **Cash Flow Management**
   - Daily revenue collection
   - Banking relationships for deposits
   - Working capital financing needs

3. **Customer Preferences**
   - Payment method acceptance strategies
   - Incentives for preferred methods
   - Technology adoption costs

### Enhanced Agent Behaviors

#### Consumer Real-World Decision Making
- **Payment Method Selection**: Based on transaction size, merchant acceptance, convenience
- **Economic Shocks**: Job loss, medical expenses affecting payment preferences
- **Social Learning**: Observing friends/family payment choices
- **Security Concerns**: Fraud protection, privacy preferences

#### Bank Real-World Strategies
- **Merchant Acquiring**: Competing for business payment processing
- **Consumer Credit**: Credit cards competing with CBDC convenience
- **Business Banking**: Commercial lending affected by CBDC business adoption
- **Fee Structures**: Adapting pricing to compete with free/low-cost CBDC

#### Central Bank Real-World Policies
- **Merchant Incentives**: Encouraging CBDC acceptance through subsidies
- **Financial Inclusion**: Using CBDC to reach unbanked populations
- **Stability Monitoring**: Real transaction volume impact assessment
- **International Coordination**: Cross-border CBDC implications

## Implementation Strategy

### Phase 1: Merchant Agent Creation
- Create Merchant class with payment preferences
- Add merchant-consumer transaction patterns
- Implement payment method selection logic

### Phase 2: Real Transaction Flows
- Add transaction categories (retail, utilities, e-commerce)
- Implement payment processing costs and preferences
- Add merchant banking relationships

### Phase 3: Economic Realism
- Add income variability and economic shocks
- Implement loyalty programs and payment incentives
- Add business-to-business transaction patterns

### Phase 4: Advanced Scenarios
- Cross-border transactions and remittances
- Financial inclusion use cases
- Small business financing through CBDC

This enhanced model would provide much more realistic insights into CBDC adoption patterns and economic impacts in real-world scenarios.