from mesa import Agent
import numpy as np

class CentralBank(Agent):
    """
    Central Bank agent that issues CBDC and implements monetary policy.
    
    The central bank introduces CBDC at a specified time and manages its adoption
    through interest rates and policy measures.
    """
    
    def __init__(self, unique_id, model, cbdc_interest_rate=0.01, initial_cbdc_supply=0):
        super().__init__()
        
        # Store agent properties
        self.unique_id = unique_id
        self.model = model
        
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
    
    def step(self):
        """Execute one step of central bank operations."""
        if self.cbdc_introduced:
            # Monitor CBDC adoption and impact
            self.monitor_cbdc_impact()
            
            # Adjust CBDC policy if needed
            self.adjust_cbdc_policy()
            
            # Monitor banking system stability
            self.monitor_banking_system()
            
            # Update CBDC outstanding
            self.update_cbdc_outstanding()
    
    def introduce_cbdc(self):
        """Introduce CBDC to the economy."""
        self.cbdc_introduced = True
        self.cbdc_supply = 1000000  # Initial CBDC supply
        
        # Notify all consumers about CBDC availability
        for consumer in self.model.consumers:
            consumer.cbdc_available = True
        
        print(f"Central Bank introduced CBDC with {self.cbdc_interest_rate*100:.1f}% interest rate")
    
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
    
    def adjust_cbdc_policy(self):
        """Adjust CBDC policy based on system conditions."""
        # If systemic risk is high, consider policy adjustments
        if self.systemic_risk_level > 0.7:
            # Reduce CBDC attractiveness to slow adoption
            self.cbdc_attractiveness *= 0.95  # Gradual reduction
            
            # Potentially lower CBDC interest rate
            if self.cbdc_interest_rate > 0.005:  # Don't go below 0.5%
                self.cbdc_interest_rate *= 0.98
        
        elif self.systemic_risk_level < 0.3 and self.cbdc_adoption_rate < 0.2:
            # Low risk and slow adoption - can increase attractiveness
            self.cbdc_attractiveness *= 1.02
            
            # Potentially increase CBDC interest rate to encourage adoption
            if self.cbdc_interest_rate < 0.03:  # Cap at 3%
                self.cbdc_interest_rate *= 1.01
    
    def monitor_banking_system(self):
        """Monitor the health of the commercial banking system."""
        # Check individual bank health
        weak_banks = 0
        total_banks = len(self.model.commercial_banks)
        
        for bank in self.model.commercial_banks:
            # A bank is considered weak if liquidity ratio is too low
            if bank.liquidity_ratio < 0.05:  # Less than 5% liquidity
                weak_banks += 1
        
        # If too many banks are weak, consider intervention
        if weak_banks / total_banks > 0.3:  # More than 30% of banks are weak
            self.implement_emergency_measures()
    
    def implement_emergency_measures(self):
        """Implement emergency measures if banking system is under stress."""
        # Lower monetary policy rate to support banks
        self.monetary_policy_rate = max(0.001, self.monetary_policy_rate * 0.9)
        
        # Reduce CBDC attractiveness temporarily
        self.cbdc_attractiveness *= 0.9
        
        # Provide liquidity support (simplified)
        for bank in self.model.commercial_banks:
            if bank.liquidity_ratio < 0.05:
                # Emergency liquidity injection
                emergency_liquidity = bank.total_deposits * 0.1
                bank.reserves += emergency_liquidity
                bank.capital += emergency_liquidity  # Assume this is emergency funding
    
    def update_cbdc_outstanding(self):
        """Update the total CBDC outstanding in the economy."""
        self.cbdc_outstanding = sum(
            consumer.cbdc_holdings for consumer in self.model.consumers
            if hasattr(consumer, 'cbdc_holdings')
        )
    
    def get_policy_effectiveness(self):
        """Assess the effectiveness of CBDC policy."""
        # Effectiveness based on achieving objectives without excessive systemic risk
        adoption_score = min(1.0, self.cbdc_adoption_rate / 0.3)  # Target 30% adoption
        stability_score = 1 - self.systemic_risk_level
        
        # Balanced score
        effectiveness = (adoption_score + stability_score) / 2
        return effectiveness
    
    def get_cbdc_statistics(self):
        """Get comprehensive CBDC statistics."""
        return {
            'cbdc_introduced': self.cbdc_introduced,
            'cbdc_adoption_rate': self.cbdc_adoption_rate,
            'cbdc_outstanding': self.cbdc_outstanding,
            'cbdc_interest_rate': self.cbdc_interest_rate,
            'banking_system_health': self.banking_system_health,
            'systemic_risk_level': self.systemic_risk_level,
            'policy_effectiveness': self.get_policy_effectiveness()
        }
    
    def __str__(self):
        return f"CentralBank: CBDC Outstanding=${self.cbdc_outstanding:.0f}, Adoption Rate={self.cbdc_adoption_rate:.1%}, System Health={self.banking_system_health:.2f}"
