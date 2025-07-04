#!/usr/bin/env python3
"""
Test script for consumer-merchant transactions with CBDC payments.
"""

from model import CBDCBankingModel
import numpy as np

def test_consumer_merchant_transactions():
    """Test the enhanced consumer-merchant transaction system."""
    
    print("=== Enhanced CBDC Simulation: Consumer-Merchant Transactions ===")
    
    # Create smaller model for testing
    model = CBDCBankingModel(
        n_consumers=10,
        n_commercial_banks=2,
        n_merchants=3,
        cbdc_introduction_step=8,
        cbdc_adoption_rate=0.2,
        cbdc_attractiveness=2.5,
        initial_consumer_wealth=8400,
        bank_interest_rate=0.048,
        cbdc_interest_rate=0.045
    )
    
    print(f"Consumers: {len(model.consumers)}")
    print(f"Commercial Banks: {len(model.commercial_banks)}")
    print(f"Merchants: {len(model.merchants)}")
    
    # Check initial merchant setup
    print("\nInitial Merchant Setup:")
    for i, merchant in enumerate(model.merchants):
        bank_id = merchant.primary_bank.unique_id if merchant.primary_bank else "None"
        print(f"Merchant {i+1}: {merchant.business_type} ({merchant.size}), Bank: {bank_id}")
        print(f"  CBDC Wallet: ${getattr(merchant, 'cbdc_wallet_balance', 0):.2f}")
        print(f"  Bank Account: ${getattr(merchant, 'bank_account_balance', 0):.2f}")
        print(f"  Accepts CBDC: {getattr(merchant, 'accepts_cbdc', False)}")
    
    # Run simulation
    print("\n=== Running Simulation ===")
    for step in range(15):
        try:
            model.step()
            
            if step == 5:
                print(f"\nStep {step}: Pre-CBDC")
                print(f"CBDC Adoption Rate: {model.compute_cbdc_adoption_rate():.1%}")
                merchants_accepting_cbdc = sum(1 for m in model.merchants if getattr(m, 'accepts_cbdc', False))
                print(f"Merchants accepting CBDC: {merchants_accepting_cbdc}/{len(model.merchants)}")
            
            elif step == 12:
                print(f"\nStep {step}: Post-CBDC Introduction")
                print(f"CBDC Adoption Rate: {model.compute_cbdc_adoption_rate():.1%}")
                merchants_accepting_cbdc = sum(1 for m in model.merchants if getattr(m, 'accepts_cbdc', False))
                print(f"Merchants accepting CBDC: {merchants_accepting_cbdc}/{len(model.merchants)}")
                
                # Check payment flows
                total_cbdc_merchant_wallets = sum(getattr(m, 'cbdc_wallet_balance', 0) for m in model.merchants)
                total_bank_merchant_accounts = sum(getattr(m, 'bank_account_balance', 0) for m in model.merchants)
                print(f"Total CBDC in merchant wallets: ${total_cbdc_merchant_wallets:.2f}")
                print(f"Total bank transfers to merchants: ${total_bank_merchant_accounts:.2f}")
        
        except Exception as e:
            print(f"Error at step {step}: {e}")
            break
    
    # Final results
    print(f"\n=== Final Results ===")
    print(f"CBDC Adoption Rate: {model.compute_cbdc_adoption_rate():.1%}")
    merchants_accepting_cbdc = sum(1 for m in model.merchants if getattr(m, 'accepts_cbdc', False))
    print(f"Merchants accepting CBDC: {merchants_accepting_cbdc}/{len(model.merchants)}")
    
    # Payment flow analysis
    total_cbdc_merchant_wallets = sum(getattr(m, 'cbdc_wallet_balance', 0) for m in model.merchants)
    total_bank_merchant_accounts = sum(getattr(m, 'bank_account_balance', 0) for m in model.merchants)
    total_cash_merchant = sum(getattr(m, 'cash_balance', 0) for m in model.merchants)
    
    print(f"\n=== Payment Flow Analysis ===")
    print(f"Total CBDC in merchant wallets: ${total_cbdc_merchant_wallets:.2f}")
    print(f"Total bank transfers to merchants: ${total_bank_merchant_accounts:.2f}")
    print(f"Total cash payments to merchants: ${total_cash_merchant:.2f}")
    
    # Consumer holdings
    total_consumer_cbdc = sum(c.cbdc_holdings for c in model.consumers)
    total_consumer_bank_deposits = sum(c.bank_deposits for c in model.consumers)
    print(f"\nConsumer Holdings:")
    print(f"Total consumer CBDC holdings: ${total_consumer_cbdc:.2f}")
    print(f"Total consumer bank deposits: ${total_consumer_bank_deposits:.2f}")
    
    # Transaction volumes
    if hasattr(model, 'transaction_volumes'):
        print(f"\n=== Transaction Volumes ===")
        for method, volume in model.transaction_volumes.items():
            if volume > 0:
                print(f"{method}: ${volume:.2f}")
    
    print("\n✓ Enhanced simulation with consumer-merchant transactions completed!")
    return model

if __name__ == "__main__":
    test_consumer_merchant_transactions()