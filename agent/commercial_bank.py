from mesa import Agent
import numpy as np

class CommercialBank(Agent):
    """
    Commercial Bank agent that accepts deposits and provides loans.
    
    Banks compete with CBDC by adjusting interest rates and maintaining liquidity.
    They experience deposit outflows when consumers adopt CBDC.
    """
    
    def __init__(self, unique_id, model, interest_rate=0.02, lending_rate=0.05, 
                 initial_capital=50000, reserve_requirement=0.1, bank_type="small_medium", 
                 network_centrality=0.3):
        super().__init__(model)
        
        # Store agent properties
        self.unique_id = unique_id
        
        # Bank characteristics
        self.interest_rate = interest_rate  # Rate paid on deposits
        self.lending_rate = lending_rate    # Rate charged on loans
        self.initial_capital = initial_capital
        self.reserve_requirement = reserve_requirement
        self.bank_type = bank_type  # "large" or "small_medium"
        # H1: Multiple network centrality metrics
        self.network_centrality = network_centrality  # General economic centrality
        self.degree_centrality = 0.0       # Number of direct connections
        self.betweenness_centrality = 0.0  # Intermediary position strength
        self.closeness_centrality = 0.0    # Proximity to all other nodes
        self.eigenvector_centrality = 0.0  # Influence based on connections' importance
        
        # 2025-calibrated balance sheet structure
        self.capital = initial_capital
        
        # Balance sheet components based on 2025 banking data
        if self.bank_type == "large":
            # Large bank balance sheet (75% deposits, 55% loans, 15% reserves)
            self.target_deposit_ratio = 0.75    # 75% of assets as deposits
            self.target_loan_ratio = 0.55       # 55% of assets as loans  
            self.target_reserve_ratio = 0.15    # 15% cash & reserves
            self.target_securities_ratio = 0.25 # 25% securities
            self.loan_to_deposit_target = 0.733 # 73.3% LTD ratio
            self.net_interest_margin = 0.028    # 2.8% NIM
            self.capital_ratio = 0.12           # 12% equity ratio
        else:
            # Small bank balance sheet (82% deposits, 62% loans, 12% reserves)
            self.target_deposit_ratio = 0.82    # 82% of assets as deposits
            self.target_loan_ratio = 0.62       # 62% of assets as loans
            self.target_reserve_ratio = 0.12    # 12% cash & reserves  
            self.target_securities_ratio = 0.20 # 20% securities
            self.loan_to_deposit_target = 0.756 # 75.6% LTD ratio
            self.net_interest_margin = 0.034    # 3.4% NIM
            self.capital_ratio = 0.10           # 10% equity ratio
        
        # Balance sheet will be initialized with 2025-calibrated values in initialize_bank_balance_sheets()
        # after customer assignment determines actual deposit base
        self.total_deposits = 0
        self.demand_deposits = 0
        self.time_deposits = 0
        self.total_loans = 0
        self.consumer_loans = 0
        self.commercial_loans = 0
        self.real_estate_loans = 0
        self.cash_reserves = 0
        self.securities = 0
        self.borrowings = 0
        self.other_liabilities = 0
        
        self.customers = []
        
        # Basel III Compliance Metrics (Reference: Basel Committee 2024)
        self.tier_1_capital = initial_capital * 0.12  # 12% of initial capital as Tier 1
        self.tier_2_capital = initial_capital * 0.03  # 3% of initial capital as Tier 2
        self.capital_conservation_buffer = 0.025  # 2.5% conservation buffer
        self.countercyclical_buffer = 0.0  # Variable based on economic conditions
        
        # Risk Management Attributes (BIS 2024, IMF 2024)
        self.operational_capacity = 1.0  # 100% operational capacity
        self.cyber_incident_flag = False
        self.cyber_losses = 0.0
        self.liquidity_stress_flag = False
        self.stressed_liquidity_ratio = 1.0
        self.digital_run_flag = False
        self.previous_deposits = 0
        
        # Enhanced Capital Requirements (Basel III Endgame 2025)
        self.enhanced_capital_requirement = False
        self.capital_buffer_requirement = 0.0
        
        # Operational Risk Indicators (BIS 2024)
        self.operational_risk_score = 0.05  # 5% baseline operational risk
        self.business_continuity_score = 0.95  # 95% business continuity
        self.third_party_risk_exposure = 0.1  # 10% third-party risk exposure
        
        # Liquidity Risk Management (Basel III LCR/NSFR)
        self.liquidity_coverage_ratio = 1.2  # 120% LCR (above 100% requirement)
        self.net_stable_funding_ratio = 1.1  # 110% NSFR (above 100% requirement)
        self.emergency_liquidity_access = True  # Access to central bank facilities
        
        # CBDC exchange tracking
        self.cbdc_related_outflows = 0      # Total deposits lost to CBDC exchanges
        self.reserves_transferred_to_cb = 0 # Reserves transferred to central bank for CBDC
        
        # 2025-calibrated performance metrics
        self.liquidity_ratio = 1.0  # Will be calculated dynamically
        self.loan_to_deposit_ratio = 0.0  # Will track against target
        self.liquidity_coverage_ratio = 1.25 if bank_type == "large" else 1.10  # Basel III LCR
        
        # Profitability metrics
        self.net_interest_income = 0.0
        self.non_interest_income = 0.0
        self.operating_expenses = 0.0
        self.net_income = 0.0
        self.return_on_equity = 0.0
        self.return_on_assets = 0.0
        self.efficiency_ratio = 0.58 if bank_type == "large" else 0.65  # 2025 industry average
        
        # Market position
        self.market_share = 0.0
        self.customer_retention_rate = 1.0
        
        # Network and systemic risk metrics (H1, H3, H4, H5)
        self.interbank_connections = 0  # Number of interbank relationships
        self.systemic_importance = 0.0  # Systemic importance score
        self.liquidity_stress_level = 0.0  # H3: Liquidity stress indicator
        self.cbdc_impact_factor = 1.0  # How much CBDC affects this bank
        
        # H2: 2025-calibrated bank vulnerabilities
        if self.bank_type == "small_medium":
            self.cbdc_vulnerability = 0.65  # Moderate vulnerability (improved digital capabilities)
            self.customer_stickiness = 0.45  # Relationship-based retention
            self.digital_capability = 0.65   # Limited fintech resources
        else:
            self.cbdc_vulnerability = 0.25  # Lower vulnerability (stronger competitive position)
            self.customer_stickiness = 0.80  # Strong brand loyalty and services
            self.digital_capability = 0.90   # Advanced fintech integration
        
        # Initialize centrality measures
        self.initialize_centrality_measures()
    
    def step(self):
        """Execute one step of bank operations."""
        # Update customer deposits
        self.update_deposits()
        
        # Make lending decisions
        self.make_loans()
        
        # Calculate performance metrics
        self.calculate_metrics()
        
        # Adjust strategy based on CBDC competition
        self.adjust_competitive_strategy()
        
        # Handle customer attrition due to CBDC
        self.handle_customer_attrition()
        
        # Update network centrality and systemic metrics (H1, H4, H5)
        self.update_network_metrics()
        
        # Calculate liquidity stress (H3)
        self.calculate_liquidity_stress()
        
        # Enhanced Risk Management (Basel III + Real-world complexities)
        self.assess_operational_risks()
        self.monitor_basel_compliance()
        self.manage_liquidity_risks()
        self.respond_to_cyber_threats()
        self.update_risk_appetite()
    
    def add_customer(self, consumer):
        """Add a new customer to the bank."""
        if consumer not in self.customers:
            self.customers.append(consumer)
    
    def remove_customer(self, consumer):
        """Remove a customer from the bank."""
        if consumer in self.customers:
            self.customers.remove(consumer)
    
    def update_deposits(self):
        """Update total deposits from all customers and track CBDC-related outflows."""
        # Calculate current customer deposits
        current_customer_deposits = sum(
            customer.bank_deposits for customer in self.customers
            if hasattr(customer, 'bank_deposits')
        )
        
        # Track deposit changes (likely due to CBDC exchanges)
        previous_deposits = getattr(self, 'total_deposits', current_customer_deposits)
        deposit_change = current_customer_deposits - previous_deposits
        
        if deposit_change < 0:  # Deposits decreased
            deposit_outflow = abs(deposit_change)
            # Track as CBDC-related outflow (customers exchanging deposits for CBDC)
            self.cbdc_related_outflows = getattr(self, 'cbdc_related_outflows', 0) + deposit_outflow
        
        # Update total deposits
        self.total_deposits = current_customer_deposits
        
        # Update demand/time deposit composition
        if self.total_deposits > 0:
            if self.bank_type == "large":
                self.demand_deposits = self.total_deposits * 0.60
                self.time_deposits = self.total_deposits * 0.40
            else:
                self.demand_deposits = self.total_deposits * 0.70
                self.time_deposits = self.total_deposits * 0.30
    
    def make_loans(self):
        """Make loans based on available liquidity."""
        # Available funds for lending (deposits - reserves)
        available_for_lending = max(0, self.total_deposits - (self.total_deposits * self.reserve_requirement))
        
        # Loan demand (simplified model)
        # In reality, this would depend on economic conditions and loan applications
        loan_demand = available_for_lending * 0.8  # Assume 80% utilization
        
        # Adjust for risk and market conditions
        if self.model.cbdc_introduced:
            # Reduce lending during CBDC transition due to uncertainty
            risk_adjustment = 0.9
            loan_demand *= risk_adjustment
        
        # Update total loans (simplified - assumes all loans are approved)
        self.total_loans = min(loan_demand, available_for_lending)
        
        # Update cash reserves (maintain compatibility)
        self.reserves = self.cash_reserves  # For backward compatibility
    
    def calculate_metrics(self):
        """Calculate 2025-calibrated key performance metrics."""
        if self.total_deposits > 0:
            self.liquidity_ratio = self.cash_reserves / self.total_deposits
            self.loan_to_deposit_ratio = self.total_loans / self.total_deposits
        else:
            self.liquidity_ratio = 1.0
            self.loan_to_deposit_ratio = 0.0
        
        # Loan-to-deposit ratio
        self.loan_to_deposit_ratio = (
            self.total_loans / self.total_deposits if self.total_deposits > 0 else 0.0
        )
        
        # Profitability (simplified: loan income - deposit costs)
        loan_income = self.total_loans * self.lending_rate
        deposit_costs = self.total_deposits * self.interest_rate
        self.profitability = loan_income - deposit_costs
        
        # Market share (among all banks)
        total_market_deposits = sum(bank.total_deposits for bank in self.model.commercial_banks)
        self.market_share = (
            self.total_deposits / total_market_deposits if total_market_deposits > 0 else 0.0
        )
    
    def adjust_competitive_strategy(self):
        """Adjust strategy in response to CBDC competition."""
        if self.model.cbdc_introduced:
            # Increase deposit rates to compete with CBDC
            cbdc_rate = self.model.central_bank.cbdc_interest_rate
            cbdc_adoption_rate = self.model.compute_cbdc_adoption_rate()
            
            # Competitive response: increase rates based on CBDC threat
            competitive_pressure = cbdc_adoption_rate * 0.5  # Up to 50% of adoption rate
            base_premium = max(0, cbdc_rate - self.interest_rate) * 0.8  # 80% of CBDC premium
            
            # Adjust interest rate (capped to maintain profitability)
            max_rate_increase = 0.015  # Maximum 1.5% increase
            rate_adjustment = min(competitive_pressure + base_premium, max_rate_increase)
            
            # Only adjust if it maintains positive spread
            new_rate = self.interest_rate + rate_adjustment
            if self.lending_rate - new_rate > 0.01:  # Maintain at least 1% spread
                self.interest_rate = new_rate
    
    def handle_customer_attrition(self):
        """Handle customer attrition due to CBDC adoption."""
        if self.model.cbdc_introduced:
            # Some customers may switch to CBDC
            customers_to_remove = []
            
            for customer in self.customers:
                if hasattr(customer, 'cbdc_adopter') and customer.cbdc_adopter:
                    # CBDC adopters may reduce their bank relationship
                    if np.random.random() < 0.1:  # 10% chance to leave completely
                        customers_to_remove.append(customer)
                        customer.primary_bank = None
            
            # Remove customers who switched completely to CBDC
            for customer in customers_to_remove:
                self.remove_customer(customer)
            
            # Update customer retention rate
            if len(self.customers) > 0:
                retained_customers = len(self.customers) - len(customers_to_remove)
                self.customer_retention_rate = retained_customers / len(self.customers)
    
    def update_network_metrics(self):
        """Update network centrality and connectivity metrics (H1, H4)."""
        if self.model.cbdc_introduced:
            # H1: CBDC reduces network centrality, especially for small banks
            cbdc_adoption_rate = self.model.compute_cbdc_adoption_rate()
            
            # Dynamic centrality reduction based on CBDC adoption and customer loss
            customer_loss_rate = 1 - self.customer_retention_rate
            centrality_impact = cbdc_adoption_rate * self.cbdc_vulnerability * (1 + customer_loss_rate)
            
            # Small banks lose centrality faster and more dramatically
            if self.bank_type == "small_medium":
                centrality_impact *= 2.0  # Double impact for small banks
                # Additional penalty for deposit concentration
                deposit_loss_rate = max(0, (self.initial_capital - self.total_deposits) / self.initial_capital)
                centrality_impact *= (1 + deposit_loss_rate)
            
            # Apply gradual centrality decay
            decay_rate = min(0.05, centrality_impact * 0.03)  # Max 5% decay per step
            self.network_centrality = max(0.05, self.network_centrality - decay_rate)
            
            # Update multiple centrality measures
            self.update_all_centrality_measures(cbdc_adoption_rate, customer_loss_rate)
            
            # H4: Reduce interbank connections as CBDC provides alternative
            if cbdc_adoption_rate > 0.2:  # When CBDC adoption exceeds 20%
                connection_impact = (cbdc_adoption_rate - 0.2) * 0.15
                if self.bank_type == "small_medium":
                    connection_impact *= 1.5  # Small banks lose connections faster
                
                connection_loss = connection_impact * 0.1  # Gradual loss
                self.interbank_connections = max(0, self.interbank_connections - connection_loss)
    
    def update_all_centrality_measures(self, cbdc_adoption_rate, customer_loss_rate):
        """Update all centrality measures based on CBDC impact."""
        # Base impact factors
        base_impact = cbdc_adoption_rate * self.cbdc_vulnerability * (1 + customer_loss_rate)
        small_bank_multiplier = 2.0 if self.bank_type == "small_medium" else 1.0
        
        # Degree Centrality: Direct connections (banking relationships)
        degree_impact = base_impact * small_bank_multiplier * 0.8  # Strong impact on direct connections
        degree_decay = min(0.08, degree_impact * 0.04)  # Max 8% decay per step
        self.degree_centrality = max(0.05, self.degree_centrality - degree_decay)
        
        # Betweenness Centrality: Intermediary role in financial flows
        betweenness_impact = base_impact * small_bank_multiplier * 1.2  # Highest impact - CBDC bypasses intermediation
        betweenness_decay = min(0.10, betweenness_impact * 0.05)  # Max 10% decay per step
        self.betweenness_centrality = max(0.02, self.betweenness_centrality - betweenness_decay)
        
        # Closeness Centrality: Proximity to all network nodes
        closeness_impact = base_impact * small_bank_multiplier * 0.6  # Moderate impact
        closeness_decay = min(0.06, closeness_impact * 0.03)  # Max 6% decay per step
        self.closeness_centrality = max(0.08, self.closeness_centrality - closeness_decay)
        
        # Eigenvector Centrality: Influence based on connections' importance
        eigenvector_impact = base_impact * small_bank_multiplier * 0.9  # High impact - network effects
        eigenvector_decay = min(0.07, eigenvector_impact * 0.035)  # Max 7% decay per step
        self.eigenvector_centrality = max(0.04, self.eigenvector_centrality - eigenvector_decay)
    
    def initialize_centrality_measures(self):
        """Initialize centrality measures based on bank type and market position."""
        if self.bank_type == "large":
            # Large banks: High centrality across all measures
            self.degree_centrality = 0.85 + np.random.normal(0, 0.05)  # Many direct connections
            self.betweenness_centrality = 0.90 + np.random.normal(0, 0.03)  # Key intermediaries
            self.closeness_centrality = 0.80 + np.random.normal(0, 0.04)  # Close to all nodes
            self.eigenvector_centrality = 0.88 + np.random.normal(0, 0.04)  # High influence
        else:
            # Small-medium banks: Lower centrality, more vulnerable
            self.degree_centrality = 0.35 + np.random.normal(0, 0.08)  # Fewer connections
            self.betweenness_centrality = 0.25 + np.random.normal(0, 0.05)  # Limited intermediary role
            self.closeness_centrality = 0.45 + np.random.normal(0, 0.06)  # More peripheral
            self.eigenvector_centrality = 0.30 + np.random.normal(0, 0.05)  # Lower influence
        
        # Ensure all values are within valid bounds [0, 1]
        self.degree_centrality = max(0.05, min(1.0, self.degree_centrality))
        self.betweenness_centrality = max(0.02, min(1.0, self.betweenness_centrality))
        self.closeness_centrality = max(0.08, min(1.0, self.closeness_centrality))
        self.eigenvector_centrality = max(0.04, min(1.0, self.eigenvector_centrality))
    
    def calculate_liquidity_stress(self):
        """Calculate liquidity stress level (H3)."""
        if self.model.cbdc_introduced:
            # H3: Rapid CBDC adoption creates liquidity stress
            cbdc_adoption_rate = self.model.compute_cbdc_adoption_rate()
            
            # Calculate deposit outflow velocity (rate of change)
            current_deposits = self.total_deposits
            deposit_change_rate = max(0, (self.initial_capital - current_deposits) / self.initial_capital)
            
            # Stress increases with both adoption rate and deposit velocity
            base_stress = cbdc_adoption_rate * self.cbdc_vulnerability
            velocity_stress = deposit_change_rate * 0.5  # Velocity component
            
            # Liquidity stress combines multiple factors
            liquidity_gap = max(0, 1 - self.liquidity_ratio)  # How far from adequate liquidity
            customer_flight = 1 - self.customer_retention_rate  # Customer loss rate
            
            self.liquidity_stress_level = min(1.0, 
                base_stress + velocity_stress + (liquidity_gap * 0.3) + (customer_flight * 0.2))
            
            # Small banks experience compounding stress effects
            if self.bank_type == "small_medium":
                # Stress amplification for small banks
                stress_multiplier = 1.0 + (cbdc_adoption_rate * 0.8)  # Up to 80% more stress
                self.liquidity_stress_level = min(1.0, self.liquidity_stress_level * stress_multiplier)
                
                # Crisis threshold - small banks hit critical stress faster
                if self.liquidity_stress_level > 0.7 and cbdc_adoption_rate > 0.4:
                    self.liquidity_stress_level = min(1.0, self.liquidity_stress_level * 1.2)
    
    def get_financial_strength(self):
        """Calculate overall financial strength score."""
        # Weighted score based on key metrics
        liquidity_score = min(self.liquidity_ratio / 0.2, 1.0)  # Target 20% liquidity
        profitability_score = max(0, min(self.profitability / 1000, 1.0))  # Normalize profitability
        market_share_score = self.market_share
        
        # H5: Include network centrality and systemic risk in strength calculation
        centrality_score = self.network_centrality
        stress_penalty = max(0, 1 - self.liquidity_stress_level)
        
        # Weighted average including network effects
        strength_score = (
            liquidity_score * 0.3 +
            profitability_score * 0.3 +
            market_share_score * 0.2 +
            centrality_score * 0.1 +
            stress_penalty * 0.1
        )
        
        return strength_score
    
    def assess_operational_risks(self):
        """
        Assess operational risks based on BIS framework.
        
        Reference: BIS (2024) "CBDC Information Security and Operational Risks to Central Banks"
        """
        # Technology risk assessment
        tech_risk = 0.0
        if self.cyber_incident_flag:
            tech_risk += 0.2  # 20% increase from cyber incidents
        
        # Business continuity risk
        if self.operational_capacity < 0.9:
            tech_risk += (1 - self.operational_capacity) * 0.3
        
        # Update operational risk score
        self.operational_risk_score = min(0.3, tech_risk + self.third_party_risk_exposure * 0.1)
        
        # Impact on business continuity
        self.business_continuity_score = max(0.5, 1.0 - self.operational_risk_score)
        
    def monitor_basel_compliance(self):
        """
        Monitor Basel III compliance requirements.
        
        Reference: Basel Committee (2024) "Basel III Endgame Implementation Guidelines"
        """
        # Calculate risk-weighted assets
        risk_weighted_assets = (
            self.consumer_loans * 0.75 +  # 75% risk weight
            self.commercial_loans * 1.0 +  # 100% risk weight
            self.real_estate_loans * 0.35 +  # 35% risk weight
            self.securities * 0.2 +  # 20% risk weight
            self.cash_reserves * 0.0  # 0% risk weight
        )
        
        # Calculate capital ratios
        total_capital = self.tier_1_capital + self.tier_2_capital
        if risk_weighted_assets > 0:
            capital_ratio = total_capital / risk_weighted_assets
            tier_1_ratio = self.tier_1_capital / risk_weighted_assets
            
            # Check capital adequacy
            required_capital = 0.08 + self.capital_conservation_buffer + self.countercyclical_buffer
            if self.enhanced_capital_requirement:
                required_capital += self.capital_buffer_requirement
                
            if capital_ratio < required_capital:
                # Capital shortfall - raise additional capital
                capital_deficit = (required_capital - capital_ratio) * risk_weighted_assets
                self.tier_1_capital += capital_deficit * 0.8  # Raise mostly Tier 1 capital
                self.tier_2_capital += capital_deficit * 0.2
        
        # Update liquidity ratios
        self.update_liquidity_ratios()
        
    def update_liquidity_ratios(self):
        """Update Basel III liquidity ratios (LCR and NSFR)."""
        # Liquidity Coverage Ratio calculation
        liquid_assets = self.cash_reserves + self.securities * 0.85  # 85% haircut on securities
        net_cash_outflows = self.total_deposits * 0.03  # 3% daily outflow assumption
        
        if net_cash_outflows > 0:
            self.liquidity_coverage_ratio = liquid_assets / net_cash_outflows
        
        # Net Stable Funding Ratio calculation
        stable_funding = self.total_deposits * 0.9 + self.borrowings * 0.5
        required_funding = (
            self.consumer_loans * 0.65 +
            self.commercial_loans * 0.85 +
            self.real_estate_loans * 0.65 +
            self.securities * 0.15
        )
        
        if required_funding > 0:
            self.net_stable_funding_ratio = stable_funding / required_funding
            
    def manage_liquidity_risks(self):
        """
        Manage liquidity risks during CBDC transition.
        
        Reference: ECB (2024) "Tiered CBDC and the Financial System"
        """
        # Monitor deposit velocity
        if hasattr(self, 'previous_deposits') and self.previous_deposits > 0:
            deposit_change_rate = (self.previous_deposits - self.total_deposits) / self.previous_deposits
            
            if deposit_change_rate > 0.1:  # 10% deposit outflow
                self.liquidity_stress_flag = True
                
                # Emergency liquidity measures
                if self.emergency_liquidity_access:
                    # Access central bank emergency lending
                    emergency_funding = min(
                        deposit_change_rate * self.total_deposits,
                        self.cash_reserves * 0.5
                    )
                    self.borrowings += emergency_funding
                    self.cash_reserves += emergency_funding
        
        # Proactive liquidity management
        if self.liquidity_coverage_ratio < 1.1:  # Below 110%
            # Increase liquid asset holdings
            liquidity_buffer = self.total_deposits * 0.05  # 5% additional buffer
            self.securities += liquidity_buffer * 0.6  # 60% in securities
            self.cash_reserves += liquidity_buffer * 0.4  # 40% in cash
            
    def respond_to_cyber_threats(self):
        """
        Respond to cybersecurity incidents.
        
        Reference: IMF (2024) "Rising Cyber Threats Pose Serious Concerns for Financial Stability"
        """
        if self.cyber_incident_flag:
            # Immediate response measures
            self.operational_capacity *= 0.9  # 10% capacity reduction
            
            # Increase cybersecurity spending (operational cost)
            cyber_investment = self.cyber_losses * 0.5  # 50% of losses in security investment
            self.tier_1_capital -= cyber_investment
            
            # Customer confidence impact
            customer_impact = min(0.1, self.cyber_losses / max(self.total_deposits, 1))
            for customer in self.customers:
                if hasattr(customer, 'bank_loyalty'):
                    customer.bank_loyalty *= (1 - customer_impact)
            
            # Recovery planning
            if self.operational_capacity < 0.8:
                # Activate business continuity plan
                self.business_continuity_score *= 0.9
                # Gradual capacity restoration
                self.operational_capacity = min(1.0, self.operational_capacity * 1.05)
            
            # Reset incident flag after response
            self.cyber_incident_flag = False
            
    def update_risk_appetite(self):
        """
        Update risk appetite based on current conditions.
        
        Reference: Federal Reserve (2024) "Financial Stability Implications of CBDC"
        """
        # Calculate overall risk exposure
        cbdc_risk = self.model.compute_cbdc_adoption_rate() * self.cbdc_vulnerability
        operational_risk = self.operational_risk_score
        liquidity_risk = max(0, 1.1 - self.liquidity_coverage_ratio)
        
        total_risk_exposure = cbdc_risk + operational_risk + liquidity_risk
        
        # Adjust risk appetite (conservative during high risk periods)
        if total_risk_exposure > 0.4:
            # Conservative approach
            self.lending_rate += 0.001  # Increase lending rates
            self.interest_rate -= 0.0005  # Reduce deposit rates slightly
            # Reduce lending exposure
            target_loan_reduction = min(0.05, total_risk_exposure * 0.1)
            self.target_loan_ratio *= (1 - target_loan_reduction)
        elif total_risk_exposure < 0.2:
            # More aggressive approach
            self.lending_rate = max(self.lending_rate - 0.0005, 0.03)  # Reduce lending rates
            self.interest_rate += 0.0003  # Slightly increase deposit rates
        
        # Update countercyclical buffer based on systemic risk
        if hasattr(self.model, 'systemic_risk_score'):
            self.countercyclical_buffer = min(0.025, self.model.systemic_risk_score * 0.05)
    
    def __str__(self):
        return f"CommercialBank_{self.unique_id}: Deposits=${self.total_deposits:.0f}, Loans=${self.total_loans:.0f}, Customers={len(self.customers)}"
