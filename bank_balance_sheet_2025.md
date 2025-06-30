# Bank Balance Sheet Parameters - 2025 Calibration

## Overview
This document provides realistic balance sheet parameters for the CBDC simulation based on actual 2025 US banking data.

## Data Sources
- Federal Reserve H.8 Assets and Liabilities of Commercial Banks (2025)
- FDIC Quarterly Banking Profile Q4 2024/Q1 2025
- Call Report data for large vs community banks
- Federal Reserve Bank of St. Louis FRED database

## Large Banks (Top 4: JPMorgan, BofA, Wells Fargo, Citi)

### Balance Sheet Structure (Average %)
| Asset Category | Percentage | Amount (scaled) |
|---------------|------------|-----------------|
| Cash & Reserves | 15% | $120,960 |
| Securities | 25% | $201,600 |
| Loans Total | 55% | $443,520 |
| - Consumer Loans | 20% | $161,280 |
| - Commercial Loans | 25% | $201,600 |
| - Real Estate | 10% | $80,640 |
| Other Assets | 5% | $40,320 |
| **Total Assets** | **100%** | **$806,400** |

| Liability Category | Percentage | Amount (scaled) |
|-------------------|------------|-----------------|
| Deposits Total | 75% | $604,800 |
| - Demand Deposits | 45% | $362,880 |
| - Time Deposits | 30% | $241,920 |
| Borrowings | 10% | $80,640 |
| Other Liabilities | 3% | $24,192 |
| **Total Equity** | **12%** | **$96,768** |

### Key Ratios (2025 Large Banks)
- **Loan-to-Deposit Ratio**: 73.3%
- **Capital Adequacy**: 12.0%
- **Liquidity Coverage Ratio**: 125%
- **Net Interest Margin**: 2.8%

## Small-Medium Banks (Community Banks <$10B assets)

### Balance Sheet Structure (Average %)
| Asset Category | Percentage | Amount (scaled) |
|---------------|------------|-----------------|
| Cash & Reserves | 12% | $9,216 |
| Securities | 20% | $15,360 |
| Loans Total | 62% | $47,616 |
| - Consumer Loans | 15% | $11,520 |
| - Commercial Loans | 35% | $26,880 |
| - Real Estate | 12% | $9,216 |
| Other Assets | 6% | $4,608 |
| **Total Assets** | **100%** | **$76,800** |

| Liability Category | Percentage | Amount (scaled) |
|-------------------|------------|-----------------|
| Deposits Total | 82% | $62,976 |
| - Demand Deposits | 50% | $38,400 |
| - Time Deposits | 32% | $24,576 |
| Borrowings | 6% | $4,608 |
| Other Liabilities | 2% | $1,536 |
| **Total Equity** | **10%** | **$7,680** |

### Key Ratios (2025 Small Banks)
- **Loan-to-Deposit Ratio**: 75.6%
- **Capital Adequacy**: 10.0%
- **Liquidity Coverage Ratio**: 110%
- **Net Interest Margin**: 3.4%

## Interest Rate Environment (2025)

### Deposit Rates by Product
| Product | Large Banks | Small Banks | Source |
|---------|-------------|-------------|---------|
| Checking | 0.5% | 0.8% | Bankrate 2025 |
| Savings | 4.2% | 4.8% | NerdWallet 2025 |
| Money Market | 4.5% | 5.0% | DepositAccounts 2025 |
| 1-Year CD | 4.8% | 5.2% | Bankrate 2025 |
| **Blended Rate** | **4.1%** | **4.6%** | **Weighted Average** |

### Lending Rates by Product
| Product | Large Banks | Small Banks | Source |
|---------|-------------|-------------|---------|
| Prime Rate | 8.5% | 8.5% | Federal Reserve |
| Credit Cards | 21.5% | 23.2% | Fed Consumer Credit |
| Auto Loans | 7.2% | 8.1% | Bankrate 2025 |
| Mortgages | 7.1% | 7.4% | Freddie Mac |
| Commercial | 8.8% | 9.5% | Fed Survey |
| **Blended Rate** | **9.1%** | **10.3%** | **Portfolio Weighted** |

