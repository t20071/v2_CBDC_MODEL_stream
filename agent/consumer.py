from mesa import Agent
import numpy as np
import random
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
        super().__init__(unique_id,model)
        
        # Store agent properties
        self.unique_id = unique_id
        
        # Consumer characteristics
        self.initial_wealth = initial_wealth
        self.wealth = initial_wealth
        self.risk_aversion = max(0.1, min(0.9, risk_aversion))  # Constrain between 0.1 and 0.9
        self.cbdc_adoption_probability = cbdc_adoption_probability
        
        # Financial holdings - Three-tier monetary system
        # Central bank liabilities: banknotes + CBDC
        # Commercial bank liabilities: deposits
        self.bank_deposits = initial_wealth * 0.30  # 30% in bank deposits (commercial bank liability)
        self.banknote_holdings = initial_wealth * 0.12  # 12% in cash/banknotes (central bank liability)
        self.cbdc_holdings = 0  # No CBDC initially (will be central bank liability)
        self.other_assets = initial_wealth * 0.58  # 58% in other assets (investments, etc.)
        
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
        
        # Shopping and payment behavior
        self.monthly_spending = initial_wealth * 0.15  # 15% of wealth spent monthly
        self.cbdc_wallet_balance = 0  # CBDC wallet for direct merchant payments
        self.transaction_history = []  # Track payment methods used
        self.preferred_payment_method = "bank_transfer"  # Default before CBDC
    
    def get_model(self) -> 'CBDCBankingModel':
        """Get model with proper typing"""
        # Type: ignore the model attribute access for LSP
        return self.model  # type: ignore
    
    def step(self):
        """Execute one step of consumer behavior."""
        # Economic activities (income and spending)
        self.economic_activity()
        
        # Shopping with merchants
        self.conduct_merchant_transactions()
        
        # CBDC adoption decision
        if self.cbdc_available and not self.cbdc_adopter:
            self.consider_cbdc_adoption()
        
        # Portfolio rebalancing
        if self.cbdc_adopter:
            self.rebalance_portfolio()
        
        # Update bank relationship
        self.update_banking_relationship()

    def conduct_merchant_transactions(self):
        """Handle consumer purchases from merchants with payment method selection."""
        model = self.get_model()
        
        # Calculate transaction budget based on wealth and spending patterns
        transaction_budget = self.wealth * 0.003  # 0.3% of wealth per step for transactions
        
        if transaction_budget < 1:
            return
        
        # Select merchants for transactions
        if not hasattr(model, 'merchants') or len(model.merchants) == 0:
            return
        
        num_transactions = max(1, int(np.random.poisson(2)))  # Average 2 transactions per step
        
        for _ in range(num_transactions):
            if transaction_budget <= 1:
                break
            
            # Select random merchant
            merchant = random.choice(model.merchants)
            
            # Determine transaction size based on merchant type
            if merchant.business_type == "grocery":
                transaction_size = min(transaction_budget, max(5, np.random.normal(40, 15)))
            elif merchant.business_type == "restaurant":
                transaction_size = min(transaction_budget, max(5, np.random.normal(25, 10)))
            elif merchant.business_type == "retail":
                transaction_size = min(transaction_budget, max(5, np.random.normal(60, 25)))
            elif merchant.business_type == "utility":
                transaction_size = min(transaction_budget, max(10, np.random.normal(100, 20)))
            elif merchant.business_type == "online":
                transaction_size = min(transaction_budget, max(5, np.random.normal(80, 35)))
            else:
                transaction_size = min(transaction_budget, max(5, np.random.normal(30, 15)))
            
            transaction_size = max(1, transaction_size)
            
            # Determine payment method
            payment_method = self.select_payment_method_for_transaction(transaction_size, merchant)
            
            # Execute transaction
            if self.execute_transaction(transaction_size, payment_method, merchant):
                transaction_budget -= transaction_size
    
    def select_payment_method_for_transaction(self, transaction_size, merchant):
        """Select payment method for transaction with specific merchant."""
        model = self.get_model()
        
        # Check if CBDC is available and adopted
        if self.cbdc_adopter and hasattr(model, 'cbdc_introduced') and model.cbdc_introduced:
            # Check if merchant accepts CBDC
            if hasattr(merchant, 'accepts_cbdc') and merchant.accepts_cbdc:
                # Prefer CBDC for direct peer-to-peer transactions
                if self.cbdc_holdings >= transaction_size:
                    return "CBDC_DIRECT"
            
            # If merchant doesn't accept CBDC or insufficient CBDC, use bank transfer
            if self.bank_deposits >= transaction_size:
                return "BANK_TRANSFER"
        
        # Before CBDC or non-adopters use traditional methods
        if self.bank_deposits >= transaction_size:
            return "BANK_TRANSFER"
        elif self.other_assets >= transaction_size:
            return "CASH"
        else:
            return "INSUFFICIENT_FUNDS"
    
    def execute_transaction(self, amount, payment_method, merchant):
        """Execute transaction with specified payment method."""
        model = self.get_model()
        
        if payment_method == "CBDC_DIRECT":
            # Direct CBDC payment to merchant's wallet
            if self.cbdc_holdings >= amount:
                self.cbdc_holdings -= amount
                # Add to merchant's CBDC wallet
                if hasattr(merchant, 'cbdc_wallet_balance'):
                    merchant.cbdc_wallet_balance += amount
                else:
                    merchant.cbdc_wallet_balance = amount
                
                self.record_transaction(amount, "CBDC_DIRECT", model)
                return True
        
        elif payment_method == "BANK_TRANSFER":
            # Traditional bank transfer to merchant's bank account
            if self.bank_deposits >= amount:
                self.bank_deposits -= amount
                # Add to merchant's bank account
                if hasattr(merchant, 'bank_account_balance'):
                    merchant.bank_account_balance += amount
                else:
                    merchant.bank_account_balance = amount
                
                self.record_transaction(amount, "BANK_TRANSFER", model)
                return True
        
        elif payment_method == "CASH":
            # Cash payment (deducted from other assets)
            if self.other_assets >= amount:
                self.other_assets -= amount
                # Add to merchant's cash
                if hasattr(merchant, 'cash_balance'):
                    merchant.cash_balance += amount
                else:
                    merchant.cash_balance = amount
                
                self.record_transaction(amount, "CASH", model)
                return True
        
        return False
    
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
        """Rebalance portfolio between bank deposits, banknotes, CBDC, and other assets."""
        if not self.cbdc_adopter:
            return
        
        # Total liquid wealth includes all money types
        moveable_other_assets = self.other_assets * 0.5  # 50% of other assets can be moved
        total_liquid_wealth = self.bank_deposits + self.banknote_holdings + self.cbdc_holdings + moveable_other_assets
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
                # Process conversions through central bank (proper liability tracking)
                model = self.get_model()
                
                # Strategy: Convert banknotes first (easier 1:1 exchange), then deposits
                from_banknotes = min(adjustment, self.banknote_holdings)
                remaining_needed = adjustment - from_banknotes
                
                # Convert banknotes to CBDC through central bank
                if from_banknotes > 0:
                    model.central_bank.process_cbdc_conversion(self, from_banknotes, "banknotes")
                
                # Convert deposits to CBDC through central bank
                from_deposits = min(remaining_needed, self.bank_deposits)
                if from_deposits > 0:
                    model.central_bank.process_cbdc_conversion(self, from_deposits, "deposits")
                
                # If still need more, use other assets
                remaining_needed = adjustment - from_banknotes - from_deposits
                from_other = min(remaining_needed, moveable_other_assets)
                if from_other > 0:
                    self.other_assets -= from_other
                    self.cbdc_holdings += from_other
                
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
        """Execute daily transactions with merchants using preferred payment methods."""
        if total_spending <= 0:
            return
        
        # Get model reference for transaction tracking and merchant access
        model = self.get_model()
        
        # Real-world transaction scenarios with merchants
        if hasattr(model, 'merchants') and model.merchants:
            # Select merchants for transactions (simulate daily shopping patterns)
            daily_transaction_count = max(1, int(np.random.poisson(3)))  # Average 3 transactions per day
            
            remaining_spending = total_spending
            for _ in range(daily_transaction_count):
                if remaining_spending <= 1:
                    break
                
                # Select random merchant for transaction
                merchant = random.choice(model.merchants)
                
                # Transaction size based on merchant type and consumer spending pattern
                if merchant.business_type == "grocery":
                    transaction_size = min(remaining_spending, np.random.normal(65, 25))
                elif merchant.business_type == "restaurant":
                    transaction_size = min(remaining_spending, np.random.normal(35, 15))
                elif merchant.business_type == "retail":
                    transaction_size = min(remaining_spending, np.random.normal(85, 40))
                elif merchant.business_type == "utility":
                    transaction_size = min(remaining_spending, np.random.normal(150, 30))
                elif merchant.business_type == "online":
                    transaction_size = min(remaining_spending, np.random.normal(120, 60))
                else:
                    transaction_size = min(remaining_spending, np.random.normal(50, 25))
                
                transaction_size = max(1, transaction_size)
                
                # Determine payment method based on CBDC adoption, merchant acceptance, and transaction size
                payment_method = self.select_payment_method_for_merchant(transaction_size, merchant)
                
                # Execute transaction based on payment method
                if payment_method == "CBDC" and self.cbdc_holdings >= transaction_size:
                    self.cbdc_holdings -= transaction_size
                    self.record_transaction(transaction_size, "CBDC", model)
                elif payment_method == "bank_transfer" and self.bank_deposits >= transaction_size:
                    self.bank_deposits -= transaction_size
                    self.record_transaction(transaction_size, "Bank", model)
                elif payment_method in ["cash", "card"]:
                    # For cash/card, deduct from bank deposits (simplified)
                    if self.bank_deposits >= transaction_size:
                        self.bank_deposits -= transaction_size
                        self.record_transaction(transaction_size, "Other", model)
                    elif self.other_assets >= transaction_size:
                        # Use other assets if bank deposits insufficient
                        self.other_assets -= transaction_size
                        self.record_transaction(transaction_size, "Other", model)
                
                remaining_spending -= transaction_size
    
    def select_payment_method_for_merchant(self, transaction_size, merchant):
        """Select payment method for transaction with specific merchant."""
        # Base preferences: consumer's CBDC adoption and holdings
        payment_options = {}
        
        # CBDC option (if adopted and merchant accepts)
        if self.cbdc_adopter and self.cbdc_holdings >= transaction_size:
            # Check if merchant accepts CBDC
            if hasattr(merchant, 'payment_preferences') and merchant.payment_preferences.get("cbdc", 0) > 0:
                payment_options["CBDC"] = merchant.payment_preferences["cbdc"] * self.get_cbdc_preference()
        
        # Bank transfer option
        if self.bank_deposits >= transaction_size:
            bank_score = merchant.payment_preferences.get("bank_transfer", 0.3)
            # Large transactions favor bank transfers
            if transaction_size > 100:
                bank_score *= 1.5
            payment_options["bank_transfer"] = bank_score
        
        # Cash option (prefer for small transactions if available)
        if transaction_size < 50 and self.bank_deposits >= transaction_size:
            cash_score = merchant.payment_preferences.get("cash", 0.6)
            payment_options["cash"] = cash_score * 1.2  # Boost cash for small amounts
        
        # Card option (general fallback)
        if self.bank_deposits >= transaction_size:
            card_score = merchant.payment_preferences.get("card", 0.8)
            payment_options["card"] = card_score
        
        # Select payment method with highest score
        if payment_options:
            return max(payment_options.items(), key=lambda x: x[1])[0]
        
        # Fallback to bank transfer if no specific preferences
        return "bank_transfer"
    
    def record_transaction(self, amount, payment_method, model):
        """Record transaction for analysis and tracking."""
        # Initialize transaction tracking if needed
        if not hasattr(model, 'transaction_volumes'):
            model.transaction_volumes = {
                "Bank": 0, "CBDC": 0, "Other": 0, 
                "BANK_TRANSFER": 0, "CBDC_DIRECT": 0, "CASH": 0
            }
        
        if not hasattr(model, 'transaction_counts'):
            model.transaction_counts = {
                "Bank": 0, "CBDC": 0, "Other": 0,
                "BANK_TRANSFER": 0, "CBDC_DIRECT": 0, "CASH": 0
            }
        
        # Ensure the payment method exists in tracking
        if payment_method not in model.transaction_volumes:
            model.transaction_volumes[payment_method] = 0
            model.transaction_counts[payment_method] = 0
        
        # Record transaction
        model.transaction_volumes[payment_method] += amount
        model.transaction_counts[payment_method] += 1
        
        # Map to legacy categories for compatibility
        legacy_mapping = {
            "BANK_TRANSFER": "Bank",
            "CBDC_DIRECT": "CBDC", 
            "CASH": "Other"
        }
        
        if payment_method in legacy_mapping:
            legacy_method = legacy_mapping[payment_method]
            model.transaction_volumes[legacy_method] += amount
            model.transaction_counts[legacy_method] += 1
        
        # Track monthly totals for step-by-step analysis  
        current_step = model.current_step
        if not hasattr(model, 'monthly_transactions'):
            model.monthly_transactions = {}
        
        if current_step not in model.monthly_transactions:
            model.monthly_transactions[current_step] = {
                "Bank": 0, "CBDC": 0, "Other": 0,
                "BANK_TRANSFER": 0, "CBDC_DIRECT": 0, "CASH": 0
            }
        
        # Ensure payment method exists in monthly tracking
        if payment_method not in model.monthly_transactions[current_step]:
            model.monthly_transactions[current_step][payment_method] = 0
        
        model.monthly_transactions[current_step][payment_method] += amount
        
        # Also update legacy category
        if payment_method in legacy_mapping:
            legacy_method = legacy_mapping[payment_method]
            if legacy_method not in model.monthly_transactions[current_step]:
                model.monthly_transactions[current_step][legacy_method] = 0
            model.monthly_transactions[current_step][legacy_method] += amount

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
