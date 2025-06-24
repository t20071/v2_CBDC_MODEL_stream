# CBDC Banking Simulation

## Overview

This is an agent-based simulation built with Python that models the impact of Central Bank Digital Currency (CBDC) on commercial banking intermediation. The application uses the Mesa framework for agent-based modeling and Streamlit for the web interface, providing an interactive platform to explore how CBDC introduction affects traditional banking operations.

## System Architecture

The application follows a Model-View architecture pattern:
- **Model Layer**: Mesa-based agent simulation with three agent types (Central Bank, Commercial Banks, Consumers)
- **View Layer**: Streamlit web interface for parameter configuration and visualization
- **Data Layer**: In-memory data structures with NumPy and Pandas for analysis

### Core Technologies
- **Mesa**: Agent-based modeling framework
- **Streamlit**: Web application framework
- **NetworkX**: Graph-based agent interactions
- **Plotly**: Interactive data visualization
- **NumPy/Pandas**: Numerical computing and data analysis

## Key Components

### Agent Classes
1. **CentralBank** (`agent/central_bank.py`): Manages CBDC introduction, monetary policy, and system monitoring
2. **CommercialBank** (`agent/commercial_bank.py`): Handles deposits, loans, and competitive responses to CBDC
3. **Consumer** (`agent/consumer.py`): Makes financial decisions between traditional banking and CBDC

### Model Framework
- **CBDCBankingModel** (`model.py`): Main simulation engine that orchestrates agent interactions
- Uses Mesa's RandomActivation scheduler for agent execution
- NetworkGrid topology for agent relationships based on Erdős-Rényi random graphs

### Web Interface
- **Streamlit App** (`app.py`): Interactive parameter configuration and visualization dashboard
- Real-time simulation controls with parameter sliders
- Plotly-based charts for results visualization

## Data Flow

1. **Initialization**: Create agents with specified parameters and network topology
2. **Simulation Steps**: 
   - Agents execute their step() methods in random order
   - Central bank monitors system and may introduce CBDC
   - Commercial banks adjust strategies and process transactions
   - Consumers make portfolio allocation decisions
3. **Data Collection**: Mesa's DataCollector gathers metrics at each step
4. **Visualization**: Streamlit displays results through Plotly charts

## External Dependencies

### Core Simulation Framework
- **Mesa (>=3.2.0)**: Agent-based modeling platform providing the foundation for multi-agent simulations
- **NetworkX (>=3.5)**: Graph library for modeling agent interaction networks

### Data Processing & Analysis
- **NumPy (>=2.3.0)**: Numerical computing for agent calculations and random processes
- **Pandas (>=2.3.0)**: Data manipulation and analysis for simulation results

### Web Interface & Visualization
- **Streamlit (>=1.45.1)**: Web framework for the interactive simulation dashboard
- **Plotly (>=6.1.2)**: Interactive visualization library for charts and graphs

### Additional Dependencies (auto-resolved)
- **Altair**: Alternative visualization backend
- **NetworkX**: Graph algorithms for agent networks
- **Jinja2, Blinker**: Streamlit web framework dependencies

## Deployment Strategy

### Replit Configuration
- **Runtime**: Python 3.11 with Nix package manager
- **Deployment Target**: Autoscale deployment for web serving
- **Port Configuration**: Streamlit server on port 5000
- **Module Management**: UV package manager for dependency resolution

### Workflow Setup
- **Development**: Parallel workflow execution with automatic dependency installation
- **Production**: Streamlit web server with headless configuration
- **Dependencies**: Automatic installation of Mesa and Plotly via UV package manager

### Configuration Files
- `.replit`: Main Replit configuration with deployment and workflow settings
- `.streamlit/config.toml`: Streamlit server configuration for headless operation
- `pyproject.toml`: Python package configuration with dependency specifications

## Model Documentation

- **model_assumptions.md**: Comprehensive documentation of all model assumptions, agent behaviors, and academic references
- **initial_conditions.md**: Detailed documentation of all initial conditions, parameter values, and empirical sources
- **Agent Flow Chart**: Interactive visualization of agent interactions available in the simulation interface

## Changelog

```
Changelog:
- June 15, 2025. Initial setup
- June 15, 2025. Enhanced CBDC substitution analysis with dynamic time-series visualizations
- June 15, 2025. Fixed Mesa 3.2.0 compatibility issues and agent initialization
- June 15, 2025. Improved deposit substitution tracking and market share calculations
- June 15, 2025. Implemented network centrality analysis for 6 CBDC hypotheses testing
- June 15, 2025. Added bank size differentiation (large vs small/medium) and systemic risk metrics
- June 15, 2025. Created dedicated visualization tabs for H1, H3, H4, H6 hypothesis testing
- June 16, 2025. Implemented 37% initial bank deposit baseline for consumer wealth allocation
- June 16, 2025. Converted all monetary displays to percentage-based wealth allocation tracking
- June 16, 2025. Fixed LSP type annotation errors throughout agent classes for proper model access
- June 16, 2025. Enhanced transfer mechanics to draw from both bank deposits and other assets
- June 24, 2025. Created interactive agent flow chart visualization
- June 24, 2025. Added comprehensive VS Code setup with requirements.txt and configuration files
- June 24, 2025. Documented all model assumptions with academic references
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```