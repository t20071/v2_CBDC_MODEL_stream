"""
Risk Manager Agent - Comprehensive Risk Assessment and Management for CBDC Banking Simulation

This agent implements real-world risk scenarios including:
- Cybersecurity threats and digital bank runs
- Basel III regulatory compliance monitoring
- Liquidity stress testing scenarios
- Operational risk modeling
- Systemic risk assessment

References:
- IMF (2024). "Central Bank Digital Currency and Financial Stability"
- BIS (2024). "Information Security and Operational Risks to Central Banks"
- Federal Reserve (2024). "Financial Stability Implications of CBDC"
- ECB (2024). "Tiered CBDC and the Financial System"
- Basel Committee (2024). "Basel III Endgame Implementation Guidelines"
"""

import numpy as np
from mesa import Agent
from typing import TYPE_CHECKING, Dict, List, Tuple, Optional
import random

if TYPE_CHECKING:
    from model import CBDCBankingModel

class RiskManager(Agent):
    """
    Risk Manager agent that monitors and manages systemic risks in the CBDC banking system.
    
    This agent represents the regulatory and supervisory framework that oversees
    financial stability during CBDC implementation. It monitors cybersecurity threats,
    conducts stress testing, and ensures Basel III compliance.
    
    Based on research from:
    - IMF FinTech Notes (2024): "Implications of Central Bank Digital Currency for Monetary Operations"
    - BIS Papers (2024): "CBDC Information Security and Operational Risks"
    - Federal Reserve (2024): "Financial Stability Implications of CBDC"
    """
    
    def __init__(self, unique_id: int, model: 'CBDCBankingModel'):
        super().__init__(unique_id,model)
        self.unique_id = unique_id
        self.model = model
        
        # Cybersecurity Risk Parameters (based on 2024 threat landscape)
        self.cyber_threat_level = 0.15  # 15% baseline cyber risk (IMF 2024)
        self.ransomware_probability = 0.002  # 0.2% per step (520% increase per BIS 2024)
        self.phishing_success_rate = 0.08  # 8% success rate (industry average)
        self.ddos_frequency = 0.001  # 0.1% per step (finance sector target)
        
        # Basel III Compliance Parameters
        self.capital_adequacy_threshold = 0.08  # 8% minimum capital ratio
        self.liquidity_coverage_ratio = 1.0  # 100% LCR requirement
        self.net_stable_funding_ratio = 1.0  # 100% NSFR requirement
        self.leverage_ratio_minimum = 0.03  # 3% minimum leverage ratio
        
        # Stress Testing Scenarios (ECB 2024)
        self.stress_scenarios = {
            'mild': {'deposit_outflow': 0.1, 'cbdc_surge': 0.15, 'cyber_impact': 0.05},
            'moderate': {'deposit_outflow': 0.25, 'cbdc_surge': 0.35, 'cyber_impact': 0.15},
            'severe': {'deposit_outflow': 0.5, 'cbdc_surge': 0.7, 'cyber_impact': 0.3}
        }
        
        # Operational Risk Indicators
        self.operational_risk_score = 0.0
        self.cyber_incidents_count = 0
        self.system_downtime_hours = 0
        self.data_breaches_count = 0
        
        # Regulatory Monitoring
        self.compliance_violations = []
        self.enforcement_actions = []
        self.systemic_risk_alerts = []
        
        # Digital Bank Run Detection
        self.deposit_velocity_threshold = 0.2  # 20% daily outflow triggers alert
        self.cbdc_adoption_velocity = 0.0
        self.digital_run_probability = 0.0
        
        # Market Confidence Metrics
        self.market_confidence = 1.0  # 100% baseline confidence
        self.regulatory_credibility = 1.0  # 100% baseline credibility
        
    def step(self):
        """Execute one step of risk management operations."""
        # Core risk assessment cycle
        self.assess_cybersecurity_risks()
        self.monitor_basel_compliance()
        self.conduct_stress_testing()
        self.detect_digital_bank_runs()
        self.assess_operational_risks()
        self.update_systemic_risk_indicators()
        self.implement_regulatory_actions()
        
    def assess_cybersecurity_risks(self):
        """
        Assess cybersecurity threats based on 2024 threat landscape.
        
        Reference: IMF Blog (2024) "Rising Cyber Threats Pose Serious Concerns for Financial Stability"
        - 520% increase in phishing/ransomware attacks
        - $2.5 billion in extreme cyber losses (quadrupled since 2017)
        - 80% increase in multi-vector DDoS attacks
        """
        model = self.model
        
        # Ransomware threat assessment
        if np.random.random() < self.ransomware_probability:
            self.cyber_incidents_count += 1
            affected_banks = np.random.choice(
                model.commercial_banks, 
                size=max(1, int(len(model.commercial_banks) * 0.2)), 
                replace=False
            )
            
            for bank in affected_banks:
                # Ransomware impact: 5-15% operational capacity loss
                capacity_loss = np.random.uniform(0.05, 0.15)
                bank.operational_capacity *= (1 - capacity_loss)
                bank.cyber_incident_flag = True
                
                # Financial impact: 2-8% of deposits
                financial_impact = bank.total_deposits * np.random.uniform(0.02, 0.08)
                bank.cyber_losses += financial_impact
                
            self.systemic_risk_alerts.append({
                'type': 'ransomware_attack',
                'step': model.current_step,
                'affected_banks': len(affected_banks),
                'severity': 'high'
            })
        
        # Phishing campaign assessment
        if np.random.random() < 0.005:  # 0.5% chance per step
            # Consumer credential theft
            affected_consumers = np.random.choice(
                model.consumers,
                size=max(1, int(len(model.consumers) * self.phishing_success_rate)),
                replace=False
            )
            
            for consumer in affected_consumers:
                # Account compromise: 10-30% wealth loss
                wealth_loss = consumer.wealth * np.random.uniform(0.1, 0.3)
                consumer.wealth -= wealth_loss
                consumer.cyber_victim_flag = True
                
        # DDoS attack assessment
        if np.random.random() < self.ddos_frequency:
            # System-wide impact on CBDC infrastructure
            self.system_downtime_hours += np.random.uniform(2, 8)
            model.cbdc_operational_capacity *= 0.8  # 20% capacity reduction
            
            self.systemic_risk_alerts.append({
                'type': 'ddos_attack',
                'step': model.current_step,
                'downtime_hours': self.system_downtime_hours,
                'severity': 'moderate'
            })
        
        # Update overall cyber threat level
        recent_incidents = sum(1 for alert in self.systemic_risk_alerts[-10:] 
                             if alert['type'] in ['ransomware_attack', 'ddos_attack'])
        self.cyber_threat_level = min(0.5, 0.15 + (recent_incidents * 0.05))
        
    def monitor_basel_compliance(self):
        """
        Monitor Basel III compliance across commercial banks.
        
        Reference: Basel Committee (2024) "Basel III Endgame Implementation Guidelines"
        - Common Equity Tier 1: 4.5% minimum
        - Total Capital Ratio: 8% minimum
        - Liquidity Coverage Ratio: 100% minimum
        - Net Stable Funding Ratio: 100% minimum
        """
        model = self.model
        violations = []
        
        for bank in model.commercial_banks:
            # Calculate risk-weighted assets (simplified)
            risk_weighted_assets = (
                bank.consumer_loans * 0.75 +  # 75% risk weight for consumer loans
                bank.commercial_loans * 1.0 +  # 100% risk weight for commercial loans
                bank.real_estate_loans * 0.35 +  # 35% risk weight for real estate
                bank.securities * 0.2 +  # 20% risk weight for securities
                bank.cash_reserves * 0.0  # 0% risk weight for cash
            )
            
            # Capital adequacy assessment
            tier_1_capital = bank.tier_1_capital if hasattr(bank, 'tier_1_capital') else bank.total_deposits * 0.12
            total_capital = tier_1_capital * 1.25  # Assume Tier 2 is 25% of Tier 1
            
            capital_ratio = total_capital / max(risk_weighted_assets, 1)
            if capital_ratio < self.capital_adequacy_threshold:
                violations.append({
                    'bank_id': bank.unique_id,
                    'violation_type': 'capital_adequacy',
                    'required': self.capital_adequacy_threshold,
                    'actual': capital_ratio,
                    'severity': 'high' if capital_ratio < 0.06 else 'moderate'
                })
            
            # Liquidity Coverage Ratio assessment
            liquid_assets = bank.cash_reserves + bank.securities * 0.85  # 85% haircut on securities
            net_cash_outflows = bank.total_deposits * 0.03  # 3% daily outflow assumption
            lcr = liquid_assets / max(net_cash_outflows, 1)
            
            if lcr < self.liquidity_coverage_ratio:
                violations.append({
                    'bank_id': bank.unique_id,
                    'violation_type': 'liquidity_coverage',
                    'required': self.liquidity_coverage_ratio,
                    'actual': lcr,
                    'severity': 'high' if lcr < 0.8 else 'moderate'
                })
            
            # Net Stable Funding Ratio assessment
            stable_funding = bank.total_deposits * 0.9 + bank.borrowings * 0.5
            required_funding = (
                bank.consumer_loans * 0.65 +
                bank.commercial_loans * 0.85 +
                bank.real_estate_loans * 0.65 +
                bank.securities * 0.15
            )
            nsfr = stable_funding / max(required_funding, 1)
            
            if nsfr < self.net_stable_funding_ratio:
                violations.append({
                    'bank_id': bank.unique_id,
                    'violation_type': 'stable_funding',
                    'required': self.net_stable_funding_ratio,
                    'actual': nsfr,
                    'severity': 'moderate'
                })
        
        self.compliance_violations.extend(violations)
        
        # Update regulatory credibility based on enforcement effectiveness
        if violations:
            self.regulatory_credibility *= 0.99  # Small credibility loss
        else:
            self.regulatory_credibility = min(1.0, self.regulatory_credibility * 1.001)
            
    def conduct_stress_testing(self):
        """
        Conduct comprehensive stress testing scenarios.
        
        Reference: ECB Working Paper (2024) "Tiered CBDC and the Financial System"
        - Mild stress: 10% deposit outflow, 15% CBDC surge
        - Moderate stress: 25% deposit outflow, 35% CBDC surge
        - Severe stress: 50% deposit outflow, 70% CBDC surge
        """
        model = self.model
        
        # Determine stress scenario based on current conditions
        cbdc_adoption_rate = model.compute_cbdc_adoption_rate()
        economic_stress = 1 - model.economic_conditions
        
        if economic_stress > 0.1 or cbdc_adoption_rate > 0.5:
            scenario = 'severe'
        elif economic_stress > 0.05 or cbdc_adoption_rate > 0.3:
            scenario = 'moderate'
        else:
            scenario = 'mild'
        
        stress_params = self.stress_scenarios[scenario]
        
        # Simulate deposit outflow stress
        for bank in model.commercial_banks:
            stressed_deposits = bank.total_deposits * (1 - stress_params['deposit_outflow'])
            liquidity_gap = bank.total_deposits - stressed_deposits
            
            # Check if bank can meet liquidity requirements
            available_liquidity = bank.cash_reserves + bank.securities * 0.8
            if liquidity_gap > available_liquidity:
                bank.liquidity_stress_flag = True
                bank.stressed_liquidity_ratio = available_liquidity / liquidity_gap
                
                self.systemic_risk_alerts.append({
                    'type': 'liquidity_stress',
                    'step': model.current_step,
                    'bank_id': bank.unique_id,
                    'scenario': scenario,
                    'severity': 'high' if bank.stressed_liquidity_ratio < 0.5 else 'moderate'
                })
        
        # CBDC surge stress test
        potential_cbdc_demand = model.compute_total_consumer_wealth() * stress_params['cbdc_surge']
        current_cbdc_capacity = model.central_bank.cbdc_outstanding + model.central_bank.cbdc_reserves
        
        if potential_cbdc_demand > current_cbdc_capacity * 1.2:
            model.cbdc_capacity_stress = True
            self.systemic_risk_alerts.append({
                'type': 'cbdc_capacity_stress',
                'step': model.current_step,
                'demand': potential_cbdc_demand,
                'capacity': current_cbdc_capacity,
                'severity': 'high'
            })
            
    def detect_digital_bank_runs(self):
        """
        Detect potential digital bank runs using velocity indicators.
        
        Reference: Federal Reserve (2024) "Financial Stability Implications of CBDC"
        - Digital bank runs can occur 2-3x faster than traditional runs
        - 20% daily deposit outflow triggers systemic alert
        - CBDC adoption velocity is key early warning indicator
        """
        model = self.model
        
        # Calculate deposit velocity (rate of change)
        if hasattr(model, 'previous_total_deposits'):
            current_deposits = model.compute_total_bank_deposits()
            previous_deposits = model.previous_total_deposits
            
            if previous_deposits > 0:
                deposit_velocity = (previous_deposits - current_deposits) / previous_deposits
                
                if deposit_velocity > self.deposit_velocity_threshold:
                    # Digital bank run detected
                    self.digital_run_probability = min(1.0, deposit_velocity * 2)
                    
                    # Identify most affected banks
                    affected_banks = []
                    for bank in model.commercial_banks:
                        if hasattr(bank, 'previous_deposits'):
                            bank_velocity = (bank.previous_deposits - bank.total_deposits) / max(bank.previous_deposits, 1)
                            if bank_velocity > 0.15:  # 15% individual bank threshold
                                affected_banks.append(bank)
                                bank.digital_run_flag = True
                    
                    self.systemic_risk_alerts.append({
                        'type': 'digital_bank_run',
                        'step': model.current_step,
                        'deposit_velocity': deposit_velocity,
                        'affected_banks': len(affected_banks),
                        'severity': 'critical' if deposit_velocity > 0.4 else 'high'
                    })
                    
                    # Market confidence impact
                    confidence_impact = min(0.2, deposit_velocity * 0.5)
                    self.market_confidence *= (1 - confidence_impact)
        
        # Store current deposits for next step
        model.previous_total_deposits = model.compute_total_bank_deposits()
        for bank in model.commercial_banks:
            bank.previous_deposits = bank.total_deposits
            
    def assess_operational_risks(self):
        """
        Assess operational risks based on BIS framework.
        
        Reference: BIS (2024) "CBDC Information Security and Operational Risks to Central Banks"
        - Technology risks: DLT vulnerabilities, system failures
        - Governance risks: Coordinated security practices
        - Third-party risks: Service provider dependencies
        """
        model = self.model
        
        # Technology risk assessment
        tech_risk = 0.0
        if hasattr(model, 'cbdc_operational_capacity'):
            tech_risk += (1 - model.cbdc_operational_capacity) * 0.3
        
        # Governance risk assessment
        governance_risk = 0.0
        if len(self.compliance_violations) > 0:
            governance_risk += min(0.2, len(self.compliance_violations) * 0.02)
        
        # Third-party risk assessment
        third_party_risk = 0.0
        for merchant in model.merchants:
            if hasattr(merchant, 'payment_processor_reliability'):
                third_party_risk += (1 - merchant.payment_processor_reliability) * 0.01
        
        # Cyber risk component
        cyber_risk = self.cyber_threat_level * 0.4
        
        # Calculate overall operational risk score
        self.operational_risk_score = min(1.0, tech_risk + governance_risk + third_party_risk + cyber_risk)
        
        # Update economic conditions based on operational risk
        if self.operational_risk_score > 0.3:
            model.economic_conditions *= (1 - self.operational_risk_score * 0.1)
            
    def update_systemic_risk_indicators(self):
        """Update comprehensive systemic risk indicators."""
        model = self.model
        
        # Calculate systemic risk components
        bank_concentration_risk = self.calculate_bank_concentration_risk()
        cbdc_adoption_risk = self.calculate_cbdc_adoption_risk()
        liquidity_system_risk = self.calculate_liquidity_system_risk()
        
        # Aggregate systemic risk score
        systemic_risk_score = (
            bank_concentration_risk * 0.3 +
            cbdc_adoption_risk * 0.3 +
            liquidity_system_risk * 0.2 +
            self.operational_risk_score * 0.2
        )
        
        model.systemic_risk_score = systemic_risk_score
        
        # Update market confidence based on systemic risk
        if systemic_risk_score > 0.5:
            self.market_confidence *= 0.98
        elif systemic_risk_score < 0.2:
            self.market_confidence = min(1.0, self.market_confidence * 1.002)
            
    def calculate_bank_concentration_risk(self):
        """Calculate banking system concentration risk."""
        model = self.model
        
        if not model.commercial_banks:
            return 0.0
            
        # Calculate Herfindahl-Hirschman Index for deposits
        total_deposits = sum(bank.total_deposits for bank in model.commercial_banks)
        if total_deposits == 0:
            return 1.0
            
        hhi = sum((bank.total_deposits / total_deposits) ** 2 for bank in model.commercial_banks)
        
        # Convert HHI to risk score (higher concentration = higher risk)
        return min(1.0, hhi * 2)
        
    def calculate_cbdc_adoption_risk(self):
        """Calculate CBDC adoption velocity risk."""
        model = self.model
        
        adoption_rate = model.compute_cbdc_adoption_rate()
        cbdc_velocity = self.cbdc_adoption_velocity
        
        # Risk increases with rapid adoption
        if adoption_rate > 0.7 and cbdc_velocity > 0.1:
            return min(1.0, adoption_rate * cbdc_velocity * 2)
        return adoption_rate * 0.3
        
    def calculate_liquidity_system_risk(self):
        """Calculate system-wide liquidity risk."""
        model = self.model
        
        if not model.commercial_banks:
            return 0.0
            
        # Calculate average liquidity ratio
        avg_liquidity = model.compute_average_bank_liquidity()
        
        # Count banks in liquidity stress
        stressed_banks = sum(1 for bank in model.commercial_banks 
                           if hasattr(bank, 'liquidity_stress_flag') and bank.liquidity_stress_flag)
        
        stress_ratio = stressed_banks / len(model.commercial_banks)
        
        return min(1.0, (1 - avg_liquidity) * 0.5 + stress_ratio * 0.8)
        
    def implement_regulatory_actions(self):
        """Implement regulatory actions based on risk assessment."""
        model = self.model
        
        # Capital requirement adjustments
        if self.operational_risk_score > 0.4:
            for bank in model.commercial_banks:
                if not hasattr(bank, 'enhanced_capital_requirement'):
                    bank.enhanced_capital_requirement = True
                    bank.capital_buffer_requirement = 0.025  # Additional 2.5% buffer
        
        # Liquidity support measures
        if len([alert for alert in self.systemic_risk_alerts 
               if alert['type'] == 'liquidity_stress']) > 2:
            model.central_bank.emergency_liquidity_support = True
            
        # CBDC adoption controls
        if self.digital_run_probability > 0.3:
            model.central_bank.cbdc_adoption_controls = True
            # Implement holding limits or negative interest rates
            
    def get_risk_dashboard(self):
        """Get comprehensive risk dashboard for monitoring."""
        model = self.model
        
        return {
            'systemic_risk_score': model.systemic_risk_score if hasattr(model, 'systemic_risk_score') else 0,
            'operational_risk_score': self.operational_risk_score,
            'cyber_threat_level': self.cyber_threat_level,
            'cybersecurity_risk_level': self.cyber_threat_level,  # Alias for compatibility
            'market_confidence': self.market_confidence,
            'regulatory_credibility': self.regulatory_credibility,
            'digital_run_probability': self.digital_run_probability,
            'cyber_incidents_count': self.cyber_incidents_count,
            'compliance_violations': len(self.compliance_violations),
            'systemic_alerts': len(self.systemic_risk_alerts),
            'system_downtime_hours': self.system_downtime_hours,
            'basel_compliance_rate': self.regulatory_credibility,  # Basel compliance approximation
            'liquidity_stress_indicator': self.operational_risk_score  # Liquidity stress approximation
        }
        
    def __str__(self):
        return f"RiskManager(systemic_risk={self.operational_risk_score:.2f}, confidence={self.market_confidence:.2f})"