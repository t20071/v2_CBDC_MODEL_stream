from mesa import Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import networkx as nx
import numpy as np
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
    
    def __init__(self, n_consumers=200, n_commercial_banks=8, 
                 cbdc_introduction_step=30, cbdc_adoption_rate=0.03,
                 cbdc_attractiveness=1.5, initial_consumer_wealth=5000,
                 bank_interest_rate=0.02, cbdc_interest_rate=0.01):
        
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
        self.grid = NetworkGrid(self.G)
        
        # Create scheduler
        self.schedule = RandomActivation(self)
        
        # Create Central Bank (unique agent)
        central_bank = CentralBank(
            unique_id=0,
            model=self,
            cbdc_interest_rate=self.cbdc_interest_rate
        )
        self.schedule.add(central_bank)
        self.grid.place_agent(central_bank, 0)
        self.central_bank = central_bank
        
        # Create Commercial Banks
        self.commercial_banks = []
        for i in range(1, n_commercial_banks + 1):
            bank = CommercialBank(
                unique_id=i,
                model=self,
                interest_rate=self.bank_interest_rate,
                lending_rate=self.bank_interest_rate + 0.03,  # 3% markup
                initial_capital=initial_consumer_wealth * n_consumers * 0.1  # 10% of total consumer wealth
            )
            self.schedule.add(bank)
            self.grid.place_agent(bank, i)
            self.commercial_banks.append(bank)
        
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
            self.schedule.add(consumer)
            self.grid.place_agent(consumer, i)
            self.consumers.append(consumer)
            
            # Initially assign consumers to banks randomly
            chosen_bank = self.random.choice(self.commercial_banks)
            consumer.primary_bank = chosen_bank
            chosen_bank.add_customer(consumer)
        
        # Data collection
        self.datacollector = DataCollector(
            model_reporters={
                "CBDC_Adoption_Rate": self.compute_cbdc_adoption_rate,
                "Total_CBDC_Holdings": self.compute_total_cbdc_holdings,
                "Total_Bank_Deposits": self.compute_total_bank_deposits,
                "Total_Bank_Loans": self.compute_total_bank_loans,
                "CBDC_Adopters": self.compute_cbdc_adopters,
                "Average_Bank_Liquidity_Ratio": self.compute_average_bank_liquidity,
                "Step": lambda m: m.current_step
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
        
        # Introduce CBDC at specified step
        if self.current_step == self.cbdc_introduction_step:
            self.cbdc_introduced = True
            self.central_bank.introduce_cbdc()
            print(f"CBDC introduced at step {self.current_step}")
        
        # Update CBDC attractiveness over time (network effects)
        if self.cbdc_introduced:
            adoption_rate = self.compute_cbdc_adoption_rate()
            # Network effects: as more people adopt, it becomes more attractive
            network_effect = 1 + (adoption_rate * 0.5)
            self.central_bank.cbdc_attractiveness = self.cbdc_attractiveness * network_effect
        
        # Execute agent steps
        self.schedule.step()
        
        # Market dynamics: banks adjust interest rates based on deposit outflows
        self.adjust_market_conditions()
        
        # Collect data
        self.datacollector.collect(self)
    
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
