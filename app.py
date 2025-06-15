import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from model import CBDCBankingModel
import io

def main():
    st.set_page_config(
        page_title="CBDC Impact on Commercial Banking Simulation",
        page_icon="🏦",
        layout="wide"
    )
    
    st.title("🏦 CBDC Impact on Commercial Banking Intermediation")
    st.markdown("An agent-based simulation using Mesa framework to model how Central Bank Digital Currency affects commercial banking operations.")
    
    # Sidebar for simulation parameters
    st.sidebar.header("Simulation Parameters")
    
    # Model parameters
    n_consumers = st.sidebar.slider("Number of Consumers", 50, 500, 200, 25)
    n_commercial_banks = st.sidebar.slider("Number of Commercial Banks", 3, 15, 8, 1)
    steps = st.sidebar.slider("Simulation Steps", 50, 500, 200, 25)
    
    # CBDC parameters
    cbdc_introduction_step = st.sidebar.slider("CBDC Introduction Step", 10, 100, 30, 5)
    cbdc_adoption_rate = st.sidebar.slider("CBDC Adoption Rate", 0.01, 0.1, 0.03, 0.01)
    cbdc_attractiveness = st.sidebar.slider("CBDC Attractiveness Factor", 1.0, 3.0, 1.5, 0.1)
    
    # Economic parameters
    initial_consumer_wealth = st.sidebar.slider("Initial Consumer Wealth", 1000, 10000, 5000, 500)
    bank_interest_rate = st.sidebar.slider("Bank Interest Rate (%)", 0.5, 5.0, 2.0, 0.1) / 100
    cbdc_interest_rate = st.sidebar.slider("CBDC Interest Rate (%)", 0.0, 3.0, 1.0, 0.1) / 100
    
    # Run simulation button
    if st.sidebar.button("Run Simulation", type="primary"):
        with st.spinner("Running simulation..."):
            # Initialize and run model
            model = CBDCBankingModel(
                n_consumers=n_consumers,
                n_commercial_banks=n_commercial_banks,
                cbdc_introduction_step=cbdc_introduction_step,
                cbdc_adoption_rate=cbdc_adoption_rate,
                cbdc_attractiveness=cbdc_attractiveness,
                initial_consumer_wealth=initial_consumer_wealth,
                bank_interest_rate=bank_interest_rate,
                cbdc_interest_rate=cbdc_interest_rate
            )
            
            # Run simulation
            for i in range(steps):
                model.step()
            
            # Store results in session state
            st.session_state['simulation_data'] = model.datacollector.get_model_vars_dataframe()
            # Skip agent data for now due to collection issues
            st.session_state['agent_data'] = None
            st.session_state['model_params'] = {
                'n_consumers': n_consumers,
                'n_commercial_banks': n_commercial_banks,
                'steps': steps,
                'cbdc_introduction_step': cbdc_introduction_step,
                'cbdc_adoption_rate': cbdc_adoption_rate,
                'cbdc_attractiveness': cbdc_attractiveness,
                'initial_consumer_wealth': initial_consumer_wealth,
                'bank_interest_rate': bank_interest_rate * 100,
                'cbdc_interest_rate': cbdc_interest_rate * 100
            }
        
        st.success("Simulation completed successfully!")
    
    # Display results if simulation has been run
    if 'simulation_data' in st.session_state:
        display_results()

