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
        self.network_centrality = network_centrality  # H1: Network centrality metric
        
        # Bank balance sheet
        self.capital = initial_capital
        self.total_deposits = 0
        self.total_loans = 0
        self.reserves = initial_capital * 0.2  # Keep 20% as reserves initially
        self.customers = []
        
        # Performance metrics
        self.liquidity_ratio = 1.0  # reserves / deposits
        self.loan_to_deposit_ratio = 0.0
        self.profitability = 0.0
        
        # Market position
        self.market_share = 0.0
        self.customer_retention_rate = 1.0
        
        # Network and systemic risk metrics (H1, H3, H4, H5)
        self.interbank_connections = 0  # Number of interbank relationships
        self.systemic_importance = 0.0  # Systemic importance score
        self.liquidity_stress_level = 0.0  # H3: Liquidity stress indicator
        self.cbdc_impact_factor = 1.0  # How much CBDC affects this bank
        
        # H2: Small bank specific vulnerabilities
        if self.bank_type == "small_medium":
            self.cbdc_vulnerability = 0.8  # Higher vulnerability to CBDC
            self.customer_stickiness = 0.3  # Lower customer loyalty
        else:
            self.cbdc_vulnerability = 0.4  # Lower vulnerability to CBDC
            self.customer_stickiness = 0.7  # Higher customer loyalty
    
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
    
    def add_customer(self, consumer):
        """Add a new customer to the bank."""
        if consumer not in self.customers:
            self.customers.append(consumer)
    
    def remove_customer(self, consumer):
        """Remove a customer from the bank."""
        if consumer in self.customers:
            self.customers.remove(consumer)
    
    def update_deposits(self):
        """Update total deposits from all customers."""
        self.total_deposits = sum(
            customer.bank_deposits for customer in self.customers
            if hasattr(customer, 'bank_deposits')
        )
    
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
        
        # Update reserves
        self.reserves = self.total_deposits - self.total_loans
    
    def calculate_metrics(self):
        """Calculate key performance metrics."""
        # Liquidity ratio
        self.liquidity_ratio = (
            self.reserves / self.total_deposits if self.total_deposits > 0 else 1.0
        )
        
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
            centrality_decay = cbdc_adoption_rate * self.cbdc_vulnerability
            
            # Small banks lose centrality faster
            if self.bank_type == "small_medium":
                centrality_decay *= 1.5  # 50% faster decline for small banks
            
            self.network_centrality = max(0.1, self.network_centrality - centrality_decay * 0.02)
            
            # H4: Reduce interbank connections as CBDC provides alternative
            if cbdc_adoption_rate > 0.3:  # When CBDC adoption exceeds 30%
                connection_loss = (cbdc_adoption_rate - 0.3) * 0.1
                self.interbank_connections = max(0, self.interbank_connections - connection_loss)
    
    def calculate_liquidity_stress(self):
        """Calculate liquidity stress level (H3)."""
        if self.model.cbdc_introduced:
            # H3: Rapid CBDC adoption creates liquidity stress
            cbdc_adoption_rate = self.model.compute_cbdc_adoption_rate()
            deposit_outflow_rate = min(0.8, cbdc_adoption_rate * self.cbdc_vulnerability)
            
            # Liquidity stress increases with deposit outflows
            self.liquidity_stress_level = deposit_outflow_rate * (1 - self.liquidity_ratio)
            
            # Small banks experience higher stress
            if self.bank_type == "small_medium" and self.liquidity_stress_level > 0.6:
                self.liquidity_stress_level *= 1.3  # 30% higher stress
    
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
    
    def __str__(self):
        return f"CommercialBank_{self.unique_id}: Deposits=${self.total_deposits:.0f}, Loans=${self.total_loans:.0f}, Customers={len(self.customers)}"
