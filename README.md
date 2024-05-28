# Aave V3 Adapter

This project tracks the net supplied amount of ETH, USDC, and USDT for users on Aave V3 on the Arbitrum chain. It queries the subgraph and generates a CSV file with the following fields:

1. block_number
2. timestamp
3. owner_address
4. token_symbol
5. token_address
6. token_amount

## Setup

Before running the script, ensure you have the following installed:

- Python 3.x
- `requests` library
- `pandas` library

Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

To retrieve all snapshots and save them to a CSV file, run the script without any arguments:

```bash
python src/adapter.py
```
or, alternatively

To retrieve snapshots for a specific block number, use the --block_number argumen

```bash
python src/adapter.py --block_number <BLOCK_NUMBER>
```

## Directory Structure

aave-subgraph-adapter/   
├── output/   
│ └── output.csv   
├── src/  
│ └── adapter.py  
│ └── utils.py  
├── requirements.txt  
└── README.md  

- `src/adapter.py`: The main script that retrieves snapshot data from The Graph API and exports it to a CSV file.
- `src/utils.py`: A utility module containing helper functions (e.g., `from_timestamp`).
- `output`: A directory where the CSV file (`output.csv`) is saved.
- `README.md`: The main readme file with instructions and information about the project.