def display_results():
    """Display simulation results with visualizations and analysis"""
    
    data = st.session_state['simulation_data']
    agent_data = st.session_state['agent_data']
    params = st.session_state['model_params']
    
    # Key metrics summary
    st.header("📊 Simulation Results Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        final_cbdc_adoption = data['CBDC_Adoption_Rate'].iloc[-1] * 100
        st.metric("Final CBDC Adoption", f"{final_cbdc_adoption:.1f}%")
    
    with col2:
        deposit_reduction = (1 - data['Total_Bank_Deposits'].iloc[-1] / data['Total_Bank_Deposits'].iloc[0]) * 100
        st.metric("Deposit Reduction", f"{deposit_reduction:.1f}%")
    
    with col3:
        final_cbdc_holdings = data['Total_CBDC_Holdings'].iloc[-1]
        st.metric("Total CBDC Holdings", f"${final_cbdc_holdings:,.0f}")
    
    with col4:
        avg_bank_liquidity = data['Average_Bank_Liquidity_Ratio'].iloc[-1]
        st.metric("Avg Bank Liquidity", f"{avg_bank_liquidity:.2f}")
    
    # CBDC Adoption Over Time
    st.header("📈 CBDC Adoption Over Time")
    
    fig_adoption = make_subplots(
        rows=2, cols=2,
        subplot_titles=('CBDC Adoption Rate', 'CBDC Holdings vs Bank Deposits', 
                       'Consumer Distribution', 'Banking Metrics'),
        specs=[[{"secondary_y": False}, {"secondary_y": True}],
               [{"type": "pie"}, {"secondary_y": False}]]
    )
    
    # CBDC Adoption Rate
    fig_adoption.add_trace(
        go.Scatter(x=data.index, y=data['CBDC_Adoption_Rate'] * 100,
                  name='CBDC Adoption Rate (%)', line=dict(color='blue', width=3)),
        row=1, col=1
    )
    
    # CBDC Holdings vs Bank Deposits
    fig_adoption.add_trace(
        go.Scatter(x=data.index, y=data['Total_CBDC_Holdings'],
                  name='CBDC Holdings', line=dict(color='green', width=2)),
        row=1, col=2
    )
    fig_adoption.add_trace(
        go.Scatter(x=data.index, y=data['Total_Bank_Deposits'],
                  name='Bank Deposits', line=dict(color='red', width=2)),
        row=1, col=2
    )
    
    # Consumer Distribution (final state)
    final_adopters = data['CBDC_Adopters'].iloc[-1]
    final_non_adopters = params['n_consumers'] - final_adopters
    
    fig_adoption.add_trace(
        go.Pie(labels=['CBDC Adopters', 'Non-Adopters'],
               values=[final_adopters, final_non_adopters],
               hole=0.4),
        row=2, col=1
    )
    
    # Banking Metrics
    fig_adoption.add_trace(
        go.Scatter(x=data.index, y=data['Average_Bank_Liquidity_Ratio'],
                  name='Avg Liquidity Ratio', line=dict(color='purple', width=2)),
        row=2, col=2
    )
    fig_adoption.add_trace(
        go.Scatter(x=data.index, y=data['Total_Bank_Loans'] / 1000,
                  name='Total Loans (K)', line=dict(color='orange', width=2)),
        row=2, col=2
    )
    
    fig_adoption.update_layout(height=800, showlegend=True, 
                              title_text="CBDC Impact Analysis Dashboard")
    
    # Add vertical line for CBDC introduction
    for i in range(1, 3):
        for j in range(1, 3):
            if not (i == 2 and j == 1):  # Skip pie chart
                fig_adoption.add_vline(x=params['cbdc_introduction_step'], 
                                     line_dash="dash", line_color="red",
                                     annotation_text="CBDC Introduced",
                                     row=i, col=j)
    
    st.plotly_chart(fig_adoption, use_container_width=True)
    
    # Detailed Time Series Analysis
    st.header("📊 Detailed Time Series Analysis")
    
    # Create tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["Substitution Effects", "Banking Impact", "Market Dynamics"])
    
    with tab1:
        st.subheader("CBDC Substitution Effects")
        
        # Calculate substitution metrics
        data['Deposit_Substitution_Rate'] = (data['Total_Bank_Deposits'].iloc[0] - data['Total_Bank_Deposits']) / data['Total_Bank_Deposits'].iloc[0] * 100
        data['CBDC_Growth_Rate'] = data['Total_CBDC_Holdings'].pct_change() * 100
        
        fig_sub = make_subplots(rows=2, cols=1, 
                               subplot_titles=('Deposit Substitution Over Time', 'CBDC Growth Rate'))
        
        fig_sub.add_trace(
            go.Scatter(x=data.index, y=data['Deposit_Substitution_Rate'],
                      name='Deposit Substitution Rate (%)', fill='tonexty'),
            row=1, col=1
        )
        
        fig_sub.add_trace(
            go.Scatter(x=data.index, y=data['CBDC_Growth_Rate'].rolling(5).mean(),
                      name='CBDC Growth Rate (5-period MA)', line=dict(color='green')),
            row=2, col=1
        )
        
        fig_sub.update_layout(height=600, title_text="CBDC Substitution Analysis")
        st.plotly_chart(fig_sub, use_container_width=True)
    
    with tab2:
        st.subheader("Commercial Banking Impact")
        
        fig_bank = make_subplots(rows=2, cols=2,
                                subplot_titles=('Bank Deposits vs Loans', 'Liquidity Ratios',
                                              'Interest Rate Spread', 'Bank Profitability'))
        
        # Bank Deposits vs Loans
        fig_bank.add_trace(
            go.Scatter(x=data.index, y=data['Total_Bank_Deposits'],
                      name='Deposits', line=dict(color='blue')),
            row=1, col=1
        )
        fig_bank.add_trace(
            go.Scatter(x=data.index, y=data['Total_Bank_Loans'],
                      name='Loans', line=dict(color='red')),
            row=1, col=1
        )
        
        # Liquidity Ratios
        fig_bank.add_trace(
            go.Scatter(x=data.index, y=data['Average_Bank_Liquidity_Ratio'],
                      name='Avg Liquidity Ratio', fill='tonexty'),
            row=1, col=2
        )
        
        # Interest Rate Spread (simplified calculation)
        lending_rate = params['bank_interest_rate'] + 2  # Assume 2% markup
        rate_spread = lending_rate - params['cbdc_interest_rate']
        fig_bank.add_hline(y=rate_spread, line_dash="dash", 
                          annotation_text=f"Rate Spread: {rate_spread:.1f}%",
                          row=2, col=1)
        
        # Bank Profitability Proxy (Loans - Deposits differential)
        data['Profitability_Proxy'] = (data['Total_Bank_Loans'] - data['Total_Bank_Deposits']) / data['Total_Bank_Deposits'].iloc[0] * 100
        fig_bank.add_trace(
            go.Scatter(x=data.index, y=data['Profitability_Proxy'],
                      name='Profitability Proxy', line=dict(color='green')),
            row=2, col=2
        )
        
        fig_bank.update_layout(height=600, title_text="Commercial Banking Impact Analysis")
        st.plotly_chart(fig_bank, use_container_width=True)
    
    with tab3:
        st.subheader("Market Dynamics")
        
        # Calculate market concentration and dynamics
        data['Market_Concentration'] = data['Total_Bank_Deposits'] / (data['Total_Bank_Deposits'] + data['Total_CBDC_Holdings'])
        data['CBDC_Market_Share'] = data['Total_CBDC_Holdings'] / (data['Total_Bank_Deposits'] + data['Total_CBDC_Holdings'])
        
        fig_market = px.area(data.reset_index(), x='Step', 
                           y=['Market_Concentration', 'CBDC_Market_Share'],
                           title='Market Share Evolution: Traditional Banking vs CBDC')
        
        st.plotly_chart(fig_market, use_container_width=True)
        
        # Consumer behavior analysis
        if agent_data is not None and len(agent_data) > 0:
            consumer_data = agent_data[agent_data['AgentID'].str.startswith('Consumer')]
            if len(consumer_data) > 0:
                final_step_data = consumer_data[consumer_data['Step'] == consumer_data['Step'].max()]
                
                fig_consumer = px.histogram(final_step_data, x='Wealth', 
                                          color='CBDC_Adopter', nbins=20,
                                          title='Consumer Wealth Distribution by CBDC Adoption Status')
                st.plotly_chart(fig_consumer, use_container_width=True)
        else:
            st.info("Agent-level data analysis is currently unavailable. The model-level metrics above show the key CBDC substitution effects.")
    
    # Data Export Section
    st.header("💾 Data Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Download Model Data as CSV"):
            csv_buffer = io.StringIO()
            data.to_csv(csv_buffer, index=True)
            csv_string = csv_buffer.getvalue()
            
            st.download_button(
                label="📥 Download Model Data CSV",
                data=csv_string,
                file_name=f"cbdc_simulation_model_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if agent_data is not None and len(agent_data) > 0 and st.button("Download Agent Data as CSV"):
            csv_buffer = io.StringIO()
            agent_data.to_csv(csv_buffer, index=True)
            csv_string = csv_buffer.getvalue()
            
            st.download_button(
                label="📥 Download Agent Data CSV",
                data=csv_string,
                file_name=f"cbdc_simulation_agent_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Agent data download currently unavailable")
    
    # Parameter Summary
    with st.expander("📋 Simulation Parameters Used"):
        param_df = pd.DataFrame([params]).T
        param_df.columns = ['Value']
        st.dataframe(param_df)

if __name__ == "__main__":
    main()