## Reserve Requirements (2025)

### Federal Reserve Requirements
- **Transaction Accounts >$127.4M**: 10%
- **Transaction Accounts <$127.4M**: 0%
- **Time Deposits**: 0%
- **Eurocurrency Liabilities**: 0%

### Practical Reserve Holdings
| Bank Type | Excess Reserves | Required | Total Reserves |
|-----------|----------------|----------|----------------|
| Large Banks | 12% | 3% | 15% |
| Small Banks | 9% | 3% | 12% |

## Liquidity Requirements (2025)

### Basel III LCR Implementation
- **Large Banks (>$250B)**: 125% minimum
- **Regional Banks ($100-250B)**: 110% minimum
- **Community Banks (<$100B)**: Not required but 105% typical

### High-Quality Liquid Assets (HQLA)
| Asset Type | Haircut | Large Banks | Small Banks |
|------------|---------|-------------|-------------|
| Cash | 0% | 60% | 55% |
| Treasuries | 0% | 30% | 35% |
| Agency MBS | 15% | 10% | 10% |

## Capital Requirements (2025)

### Basel III Implementation
| Requirement | Large Banks | Small Banks |
|-------------|-------------|-------------|
| Common Equity Tier 1 | 7.0% | 7.0% |
| Tier 1 Capital | 8.5% | 8.5% |
| Total Capital | 10.5% | 10.5% |
| Leverage Ratio | 4.0% | 4.0% |

### Stress Test Buffers (Large Banks Only)
- **Stress Capital Buffer**: 2.5%
- **G-SIB Surcharge**: 1.0-3.5%
- **Total Buffer**: 3.5-6.0%

## Implementation Parameters

### Large Bank Balance Sheet
```python
large_bank_balance_sheet = {
    # Assets
    'cash_reserves': 0.15,           # 15% - high liquidity post-SVB
    'securities': 0.25,              # 25% - AFS securities
    'total_loans': 0.55,             # 55% - core business
    'other_assets': 0.05,            # 5% - premises, goodwill
    
    # Liabilities  
    'total_deposits': 0.75,          # 75% - funding base
    'demand_deposits': 0.45,         # 45% - checking, savings
    'time_deposits': 0.30,           # 30% - CDs, time
    'borrowings': 0.10,              # 10% - FHLB, Fed funds
    'other_liabilities': 0.03,       # 3% - accruals, other
    'equity': 0.12,                  # 12% - strong capital
    
    # Performance
    'loan_to_deposit_ratio': 0.733,  # 73.3%
    'net_interest_margin': 0.028,    # 2.8%
    'efficiency_ratio': 0.58,       # 58%
    'roe': 0.12                      # 12%
}
```

### Small Bank Balance Sheet
```python
small_bank_balance_sheet = {
    # Assets
    'cash_reserves': 0.12,           # 12% - adequate liquidity
    'securities': 0.20,              # 20% - municipal focus
    'total_loans': 0.62,             # 62% - relationship lending
    'other_assets': 0.06,            # 6% - premises higher %
    
    # Liabilities
    'total_deposits': 0.82,          # 82% - deposit-dependent
    'demand_deposits': 0.50,         # 50% - relationship accounts
    'time_deposits': 0.32,           # 32% - local CDs
    'borrowings': 0.06,              # 6% - limited access
    'other_liabilities': 0.02,       # 2% - minimal
    'equity': 0.10,                  # 10% - adequate capital
    
    # Performance
    'loan_to_deposit_ratio': 0.756,  # 75.6%
    'net_interest_margin': 0.034,    # 3.4%
    'efficiency_ratio': 0.65,       # 65%
    'roe': 0.10                      # 10%
}
```