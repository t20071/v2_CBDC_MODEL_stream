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
        initial_deposits = data['Total_Bank_Deposits'].iloc[0]
        final_deposits = data['Total_Bank_Deposits'].iloc[-1]
        if initial_deposits > 0:
            deposit_change = ((final_deposits - initial_deposits) / initial_deposits) * 100
            if deposit_change >= 0:
                st.metric("Deposit Growth", f"+{deposit_change:.1f}%")
            else:
                st.metric("Deposit Reduction", f"{deposit_change:.1f}%")
        else:
            st.metric("Deposit Change", "N/A")
    
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
    
    # Note: CBDC introduction step marked in chart titles
    
    st.plotly_chart(fig_adoption, use_container_width=True)
    
    # Wealth Allocation Dashboard
    st.header("💰 Consumer Wealth Allocation (37% Initial Bank Deposit Baseline)")
    
    # Calculate wealth allocation percentages
    total_consumer_wealth = params['n_consumers'] * params['initial_consumer_wealth']
    
    # Current allocations as percentages of total wealth
    current_bank_pct = (data['Total_Bank_Deposits'] / total_consumer_wealth * 100).fillna(0)
    current_cbdc_pct = (data['Total_CBDC_Holdings'] / total_consumer_wealth * 100).fillna(0)
    current_other_pct = 100 - current_bank_pct - current_cbdc_pct  # Other assets
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Initial Bank Deposits", "37.0%", delta=None)
    
    with col2:
        final_bank_pct = current_bank_pct.iloc[-1]
        bank_change = final_bank_pct - 37.0
        st.metric("Final Bank Deposits", f"{final_bank_pct:.1f}%", delta=f"{bank_change:.1f}%")
    
    with col3:
        final_cbdc_pct = current_cbdc_pct.iloc[-1]
        st.metric("CBDC Holdings", f"{final_cbdc_pct:.1f}%", delta=f"+{final_cbdc_pct:.1f}%")
    
    with col4:
        deposit_shift = 37.0 - final_bank_pct
        st.metric("Deposit Shift to CBDC", f"{deposit_shift:.1f}%", delta=f"-{deposit_shift:.1f}%")
    
    # Wealth allocation over time
    fig_wealth = go.Figure()
    
    fig_wealth.add_trace(go.Scatter(
        x=data.index, y=current_bank_pct,
        name='Bank Deposits %', fill='tonexty',
        line=dict(color='blue', width=2)
    ))
    
    fig_wealth.add_trace(go.Scatter(
        x=data.index, y=current_cbdc_pct,
        name='CBDC Holdings %', fill='tonexty',
        line=dict(color='gold', width=2)
    ))
    
    fig_wealth.add_trace(go.Scatter(
        x=data.index, y=current_other_pct,
        name='Other Assets %', fill='tonexty',
        line=dict(color='gray', width=1)
    ))
    
    # Add CBDC introduction line
    fig_wealth.add_vline(x=params['cbdc_introduction_step'], 
                        line_dash="dash", line_color="red",
                        annotation_text="CBDC Launch")
    
    fig_wealth.update_layout(
        title="Consumer Wealth Allocation Over Time (% of Total Wealth)",
        xaxis_title="Simulation Step",
        yaxis_title="Percentage of Total Consumer Wealth",
        yaxis=dict(range=[0, 100]),
        height=500
    )
    
    st.plotly_chart(fig_wealth, use_container_width=True)
    
    # Detailed Time Series Analysis
    st.header("📊 Detailed Time Series Analysis")
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "CBDC Substitution", 
        "H1: Network Centrality", 
        "H3: Liquidity Stress", 
        "H4: Network Connectivity", 
        "H6: Central Bank Dominance",
        "Transaction Analysis",
        "Agent Flow Chart"
    ])
    
    with tab1:
        st.subheader("CBDC Substitution Effects")
        
        # Calculate substitution metrics with proper baseline
        # CBDC substitution should be zero before introduction
        cbdc_intro_step = params['cbdc_introduction_step']
        
        # Initialize substitution rate to zero
        data['Deposit_Substitution_Rate'] = 0.0
        
        # Find pre-CBDC baseline (deposits just before CBDC introduction)
        pre_cbdc_data = data[data.index < cbdc_intro_step]
        post_cbdc_data = data[data.index >= cbdc_intro_step]
        
        if len(pre_cbdc_data) > 0 and len(post_cbdc_data) > 0:
            # Use average of last few steps before CBDC as baseline
            baseline_steps = min(5, len(pre_cbdc_data))
            baseline_deposits = pre_cbdc_data['Total_Bank_Deposits'].tail(baseline_steps).mean()
            
            # Calculate substitution only for post-CBDC period
            if baseline_deposits > 0:
                post_cbdc_substitution = (baseline_deposits - post_cbdc_data['Total_Bank_Deposits']) / baseline_deposits * 100
                data.loc[post_cbdc_data.index, 'Deposit_Substitution_Rate'] = post_cbdc_substitution
        
        # Calculate CBDC metrics - should be zero before introduction
        data['CBDC_Growth_Rate'] = 0.0
        data['Cumulative_CBDC_Share'] = 0.0
        
        # Calculate CBDC growth rate only for post-introduction period
        if len(post_cbdc_data) > 0:
            cbdc_growth = post_cbdc_data['Total_CBDC_Holdings'].pct_change().fillna(0) * 100
            data.loc[post_cbdc_data.index, 'CBDC_Growth_Rate'] = cbdc_growth
            
            # Calculate market share only where CBDC exists
            total_financial_assets = post_cbdc_data['Total_CBDC_Holdings'] + post_cbdc_data['Total_Bank_Deposits']
            cbdc_share = post_cbdc_data['Total_CBDC_Holdings'] / total_financial_assets * 100
            data.loc[post_cbdc_data.index, 'Cumulative_CBDC_Share'] = cbdc_share.fillna(0)
        
        fig_sub = make_subplots(rows=3, cols=1, 
                               subplot_titles=('Deposit Substitution from 37% Baseline (%)', 
                                             'CBDC Market Share Growth (%)',
                                             'Wealth Allocation: CBDC vs Bank Deposits (%)')) 
        
        # Deposit substitution rate over time
        fig_sub.add_trace(
            go.Scatter(x=data.index, y=data['Deposit_Substitution_Rate'],
                      name='Deposit Substitution Rate (%)', 
                      line=dict(color='red', width=3),
                      fill='tonexty'),
            row=1, col=1
        )
        
        # CBDC market share over time
        fig_sub.add_trace(
            go.Scatter(x=data.index, y=data['Cumulative_CBDC_Share'],
                      name='CBDC Market Share (%)', 
                      line=dict(color='blue', width=3)),
            row=2, col=1
        )
        
        # Percentage allocation comparison
        fig_sub.add_trace(
            go.Scatter(x=data.index, y=current_bank_pct,
                      name='Bank Deposits % of Total Wealth', line=dict(color='orange')),
            row=3, col=1
        )
        fig_sub.add_trace(
            go.Scatter(x=data.index, y=current_cbdc_pct,
                      name='CBDC Holdings % of Total Wealth', line=dict(color='green')),
            row=3, col=1
        )
        
        # Add 37% baseline reference line to third subplot
        baseline_trace = go.Scatter(
            x=data.index, 
            y=[37.0] * len(data.index),
            mode='lines',
            line=dict(dash='dash', color='blue', width=2),
            name='37% Initial Baseline',
            showlegend=True
        )
        fig_sub.add_trace(baseline_trace, row=3, col=1)
        
        # Add CBDC introduction line to all subplots
        for i in range(1, 4):
            fig_sub.add_vline(x=cbdc_intro_step, 
                            line_dash="dash", line_color="red", opacity=0.7,
                            annotation_text="CBDC Launch" if i == 1 else "",
                            row=i, col=1)
        
        fig_sub.update_layout(height=800, title_text="CBDC Substitution Analysis Over Time")
        st.plotly_chart(fig_sub, use_container_width=True)
        
        # Key insights
        col1, col2, col3 = st.columns(3)
        with col1:
            max_substitution = data['Deposit_Substitution_Rate'].max()
            st.metric("Peak Substitution Rate", f"{max_substitution:.1f}%")
        with col2:
            final_cbdc_share = data['Cumulative_CBDC_Share'].iloc[-1]
            st.metric("Final CBDC Market Share", f"{final_cbdc_share:.1f}%")
        with col3:
            cbdc_introduction = params['cbdc_introduction_step']
            st.metric("CBDC Introduction Step", cbdc_introduction)
    
    with tab2:
        st.subheader("H1: Network Centrality Analysis")
        st.write("Testing hypothesis: CBDC reduces centrality of commercial banks, especially small banks")
        
        # Network centrality comparison
        fig_centrality = make_subplots(rows=2, cols=1,
                                     subplot_titles=('Bank Centrality Over Time', 
                                                   'Large vs Small Bank Centrality'))
        
        # Overall bank centrality trend
        fig_centrality.add_trace(
            go.Scatter(x=data.index, y=data['Average_Bank_Centrality'],
                      name='Average Bank Centrality', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Centrality comparison by bank size
        fig_centrality.add_trace(
            go.Scatter(x=data.index, y=data['Large_Bank_Centrality'],
                      name='Large Banks', line=dict(color='green')),
            row=2, col=1
        )
        fig_centrality.add_trace(
            go.Scatter(x=data.index, y=data['Small_Bank_Centrality'],
                      name='Small/Medium Banks', line=dict(color='red')),
            row=2, col=1
        )
        
        fig_centrality.update_layout(height=600, title_text="Network Centrality Impact Analysis")
        st.plotly_chart(fig_centrality, use_container_width=True)
        
        # H1 Analysis metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            initial_avg_centrality = data['Average_Bank_Centrality'].iloc[0]
            final_avg_centrality = data['Average_Bank_Centrality'].iloc[-1]
            centrality_decline = ((initial_avg_centrality - final_avg_centrality) / initial_avg_centrality) * 100
            st.metric("Overall Centrality Decline", f"{centrality_decline:.1f}%")
        with col2:
            small_bank_decline = ((data['Small_Bank_Centrality'].iloc[0] - data['Small_Bank_Centrality'].iloc[-1]) / data['Small_Bank_Centrality'].iloc[0]) * 100
            st.metric("Small Bank Centrality Loss", f"{small_bank_decline:.1f}%")
        with col3:
            large_bank_decline = ((data['Large_Bank_Centrality'].iloc[0] - data['Large_Bank_Centrality'].iloc[-1]) / data['Large_Bank_Centrality'].iloc[0]) * 100
            st.metric("Large Bank Centrality Loss", f"{large_bank_decline:.1f}%")
    
    with tab3:
        st.subheader("H3: Systemic Liquidity Risk Analysis")
        st.write("Testing hypothesis: CBDC increases liquidity risk during rapid adoption")
        
        # Liquidity stress analysis
        fig_stress = make_subplots(rows=2, cols=1,
                                 subplot_titles=('Liquidity Stress Over Time',
                                               'CBDC Adoption vs Liquidity Stress'))
        
        # Liquidity stress trend
        fig_stress.add_trace(
            go.Scatter(x=data.index, y=data['Average_Liquidity_Stress'],
                      name='Average Liquidity Stress', 
                      line=dict(color='red', width=3),
                      fill='tonexty'),
            row=1, col=1
        )
        
        # Correlation with CBDC adoption
        fig_stress.add_trace(
            go.Scatter(x=data['CBDC_Adoption_Rate'], y=data['Average_Liquidity_Stress'],
                      mode='markers',
                      name='Stress vs CBDC Adoption',
                      marker=dict(color='orange', size=8)),
            row=2, col=1
        )
        
        fig_stress.update_layout(height=600, title_text="Systemic Liquidity Risk Analysis")
        st.plotly_chart(fig_stress, use_container_width=True)
        
        # H3 Risk metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            max_stress = data['Average_Liquidity_Stress'].max()
            st.metric("Peak Liquidity Stress", f"{max_stress:.2f}")
        with col2:
            stress_at_30_adoption = data[data['CBDC_Adoption_Rate'] >= 0.3]['Average_Liquidity_Stress'].mean() if len(data[data['CBDC_Adoption_Rate'] >= 0.3]) > 0 else 0
            st.metric("Stress at 30% CBDC Adoption", f"{stress_at_30_adoption:.2f}")
        with col3:
            crisis_threshold = 0.7  # Define crisis threshold
            crisis_periods = len(data[data['Average_Liquidity_Stress'] > crisis_threshold])
            st.metric("High Stress Periods", crisis_periods)
    
    with tab4:
        st.subheader("H4: Banking Network Connectivity")
        st.write("Testing hypothesis: CBDC weakens interbank network connections")
        
        # Network density analysis
        fig_network = go.Figure()
        
        fig_network.add_trace(
            go.Scatter(x=data.index, y=data['Banking_Network_Density'],
                      name='Network Density',
                      line=dict(color='purple', width=3),
                      fill='tonexty')
        )
        
        fig_network.update_layout(
            title="Banking Network Density Over Time",
            xaxis_title="Simulation Step",
            yaxis_title="Network Density",
            height=400
        )
        st.plotly_chart(fig_network, use_container_width=True)
        
        # H4 Network metrics
        col1, col2 = st.columns(2)
        with col1:
            initial_density = data['Banking_Network_Density'].iloc[0]
            final_density = data['Banking_Network_Density'].iloc[-1]
            density_decline = ((initial_density - final_density) / initial_density) * 100 if initial_density > 0 else 0
            st.metric("Network Density Decline", f"{density_decline:.1f}%")
        with col2:
            avg_density_post_cbdc = data[data.index >= params['cbdc_introduction_step']]['Banking_Network_Density'].mean()
            st.metric("Avg Density Post-CBDC", f"{avg_density_post_cbdc:.3f}")
    
    with tab6:
        st.subheader("Consumer-to-Consumer Transaction Analysis")
        st.write("Analysis of payment method usage before and after CBDC introduction")
        
        # Get transaction analysis
        transaction_analysis = st.session_state.model.get_transaction_analysis()
        
        if transaction_analysis:
            pre_period = transaction_analysis.get('pre_cbdc_period', {})
            post_period = transaction_analysis.get('post_cbdc_period', {})
            substitution = transaction_analysis.get('substitution_analysis', {})
            
            # Transaction volume comparison
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Pre-CBDC Period")
                if pre_period.get('total_volume', 0) > 0:
                    pre_bank_pct = pre_period.get('bank_volume', 0) / pre_period.get('total_volume', 1) * 100
                    pre_other_pct = pre_period.get('other_volume', 0) / pre_period.get('total_volume', 1) * 100
                    
                    st.metric("Total Transaction Volume", f"${pre_period.get('total_volume', 0):,.0f}")
                    st.metric("Bank Transactions", f"{pre_bank_pct:.1f}%")
                    st.metric("CBDC Transactions", "0.0%")
                    st.metric("Other Payment Methods", f"{pre_other_pct:.1f}%")
                else:
                    st.info("Run simulation to see pre-CBDC transaction data")
            
            with col2:
                st.subheader("Post-CBDC Period")
                if post_period.get('total_volume', 0) > 0:
                    post_bank_pct = post_period.get('bank_volume', 0) / post_period.get('total_volume', 1) * 100
                    post_cbdc_pct = post_period.get('cbdc_volume', 0) / post_period.get('total_volume', 1) * 100
                    post_other_pct = post_period.get('other_volume', 0) / post_period.get('total_volume', 1) * 100
                    
                    st.metric("Total Transaction Volume", f"${post_period.get('total_volume', 0):,.0f}")
                    st.metric("Bank Transactions", f"{post_bank_pct:.1f}%", f"{post_bank_pct - 100:.1f}%")
                    st.metric("CBDC Transactions", f"{post_cbdc_pct:.1f}%", f"+{post_cbdc_pct:.1f}%")
                    st.metric("Other Payment Methods", f"{post_other_pct:.1f}%")
                else:
                    st.info("CBDC not yet introduced or insufficient post-CBDC data")
            
            # Transaction volume over time
            if len(data) > 0 and 'Bank_Transaction_Volume' in data.columns:
                st.subheader("Transaction Volume Trends")
                
                fig_transactions = go.Figure()
                
                # Add transaction volume traces
                fig_transactions.add_trace(
                    go.Scatter(x=data.index, y=data['Bank_Transaction_Volume'],
                              name='Bank Transactions', 
                              fill='tonexty',
                              line=dict(color='blue'))
                )
                
                fig_transactions.add_trace(
                    go.Scatter(x=data.index, y=data['CBDC_Transaction_Volume'],
                              name='CBDC Transactions',
                              fill='tonexty', 
                              line=dict(color='green'))
                )
                
                fig_transactions.add_trace(
                    go.Scatter(x=data.index, y=data['Other_Transaction_Volume'],
                              name='Other Transactions',
                              fill='tonexty',
                              line=dict(color='orange'))
                )
                
                # Add CBDC introduction line
                cbdc_intro_step = transaction_analysis.get('cbdc_introduction_step', 30)
                fig_transactions.add_vline(x=cbdc_intro_step, line_dash="dash", line_color="red",
                                         annotation_text="CBDC Launch")
                
                fig_transactions.update_layout(
                    title="Transaction Volume by Payment Method",
                    xaxis_title="Simulation Step",
                    yaxis_title="Transaction Volume ($)",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_transactions, use_container_width=True)
                
                # CBDC transaction share over time
                fig_share = go.Figure()
                fig_share.add_trace(
                    go.Scatter(x=data.index, y=data['CBDC_Transaction_Share'],
                              name='CBDC Transaction Share',
                              line=dict(color='green', width=3),
                              fill='tonexty')
                )
                
                fig_share.add_vline(x=cbdc_intro_step, line_dash="dash", line_color="red",
                                   annotation_text="CBDC Launch")
                
                fig_share.update_layout(
                    title="CBDC Market Share in Transactions",
                    xaxis_title="Simulation Step",
                    yaxis_title="CBDC Share (%)",
                    yaxis=dict(range=[0, 100])
                )
                
                st.plotly_chart(fig_share, use_container_width=True)
            
            # Substitution analysis
            if substitution:
                st.subheader("Payment Method Substitution Analysis")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Pre-CBDC Bank Share", 
                             f"{substitution.get('pre_cbdc_bank_share', 0):.1f}%")
                with col2:
                    st.metric("Post-CBDC Bank Share", 
                             f"{substitution.get('post_cbdc_bank_share', 0):.1f}%",
                             f"{substitution.get('post_cbdc_bank_share', 0) - substitution.get('pre_cbdc_bank_share', 0):.1f}%")
                with col3:
                    st.metric("Transaction Substitution Rate", 
                             f"{substitution.get('transaction_substitution_rate', 0):.1f}%")
                
                # Create substitution visualization
                labels = ['Bank (Post-CBDC)', 'CBDC (Post-CBDC)', 'Other (Post-CBDC)']
                values = [
                    substitution.get('post_cbdc_bank_share', 0),
                    substitution.get('post_cbdc_cbdc_share', 0),
                    100 - substitution.get('post_cbdc_bank_share', 0) - substitution.get('post_cbdc_cbdc_share', 0)
                ]
                colors = ['lightblue', 'lightgreen', 'lightorange']
                
                fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
                fig_pie.update_traces(marker=dict(colors=colors))
                fig_pie.update_layout(title="Payment Method Distribution (Post-CBDC)")
                
                st.plotly_chart(fig_pie, use_container_width=True)
        
        else:
            st.info("Run the simulation to see transaction analysis")
        
        # CBDC Exchange Mechanism
        st.subheader("CBDC Exchange Mechanism (1:1 Ratio)")
        
        if hasattr(st.session_state.model.central_bank, 'central_bank_deposits'):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("CBDC Outstanding", 
                         f"${st.session_state.model.central_bank.cbdc_outstanding:,.0f}")
            with col2:
                st.metric("Central Bank Deposits", 
                         f"${st.session_state.model.central_bank.central_bank_deposits:,.0f}")
            with col3:
                exchange_balance = st.session_state.model.central_bank.cbdc_outstanding - st.session_state.model.central_bank.central_bank_deposits
                st.metric("Exchange Balance", 
                         f"${exchange_balance:,.0f}",
                         "✓ Balanced" if abs(exchange_balance) < 1 else "⚠ Imbalanced")
            
            st.info("💡 The 1:1 exchange mechanism ensures no new money is created. CBDC is issued only when commercial banks transfer equivalent deposits to the central bank.")
        
        # Bank outflow tracking
        st.subheader("Commercial Bank CBDC Outflows")
        
        bank_outflow_data = []
        for bank in st.session_state.model.commercial_banks:
            if hasattr(bank, 'cbdc_related_outflows'):
                bank_outflow_data.append({
                    'Bank ID': f"Bank {bank.unique_id}",
                    'Bank Type': bank.bank_type,
                    'CBDC Outflows': bank.cbdc_related_outflows,
                    'Total Deposits': bank.total_deposits,
                    'Outflow Rate': (bank.cbdc_related_outflows / max(bank.total_deposits + bank.cbdc_related_outflows, 1)) * 100
                })
        
        if bank_outflow_data:
            import pandas as pd
            df_outflows = pd.DataFrame(bank_outflow_data)
            st.dataframe(df_outflows, use_container_width=True)
        else:
            st.info("No CBDC-related outflows recorded yet")

    with tab7:
        st.subheader("H6: Central Bank Network Dominance")
        st.write("Testing hypothesis: Central bank becomes dominant network node with CBDC")
        
        # Central bank vs commercial bank centrality
        fig_dominance = go.Figure()
        
        fig_dominance.add_trace(
            go.Scatter(x=data.index, y=data['Central_Bank_Centrality'],
                      name='Central Bank Centrality',
                      line=dict(color='gold', width=4))
        )
        
        fig_dominance.add_trace(
            go.Scatter(x=data.index, y=data['Average_Bank_Centrality'],
                      name='Average Commercial Bank Centrality',
                      line=dict(color='blue', width=2))
        )
        
        fig_dominance.update_layout(
            title="Central Bank vs Commercial Bank Network Centrality",
            xaxis_title="Simulation Step",
            yaxis_title="Network Centrality",
            height=400
        )
        st.plotly_chart(fig_dominance, use_container_width=True)
        
        # H6 Dominance metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            final_cb_centrality = data['Central_Bank_Centrality'].iloc[-1]
            st.metric("Final Central Bank Centrality", f"{final_cb_centrality:.2f}")
        with col2:
            final_avg_bank_centrality = data['Average_Bank_Centrality'].iloc[-1]
            st.metric("Final Avg Bank Centrality", f"{final_avg_bank_centrality:.2f}")
        with col3:
            dominance_ratio = final_cb_centrality / final_avg_bank_centrality if final_avg_bank_centrality > 0 else 0
            st.metric("CB Dominance Ratio", f"{dominance_ratio:.1f}x")
    
    with tab6:
        st.subheader("Agent Interaction Flow Chart")
        st.markdown("""
        This interactive flow chart shows how the three types of agents interact in the CBDC banking simulation:
        - **Central Bank** (Gold Diamond): Issues CBDC and manages monetary policy
        - **Commercial Banks** (Blue Square): Provide traditional banking services and compete with CBDC
        - **Consumers** (Green Circle): Make financial decisions between bank deposits and CBDC
        """)
        
        # Create agent interaction flowchart
        fig_flow = go.Figure()
        
        # Define positions for agents
        central_bank_pos = (0.5, 0.9)
        commercial_banks_pos = (0.2, 0.4)
        consumers_pos = (0.8, 0.4)
        
        # Add agent nodes
        fig_flow.add_trace(go.Scatter(
            x=[central_bank_pos[0]], y=[central_bank_pos[1]],
            mode='markers+text',
            marker=dict(size=80, color='gold', symbol='diamond'),
            text=['Central Bank'],
            textposition="middle center",
            textfont=dict(size=12, color='black'),
            name='Central Bank',
            hovertemplate='<b>Central Bank</b><br>' +
                         '• Issues CBDC<br>' +
                         '• Sets monetary policy<br>' +
                         '• Monitors systemic risk<br>' +
                         '• Promotes CBDC adoption<extra></extra>'
        ))
        
        fig_flow.add_trace(go.Scatter(
            x=[commercial_banks_pos[0]], y=[commercial_banks_pos[1]],
            mode='markers+text',
            marker=dict(size=80, color='lightblue', symbol='square'),
            text=['Commercial<br>Banks'],
            textposition="middle center",
            textfont=dict(size=12, color='black'),
            name='Commercial Banks',
            hovertemplate='<b>Commercial Banks</b><br>' +
                         '• Accept deposits<br>' +
                         '• Provide loans<br>' +
                         '• Compete with CBDC<br>' +
                         '• Adjust interest rates<extra></extra>'
        ))
        
        fig_flow.add_trace(go.Scatter(
            x=[consumers_pos[0]], y=[consumers_pos[1]],
            mode='markers+text',
            marker=dict(size=80, color='lightgreen', symbol='circle'),
            text=['Consumers'],
            textposition="middle center",
            textfont=dict(size=12, color='black'),
            name='Consumers',
            hovertemplate='<b>Consumers</b><br>' +
                         '• Make financial decisions<br>' +
                         '• Choose between bank deposits and CBDC<br>' +
                         '• Respond to interest rates<br>' +
                         '• Influenced by peers<extra></extra>'
        ))
        
        # Add interaction arrows
        interactions = [
            # Central Bank to Commercial Banks
            {
                'start': central_bank_pos,
                'end': commercial_banks_pos,
                'label': 'CBDC Competition\nMonetary Policy\nSystemic Risk Monitoring',
                'color': 'red'
            },
            # Central Bank to Consumers
            {
                'start': central_bank_pos,
                'end': consumers_pos,
                'label': 'CBDC Issuance\nCBDC Interest Rates\nAdoption Incentives',
                'color': 'orange'
            },
            # Commercial Banks to Consumers
            {
                'start': commercial_banks_pos,
                'end': consumers_pos,
                'label': 'Deposit Services\nLoan Products\nCompetitive Rates',
                'color': 'blue'
            },
            # Consumer feedback to Commercial Banks
            {
                'start': consumers_pos,
                'end': commercial_banks_pos,
                'label': 'Deposit Flows\nCustomer Attrition\nDemand for Services',
                'color': 'green'
            },
            # Consumer feedback to Central Bank
            {
                'start': consumers_pos,
                'end': central_bank_pos,
                'label': 'CBDC Adoption\nMarket Response\nUsage Patterns',
                'color': 'purple'
            }
        ]
        
        # Add arrows for interactions
        for i, interaction in enumerate(interactions):
            start_x, start_y = interaction['start']
            end_x, end_y = interaction['end']
            
            # Offset arrows slightly to avoid overlap
            offset = 0.03 * (i % 2 * 2 - 1)  # Alternate between -0.03 and 0.03
            
            fig_flow.add_annotation(
                x=end_x,
                y=end_y,
                ax=start_x + offset,
                ay=start_y + offset,
                xref="x", yref="y",
                axref="x", ayref="y",
                arrowhead=2,
                arrowsize=1.5,
                arrowwidth=3,
                arrowcolor=interaction['color'],
                showarrow=True
            )
            
            # Add label at midpoint
            mid_x = (start_x + end_x) / 2 + offset
            mid_y = (start_y + end_y) / 2 + offset
            
            fig_flow.add_annotation(
                x=mid_x,
                y=mid_y,
                text=interaction['label'],
                showarrow=False,
                font=dict(size=9, color=interaction['color']),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor=interaction['color'],
                borderwidth=1
            )
        
        # Update layout
        fig_flow.update_layout(
            title={
                'text': "Agent Interaction Overview",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18}
            },
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
            showlegend=False,
            height=600,
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig_flow, use_container_width=True)
        
        # Key interactions summary
        st.subheader("Key Interactions Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Central Bank Actions:**
            - Issues CBDC currency to consumers
            - Sets CBDC interest rates for competition
            - Creates monetary policy affecting banks
            - Monitors systemic risk in banking system
            - Promotes CBDC adoption through incentives
            """)
            
            st.markdown("""
            **Commercial Bank Actions:**
            - Accept consumer deposits
            - Provide loan products and services
            - Adjust interest rates to compete with CBDC
            - Maintain customer relationships
            - Respond to deposit outflows
            """)
        
        with col2:
            st.markdown("""
            **Consumer Actions:**
            - Make portfolio allocation decisions
            - Choose between bank deposits and CBDC
            - Respond to interest rate differentials
            - Influenced by peer adoption patterns
            - Provide feedback through usage patterns
            """)
            
            st.markdown("""
            **Feedback Mechanisms:**
            - Deposit flows signal consumer preferences
            - CBDC adoption rates guide central bank policy
            - Banking system stress triggers support measures
            - Market dynamics drive competitive responses
            """)
    
    # Previous Banking Impact tab content (now hidden, but keeping structure)
    with st.expander("Commercial Banking Details"):
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
        
        # Interest Rate Spread (simplified visualization)
        lending_rate = params['bank_interest_rate'] + 2  # Assume 2% markup
        rate_spread = lending_rate - params['cbdc_interest_rate']
        # Show rate spread as a constant line
        spread_line = [rate_spread] * len(data)
        fig_bank.add_trace(
            go.Scatter(x=data.index, y=spread_line,
                      name=f'Rate Spread ({rate_spread:.1f}%)', line=dict(color='purple', dash='dash')),
            row=2, col=1
        )
        
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
