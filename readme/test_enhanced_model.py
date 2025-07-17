#!/usr/bin/env python3
"""
Test script for the enhanced CBDC banking simulation with merchants and real-world scenarios.
This demonstrates the new features and realistic economic behavior.
"""

import pandas as pd
import numpy as np
from model import CBDCBankingModel

def run_enhanced_simulation_test():
    """Run a comprehensive test of the enhanced model with real-world scenarios."""
    
    print("🏦 CBDC Banking Simulation - Enhanced Real-World Model Test")
    print("=" * 70)
    
    # Create model with enhanced parameters
    print("Creating enhanced model with:")
    print("- 100 Consumers (diverse financial profiles)")
    print("- 6 Commercial Banks (mix of large and small)")  
    print("- 15 Merchants (5 business types)")
    print("- CBDC introduction at step 20")
    
    model = CBDCBankingModel(
        n_consumers=100,
        n_commercial_banks=6,
        n_merchants=15,
        cbdc_introduction_step=20,
        cbdc_adoption_rate=0.06,
        cbdc_attractiveness=2.5,
        initial_consumer_wealth=8400,
        bank_interest_rate=0.048,
        cbdc_interest_rate=0.045
    )
    
    print("\n📊 Initial Model State:")
    print(f"- Total Consumers: {len(model.consumers)}")
    print(f"- Total Banks: {len(model.commercial_banks)}")
    print(f"- Total Merchants: {len(model.merchants)}")
    print(f"- Economic Conditions: {model.economic_conditions:.2f}")
    
    # Show merchant distribution
    merchant_types = {}
    for merchant in model.merchants:
        business_type = merchant.business_type
        merchant_types[business_type] = merchant_types.get(business_type, 0) + 1
    
    print(f"\n🏪 Merchant Distribution:")
    for business_type, count in merchant_types.items():
        print(f"  - {business_type.title()}: {count}")
    
    # Show initial bank distribution
    large_banks = len(model.large_banks)
    small_banks = len(model.small_medium_banks)
    print(f"\n🏛️ Bank Distribution:")
    print(f"  - Large Banks: {large_banks}")
    print(f"  - Small/Medium Banks: {small_banks}")
    
    # Run simulation for 50 steps (about 4 years)
    print(f"\n🚀 Running simulation for 50 steps...")
    steps = 50
    
    # Track key metrics during simulation
    results = {
        'step': [],
        'cbdc_adoption_rate': [],
        'total_cbdc_holdings': [],
        'total_bank_deposits': [],
        'economic_conditions': [],
        'average_bank_liquidity': [],
        'merchant_cbdc_usage': []
    }
    
    for step in range(steps):
        model.step()
        
        # Collect metrics
        results['step'].append(step + 1)
        results['cbdc_adoption_rate'].append(model.compute_cbdc_adoption_rate())
        results['total_cbdc_holdings'].append(model.compute_total_cbdc_holdings())
        results['total_bank_deposits'].append(model.compute_total_bank_deposits())
        results['economic_conditions'].append(model.economic_conditions)
        results['average_bank_liquidity'].append(model.compute_average_bank_liquidity())
        
        # Calculate merchant CBDC usage
        merchant_cbdc_total = 0
        merchant_total_volume = 0
        for merchant in model.merchants:
            total_volume = sum(merchant.payment_method_volumes.values())
            cbdc_volume = merchant.payment_method_volumes.get('cbdc', 0)
            merchant_cbdc_total += cbdc_volume
            merchant_total_volume += total_volume
        
        merchant_cbdc_rate = merchant_cbdc_total / max(1, merchant_total_volume)
        results['merchant_cbdc_usage'].append(merchant_cbdc_rate)
        
        # Print progress every 10 steps
        if (step + 1) % 10 == 0:
            cbdc_rate = model.compute_cbdc_adoption_rate()
            economic_cond = model.economic_conditions
            print(f"  Step {step + 1}: CBDC Adoption: {cbdc_rate:.1%}, Economic Conditions: {economic_cond:.3f}")
    
    print(f"\n✅ Simulation completed!")
    
    # Analysis of results
    df = pd.DataFrame(results)
    
    print(f"\n📈 Final Results Summary:")
    final_adoption = df['cbdc_adoption_rate'].iloc[-1]
    final_cbdc_holdings = df['total_cbdc_holdings'].iloc[-1]
    final_bank_deposits = df['total_bank_deposits'].iloc[-1]
    final_economic_conditions = df['economic_conditions'].iloc[-1]
    final_merchant_cbdc = df['merchant_cbdc_usage'].iloc[-1]
    
    print(f"- Final CBDC Adoption Rate: {final_adoption:.1%}")
    print(f"- Total CBDC Holdings: ${final_cbdc_holdings:,.0f}")
    print(f"- Total Bank Deposits: ${final_bank_deposits:,.0f}")
    print(f"- Final Economic Conditions: {final_economic_conditions:.3f}")
    print(f"- Merchant CBDC Usage: {final_merchant_cbdc:.1%}")
    
    # Show CBDC impact on different merchant types
    print(f"\n🏪 Merchant Payment Method Analysis:")
    for merchant in model.merchants[:5]:  # Show first 5 merchants
        profile = merchant.get_business_profile()
        print(f"  {profile['business_type'].title()} ({profile['size']}): "
              f"CBDC {profile['cbdc_share']:.1%}, "
              f"Card {profile['card_share']:.1%}, "
              f"Cash {profile['cash_share']:.1%}")
    
    # Bank health analysis
    print(f"\n🏛️ Banking System Health:")
    avg_liquidity = model.compute_average_bank_liquidity()
    print(f"- Average Bank Liquidity: {avg_liquidity:.1%}")
    
    # Show impact on different bank types
    large_bank_deposits = sum(bank.total_deposits for bank in model.large_banks)
    small_bank_deposits = sum(bank.total_deposits for bank in model.small_medium_banks)
    total_deposits = large_bank_deposits + small_bank_deposits
    
    if total_deposits > 0:
        large_share = large_bank_deposits / total_deposits
        small_share = small_bank_deposits / total_deposits
        print(f"- Large Bank Deposit Share: {large_share:.1%}")
        print(f"- Small/Medium Bank Share: {small_share:.1%}")
    
    # Real-world scenario insights
    print(f"\n🌍 Real-World Scenario Insights:")
    
    # Economic efficiency gains
    if final_economic_conditions > 1.0:
        efficiency_gain = (final_economic_conditions - 1.0) * 100
        print(f"- Economic Efficiency Gain: +{efficiency_gain:.1f}%")
    else:
        efficiency_loss = (1.0 - final_economic_conditions) * 100
        print(f"- Economic Efficiency Loss: -{efficiency_loss:.1f}%")
    
    # Payment modernization
    print(f"- Payment System Modernization: {final_merchant_cbdc:.1%} of merchant transactions use CBDC")
    
    # Financial inclusion impact
    cbdc_users = sum(1 for consumer in model.consumers if consumer.cbdc_adopter)
    inclusion_rate = cbdc_users / len(model.consumers)
    print(f"- Digital Financial Inclusion: {inclusion_rate:.1%} of consumers adopted CBDC")
    
    # Transaction cost reduction (estimated)
    if final_merchant_cbdc > 0:
        cost_savings = final_merchant_cbdc * 2.0  # Assume 2% cost reduction
        print(f"- Estimated Transaction Cost Savings: {cost_savings:.1f}%")
    
    print(f"\n💡 Key Findings:")
    
    # Network effects
    if final_adoption > 0.3:
        print("- Strong network effects: High CBDC adoption drives merchant acceptance")
    elif final_adoption > 0.1:
        print("- Moderate adoption: CBDC gaining traction in specific use cases")
    else:
        print("- Limited adoption: Traditional banking remains dominant")
    
    # Banking sector impact
    liquidity_stress = 1 - avg_liquidity
    if liquidity_stress > 0.3:
        print("- Significant banking sector stress from deposit outflows")
    elif liquidity_stress > 0.1:
        print("- Moderate banking sector adaptation to CBDC competition")
    else:
        print("- Banking sector remains stable despite CBDC introduction")
    
    # Economic transformation
    if final_economic_conditions > 1.01:
        print("- CBDC driving positive economic transformation through efficiency gains")
    elif final_economic_conditions < 0.99:
        print("- CBDC transition creating short-term economic friction")
    else:
        print("- Neutral economic impact with balanced benefits and costs")
    
    return df, model

if __name__ == "__main__":
    # Run the test
    results_df, test_model = run_enhanced_simulation_test()
    
    print(f"\n📊 Data collected for {len(results_df)} simulation steps")
    print("Test completed successfully! Enhanced model with real-world scenarios is working.")