# Running CBDC Banking Simulation in VS Code

This guide will help you set up and run the CBDC Banking Simulation in VS Code on your local machine.

## Quick Start

Run the setup script to create all necessary files:
```bash
python setup_vscode.py
```

Then follow the instructions printed by the script.

## Prerequisites

- Python 3.11 or higher
- VS Code with Python extension
- Git (optional, if cloning from repository)

## Setup Instructions

### 1. Download/Clone the Project

If you have the project files, ensure you have these key files in your project folder:
```
cbdc-simulation/
├── app.py
├── model.py
├── requirements.txt
├── agent/
│   ├── __init__.py
│   ├── central_bank.py
│   ├── commercial_bank.py
│   └── consumer.py
└── .streamlit/
    └── config.toml
```

### 2. Create Virtual Environment

Open VS Code terminal (Terminal > New Terminal) and run:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Streamlit Configuration

Create the `.streamlit` folder and `config.toml` file:

```bash
mkdir .streamlit
```

Then create `.streamlit/config.toml` with this content:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`

**Note**: If it doesn't open automatically, manually navigate to `http://localhost:8501` in your browser.

## VS Code Configuration

### Recommended Extensions
- Python (Microsoft)
- Pylance (Microsoft)
- Python Docstring Generator
- autoDocstring

### Launch Configuration (Optional)

Create `.vscode/launch.json` for debugging:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Streamlit",
            "type": "python",
            "request": "launch",
            "program": "-m",
            "args": ["streamlit", "run", "app.py"],
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

## Project Structure

- **app.py**: Main Streamlit application with UI and visualizations
- **model.py**: Mesa-based agent simulation model
- **agent/**: Directory containing agent classes
  - **central_bank.py**: Central bank agent implementation
  - **commercial_bank.py**: Commercial bank agent implementation  
  - **consumer.py**: Consumer agent implementation
- **requirements.txt**: Python dependencies

## Usage

1. Start the application using `streamlit run app.py`
2. Adjust simulation parameters in the sidebar
3. Click "Run Simulation" to execute the model
4. Explore results in different tabs:
   - CBDC Substitution: Deposit substitution analysis
   - H1: Network Centrality: Bank centrality changes
   - H3: Liquidity Stress: Banking system stress analysis
   - H4: Network Connectivity: Interbank network analysis
   - H6: Central Bank Dominance: Central bank network position
   - Agent Flow Chart: Visual representation of agent interactions

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure virtual environment is activated and all dependencies are installed
2. **Port Already in Use**: Change port in `.streamlit/config.toml` or use `streamlit run app.py --server.port 8502`
3. **Python Version**: Ensure you're using Python 3.11+
4. **Browser Won't Open**: 
   - If browser doesn't open automatically, go to `http://localhost:8501` manually
   - Never use `http://0.0.0.0:8501` - this won't work in browsers
   - Make sure no firewall is blocking the port

### Dependencies Issues

If you encounter dependency conflicts, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Performance Issues

For better performance with large simulations:
- Reduce number of consumers/banks in sidebar
- Decrease simulation steps
- Close other resource-intensive applications

## Development

### Code Structure
- The simulation uses Mesa framework for agent-based modeling
- Streamlit provides the web interface
- Plotly handles interactive visualizations
- NetworkX manages agent network relationships

### Customization
- Modify agent behavior in `agent/` directory
- Adjust simulation parameters in `model.py`
- Customize visualizations in `app.py`

## Support

If you encounter issues:
1. Check Python version compatibility
2. Verify all dependencies are installed
3. Ensure virtual environment is activated
4. Check for any error messages in the terminal