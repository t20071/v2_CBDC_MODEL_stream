from mesa import Agent
import numpy as np
import random

class Merchant(Agent):
    """
    Merchant agent representing real-world businesses that accept payments.
    
    Merchants provide goods/services to consumers and have preferences for
    different payment methods based on costs, convenience, and customer demand.
    """
    
    def __init__(self, unique_id, model, business_type="retail", size="small", 
                 initial_revenue=5000, payment_processing_bank=None):
        super().__init__(model)
        
        # Store agent properties
        self.unique_id = unique_id
        
        # Business characteristics
        self.business_type = business_type  # "retail", "restaurant", "online", "utility", "grocery"
        self.size = size  # "small", "medium", "large"
        self.initial_revenue = initial_revenue
        self.monthly_revenue = initial_revenue
        
        # Banking relationships
        self.primary_bank = payment_processing_bank
        self.business_deposits = initial_revenue * 0.2  # 20% of revenue as working capital
        
        # Payment balances for consumer transactions
        self.bank_account_balance = 0  # Traditional bank account for payments
        self.cbdc_wallet_balance = 0  # CBDC wallet for direct payments
        self.cash_balance = 0  # Cash payments
        
        # CBDC adoption status
        self.accepts_cbdc = False
        self.cbdc_adoption_date = None
        
        # Payment method preferences and costs
        self.setup_payment_preferences()
        
        # Transaction patterns based on business type
        self.setup_transaction_patterns()
        
        # Real-world business metrics
        self.customer_base = []  # List of regular customers
        self.daily_transactions = 0
        self.average_transaction_size = 0
        self.payment_method_volumes = {
            "cash": 0, "card": 0, "bank_transfer": 0, "cbdc": 0
        }
        
        # Economic realism factors
        self.economic_sensitivity = 0.5  # How much economic conditions affect business
        self.technology_adoption_rate = 0.3  # Willingness to adopt new payment methods
        self.customer_payment_influence = 0.4  # How much customer preferences matter
        
        # Network centrality for business ecosystem
        self.network_centrality = 0.1  # Start with minimal business network presence
        self.supplier_connections = 0
        self.customer_connections = 0
        
    def setup_payment_preferences(self):
        """Set up payment method preferences based on business characteristics."""
        
        # Base costs for different payment methods (as % of transaction)
        base_costs = {
            "cash": 0.005,          # Cash handling costs (0.5%)
            "card": 0.025,          # Credit card fees (2.5%)
            "bank_transfer": 0.015, # Bank transfer fees (1.5%)
            "cbdc": 0.002          # CBDC processing (0.2% - very low)
        }
        
        # Adjust costs based on business size
        if self.size == "large":
            # Large businesses get better rates
            self.payment_costs = {k: v * 0.7 for k, v in base_costs.items()}
            self.technology_adoption_rate = 0.8  # High tech adoption
        elif self.size == "medium":
            self.payment_costs = {k: v * 0.85 for k, v in base_costs.items()}
            self.technology_adoption_rate = 0.5  # Moderate tech adoption
        else:
            self.payment_costs = base_costs.copy()
            self.technology_adoption_rate = 0.2  # Slower tech adoption
        
        # Business type specific adjustments
        if self.business_type == "online":
            # Online businesses can't accept cash, prefer digital
            self.payment_costs["cash"] = float('inf')  # Cannot accept cash
            self.payment_costs["cbdc"] *= 0.5  # Even better CBDC rates for digital
            self.technology_adoption_rate = 0.9  # Very high tech adoption
            
        elif self.business_type == "grocery":
            # Grocery stores have high volume, low margins
            self.payment_costs = {k: v * 1.2 for k, v in self.payment_costs.items()}
            self.payment_costs["cash"] *= 0.7  # Still prefer cash for small transactions
            
        elif self.business_type == "restaurant":
            # Restaurants have tipping culture, mixed preferences
            self.payment_costs["cash"] *= 0.8  # Tips often in cash
            
        # Calculate payment method preference scores (lower cost = higher preference)
        max_cost = max([c for c in self.payment_costs.values() if c != float('inf')])
        self.payment_preferences = {}
        for method, cost in self.payment_costs.items():
            if cost == float('inf'):
                self.payment_preferences[method] = 0.0
            else:
                # Inverse relationship: lower cost = higher preference
                self.payment_preferences[method] = 1.0 - (cost / max_cost)
    
    def setup_transaction_patterns(self):
        """Set up realistic transaction patterns based on business type."""
        
        # Transaction patterns: (daily_count, avg_size, size_variance)
        patterns = {
            "retail": (50, 85, 40),       # Medium volume, medium size
            "restaurant": (80, 45, 25),   # High volume, lower size
            "online": (30, 120, 80),      # Lower volume, higher size
            "utility": (200, 150, 50),    # High volume, standardized
            "grocery": (120, 65, 30)      # Very high volume, consistent size
        }
        
        if self.business_type in patterns:
            self.daily_transaction_count, self.avg_transaction_size, self.transaction_variance = patterns[self.business_type]
        else:
            self.daily_transaction_count, self.avg_transaction_size, self.transaction_variance = patterns["retail"]
        
        # Adjust for business size
        size_multipliers = {"small": 0.5, "medium": 1.0, "large": 2.5}
        multiplier = size_multipliers.get(self.size, 1.0)
        
        self.daily_transaction_count = int(self.daily_transaction_count * multiplier)
        self.avg_transaction_size *= multiplier
    
    def step(self):
        """Execute one step of merchant operations."""
        # Consider CBDC adoption
        self.consider_cbdc_adoption()
        
        # Process daily transactions with consumers
        self.process_daily_transactions()
        
        # Update business metrics
        self.update_business_metrics()
        
        # Make banking decisions
        self.manage_business_banking()
        
        # Adapt payment preferences based on CBDC adoption
        self.adapt_payment_strategy()
        
        # Update network position in business ecosystem
        self.update_network_position()
    
    def consider_cbdc_adoption(self):
        """Consider adopting CBDC for customer payments."""
        # Only consider if CBDC is available and not already adopted
        if self.accepts_cbdc or not hasattr(self.model, 'cbdc_introduced'):
            return
        
        if not self.model.cbdc_introduced:
            return
        
        # Check consumer adoption rate to determine business pressure
        cbdc_adoption_rate = self.model.compute_cbdc_adoption_rate()
        
        # Base adoption probability based on technology adoption rate
        adoption_probability = self.technology_adoption_rate
        
        # Customer pressure increases adoption probability
        customer_pressure = cbdc_adoption_rate * self.customer_payment_influence
        adoption_probability += customer_pressure
        
        # Business type influences adoption speed
        business_type_multipliers = {
            "online": 1.8,     # Online businesses adopt faster
            "retail": 1.2,     # Retail moderate adoption
            "restaurant": 1.0,  # Restaurant moderate adoption
            "grocery": 1.1,    # Grocery moderate adoption
            "utility": 0.8     # Utilities slower adoption
        }
        
        multiplier = business_type_multipliers.get(self.business_type, 1.0)
        adoption_probability *= multiplier
        
        # Size matters - larger businesses adopt faster
        size_multipliers = {"small": 0.8, "medium": 1.0, "large": 1.5}
        size_multiplier = size_multipliers.get(self.size, 1.0)
        adoption_probability *= size_multiplier
        
        # Random adoption decision
        if np.random.random() < adoption_probability:
            self.adopt_cbdc()
    
    def adopt_cbdc(self):
        """Adopt CBDC payment acceptance."""
        self.accepts_cbdc = True
        self.cbdc_adoption_date = self.model.current_step
        
        # Initialize CBDC wallet if not already done
        if not hasattr(self, 'cbdc_wallet_balance'):
            self.cbdc_wallet_balance = 0
        
        # Adjust payment preferences to include CBDC
        self.payment_preferences["cbdc"] = 0.85  # High preference for CBDC due to lower costs
    
    def process_daily_transactions(self):
        """Process daily transactions with consumers."""
        # Generate realistic daily transaction volume
        daily_count = max(1, int(np.random.normal(self.daily_transaction_count, 
                                                self.daily_transaction_count * 0.2)))
        
        daily_revenue = 0
        payment_volumes = {"cash": 0, "card": 0, "bank_transfer": 0, "cbdc": 0}
        
        # Simulate each transaction
        for _ in range(daily_count):
            # Generate transaction size
            transaction_size = max(1, np.random.normal(self.avg_transaction_size, 
                                                     self.transaction_variance))
            
            # Determine payment method based on customer preferences and merchant acceptance
            payment_method = self.select_payment_method(transaction_size)
            
            # Process transaction
            processing_cost = transaction_size * self.payment_costs.get(payment_method, 0.02)
            net_revenue = transaction_size - processing_cost
            
            daily_revenue += net_revenue
            payment_volumes[payment_method] += transaction_size
        
        # Update merchant state
        self.daily_transactions = daily_count
        self.monthly_revenue = daily_revenue * 30  # Approximate monthly
        
        # Update payment method tracking
        for method, volume in payment_volumes.items():
            self.payment_method_volumes[method] += volume
        
        # Update model-level transaction tracking
        self.model.merchant_transactions = getattr(self.model, 'merchant_transactions', {})
        for method, volume in payment_volumes.items():
            if method not in self.model.merchant_transactions:
                self.model.merchant_transactions[method] = 0
            self.model.merchant_transactions[method] += volume
    
    def select_payment_method(self, transaction_size):
        """Select payment method based on merchant preferences and realistic factors."""
        
        # Base preferences from costs
        method_scores = self.payment_preferences.copy()
        
        # Adjust for transaction size (small transactions often cash, large ones cards/transfers)
        if transaction_size < 20:
            method_scores["cash"] *= 1.5  # Prefer cash for small amounts
            method_scores["card"] *= 0.7  # Cards less preferred due to fixed costs
        elif transaction_size > 200:
            method_scores["bank_transfer"] *= 1.3  # Prefer transfers for large amounts
            method_scores["cbdc"] *= 1.2  # CBDC good for large amounts
        
        # CBDC adoption influence
        if hasattr(self.model, 'cbdc_introduced') and self.model.cbdc_introduced:
            cbdc_adoption_rate = self.model.compute_cbdc_adoption_rate()
            
            # Higher CBDC adoption makes it more attractive to merchants
            cbdc_boost = 1 + (cbdc_adoption_rate * 2.0)  # Up to 3x boost
            method_scores["cbdc"] *= cbdc_boost
            
            # Network effects: if customers use CBDC, merchants must accept it
            customer_pressure = cbdc_adoption_rate * self.customer_payment_influence
            method_scores["cbdc"] += customer_pressure
        
        # Technology adoption limits for traditional merchants
        if not self.model.cbdc_introduced or random.random() > self.technology_adoption_rate:
            method_scores["cbdc"] *= 0.1  # Not yet adopted
        
        # Business type specific adjustments
        if self.business_type == "online":
            method_scores["cash"] = 0  # Cannot use cash online
        
        # Remove methods with zero scores
        valid_methods = {k: v for k, v in method_scores.items() if v > 0}
        
        if not valid_methods:
            return "card"  # Fallback
        
        # Weighted random selection
        methods = list(valid_methods.keys())
        weights = list(valid_methods.values())
        
        return random.choices(methods, weights=weights)[0]
    
    def update_business_metrics(self):
        """Update business performance metrics."""
        # Economic conditions impact
        if hasattr(self.model, 'economic_conditions'):
            economic_factor = self.model.economic_conditions
        else:
            economic_factor = 1.0  # Neutral conditions
        
        # CBDC impact on business efficiency
        cbdc_efficiency_gain = 0.0
        if hasattr(self.model, 'cbdc_introduced') and self.model.cbdc_introduced:
            cbdc_share = self.payment_method_volumes.get("cbdc", 0) / max(1, sum(self.payment_method_volumes.values()))
            cbdc_efficiency_gain = cbdc_share * 0.02  # Up to 2% efficiency gain
        
        # Update revenue with economic and efficiency factors
        base_revenue = self.initial_revenue
        self.monthly_revenue = base_revenue * economic_factor * (1 + cbdc_efficiency_gain)
        
        # Update business deposits (working capital management)
        target_deposits = self.monthly_revenue * 0.15  # 15% as working capital
        deposit_adjustment = (target_deposits - self.business_deposits) * 0.1  # Gradual adjustment
        self.business_deposits += deposit_adjustment
    
    def manage_business_banking(self):
        """Manage banking relationships and business financial decisions."""
        if self.primary_bank:
            # Deposit daily revenues
            self.primary_bank.business_deposits = getattr(self.primary_bank, 'business_deposits', 0)
            self.primary_bank.business_deposits += self.business_deposits * 0.1  # Daily deposit
            
            # Consider business loan needs
            if self.monthly_revenue > self.initial_revenue * 1.2:  # Growing business
                loan_need = (self.monthly_revenue - self.initial_revenue) * 0.5
                # Simplified business lending (banks should track this)
                if hasattr(self.primary_bank, 'business_loans'):
                    self.primary_bank.business_loans += loan_need * 0.01  # Small monthly additions
    
    def adapt_payment_strategy(self):
        """Adapt payment acceptance strategy based on market conditions."""
        if not hasattr(self.model, 'cbdc_introduced') or not self.model.cbdc_introduced:
            return
        
        # Monitor customer CBDC adoption
        cbdc_adoption_rate = self.model.compute_cbdc_adoption_rate()
        
        # Increase CBDC acceptance if customer adoption is high
        if cbdc_adoption_rate > 0.3 and random.random() < 0.05:  # 5% chance to improve
            self.technology_adoption_rate = min(0.95, self.technology_adoption_rate * 1.05)
            
            # Reduce CBDC processing costs through economies of scale
            if self.payment_costs["cbdc"] > 0.001:
                self.payment_costs["cbdc"] *= 0.98  # Gradual cost reduction
        
        # Update preferences based on new costs
        self.setup_payment_preferences()
    
    def update_network_position(self):
        """Update merchant's position in the business network."""
        # Network centrality based on transaction volume and connections
        daily_volume = sum(self.payment_method_volumes.values())
        volume_factor = min(1.0, daily_volume / 10000)  # Normalize to max transaction volume
        
        # Customer connections (simplified as transaction count)
        customer_factor = min(1.0, self.daily_transactions / 100)
        
        # Business size factor
        size_factors = {"small": 0.3, "medium": 0.6, "large": 1.0}
        size_factor = size_factors.get(self.size, 0.5)
        
        # Calculate network centrality
        self.network_centrality = (volume_factor * 0.4 + customer_factor * 0.4 + size_factor * 0.2)
        
        # Update connections
        self.customer_connections = self.daily_transactions
        self.supplier_connections = int(self.monthly_revenue / 5000)  # Rough estimate
    
    def get_payment_method_share(self, method):
        """Get the share of a specific payment method."""
        total_volume = sum(self.payment_method_volumes.values())
        if total_volume == 0:
            return 0.0
        return self.payment_method_volumes.get(method, 0) / total_volume
    
    def get_business_profile(self):
        """Get comprehensive business profile."""
        total_volume = sum(self.payment_method_volumes.values())
        
        return {
            "business_type": self.business_type,
            "size": self.size,
            "monthly_revenue": self.monthly_revenue,
            "daily_transactions": self.daily_transactions,
            "avg_transaction_size": self.avg_transaction_size,
            "total_payment_volume": total_volume,
            "cbdc_share": self.get_payment_method_share("cbdc"),
            "card_share": self.get_payment_method_share("card"),
            "cash_share": self.get_payment_method_share("cash"),
            "bank_transfer_share": self.get_payment_method_share("bank_transfer"),
            "technology_adoption_rate": self.technology_adoption_rate,
            "network_centrality": self.network_centrality,
            "customer_connections": self.customer_connections
        }
    
    def __str__(self):
        cbdc_share = self.get_payment_method_share("cbdc")
        return f"Merchant({self.business_type}, {self.size}): Revenue=${self.monthly_revenue:.0f}, CBDC={cbdc_share:.1%}, Transactions={self.daily_transactions}"