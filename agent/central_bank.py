from mesa import Agent
import numpy as np

class CentralBank(Agent):
    """
    Central Bank agent that issues CBDC and implements monetary policy.
    
    The central bank introduces CBDC at a specified time and manages its adoption
    through interest rates and policy measures.
    """
    
    def __init__(self, unique_id, model, cbdc_interest_rate=0.045, initial_cbdc_supply=0):
        super().__init__(model)
        
        # Store agent properties
        self.unique_id = unique_id
        
        # CBDC parameters
        self.cbdc_interest_rate = cbdc_interest_rate
        self.cbdc_introduced = False
        self.cbdc_supply = initial_cbdc_supply
        self.cbdc_outstanding = 0  # Total CBDC held by consumers
        
        # Policy tools
        self.monetary_policy_rate = 0.02  # Base interest rate
        self.cbdc_attractiveness = 1.0    # Factor affecting CBDC adoption
        
        # Central bank objectives
        self.financial_stability_target = 0.8  # Target stability index
        self.inflation_target = 0.02          # 2% inflation target
        
        # Monitoring metrics
        self.banking_system_health = 1.0
        self.cbdc_adoption_rate = 0.0
        self.systemic_risk_level = 0.0
        
        # CBDC supply tracking
        self.total_supply_expansions = 0
        self.cumulative_supply_expansion = 0
        
        # CBDC exchange operations (1:1 exchange with commercial bank deposits)
        self.central_bank_deposits = 0  # Deposits received from commercial banks for CBDC exchanges
        self.total_cbdc_issued = 0      # Total CBDC issued through exchanges
        self.cbdc_reserves = 0          # CBDC reserves held by central bank
        
        # H6: Network centrality metrics for central bank dominance
        self.network_centrality = 0.1   # Minimal regulatory role initially
        self.degree_centrality = 0.05   # Limited direct connections initially
        self.betweenness_centrality = 0.08  # Some intermediary role in policy
        self.closeness_centrality = 0.12    # Central position but limited activity
        self.eigenvector_centrality = 0.06  # Low influence initially
    
    def step(self):
        """Execute one step of central bank operations."""
        if self.cbdc_introduced:
            # Monitor CBDC adoption and impact
            self.monitor_cbdc_impact()
            
            # Promote CBDC adoption continuously
            self.promote_cbdc_adoption()
            
            # Monitor banking system stability
            self.monitor_banking_system()
            
            # Update CBDC outstanding
            self.update_cbdc_outstanding()
            
            # Update centrality measures for network dominance analysis (H6)
            self.update_centrality_measures()
    
    def introduce_cbdc(self):
        """Introduce CBDC to the economy."""
        self.cbdc_introduced = True
        self.cbdc_supply = 0  # Start with zero supply - will expand based on demand
        
        # Notify all consumers about CBDC availability
        for consumer in self.model.consumers:
            consumer.cbdc_available = True
        
        print(f"Central Bank introduced CBDC with {self.cbdc_interest_rate*100:.1f}% interest rate")
        print("CBDC supply will expand automatically to meet demand")
    
    def monitor_cbdc_impact(self):
        """Monitor the impact of CBDC on the financial system."""
        # Calculate CBDC adoption rate
        self.cbdc_adoption_rate = self.model.compute_cbdc_adoption_rate()
        
        # Assess banking system health
        total_deposits_change = self.calculate_deposit_change()
        average_bank_liquidity = self.model.compute_average_bank_liquidity()
        
        # Banking system health score (0-1, where 1 is healthy)
        deposit_health = max(0, 1 - abs(total_deposits_change) * 0.5)
        liquidity_health = min(1, average_bank_liquidity / 0.2)  # Target 20% liquidity
        
        self.banking_system_health = (deposit_health + liquidity_health) / 2
        
        # Calculate systemic risk
        self.calculate_systemic_risk()
    
    def calculate_deposit_change(self):
        """Calculate the rate of change in bank deposits."""
        if len(self.model.datacollector.model_vars) > 1:
            data = self.model.datacollector.get_model_vars_dataframe()
            if len(data) > 1:
                recent_deposits = data['Total_Bank_Deposits'].iloc[-1]
                previous_deposits = data['Total_Bank_Deposits'].iloc[-2]
                return (recent_deposits - previous_deposits) / previous_deposits if previous_deposits > 0 else 0
        return 0
    
    def calculate_systemic_risk(self):
        """Calculate systemic risk level based on various factors."""
        # Factors contributing to systemic risk
        rapid_cbdc_adoption = min(1.0, self.cbdc_adoption_rate * 2)  # Risk if >50% adoption
        banking_instability = 1 - self.banking_system_health
        deposit_concentration_risk = self.calculate_deposit_concentration_risk()
        
        # Weighted systemic risk score
        self.systemic_risk_level = (
            rapid_cbdc_adoption * 0.4 +
            banking_instability * 0.4 +
            deposit_concentration_risk * 0.2
        )
    
    def calculate_deposit_concentration_risk(self):
        """Calculate risk from deposit concentration among banks."""
        bank_deposits = [bank.total_deposits for bank in self.model.commercial_banks]
        total_deposits = sum(bank_deposits)
        
        if total_deposits == 0:
            return 0
        
        # Calculate Herfindahl-Hirschman Index (HHI) for concentration
        market_shares = [deposits / total_deposits for deposits in bank_deposits]
        hhi = sum(share ** 2 for share in market_shares)
        
        # Convert HHI to risk score (higher concentration = higher risk)
        # HHI ranges from 1/n to 1, where n is number of banks
        min_hhi = 1 / len(self.model.commercial_banks)
        concentration_risk = (hhi - min_hhi) / (1 - min_hhi) if (1 - min_hhi) > 0 else 0
        
        return concentration_risk
    
    def promote_cbdc_adoption(self):
        """Actively promote CBDC adoption through positive incentives."""
        # Central bank's role is to encourage CBDC adoption, not constrain it
        # Gradually increase CBDC attractiveness over time
        self.cbdc_attractiveness *= 1.005  # Small consistent increase
        
        # Maintain competitive CBDC interest rate to encourage adoption
        if self.cbdc_interest_rate < 0.025:  # Keep rates attractive
            self.cbdc_interest_rate *= 1.002  # Gradual rate increases to stay competitive
    
    def monitor_banking_system(self):
        """Monitor the health of the commercial banking system."""
        # Check individual bank health
        weak_banks = 0
        total_banks = len(self.model.commercial_banks)
        
        for bank in self.model.commercial_banks:
            # A bank is considered weak if liquidity ratio is too low
            if bank.liquidity_ratio < 0.05:  # Less than 5% liquidity
                weak_banks += 1
        
        # If too many banks are weak, provide support while continuing CBDC promotion
        if weak_banks / total_banks > 0.3:  # More than 30% of banks are weak
            self.support_banking_system()
    
    def support_banking_system(self):
        """Provide support to banking system while continuing CBDC promotion."""
        # Lower monetary policy rate to support banks
        self.monetary_policy_rate = max(0.001, self.monetary_policy_rate * 0.9)
        
        # Continue promoting CBDC regardless of banking stress
        # Central bank maintains its CBDC objectives
        
        # Provide liquidity support (simplified)
        for bank in self.model.commercial_banks:
            if bank.liquidity_ratio < 0.05:
                # Emergency liquidity injection
                emergency_liquidity = bank.total_deposits * 0.1
                bank.reserves += emergency_liquidity
                bank.capital += emergency_liquidity  # Assume this is emergency funding
    
    def process_cbdc_exchanges(self):
        """Process 1:1 CBDC exchanges with commercial banks."""
        # Calculate current CBDC demand (total holdings by consumers)
        current_demand = sum(
            consumer.cbdc_holdings for consumer in self.model.consumers
            if hasattr(consumer, 'cbdc_holdings')
        )
        
        # Calculate new CBDC to be issued (exchange-based, not expansion)
        new_cbdc_needed = current_demand - self.cbdc_outstanding
        
        if new_cbdc_needed > 0:
            # Issue new CBDC through 1:1 exchange with bank deposits
            self.cbdc_outstanding = current_demand
            self.central_bank_deposits += new_cbdc_needed  # Receive equivalent deposits from banks
            self.total_cbdc_issued += new_cbdc_needed
            
            # Notify commercial banks to transfer deposits to central bank
            self.collect_deposits_for_cbdc_exchange(new_cbdc_needed)
            
            print(f"Central Bank issued ${new_cbdc_needed:,.0f} CBDC through 1:1 exchange")
            print(f"Total CBDC outstanding: ${self.cbdc_outstanding:,.0f}")
            print(f"Central Bank deposits from exchanges: ${self.central_bank_deposits:,.0f}")
    
    def collect_deposits_for_cbdc_exchange(self, exchange_amount):
        """Collect deposits from commercial banks for CBDC exchanges."""
        total_outflows = sum(
            getattr(bank, 'cbdc_related_outflows', 0) 
            for bank in self.model.commercial_banks
        )
        
        if total_outflows > 0:
            # Proportionally collect deposits from banks based on their CBDC outflows
            for bank in self.model.commercial_banks:
                bank_outflows = getattr(bank, 'cbdc_related_outflows', 0)
                if bank_outflows > 0:
                    bank_share = bank_outflows / total_outflows
                    bank_transfer = exchange_amount * bank_share
                    
                    # Bank transfers reserves to central bank
                    bank.cash_reserves = max(0, bank.cash_reserves - bank_transfer)
                    bank.reserves_transferred_to_cb = getattr(bank, 'reserves_transferred_to_cb', 0) + bank_transfer
    
    def update_cbdc_outstanding(self):
        """Update CBDC outstanding (calls new exchange-based method)."""
        self.process_cbdc_exchanges()
    
    def get_cbdc_promotion_effectiveness(self):
        """Assess how well CBDC promotion is working."""
        # Simple effectiveness based on adoption growth
        if self.cbdc_adoption_rate > 0.5:
            return 1.0  # Excellent adoption
        elif self.cbdc_adoption_rate > 0.3:
            return 0.8  # Good adoption
        elif self.cbdc_adoption_rate > 0.1:
            return 0.6  # Moderate adoption
        else:
            return 0.4  # Slow adoption - need more promotion
    
    def get_cbdc_statistics(self):
        """Get comprehensive CBDC statistics."""
        return {
            'cbdc_introduced': self.cbdc_introduced,
            'cbdc_adoption_rate': self.cbdc_adoption_rate,
            'cbdc_outstanding': self.cbdc_outstanding,
            'cbdc_supply': self.cbdc_supply,
            'cbdc_interest_rate': self.cbdc_interest_rate,
            'banking_system_health': self.banking_system_health,
            'systemic_risk_level': self.systemic_risk_level,
            'promotion_effectiveness': self.get_cbdc_promotion_effectiveness(),
            'total_supply_expansions': self.total_supply_expansions,
            'cumulative_supply_expansion': self.cumulative_supply_expansion
        }
    
    def update_centrality_measures(self):
        """Update central bank centrality measures based on CBDC adoption (H6)."""
        if self.cbdc_introduced:
            # Base centrality from regulatory role
            base_centrality = 0.1
            
            # Centrality boosts from CBDC adoption and market dominance
            adoption_boost = self.cbdc_adoption_rate * 0.6  # Up to 60% from adoption
            market_share = self.cbdc_outstanding / max(1, self.model.compute_total_consumer_wealth())
            market_boost = market_share * 0.4  # Up to 40% from market share
            
            # Monopoly position boost when adoption exceeds 30%
            monopoly_boost = min(0.2, self.cbdc_adoption_rate * 0.3) if self.cbdc_adoption_rate > 0.3 else 0
            
            # Update general network centrality
            self.network_centrality = base_centrality + adoption_boost + market_boost + monopoly_boost
            
            # Update specific centrality measures
            # Degree Centrality: Direct consumer connections through CBDC
            self.degree_centrality = 0.05 + (self.cbdc_adoption_rate * 0.8)  # Strong growth with adoption
            
            # Betweenness Centrality: Central position in monetary flows
            self.betweenness_centrality = 0.08 + (self.cbdc_adoption_rate * 0.85)  # Highest growth - central position
            
            # Closeness Centrality: Direct access to all market participants
            self.closeness_centrality = 0.12 + (self.cbdc_adoption_rate * 0.7)  # Moderate growth - already central
            
            # Eigenvector Centrality: Influence through network effects
            self.eigenvector_centrality = 0.06 + (self.cbdc_adoption_rate * 0.9)  # High growth - network dominance
            
            # Ensure bounds [0, 1]
            self.network_centrality = min(1.0, self.network_centrality)
            self.degree_centrality = min(1.0, self.degree_centrality)
            self.betweenness_centrality = min(1.0, self.betweenness_centrality)
            self.closeness_centrality = min(1.0, self.closeness_centrality)
            self.eigenvector_centrality = min(1.0, self.eigenvector_centrality)
    
    def __str__(self):
        return f"CentralBank: CBDC Supply=${self.cbdc_supply:.0f}, Outstanding=${self.cbdc_outstanding:.0f}, Adoption Rate={self.cbdc_adoption_rate:.1%}, System Health={self.banking_system_health:.2f}"
