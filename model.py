from mesa import Model, Agent
from mesa.datacollection import DataCollector
import networkx as nx
import random
import numpy as np
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from agent.commercial_bank import CommercialBank
    from agent.central_bank import CentralBank
    from agent.consumer import Consumer
else:
    from agent.commercial_bank import CommercialBank
    from agent.central_bank import CentralBank
    from agent.consumer import Consumer

class CBDCBankingModel(Model):
    """
    Agent-based model simulating the impact of CBDC on commercial banking intermediation.
    
    The model includes three types of agents:
    1. Central Bank - Issues CBDC and sets monetary policy
    2. Commercial Banks - Accept deposits and provide loans
    3. Consumers - Make financial decisions between traditional banking and CBDC
    """
    
    # Type annotations for model attributes
    consumers: List['Consumer']
    commercial_banks: List['CommercialBank']
    central_bank: 'CentralBank'
    large_banks: List['CommercialBank']
    small_medium_banks: List['CommercialBank']
    all_agents: List[Agent]
    datacollector: DataCollector
    cbdc_introduced: bool
    current_step: int
    cbdc_introduction_step: int
    
    def __init__(self, n_consumers=200, n_commercial_banks=8, 
                 cbdc_introduction_step=12, cbdc_adoption_rate=0.20,
                 cbdc_attractiveness=2.2, initial_consumer_wealth=8400,
                 bank_interest_rate=0.048, cbdc_interest_rate=0.055):
        
        super().__init__()
        
        # Model parameters
        self.n_consumers = n_consumers
        self.n_commercial_banks = n_commercial_banks
        self.cbdc_introduction_step = cbdc_introduction_step
        self.cbdc_adoption_rate = cbdc_adoption_rate
        self.cbdc_attractiveness = cbdc_attractiveness
        self.initial_consumer_wealth = initial_consumer_wealth
        self.bank_interest_rate = bank_interest_rate
        self.cbdc_interest_rate = cbdc_interest_rate
        
        # Model state variables
        self.cbdc_introduced = False
        self.current_step = 0
        
        # Create network topology
        self.G = nx.erdos_renyi_graph(n_consumers + n_commercial_banks + 1, 0.1)
        
        # Create simple agent list for scheduling
        self.all_agents = []
        
        # Create Central Bank (unique agent)
        central_bank = CentralBank(
            unique_id=0,
            model=self,
            cbdc_interest_rate=self.cbdc_interest_rate
        )
        self.all_agents.append(central_bank)
        self.central_bank = central_bank
        
        # Create Commercial Banks with different sizes (H1, H2)
        self.commercial_banks = []
        self.large_banks = []
        self.small_medium_banks = []
        
        total_market_capital = initial_consumer_wealth * n_consumers * 0.8
        
        for i in range(1, n_commercial_banks + 1):
            # Create bank size distribution: 20% large banks, 80% small-medium banks
            if i <= max(1, int(n_commercial_banks * 0.2)):  # Large banks (top 20%)
                bank_type = "large"
                initial_capital = int(total_market_capital * 0.6 / max(1, int(n_commercial_banks * 0.2)))  # 60% of market
                network_centrality = 0.8  # High initial centrality
            else:  # Small-medium banks
                bank_type = "small_medium"
                remaining_banks = n_commercial_banks - max(1, int(n_commercial_banks * 0.2))
                initial_capital = int(total_market_capital * 0.4 / max(1, remaining_banks))  # 40% of market
                network_centrality = 0.3  # Lower initial centrality
            
            # 2025-calibrated lending spreads
            lending_spread = 0.047 if bank_type == "large" else 0.057  # 4.7% vs 5.7% spread
            
            bank = CommercialBank(
                unique_id=i,
                model=self,
                interest_rate=self.bank_interest_rate,
                lending_rate=self.bank_interest_rate + lending_spread,
                initial_capital=initial_capital,
                bank_type=bank_type,
                network_centrality=network_centrality
            )
            self.all_agents.append(bank)
            self.commercial_banks.append(bank)
            
            if bank_type == "large":
                self.large_banks.append(bank)
            else:
                self.small_medium_banks.append(bank)
        
        # Create Consumers
        self.consumers = []
        for i in range(n_commercial_banks + 1, n_commercial_banks + n_consumers + 1):
            consumer = Consumer(
                unique_id=i,
                model=self,
                initial_wealth=self.initial_consumer_wealth,
                cbdc_adoption_probability=self.cbdc_adoption_rate,
                risk_aversion=np.random.normal(0.5, 0.2)  # Risk aversion varies among consumers
            )
            self.all_agents.append(consumer)
            self.consumers.append(consumer)
            
            # Initially assign consumers to banks randomly
            chosen_bank = random.choice(self.commercial_banks)
            consumer.primary_bank = chosen_bank
            chosen_bank.add_customer(consumer)
        
        # Initialize interbank network connections (H4)
        self.initialize_banking_network()
        
        # Initialize 2025-calibrated balance sheets for all banks
        self.initialize_bank_balance_sheets()
        
        # Transaction tracking for payment method analysis
        self.transaction_volumes = {"Bank": 0, "CBDC": 0, "Other": 0}
        self.transaction_counts = {"Bank": 0, "CBDC": 0, "Other": 0}
        self.monthly_transactions = {}
        self.step_transactions = {"Bank": 0, "CBDC": 0, "Other": 0}
        
        # Data collection
        self.datacollector = DataCollector(
            model_reporters={
                "CBDC_Adoption_Rate": self.compute_cbdc_adoption_rate,
                "Total_CBDC_Holdings": self.compute_total_cbdc_holdings,
                "Total_Bank_Deposits": self.compute_total_bank_deposits,
                "Total_Bank_Loans": self.compute_total_bank_loans,
                "CBDC_Adopters": self.compute_cbdc_adopters,
                "Average_Bank_Liquidity_Ratio": self.compute_average_bank_liquidity,
                "Step": lambda m: m.current_step,
                # H1: Network centrality metrics
                "Average_Bank_Centrality": self.compute_average_bank_centrality,
                "Small_Bank_Centrality": self.compute_small_bank_centrality,
                "Large_Bank_Centrality": self.compute_large_bank_centrality,
                # H3: Systemic risk metrics
                "Average_Liquidity_Stress": self.compute_average_liquidity_stress,
                # H4: Network connectivity
                "Banking_Network_Density": self.compute_network_density,
                # H6: Central bank centrality
                "Central_Bank_Centrality": self.compute_central_bank_centrality,
                # Transaction volume metrics
                "Bank_Transaction_Volume": lambda m: m.monthly_transactions.get(m.current_step, {}).get("Bank", 0),
                "CBDC_Transaction_Volume": lambda m: m.monthly_transactions.get(m.current_step, {}).get("CBDC", 0),
                "Other_Transaction_Volume": lambda m: m.monthly_transactions.get(m.current_step, {}).get("Other", 0),
                "Total_Transaction_Volume": self.compute_total_transaction_volume,
                "CBDC_Transaction_Share": self.compute_cbdc_transaction_share
            },
            agent_reporters={
                "AgentID": lambda a: f"{type(a).__name__}_{a.unique_id}",
                "Wealth": lambda a: getattr(a, 'wealth', 0),
                "CBDC_Holdings": lambda a: getattr(a, 'cbdc_holdings', 0),
                "Bank_Deposits": lambda a: getattr(a, 'bank_deposits', 0),
                "CBDC_Adopter": lambda a: getattr(a, 'cbdc_adopter', False),
                "Liquidity_Ratio": lambda a: getattr(a, 'liquidity_ratio', 0),
                "Total_Deposits": lambda a: getattr(a, 'total_deposits', 0),
                "Total_Loans": lambda a: getattr(a, 'total_loans', 0)
            }
        )
        
        # Collect initial data
        self.datacollector.collect(self)
    
    def step(self):
        """Advance the model by one step."""
        self.current_step += 1
        
        # Introduce CBDC at specified month
        if self.current_step == self.cbdc_introduction_step:
            self.cbdc_introduced = True
            self.central_bank.introduce_cbdc()
            print(f"CBDC introduced at month {self.current_step}")
        
        # Monthly CBDC network effects growth (research-based)
        if self.cbdc_introduced:
            adoption_rate = self.compute_cbdc_adoption_rate()
            months_since_intro = self.current_step - self.cbdc_introduction_step
            # Monthly network effects compound (Keister & Sanches, 2023)
            monthly_network_growth = 1 + (adoption_rate * 0.08)  # 8% monthly compound
            time_decay = max(0.5, 1 - (months_since_intro * 0.02))  # Diminishing returns
            self.central_bank.cbdc_attractiveness = self.cbdc_attractiveness * monthly_network_growth * time_decay
        
        # Clear step-specific transactions before agents act
        self.step_transactions = {"Bank": 0, "CBDC": 0, "Other": 0}
        
        # Execute agent steps
        for agent in self.all_agents:
            agent.step()
        
        # Record monthly transactions
        self.monthly_transactions[self.current_step] = self.step_transactions.copy()
        
        # Market dynamics: banks adjust interest rates based on deposit outflows
        self.adjust_market_conditions()
        
        # Collect data
        self.datacollector.collect(self)
    
    def record_transaction(self, amount, payment_method):
        """Record a transaction with its payment method for analysis."""
        if payment_method in self.step_transactions:
            self.step_transactions[payment_method] += amount
        
        # Also update running totals
        if payment_method in self.transaction_volumes:
            self.transaction_volumes[payment_method] += amount
            self.transaction_counts[payment_method] += 1
    
    def adjust_market_conditions(self):
        """Adjust market conditions based on current state."""
        if self.cbdc_introduced:
            # Banks may increase interest rates to compete with CBDC
            cbdc_adoption = self.compute_cbdc_adoption_rate()
            
            for bank in self.commercial_banks:
                # Adjust interest rates based on competitive pressure
                competitive_pressure = cbdc_adoption * 0.1  # Up to 1% increase
                bank.interest_rate = min(
                    self.bank_interest_rate + competitive_pressure,
                    self.bank_interest_rate * 1.5  # Cap at 50% increase
                )
                
                # Adjust lending rates accordingly
                bank.lending_rate = bank.interest_rate + 0.03  # Maintain 3% spread
    
    # Data collection methods
    def compute_cbdc_adoption_rate(self):
        """Compute the proportion of consumers who have adopted CBDC."""
        if not self.cbdc_introduced:
            return 0.0
        
        adopters = sum(1 for consumer in self.consumers if consumer.cbdc_adopter)
        return adopters / len(self.consumers) if self.consumers else 0.0
    
    def compute_total_cbdc_holdings(self):
        """Compute total CBDC holdings across all consumers."""
        return sum(consumer.cbdc_holdings for consumer in self.consumers)
    
    def compute_total_bank_deposits(self):
        """Compute total deposits across all commercial banks."""
        return sum(bank.total_deposits for bank in self.commercial_banks)
    
    def compute_total_bank_loans(self):
        """Compute total loans across all commercial banks."""
        return sum(bank.total_loans for bank in self.commercial_banks)
    
    def compute_cbdc_adopters(self):
        """Count the number of CBDC adopters."""
        return sum(1 for consumer in self.consumers if consumer.cbdc_adopter)
    
    def compute_average_bank_liquidity(self):
        """Compute average liquidity ratio across commercial banks."""
        if not self.commercial_banks:
            return 0.0
        
        total_liquidity = sum(bank.liquidity_ratio for bank in self.commercial_banks)
        return total_liquidity / len(self.commercial_banks)
    
    # H1: Network centrality computation methods
    def compute_average_bank_centrality(self):
        """Compute average network centrality across all commercial banks."""
        if not self.commercial_banks:
            return 0.0
        return sum(bank.network_centrality for bank in self.commercial_banks) / len(self.commercial_banks)
    
    def compute_small_bank_centrality(self):
        """Compute average centrality for small and medium banks (H1)."""
        small_banks = [bank for bank in self.commercial_banks if bank.bank_type == "small_medium"]
        if not small_banks:
            return 0.0
        return sum(bank.network_centrality for bank in small_banks) / len(small_banks)
    
    def compute_large_bank_centrality(self):
        """Compute average centrality for large banks (H1)."""
        large_banks = [bank for bank in self.commercial_banks if bank.bank_type == "large"]
        if not large_banks:
            return 0.0
        return sum(bank.network_centrality for bank in large_banks) / len(large_banks)
    
    # H3: Systemic risk computation
    def compute_average_liquidity_stress(self):
        """Compute average liquidity stress across banks (H3)."""
        if not self.commercial_banks:
            return 0.0
        return sum(bank.liquidity_stress_level for bank in self.commercial_banks) / len(self.commercial_banks)
    
    # H4: Network connectivity computation
    def compute_network_density(self):
        """Compute banking network density (H4)."""
        if len(self.commercial_banks) <= 1:
            return 0.0
        
        # Calculate actual connections vs possible connections
        total_connections = sum(bank.interbank_connections for bank in self.commercial_banks)
        max_possible_connections = len(self.commercial_banks) * (len(self.commercial_banks) - 1)
        
        if max_possible_connections == 0:
            return 0.0
        return total_connections / max_possible_connections
    

    
    def initialize_bank_balance_sheets(self):
        """Initialize 2025-calibrated balance sheets as starting conditions."""
        for bank in self.commercial_banks:
            # Calculate actual deposits: consumers deposit 37% of their wealth
            initial_customer_deposits = 0
            for consumer in self.consumers:
                if consumer.primary_bank == bank:
                    # Consumer deposits 37% of their 8,400 wealth = 3,108 per consumer
                    consumer_deposit = consumer.initial_wealth * 0.37
                    initial_customer_deposits += consumer_deposit
                    # Update consumer's portfolio allocation
                    consumer.bank_deposits = consumer_deposit
                    consumer.other_assets = consumer.initial_wealth - consumer_deposit
            
            # Set bank's total deposits to match actual consumer deposits
            bank.total_deposits = initial_customer_deposits
            
            if bank.bank_type == "large":
                # Large bank 2025 balance sheet structure
                bank.demand_deposits = bank.total_deposits * 0.60  # 60% demand
                bank.time_deposits = bank.total_deposits * 0.40    # 40% time
                
                # Set loan portfolio to target ratio
                bank.total_loans = bank.total_deposits * 0.733  # 73.3% LTD ratio
                bank.consumer_loans = bank.total_loans * 0.36   # 36% consumer
                bank.commercial_loans = bank.total_loans * 0.45 # 45% commercial  
                bank.real_estate_loans = bank.total_loans * 0.19 # 19% real estate
                
                # Adjust cash reserves to balance
                target_assets = bank.total_deposits / 0.75  # Deposits are 75% of assets
                bank.cash_reserves = target_assets * 0.15   # 15% cash & reserves
                bank.securities = target_assets * 0.25      # 25% securities
                
                # Set borrowings and other funding
                bank.borrowings = target_assets * 0.10      # 10% borrowings
                bank.other_liabilities = target_assets * 0.03 # 3% other liabilities
                
            else:
                # Small bank 2025 balance sheet structure  
                bank.demand_deposits = bank.total_deposits * 0.61  # 61% demand
                bank.time_deposits = bank.total_deposits * 0.39    # 39% time
                
                # Set loan portfolio to target ratio
                bank.total_loans = bank.total_deposits * 0.756  # 75.6% LTD ratio
                bank.consumer_loans = bank.total_loans * 0.24   # 24% consumer
                bank.commercial_loans = bank.total_loans * 0.56 # 56% commercial
                bank.real_estate_loans = bank.total_loans * 0.20 # 20% real estate
                
                # Adjust cash reserves to balance
                target_assets = bank.total_deposits / 0.82  # Deposits are 82% of assets
                bank.cash_reserves = target_assets * 0.12   # 12% cash & reserves
                bank.securities = target_assets * 0.20      # 20% securities
                
                # Set borrowings and other funding
                bank.borrowings = target_assets * 0.06      # 6% borrowings
                bank.other_liabilities = target_assets * 0.02 # 2% other liabilities
            
            # Calculate initial performance metrics
            bank.calculate_metrics()
            
            # Ensure minimum regulatory compliance - calculate LCR manually since method doesn't exist yet
            hqla = bank.cash_reserves + (bank.securities * 0.85)  # High-Quality Liquid Assets
            deposit_outflow_rate = 0.05 if bank.bank_type == "large" else 0.03
            net_cash_outflows = bank.total_deposits * deposit_outflow_rate
            
            if net_cash_outflows > 0:
                lcr = hqla / net_cash_outflows
                target_lcr = 1.25 if bank.bank_type == "large" else 1.10
                
                if lcr < target_lcr:
                    # Increase cash reserves to meet LCR
                    additional_cash = bank.total_deposits * 0.05  # Add 5% buffer
                    bank.cash_reserves += additional_cash
                    bank.total_loans -= additional_cash  # Reduce loans to balance
                    bank.calculate_metrics()  # Recalculate
    
    def compute_total_transaction_volume(self):
        """Compute total transaction volume for current step."""
        current_transactions = self.monthly_transactions.get(self.current_step, {})
        return sum(current_transactions.values())
    
    def compute_cbdc_transaction_share(self):
        """Compute CBDC's share of total transaction volume."""
        current_transactions = self.monthly_transactions.get(self.current_step, {})
        total_volume = sum(current_transactions.values())
        cbdc_volume = current_transactions.get("CBDC", 0)
        
        return (cbdc_volume / total_volume * 100) if total_volume > 0 else 0
    
    def get_transaction_analysis(self):
        """Get comprehensive transaction analysis before and after CBDC."""
        if not self.monthly_transactions:
            return {}
        
        # Pre-CBDC analysis (steps before introduction)
        pre_cbdc_steps = [step for step in self.monthly_transactions.keys() if step < self.cbdc_introduction_step]
        post_cbdc_steps = [step for step in self.monthly_transactions.keys() if step >= self.cbdc_introduction_step]
        
        def analyze_period(steps):
            if not steps:
                return {"bank_volume": 0, "cbdc_volume": 0, "other_volume": 0, "total_volume": 0}
            
            bank_total = sum(self.monthly_transactions[step].get("Bank", 0) for step in steps)
            cbdc_total = sum(self.monthly_transactions[step].get("CBDC", 0) for step in steps)
            other_total = sum(self.monthly_transactions[step].get("Other", 0) for step in steps)
            
            return {
                "bank_volume": bank_total,
                "cbdc_volume": cbdc_total,
                "other_volume": other_total,
                "total_volume": bank_total + cbdc_total + other_total
            }
        
        pre_cbdc = analyze_period(pre_cbdc_steps)
        post_cbdc = analyze_period(post_cbdc_steps)
        
        # Calculate substitution metrics
        substitution_analysis = {}
        if pre_cbdc["total_volume"] > 0 and post_cbdc["total_volume"] > 0:
            pre_bank_share = pre_cbdc["bank_volume"] / pre_cbdc["total_volume"] * 100
            post_bank_share = post_cbdc["bank_volume"] / post_cbdc["total_volume"] * 100
            post_cbdc_share = post_cbdc["cbdc_volume"] / post_cbdc["total_volume"] * 100
            
            substitution_analysis = {
                "pre_cbdc_bank_share": pre_bank_share,
                "post_cbdc_bank_share": post_bank_share,
                "post_cbdc_cbdc_share": post_cbdc_share,
                "transaction_substitution_rate": pre_bank_share - post_bank_share
            }
        
        return {
            "pre_cbdc_period": pre_cbdc,
            "post_cbdc_period": post_cbdc,
            "substitution_analysis": substitution_analysis,
            "cbdc_introduction_step": self.cbdc_introduction_step
        }

    # H6: Central bank centrality computation
    def compute_central_bank_centrality(self):
        """Compute central bank's network centrality (H6)."""
        if not self.cbdc_introduced:
            return 0.1  # Minimal centrality before CBDC
        
        # Central bank centrality increases with CBDC adoption and usage
        cbdc_adoption = self.compute_cbdc_adoption_rate()
        total_cbdc_holdings = self.compute_total_cbdc_holdings()
        total_bank_deposits = self.compute_total_bank_deposits()
        
        # Market share component
        total_financial_assets = total_cbdc_holdings + total_bank_deposits
        cbdc_market_share = total_cbdc_holdings / total_financial_assets if total_financial_assets > 0 else 0
        
        # Network dominance grows with both adoption rate and market share
        base_centrality = 0.1
        adoption_boost = cbdc_adoption * 0.6  # Up to 60% from adoption
        market_boost = cbdc_market_share * 0.4  # Up to 40% from market share
        
        # Additional boost from being the sole CBDC issuer
        monopoly_boost = min(0.2, cbdc_adoption * 0.3) if cbdc_adoption > 0.3 else 0
        
        final_centrality = base_centrality + adoption_boost + market_boost + monopoly_boost
        return min(1.0, final_centrality)
    
    def initialize_banking_network(self):
        """Initialize interbank network connections for H4 analysis."""
        n_banks = len(self.commercial_banks)
        if n_banks <= 1:
            return
        
        # Create initial network connections based on bank size and proximity
        for i, bank in enumerate(self.commercial_banks):
            # Large banks have more connections
            if bank.bank_type == "large":
                target_connections = min(n_banks - 1, int(n_banks * 0.6))  # Connect to 60% of banks
            else:
                target_connections = min(n_banks - 1, int(n_banks * 0.3))  # Connect to 30% of banks
            
            bank.interbank_connections = target_connections
    
    def get_simulation_summary(self):
        """Get a summary of the simulation results."""
        data = self.datacollector.get_model_vars_dataframe()
        
        summary = {
            'final_cbdc_adoption_rate': data['CBDC_Adoption_Rate'].iloc[-1],
            'final_cbdc_holdings': data['Total_CBDC_Holdings'].iloc[-1],
            'initial_bank_deposits': data['Total_Bank_Deposits'].iloc[0],
            'final_bank_deposits': data['Total_Bank_Deposits'].iloc[-1],
            'deposit_reduction_rate': (data['Total_Bank_Deposits'].iloc[0] - data['Total_Bank_Deposits'].iloc[-1]) / data['Total_Bank_Deposits'].iloc[0],
            'final_bank_loans': data['Total_Bank_Loans'].iloc[-1],
            'average_final_liquidity': data['Average_Bank_Liquidity_Ratio'].iloc[-1]
        }
        
        return summary
