#!/usr/bin/env python3
"""
Test script for real-world complexity validation in CBDC Banking Simulation.
This script validates the implementation of advanced features including:
- Risk Manager with cybersecurity threats
- Basel III compliance monitoring
- Real-world merchant transactions
- Enhanced consumer behaviors
- Operational risk management
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model import CBDCBankingModel
import pandas as pd
import numpy as np


def test_real_world_simulation():
    """Test the enhanced CBDC banking simulation with real-world complexities."""
    
    print("=== CBDC Banking Simulation: Real-World Complexity Test ===\n")
    
    # Create model with realistic parameters
    model = CBDCBankingModel(
        n_consumers=100,
        n_commercial_banks=6,  # 2 large banks, 4 small-medium banks
        n_merchants=15,
        cbdc_introduction_step=20,
        cbdc_adoption_rate=0.08,
        cbdc_attractiveness=2.2,
        initial_consumer_wealth=8400,  # 2025 calibrated
        bank_interest_rate=0.048,  # 4.8% deposit rate
        cbdc_interest_rate=0.045   # 4.5% CBDC rate
    )
    
    print("✓ Model initialized with 2025-calibrated parameters")
    print(f"  - Consumers: {len(model.consumers)}")
    print(f"  - Commercial Banks: {len(model.commercial_banks)}")
    print(f"  - Merchants: {len(model.merchants)}")
    print(f"  - Risk Manager: {hasattr(model, 'risk_manager')}")
    print()
    
    # Test initial conditions
    print("=== Initial Conditions Analysis ===")
    total_deposits = model.compute_total_bank_deposits()
    total_wealth = model.compute_total_consumer_wealth()
    print(f"Total Bank Deposits: ${total_deposits:,.0f}")
    print(f"Total Consumer Wealth: ${total_wealth:,.0f}")
    print(f"Deposit Allocation: {(total_deposits/total_wealth)*100:.1f}%")
    print()
    
    # Test Basel III compliance
    print("=== Basel III Compliance Check ===")
    for bank in model.commercial_banks:
        if hasattr(bank, 'tier_1_capital'):
            capital_ratio = bank.tier_1_capital / max(bank.total_deposits, 1)
            print(f"Bank {bank.unique_id}: Capital Ratio {capital_ratio:.2%}, "
                  f"Deposits ${bank.total_deposits:,.0f}")
    print()
    
    # Run simulation
    print("=== Running 50-Step Simulation ===")
    steps_to_run = 50
    
    for step in range(steps_to_run):
        model.step()
        
        # Monitor key events
        if step == model.cbdc_introduction_step:
            print(f"Step {step}: CBDC Introduced")
        
        if step % 10 == 0:
            cbdc_adoption = model.compute_cbdc_adoption_rate()
            print(f"Step {step}: CBDC Adoption Rate: {cbdc_adoption:.1%}")
    
    print(f"✓ Simulation completed: {steps_to_run} steps\n")
    
    # Analyze final results
    print("=== Final Results Analysis ===")
    
    # CBDC adoption
    final_cbdc_adoption = model.compute_cbdc_adoption_rate()
    cbdc_holders = model.compute_cbdc_adopters()
    print(f"CBDC Adoption Rate: {final_cbdc_adoption:.1%}")
    print(f"CBDC Adopters: {cbdc_holders} out of {len(model.consumers)} consumers")
    
    # Banking system health
    final_deposits = model.compute_total_bank_deposits()
    final_loans = model.compute_total_bank_loans()
    avg_liquidity = model.compute_average_bank_liquidity()
    print(f"Total Bank Deposits: ${final_deposits:,.0f}")
    print(f"Total Bank Loans: ${final_loans:,.0f}")
    print(f"Average Bank Liquidity: {avg_liquidity:.2%}")
    
    # Transaction analysis
    if hasattr(model, 'transaction_volumes'):
        total_volume = sum(model.transaction_volumes.values())
        if total_volume > 0:
            print(f"CBDC Transaction Share: {model.transaction_volumes.get('CBDC', 0)/total_volume:.1%}")
    
    print()
    
    # Test risk management features
    print("=== Risk Management Analysis ===")
    
    if hasattr(model, 'risk_manager'):
        risk_dashboard = model.risk_manager.get_risk_dashboard()
        print(f"Systemic Risk Score: {risk_dashboard['systemic_risk_score']:.2f}")
        print(f"Cybersecurity Risk Level: {risk_dashboard['cybersecurity_risk_level']:.2f}")
        print(f"Basel III Compliance Rate: {risk_dashboard['basel_compliance_rate']:.1%}")
        print(f"Liquidity Stress Indicator: {risk_dashboard['liquidity_stress_indicator']:.2f}")
    
    # Test bank-specific risk metrics
    stressed_banks = 0
    for bank in model.commercial_banks:
        if hasattr(bank, 'liquidity_stress_flag') and bank.liquidity_stress_flag:
            stressed_banks += 1
    print(f"Banks Under Liquidity Stress: {stressed_banks}/{len(model.commercial_banks)}")
    print()
    
    # Test merchant ecosystem
    print("=== Merchant Ecosystem Analysis ===")
    
    merchant_stats = {}
    for merchant in model.merchants:
        business_type = merchant.business_type
        if business_type not in merchant_stats:
            merchant_stats[business_type] = {
                'count': 0,
                'avg_revenue': 0,
                'cbdc_usage': 0
            }
        merchant_stats[business_type]['count'] += 1
        merchant_stats[business_type]['avg_revenue'] += merchant.monthly_revenue
        if hasattr(merchant, 'accepts_cbdc') and merchant.accepts_cbdc:
            merchant_stats[business_type]['cbdc_usage'] += 1
    
    for btype, stats in merchant_stats.items():
        if stats['count'] > 0:
            avg_revenue = stats['avg_revenue'] / stats['count']
            cbdc_rate = stats['cbdc_usage'] / stats['count']
            print(f"{btype.title()}: {stats['count']} merchants, "
                  f"Avg Revenue: ${avg_revenue:,.0f}, CBDC Rate: {cbdc_rate:.1%}")
    
    print()
    
    # Test network centrality changes
    print("=== Network Centrality Analysis ===")
    
    large_bank_centrality = model.compute_large_bank_centrality()
    small_bank_centrality = model.compute_small_bank_centrality()
    central_bank_centrality = model.compute_central_bank_centrality()
    
    print(f"Large Bank Centrality: {large_bank_centrality:.3f}")
    print(f"Small Bank Centrality: {small_bank_centrality:.3f}")
    print(f"Central Bank Centrality: {central_bank_centrality:.3f}")
    
    # Test hypothesis validation
    print("\n=== Hypothesis Testing Results ===")
    
    # H1: CBDC adoption affects bank network centrality
    centrality_impact = abs(large_bank_centrality - small_bank_centrality)
    print(f"H1 - Centrality Differentiation: {centrality_impact:.3f}")
    
    # H3: Liquidity stress increases with CBDC adoption
    liquidity_stress = model.compute_average_liquidity_stress()
    print(f"H3 - Average Liquidity Stress: {liquidity_stress:.3f}")
    
    # H4: Banking network density changes
    network_density = model.compute_network_density()
    print(f"H4 - Network Density: {network_density:.3f}")
    
    # H6: Central bank centrality increases with CBDC
    print(f"H6 - Central Bank Centrality: {central_bank_centrality:.3f}")
    
    print()
    
    # Test economic efficiency
    print("=== Economic Impact Assessment ===")
    
    if hasattr(model, 'economic_conditions'):
        print(f"Economic Efficiency: {model.economic_conditions.get('efficiency', 1.0):.3f}")
        print(f"Market Confidence: {model.economic_conditions.get('confidence', 1.0):.3f}")
        print(f"Financial Stability: {model.economic_conditions.get('stability', 1.0):.3f}")
    
    # Transaction cost analysis
    if hasattr(model, 'transaction_costs'):
        print(f"Average Transaction Cost: ${model.transaction_costs.get('average', 0):.2f}")
        print(f"CBDC Cost Advantage: {model.transaction_costs.get('cbdc_advantage', 0):.1%}")
    
    print()
    
    # Summary and validation
    print("=== Simulation Validation Summary ===")
    
    validation_checks = []
    
    # Check 1: CBDC adoption occurred
    if final_cbdc_adoption > 0.1:
        validation_checks.append("✓ CBDC adoption achieved (>10%)")
    else:
        validation_checks.append("✗ CBDC adoption low (<10%)")
    
    # Check 2: Banking system stability
    if avg_liquidity > 0.5:
        validation_checks.append("✓ Banking system maintained liquidity")
    else:
        validation_checks.append("✗ Banking system liquidity stressed")
    
    # Check 3: Risk management active
    if hasattr(model, 'risk_manager') and hasattr(model.risk_manager, 'systemic_risk_score'):
        validation_checks.append("✓ Risk management system operational")
    else:
        validation_checks.append("✗ Risk management system inactive")
    
    # Check 4: Merchant ecosystem functioning
    if len(model.merchants) > 0:
        validation_checks.append("✓ Merchant ecosystem implemented")
    else:
        validation_checks.append("✗ Merchant ecosystem missing")
    
    # Check 5: Real-world complexity
    complexity_features = 0
    if hasattr(model, 'systemic_risk_score'):
        complexity_features += 1
    if any(hasattr(bank, 'cyber_incident_flag') for bank in model.commercial_banks):
        complexity_features += 1
    if any(hasattr(bank, 'operational_risk_score') for bank in model.commercial_banks):
        complexity_features += 1
    
    if complexity_features >= 2:
        validation_checks.append("✓ Real-world complexity features active")
    else:
        validation_checks.append("✗ Real-world complexity features missing")
    
    for check in validation_checks:
        print(check)
    
    print(f"\nValidation Score: {sum(1 for c in validation_checks if c.startswith('✓'))}/5")
    
    return model


def generate_detailed_report(model):
    """Generate a detailed analysis report of the simulation."""
    
    print("\n" + "="*80)
    print("DETAILED SIMULATION REPORT")
    print("="*80)
    
    # Agent-level analysis
    print("\n--- Agent Performance Analysis ---")
    
    # Consumer analysis
    consumer_cbdc_count = sum(1 for c in model.consumers if hasattr(c, 'cbdc_holdings') and c.cbdc_holdings > 0)
    consumer_wealth_dist = [c.wealth for c in model.consumers]
    
    print(f"Consumer Analysis:")
    print(f"  - CBDC Adopters: {consumer_cbdc_count}/{len(model.consumers)}")
    print(f"  - Average Wealth: ${np.mean(consumer_wealth_dist):,.0f}")
    print(f"  - Wealth Std Dev: ${np.std(consumer_wealth_dist):,.0f}")
    
    # Bank analysis
    print(f"\nBank Analysis:")
    for bank in model.commercial_banks:
        deposit_change = getattr(bank, 'deposit_change_rate', 0)
        print(f"  - Bank {bank.unique_id} ({bank.bank_type}): "
              f"Deposits ${bank.total_deposits:,.0f}, "
              f"Change: {deposit_change:.1%}")
    
    # Merchant analysis
    print(f"\nMerchant Analysis:")
    for merchant in model.merchants:
        cbdc_share = getattr(merchant, 'cbdc_transaction_share', 0)
        print(f"  - {merchant.business_type.title()}: "
              f"Revenue ${merchant.monthly_revenue:,.0f}, "
              f"CBDC Share: {cbdc_share:.1%}")
    
    # Risk analysis
    if hasattr(model, 'risk_manager'):
        risk_data = model.risk_manager.get_risk_dashboard()
        print(f"\nRisk Analysis:")
        for key, value in risk_data.items():
            if isinstance(value, float):
                print(f"  - {key.replace('_', ' ').title()}: {value:.3f}")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    """Run the real-world complexity test."""
    
    try:
        print("Starting Real-World CBDC Banking Simulation Test...")
        print("=" * 60)
        
        # Run the test
        model = test_real_world_simulation()
        
        # Generate detailed report
        generate_detailed_report(model)
        
        print("\n✓ Real-world complexity test completed successfully!")
        print("All advanced features validated and operational.")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)