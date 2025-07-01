from mesa import Agent
import numpy as np
from typing import Optional, TYPE_CHECKING, cast

if TYPE_CHECKING:
    from agent.commercial_bank import CommercialBank
    from model import CBDCBankingModel

class Consumer(Agent):
    """
    Consumer agent that makes financial decisions between traditional banking and CBDC.
    
    Consumers have different preferences, risk tolerances, and adoption behaviors.
    They can hold both bank deposits and CBDC, adjusting their portfolio based on
    interest rates, convenience, and social influence.
    """
    
    def __init__(self, unique_id, model, initial_wealth=8400, 
                 cbdc_adoption_probability=0.08, risk_aversion=0.55):
        super().__init__(model)
        
        # Store agent properties
        self.unique_id = unique_id
        
        # Consumer characteristics
        self.initial_wealth = initial_wealth
        self.wealth = initial_wealth
        self.risk_aversion = max(0.1, min(0.9, risk_aversion))  # Constrain between 0.1 and 0.9
        self.cbdc_adoption_probability = cbdc_adoption_probability
        
        # Financial holdings - 37% of wealth in bank deposits initially
        self.bank_deposits = initial_wealth * 0.37  # 37% in bank deposits
        self.cbdc_holdings = 0
        self.other_assets = initial_wealth * 0.63  # 63% in other assets (savings, investments, cash)
        
        # CBDC adoption status
        self.cbdc_adopter = False
        self.cbdc_available = False
        self.adoption_step = None
        
        # Banking relationship
        self.primary_bank: Optional['CommercialBank'] = None
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
        
        # Economic activity parameters
        self.income_rate = np.random.normal(0.02, 0.005)  # Monthly income growth
        self.income_rate = max(0.01, min(0.05, self.income_rate))
        
        self.spending_rate = np.random.normal(0.015, 0.005)  # Monthly spending rate
        self.spending_rate = max(0.005, min(0.03, self.spending_rate))
    
    def get_model(self) -> 'CBDCBankingModel':
        """Get model with proper typing"""
        # Type: ignore the model attribute access for LSP
        return self.model  # type: ignore
    
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
        
        # Realistic income allocation - new income goes to existing payment methods
        # CBDC adopters choose WHERE to receive their income (direct deposit choice)
        if self.cbdc_adopter:
            # Income can be received directly to CBDC account (like direct deposit to digital wallet)
            cbdc_income_preference = self.get_cbdc_preference() * 0.6  # Max 60% of income to CBDC
            direct_cbdc_income = monthly_income * cbdc_income_preference
            bank_income = monthly_income * 0.37  # Still need some bank relationship
            other_income = monthly_income - direct_cbdc_income - bank_income
            
            self.cbdc_holdings += direct_cbdc_income
            self.bank_deposits += bank_income  
            self.other_assets += other_income
        else:
            # Non-adopters receive all income through traditional banking
            bank_allocation = monthly_income * 0.37
            other_allocation = monthly_income * 0.63
            
            self.bank_deposits += bank_allocation
            self.other_assets += other_allocation
        
        # Consumer-to-consumer transactions (daily spending through transfers)
        monthly_spending = self.wealth * self.spending_rate
        self.execute_daily_transactions(monthly_spending)
        
        # Reduce wealth by spending amount
        self.wealth -= monthly_spending
    
    def consider_cbdc_adoption(self):
        """Decide whether to adopt CBDC."""
        # Base adoption probability
        adoption_probability = self.cbdc_adoption_probability
        
        # Adjust based on interest rate differential
        if self.primary_bank:
            bank_rate = self.primary_bank.interest_rate
            cbdc_rate = self.get_model().central_bank.cbdc_interest_rate
            rate_advantage = cbdc_rate - bank_rate
            
            # Interest-sensitive consumers are more likely to adopt if CBDC offers better rates
            rate_influence = self.interest_sensitivity * rate_advantage * 10
            adoption_probability += rate_influence
        
        # Social influence (network effects) - accelerates with time
        peer_adoption_rate = self.get_peer_adoption_rate()
        social_influence = self.social_influence_weight * peer_adoption_rate
        
        # Time momentum - adoption accelerates over time
        model = self.get_model()
        steps_since_introduction = model.current_step - model.cbdc_introduction_step
        momentum_factor = min(0.8, steps_since_introduction * 0.04)  # Builds momentum
        social_influence *= (1 + momentum_factor)  # Amplifies social influence
        
        adoption_probability += social_influence
        
        # Banking system stress drives CBDC adoption
        bank_stress = 0
        if self.primary_bank and hasattr(self.primary_bank, 'liquidity_stress_level'):
            bank_stress = self.primary_bank.liquidity_stress_level
            stress_penalty = bank_stress * 0.15  # Stress drives switch to CBDC
            adoption_probability += stress_penalty
        
        # Convenience factor (CBDC is assumed to be more convenient)
        convenience_boost = self.convenience_preference * 0.1
        adoption_probability += convenience_boost
        
        # Risk aversion reduces adoption probability (but less if bank is stressed)
        risk_penalty = self.risk_aversion * 0.05 * (1 - bank_stress * 0.5)
        adoption_probability -= risk_penalty
        
        # Bank loyalty reduces adoption probability (weakens under stress)
        loyalty_penalty = self.bank_loyalty * 0.08 * (1 - bank_stress * 0.7)
        adoption_probability -= loyalty_penalty
        
        # Make adoption decision
        if np.random.random() < adoption_probability:
            self.adopt_cbdc()
    
    def adopt_cbdc(self):
        """Adopt CBDC and start using it."""
        self.cbdc_adopter = True
        self.adoption_step = self.get_model().current_step
        
        # Realistic CBDC adoption - exchange bank deposits for CBDC through central bank
        # No new money is created, only payment method substitution
        initial_transfer_rate = 0.2 + (1 - self.bank_loyalty) * 0.3  # 20-50% initial exchange
        exchange_amount = self.bank_deposits * initial_transfer_rate
        
        # Minimum meaningful exchange (like opening a new digital wallet)
        min_exchange = min(self.bank_deposits * 0.15, self.initial_wealth * 0.1)
        exchange_amount = max(exchange_amount, min_exchange)
        
        # Cap exchange to available bank deposits
        exchange_amount = min(exchange_amount, self.bank_deposits)
        
        if exchange_amount > 0:
            # Consumer exchanges bank deposits for CBDC (1:1 exchange rate)
            self.bank_deposits -= exchange_amount
            self.cbdc_holdings += exchange_amount
            
            # Track this as a payment method substitution, not new money creation
            self.total_cbdc_exchanges = getattr(self, 'total_cbdc_exchanges', 0) + exchange_amount
            
            # Update bank's deposits (bank loses this deposit to central bank)
            if self.primary_bank:
                self.primary_bank.update_deposits()
                # Reduce bank loyalty after switching payment methods
                if exchange_amount > self.initial_wealth * 0.2:
                    self.bank_loyalty *= 0.8  # Moderate loyalty reduction
    
    def rebalance_portfolio(self):
        """Rebalance portfolio between bank deposits, CBDC, and other assets."""
        if not self.cbdc_adopter:
            return
        
        # Total liquid wealth includes bank deposits, CBDC, and moveable other assets
        moveable_other_assets = self.other_assets * 0.5  # 50% of other assets can be moved
        total_liquid_wealth = self.bank_deposits + self.cbdc_holdings + moveable_other_assets
        if total_liquid_wealth <= 0:
            return
        
        # Determine optimal CBDC allocation
        target_cbdc_ratio = self.get_cbdc_preference()
        target_cbdc_amount = total_liquid_wealth * target_cbdc_ratio
        
        # Accelerated rebalancing with momentum effect
        base_adjustment_speed = 0.2  # 20% adjustment per step (increased from 10%)
        
        # Momentum factor - people move more aggressively to CBDC over time
        momentum_boost = 0
        if hasattr(self, 'adoption_step') and self.adoption_step is not None:
            model = self.get_model()
            steps_since_adoption = model.current_step - self.adoption_step
            momentum_boost = min(0.15, steps_since_adoption * 0.01)  # Up to 15% boost
        
        adjustment_speed = base_adjustment_speed + momentum_boost
        cbdc_gap = target_cbdc_amount - self.cbdc_holdings
        adjustment = cbdc_gap * adjustment_speed
        
        # Make the adjustment with minimum threshold
        if abs(adjustment) > 10:  # Lowered threshold for more frequent adjustments
            old_bank_deposits = self.bank_deposits
            
            if adjustment > 0:  # Moving more money TO CBDC
                # Prioritize transferring from bank deposits first
                from_bank = min(adjustment, self.bank_deposits)
                remaining_needed = adjustment - from_bank
                
                # If need more, get from other assets
                from_other = min(remaining_needed, moveable_other_assets)
                
                # Execute transfers
                self.bank_deposits -= from_bank
                self.other_assets -= from_other
                self.cbdc_holdings += (from_bank + from_other)
                
            else:  # Moving money FROM CBDC (rare case)
                transfer_amount = min(abs(adjustment), self.cbdc_holdings)
                self.cbdc_holdings -= transfer_amount
                # Put back into bank deposits for simplicity
                self.bank_deposits += transfer_amount
            
            # Ensure non-negative holdings
            self.bank_deposits = max(0, self.bank_deposits)
            self.cbdc_holdings = max(0, self.cbdc_holdings)
            self.other_assets = max(0, self.other_assets)
            
            # Update bank's total deposits if significant change occurred
            if self.primary_bank and abs(self.bank_deposits - old_bank_deposits) > 50:
                self.primary_bank.update_deposits()
    
    def get_cbdc_preference(self):
        """Calculate preferred CBDC allocation ratio."""
        if not self.cbdc_adopter:
            return 0.0
        
        # Progressive base preference that grows over time
        base_preference = 0.5  # Start with 50% allocation (increased from 30%)
        
        # Time-based preference acceleration
        if hasattr(self, 'adoption_step') and self.adoption_step is not None:
            model = self.get_model()
            steps_since_adoption = model.current_step - self.adoption_step
            time_growth = min(0.4, steps_since_adoption * 0.025)  # Up to 40% growth over time
            base_preference += time_growth
        
        # Interest rate differential impact (stronger effect)
        if self.primary_bank:
            bank_rate = self.primary_bank.interest_rate
            cbdc_rate = self.get_model().central_bank.cbdc_interest_rate
            rate_advantage = cbdc_rate - bank_rate
            rate_adjustment = self.interest_sensitivity * rate_advantage * 10  # Doubled impact
            base_preference += rate_adjustment
        
        # Banking system stress drives CBDC preference
        bank_stress_boost = 0
        if self.primary_bank and hasattr(self.primary_bank, 'liquidity_stress_level'):
            bank_stress = self.primary_bank.liquidity_stress_level
            bank_stress_boost = bank_stress * 0.3  # Up to 30% boost during stress
            base_preference += bank_stress_boost
        
        # Enhanced convenience preference
        convenience_adjustment = self.convenience_preference * 0.3  # Increased from 0.2
        base_preference += convenience_adjustment
        
        # Reduced risk penalty during banking stress
        stress_modifier = 1 - (bank_stress_boost * 0.7)
        risk_adjustment = self.risk_aversion * 0.1 * stress_modifier  # Reduced penalty
        base_preference -= risk_adjustment
        
        # Weakening bank loyalty over time and stress
        model = self.get_model()
        time_growth = max(0, (model.current_step - model.cbdc_introduction_step) / 50.0)
        time_decay = min(0.5, time_growth * 2)
        stress_decay = bank_stress_boost * 0.8
        loyalty_modifier = max(0.3, 1 - time_decay - stress_decay)
        loyalty_adjustment = self.bank_loyalty * 0.15 * loyalty_modifier
        base_preference -= loyalty_adjustment
        
        # Amplified social influence
        peer_cbdc_usage = self.get_peer_cbdc_usage()
        social_adjustment = self.social_influence_weight * peer_cbdc_usage * 0.4  # Increased
        base_preference += social_adjustment
        
        # Higher maximum allocation to CBDC
        return max(0.0, min(0.9, base_preference))  # Up to 90% in CBDC
    
    def get_peer_adoption_rate(self):
        """Get CBDC adoption rate among peers (simplified as overall adoption rate)."""
        return self.model.compute_cbdc_adoption_rate()  # type: ignore
    
    def get_peer_cbdc_usage(self):
        """Get average CBDC usage ratio among peers."""
        total_cbdc = sum(consumer.cbdc_holdings for consumer in self.model.consumers if consumer.cbdc_adopter)  # type: ignore
        total_wealth = sum(consumer.cbdc_holdings + consumer.bank_deposits for consumer in self.model.consumers if consumer.cbdc_adopter)  # type: ignore
        
        if total_wealth > 0:
            return total_cbdc / total_wealth
        return 0.0
    
    def execute_daily_transactions(self, total_spending):
        """Execute daily consumer-to-consumer transactions using preferred payment methods."""
        if total_spending <= 0:
            return
        
        # Get model reference for transaction tracking
        model = self.get_model()
        
        # Determine payment method based on CBDC adoption and holdings
        if self.cbdc_adopter and self.cbdc_holdings > 0:
            # CBDC adopters prefer CBDC for transactions when available
            cbdc_preference = self.get_cbdc_preference()
            
            # Split spending between CBDC and bank transfers
            cbdc_spending = min(total_spending * cbdc_preference, self.cbdc_holdings)
            bank_spending = total_spending - cbdc_spending
            
            # Execute CBDC transactions
            if cbdc_spending > 0:
                self.cbdc_holdings -= cbdc_spending
                self.record_transaction(cbdc_spending, "CBDC", model)
            
            # Execute bank transactions for remaining amount
            if bank_spending > 0:
                bank_payment = min(bank_spending, self.bank_deposits)
                other_payment = bank_spending - bank_payment
                
                self.bank_deposits -= bank_payment
                self.other_assets -= other_payment  # Use savings if needed
                
                if bank_payment > 0:
                    self.record_transaction(bank_payment, "Bank", model)
                if other_payment > 0:
                    self.record_transaction(other_payment, "Other", model)
        else:
            # Non-adopters use traditional banking for all transactions
            bank_payment = min(total_spending, self.bank_deposits)
            other_payment = total_spending - bank_payment
            
            self.bank_deposits -= bank_payment
            self.other_assets -= other_payment
            
            if bank_payment > 0:
                self.record_transaction(bank_payment, "Bank", model)
            if other_payment > 0:
                self.record_transaction(other_payment, "Other", model)
    
    def record_transaction(self, amount, payment_method, model):
        """Record transaction for analysis and tracking."""
        # Track transaction volumes by payment method
        if not hasattr(model, 'transaction_volumes'):
            model.transaction_volumes = {"Bank": 0, "CBDC": 0, "Other": 0}
        
        if not hasattr(model, 'transaction_counts'):
            model.transaction_counts = {"Bank": 0, "CBDC": 0, "Other": 0}
        
        model.transaction_volumes[payment_method] += amount
        model.transaction_counts[payment_method] += 1
        
        # Track monthly totals for step-by-step analysis
        current_step = model.current_step
        if not hasattr(model, 'monthly_transactions'):
            model.monthly_transactions = {}
        
        if current_step not in model.monthly_transactions:
            model.monthly_transactions[current_step] = {"Bank": 0, "CBDC": 0, "Other": 0}
        
        model.monthly_transactions[current_step][payment_method] += amount

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
