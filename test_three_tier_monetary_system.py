#!/usr/bin/env python3
"""
Test script for three-tier monetary system implementation.
This tests the proper distinction between:
1. Banknotes (Central Bank liability)
2. Bank Deposits (Commercial Bank liability) 
3. CBDC (Central Bank liability)

And tracks conversion flows from banknotes and deposits to CBDC.
"""

import sys
import os
import numpy as np

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import CBDCBankingModel

def test_three_tier_monetary_system():
    """Test the three-tier monetary system with proper liability tracking."""
    
    print("=== Three-Tier Monetary System Test ===")
    print("Testing: Banknotes vs Deposits vs CBDC")
    print("Liability tracking: Central Bank (banknotes + CBDC) vs Commercial Banks (deposits)")
    print()
    
    # Create model with small number of agents for clear tracking
    model = CBDCBankingModel(
        n_consumers=5,
        n_commercial_banks=2,
        n_merchants=2,
        cbdc_introduction_step=10,
        cbdc_adoption_rate=0.3,
        initial_consumer_wealth=1000
    )
    
    print("Initial Consumer Holdings (Three-Tier System):")
    total_banknotes = 0
    total_deposits = 0
    total_cbdc = 0
    
    for i, consumer in enumerate(model.consumers):
        print(f"Consumer {i+1}:")
        print(f"  Bank Deposits: ${consumer.bank_deposits:.2f} (Commercial Bank liability)")
        print(f"  Banknotes: ${consumer.banknote_holdings:.2f} (Central Bank liability)")
        print(f"  CBDC: ${consumer.cbdc_holdings:.2f} (Central Bank liability)")
        print(f"  Other Assets: ${consumer.other_assets:.2f}")
        print(f"  Total Wealth: ${consumer.bank_deposits + consumer.banknote_holdings + consumer.cbdc_holdings + consumer.other_assets:.2f}")
        print()
        
        total_banknotes += consumer.banknote_holdings
        total_deposits += consumer.bank_deposits
        total_cbdc += consumer.cbdc_holdings
    
    print(f"System Totals (Initial):")
    print(f"Total Banknotes: ${total_banknotes:.2f}")
    print(f"Total Deposits: ${total_deposits:.2f}")
    print(f"Total CBDC: ${total_cbdc:.2f}")
    print()
    
    # Check central bank liability tracking
    print("Central Bank Liability Tracking:")
    print(f"Banknotes Outstanding: ${model.central_bank.banknotes_outstanding:.2f}")
    print(f"CBDC Outstanding: ${model.central_bank.cbdc_outstanding:.2f}")
    print(f"Total Central Bank Liabilities: ${model.central_bank.banknotes_outstanding + model.central_bank.cbdc_outstanding:.2f}")
    print()
    
    # Run simulation until CBDC is introduced
    print("=== Running Simulation Until CBDC Introduction ===")
    for step in range(15):
        model.step()
        if step == 9:  # Just before CBDC introduction
            print(f"Step {step+1} - Pre-CBDC Introduction")
        elif step == 10:  # CBDC introduction
            print(f"Step {step+1} - CBDC Introduced!")
        elif step == 14:  # Final step
            print(f"Step {step+1} - Final Results")
            break
    
    print("\n=== Final Results: Three-Tier Monetary System ===")
    
    # Consumer holdings after CBDC introduction
    final_banknotes = 0
    final_deposits = 0
    final_cbdc = 0
    
    for i, consumer in enumerate(model.consumers):
        print(f"Consumer {i+1} (Final):")
        print(f"  Bank Deposits: ${consumer.bank_deposits:.2f}")
        print(f"  Banknotes: ${consumer.banknote_holdings:.2f}")
        print(f"  CBDC: ${consumer.cbdc_holdings:.2f}")
        print(f"  CBDC Adopter: {consumer.cbdc_adopter}")
        print()
        
        final_banknotes += consumer.banknote_holdings
        final_deposits += consumer.bank_deposits
        final_cbdc += consumer.cbdc_holdings
    
    print(f"System Totals (Final):")
    print(f"Total Banknotes: ${final_banknotes:.2f}")
    print(f"Total Deposits: ${final_deposits:.2f}")  
    print(f"Total CBDC: ${final_cbdc:.2f}")
    print()
    
    # Central bank liability analysis
    cb_liability = model.central_bank.get_liability_breakdown()
    print("Central Bank Liability Analysis:")
    print(f"Banknotes Outstanding: ${cb_liability['banknotes_outstanding']:.2f}")
    print(f"CBDC Outstanding: ${cb_liability['cbdc_outstanding']:.2f}")
    print(f"Total Central Bank Liabilities: ${cb_liability['total_central_bank_liabilities']:.2f}")
    print()
    
    # Conversion tracking
    print("Conversion Flow Analysis:")
    print(f"Banknotes → CBDC: ${cb_liability['banknote_to_cbdc_conversion']:.2f}")
    print(f"Deposits → CBDC: ${cb_liability['deposit_to_cbdc_conversion']:.2f}")
    print(f"Total Conversions: ${cb_liability['banknote_to_cbdc_conversion'] + cb_liability['deposit_to_cbdc_conversion']:.2f}")
    print()
    
    # Impact on financial system
    print("Financial System Impact:")
    print(f"Change in Banknotes: ${final_banknotes - total_banknotes:.2f}")
    print(f"Change in Deposits: ${final_deposits - total_deposits:.2f}")
    print(f"Change in CBDC: ${final_cbdc - total_cbdc:.2f}")
    print()
    
    # Commercial bank impact
    total_bank_deposits_initial = sum(bank.total_deposits for bank in model.commercial_banks)
    print("Commercial Bank Impact:")
    for i, bank in enumerate(model.commercial_banks):
        print(f"Bank {i+1}:")
        print(f"  Current Deposits: ${bank.total_deposits:.2f}")
        print(f"  Liquidity Ratio: {bank.liquidity_ratio:.3f}")
        print(f"  Total Loans: ${bank.total_loans:.2f}")
        print()
    
    # Verify monetary conservation
    print("Monetary Conservation Check:")
    initial_total = total_banknotes + total_deposits + total_cbdc
    final_total = final_banknotes + final_deposits + final_cbdc
    print(f"Initial Total Money: ${initial_total:.2f}")
    print(f"Final Total Money: ${final_total:.2f}")
    print(f"Difference: ${final_total - initial_total:.2f}")
    print()
    
    # Success indicators
    success_checks = []
    success_checks.append(("Banknotes properly initialized", total_banknotes > 0))
    success_checks.append(("CBDC conversion occurred", final_cbdc > 0))
    success_checks.append(("Central bank liability tracking", cb_liability['total_central_bank_liabilities'] > 0))
    success_checks.append(("Conversion flow tracking", cb_liability['banknote_to_cbdc_conversion'] + cb_liability['deposit_to_cbdc_conversion'] > 0))
    success_checks.append(("Monetary conservation", abs(final_total - initial_total) < 1.0))
    
    print("Success Indicators:")
    for check, passed in success_checks:
        status = "✓" if passed else "✗"
        print(f"{status} {check}")
    
    all_passed = all(passed for _, passed in success_checks)
    print(f"\n{'✓' if all_passed else '✗'} Three-tier monetary system implementation {'successful' if all_passed else 'needs fixes'}!")
    
    return all_passed

if __name__ == "__main__":
    test_three_tier_monetary_system()