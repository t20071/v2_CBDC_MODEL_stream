from mesa import Agent
import numpy as np

class Consumer(Agent):
    """
    Consumer agent that makes financial decisions between traditional banking and CBDC.
    
    Consumers have different preferences, risk tolerances, and adoption behaviors.
    They can hold both bank deposits and CBDC, adjusting their portfolio based on
    interest rates, convenience, and social influence.
    """
    
    def __init__(self, unique_id, model, initial_wealth=5000, 
                 cbdc_adoption_probability=0.03, risk_aversion=0.5):
        super().__init__(model)
        
        # Store agent properties
        self.unique_id = unique_id
        
        # Consumer characteristics
        self.initial_wealth = initial_wealth
        self.wealth = initial_wealth
        self.risk_aversion = max(0.1, min(0.9, risk_aversion))  # Constrain between 0.1 and 0.9
        self.cbdc_adoption_probability = cbdc_adoption_probability
        
        # Financial holdings (free choice between cash, deposits, CBDC)
        self.cash_holdings = initial_wealth * 0.15  # Start with 15% cash
        self.bank_deposits = initial_wealth * 0.85  # 85% in bank deposits
        self.cbdc_holdings = 0
        
        # CBDC adoption status and transaction limits
        self.cbdc_adopter = False
        self.cbdc_available = False
        self.adoption_step = None
        
        # CBDC transaction tracking for limits compliance
        self.daily_cbdc_transactions = 0
        self.daily_transfer_amount = 0
        self.daily_redemption_amount = 0
        self.monthly_p2p_count = 0
        self.cooling_period_amount = 0  # First 24 hours limit
        self.last_reset_day = 0
        
        # Payment method preferences (evolve over time)
        self.cash_preference = np.random.uniform(0.1, 0.3)    # 10-30% cash preference
        self.deposit_preference = np.random.uniform(0.5, 0.8) # 50-80% deposit preference
        self.cbdc_preference = 0.0  # Will develop after CBDC introduction
        
        # Banking relationship
        self.primary_bank = None
        self.bank_loyalty = np.random.normal(0.7, 0.2)  # Loyalty to traditional banking
        self.bank_loyalty = max(0.1, min(0.95, self.bank_loyalty))
        
        # Decision-making parameters
        self.interest_sensitivity = np.random.normal(0.5, 0.2)
        self.interest_sensitivity = max(0.1, min(0.9, self.interest_sensitivity))
        
        self.convenience_preference = np.random.normal(0.5, 0.2)
        self.convenience_preference = max(0.1, min(0.9, self.convenience_preference))
        
        # Social influence parameters
        self.social_influence_weight = np.random.normal(0.3, 0.1)
        self.social_influence_weight = max(0.0, min(0.6, self.social_influence_weight))
        
        # Economic behavior
        self.spending_rate = np.random.normal(0.02, 0.005)  # Monthly spending rate
        self.spending_rate = max(0.01, min(0.05, self.spending_rate))
        
        self.income_rate = np.random.normal(0.015, 0.005)  # Monthly income rate
        self.income_rate = max(0.01, min(0.03, self.income_rate))
    
    def step(self):
        """Execute one step of consumer behavior."""
        # Economic activities (income and spending)
        self.economic_activity()
        
        # CBDC adoption decision
        if self.cbdc_available and not self.cbdc_adopter:
            self.consider_cbdc_adoption()
        
        # Portfolio rebalancing
        if self.cbdc_adopter:
            self.rebalance_portfolio()
        
        # Update bank relationship
        self.update_banking_relationship()
    
    def economic_activity(self):
        """Handle regular economic activities - income and spending."""
        # Receive income
        monthly_income = self.initial_wealth * self.income_rate
        self.wealth += monthly_income
        
        # Allocate new income
        if self.cbdc_adopter:
            # Split between bank and CBDC based on preferences
            cbdc_allocation = monthly_income * self.get_cbdc_preference()
            bank_allocation = monthly_income - cbdc_allocation
            
            self.cbdc_holdings += cbdc_allocation
            self.bank_deposits += bank_allocation
        else:
            # All income goes to bank account
            self.bank_deposits += monthly_income
        
        # Spending (reduces holdings proportionally)
        monthly_spending = self.wealth * self.spending_rate
        spending_ratio = monthly_spending / self.wealth if self.wealth > 0 else 0
        
        if spending_ratio > 0:
            self.bank_deposits *= (1 - spending_ratio)
            self.cbdc_holdings *= (1 - spending_ratio)
            self.wealth -= monthly_spending
    
    def consider_cbdc_adoption(self):
        """Decide whether to adopt CBDC."""
        # Base adoption probability
        adoption_probability = self.cbdc_adoption_probability
        
        # Adjust based on interest rate differential
        if self.primary_bank:
            bank_rate = self.primary_bank.interest_rate
            cbdc_rate = self.model.central_bank.cbdc_interest_rate
            rate_advantage = cbdc_rate - bank_rate
            
            # Interest-sensitive consumers are more likely to adopt if CBDC offers better rates
            rate_influence = self.interest_sensitivity * rate_advantage * 10
            adoption_probability += rate_influence
        
        # Social influence (network effects)
        peer_adoption_rate = self.get_peer_adoption_rate()
        social_influence = self.social_influence_weight * peer_adoption_rate
        adoption_probability += social_influence
        
        # Convenience factor (CBDC is assumed to be more convenient)
        convenience_boost = self.convenience_preference * 0.1
        adoption_probability += convenience_boost
        
        # Risk aversion reduces adoption probability
        risk_penalty = self.risk_aversion * 0.05
        adoption_probability -= risk_penalty
        
        # Bank loyalty reduces adoption probability
        loyalty_penalty = self.bank_loyalty * 0.08
        adoption_probability -= loyalty_penalty
        
        # Make adoption decision
        if np.random.random() < adoption_probability:
            self.adopt_cbdc()
    
    def adopt_cbdc(self):
        """Adopt CBDC and start using it with transaction limits compliance."""
        self.cbdc_adopter = True
        self.adoption_step = self.model.current_step
        
        # Calculate initial transfer respecting CBDC limits
        desired_transfer = self.bank_deposits * (0.2 + (1 - self.bank_loyalty) * 0.3)  # 20-50%
        
        # Apply CBDC wallet holding limit (₹1,00,000)
        wallet_limit = 100000
        transfer_amount = min(desired_transfer, wallet_limit)
        
        # Apply cooling period limit for first 24 hours (₹5,000)
        if self.adoption_step == self.model.current_step:  # First day
            cooling_limit = 5000
            transfer_amount = min(transfer_amount, cooling_limit)
            self.cooling_period_amount = transfer_amount
        
        # Execute transfer
        self.bank_deposits -= transfer_amount
        self.cbdc_holdings += transfer_amount
        
        # Develop CBDC preference (starts low, may grow)
        self.cbdc_preference = np.random.uniform(0.05, 0.25)  # 5-25% initial preference
        
        # Reset daily limits tracking
        self.reset_daily_limits_if_needed()
        
        # Update bank relationship
        if self.primary_bank and transfer_amount > self.initial_wealth * 0.3:
            pass  # Bank will handle significant deposit reduction
    
    def reset_daily_limits_if_needed(self):
        """Reset daily transaction limits if a new day has started."""
        current_day = self.model.current_step // 24  # Assuming 24 steps = 1 day
        if current_day > self.last_reset_day:
            self.daily_cbdc_transactions = 0
            self.daily_transfer_amount = 0
            self.daily_redemption_amount = 0
            self.cooling_period_amount = 0  # Reset after first day
            self.last_reset_day = current_day
    
    def rebalance_portfolio(self):
        """Rebalance portfolio between cash, bank deposits, and CBDC with limits."""
        # Reset daily limits if needed
        self.reset_daily_limits_if_needed()
        
        if not self.cbdc_adopter:
            # Only rebalance between cash and deposits
            self.rebalance_traditional_portfolio()
            return
        
        total_wealth = self.cash_holdings + self.bank_deposits + self.cbdc_holdings
        if total_wealth <= 0:
            return
        
        # Determine target allocation based on preferences
        target_cash_ratio = self.cash_preference
        target_cbdc_ratio = self.get_cbdc_preference()
        target_deposit_ratio = 1.0 - target_cash_ratio - target_cbdc_ratio
        
        # Calculate target amounts
        target_cash = total_wealth * target_cash_ratio
        target_cbdc = min(total_wealth * target_cbdc_ratio, 100000)  # Wallet limit
        target_deposits = total_wealth - target_cash - target_cbdc
        
        # Execute rebalancing with transaction limits
        self.execute_portfolio_rebalancing(target_cash, target_deposits, target_cbdc)
    
    def rebalance_traditional_portfolio(self):
        """Rebalance between cash and deposits only (no CBDC)."""
        total_wealth = self.cash_holdings + self.bank_deposits
        if total_wealth <= 0:
            return
        
        # Normalize preferences without CBDC
        total_preference = self.cash_preference + self.deposit_preference
        if total_preference > 0:
            cash_ratio = self.cash_preference / total_preference
            deposit_ratio = self.deposit_preference / total_preference
        else:
            cash_ratio = 0.2
            deposit_ratio = 0.8
        
        target_cash = total_wealth * cash_ratio
        target_deposits = total_wealth * deposit_ratio
        
        # Simple rebalancing
        cash_adjustment = target_cash - self.cash_holdings
        self.cash_holdings += cash_adjustment
        self.bank_deposits -= cash_adjustment
    
    def execute_portfolio_rebalancing(self, target_cash, target_deposits, target_cbdc):
        """Execute portfolio rebalancing with CBDC transaction limits."""
        # Calculate required adjustments
        cash_adjustment = target_cash - self.cash_holdings
        deposit_adjustment = target_deposits - self.bank_deposits
        cbdc_adjustment = target_cbdc - self.cbdc_holdings
        
        # Check CBDC transaction limits before adjustments
        if cbdc_adjustment > 0:  # Increasing CBDC holdings
            # Check daily transfer limit
            if self.daily_transfer_amount + cbdc_adjustment > 50000:  # ₹50,000 daily limit
                cbdc_adjustment = max(0, 50000 - self.daily_transfer_amount)
            
            # Check per-transaction limit
            cbdc_adjustment = min(cbdc_adjustment, 10000)  # ₹10,000 per transaction
            
            # Check wallet holding limit
            if self.cbdc_holdings + cbdc_adjustment > 100000:  # ₹1,00,000 wallet limit
                cbdc_adjustment = max(0, 100000 - self.cbdc_holdings)
        
        elif cbdc_adjustment < 0:  # Decreasing CBDC holdings (redemption)
            # Check daily redemption limit
            redemption_amount = abs(cbdc_adjustment)
            if self.daily_redemption_amount + redemption_amount > 100000:  # ₹1,00,000 daily redemption limit
                cbdc_adjustment = -max(0, 100000 - self.daily_redemption_amount)
        
        # Execute adjustments
        if abs(cbdc_adjustment) > 0:
            self.cbdc_holdings += cbdc_adjustment
            self.bank_deposits -= cbdc_adjustment  # CBDC comes from/goes to deposits
            
            # Update daily tracking
            if cbdc_adjustment > 0:
                self.daily_transfer_amount += cbdc_adjustment
            else:
                self.daily_redemption_amount += abs(cbdc_adjustment)
            
            self.daily_cbdc_transactions += 1
        
        # Adjust cash holdings
        self.cash_holdings += cash_adjustment
        self.bank_deposits -= cash_adjustment
        
        # Ensure all holdings remain non-negative
        if self.cbdc_holdings < 0:
            self.bank_deposits += self.cbdc_holdings
            self.cbdc_holdings = 0
        if self.cash_holdings < 0:
            self.bank_deposits += self.cash_holdings
            self.cash_holdings = 0
        if self.bank_deposits < 0:
            self.bank_deposits = 0
    
    def get_cbdc_preference(self):
        """Calculate preferred CBDC allocation ratio."""
        if not self.cbdc_adopter:
            return 0.0
        
        # Base preference
        base_preference = 0.3  # 30% base allocation to CBDC
        
        # Adjust based on interest rate differential
        if self.primary_bank:
            bank_rate = self.primary_bank.interest_rate
            cbdc_rate = self.model.central_bank.cbdc_interest_rate
            rate_advantage = cbdc_rate - bank_rate
            
            # Interest-sensitive consumers allocate more to higher-yielding option
            rate_adjustment = self.interest_sensitivity * rate_advantage * 5
            base_preference += rate_adjustment
        
        # Convenience preference increases CBDC allocation
        convenience_adjustment = self.convenience_preference * 0.2
        base_preference += convenience_adjustment
        
        # Risk aversion reduces CBDC allocation (familiarity with banks)
        risk_adjustment = self.risk_aversion * 0.15
        base_preference -= risk_adjustment
        
        # Bank loyalty reduces CBDC allocation
        loyalty_adjustment = self.bank_loyalty * 0.2
        base_preference -= loyalty_adjustment
        
        # Social influence (if peers use CBDC heavily, increase allocation)
        peer_cbdc_usage = self.get_peer_cbdc_usage()
        social_adjustment = self.social_influence_weight * peer_cbdc_usage * 0.3
        base_preference += social_adjustment
        
        # Constrain between 0 and 0.8 (maximum 80% in CBDC)
        return max(0.0, min(0.8, base_preference))
    
    def get_peer_adoption_rate(self):
        """Get CBDC adoption rate among peers (simplified as overall adoption rate)."""
        return self.model.compute_cbdc_adoption_rate()
    
    def get_peer_cbdc_usage(self):
        """Get average CBDC usage ratio among peers."""
        total_cbdc = sum(consumer.cbdc_holdings for consumer in self.model.consumers if consumer.cbdc_adopter)
        total_wealth = sum(consumer.cbdc_holdings + consumer.bank_deposits for consumer in self.model.consumers if consumer.cbdc_adopter)
        
        if total_wealth > 0:
            return total_cbdc / total_wealth
        return 0.0
    
    def update_banking_relationship(self):
        """Update relationship with primary bank."""
        if self.primary_bank:
            # If deposits become very low, might switch banks or reduce relationship
            if self.bank_deposits < self.initial_wealth * 0.1:  # Less than 10% of initial wealth
                # Consider reducing bank relationship
                if np.random.random() < 0.05:  # 5% chance per step
                    self.bank_loyalty *= 0.9  # Reduce loyalty
            
            # Update bank about deposit changes
            # This is handled by the bank's update_deposits method
    
    def get_financial_profile(self):
        """Get comprehensive financial profile."""
        total_assets = self.bank_deposits + self.cbdc_holdings
        
        return {
            'total_wealth': self.wealth,
            'total_liquid_assets': total_assets,
            'bank_deposits': self.bank_deposits,
            'cbdc_holdings': self.cbdc_holdings,
            'cbdc_ratio': self.cbdc_holdings / total_assets if total_assets > 0 else 0,
            'cbdc_adopter': self.cbdc_adopter,
            'adoption_step': self.adoption_step,
            'risk_aversion': self.risk_aversion,
            'bank_loyalty': self.bank_loyalty,
            'interest_sensitivity': self.interest_sensitivity
        }
    
    def __str__(self):
        return f"Consumer_{self.unique_id}: Wealth=${self.wealth:.0f}, Bank=${self.bank_deposits:.0f}, CBDC=${self.cbdc_holdings:.0f}, Adopter={self.cbdc_adopter}"
