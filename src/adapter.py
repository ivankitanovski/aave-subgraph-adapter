import logging
import requests
import pandas as pd
import argparse
from utils import from_timestamp

# set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# The Graph endpoint
endpoint = "https://api.studio.thegraph.com/query/73855/openblocklabs/v0.0.7"

# Number of records to fetch in each request
PAGE_SIZE = 1000

# GraphQL query to get net supplied amount for users
query_all = """
query($first: Int!, $timestamp: Int!){
  snapshots(orderBy: timestamp, orderDirection: asc, first: $first, where: {timestamp_gte: $timestamp}) {
    blockNumber
    netSupplied
    timestamp
    user {
      id
    }
    token {
      id
      name
      symbol
    }
  }
}
"""

# GraphQL query to get net supplied amount for users at a specific block number
query_block = """
query($first: Int!, $timestamp: Int!, $blockNumber: Int!) {
  snapshots(orderBy: timestamp, orderDirection: asc, first: $first, skip: $skip, where: {timestamp_gte: $timestamp, blockNumber: $blockNumber}) {
    blockNumber
    netSupplied
    timestamp
    user {
      id
    }
    token {
      id
      name
      symbol
    }
  }
}
"""

def get_net_supplied_amount(block_number=None):
    """Get net supplied amount for users from the Graph API"""

    timestamp = 0 # initial value for timestamp
    snapshots = [] # list to store snapshots

    query = query_all if block_number is None else query_block
    variables = {"first": PAGE_SIZE, "timestamp": timestamp}
    if block_number is not None:
        variables["blockNumber"] = block_number

    # Fetch snapshots until there are no more records. 
    while True:
        logging.info(f'Fetching snapshots with timestamp={timestamp}' + (f' at block number {block_number}' if block_number is not None else ''))
        response = requests.post(endpoint, json={'query': query, 'variables': variables}) 
        if response.status_code == 200 and not "errors" in response.json():
            current_snapshots = response.json()['data']['snapshots']
            if not current_snapshots:
                logging.info('No more snapshots to fetch')
                break

            snapshots.extend(current_snapshots)

             # Update timestamp to the last received snapshot's timestamp + 1 to avoid duplicates
            timestamp = int(current_snapshots[-1]['timestamp']) + 1
            variables["timestamp"] = timestamp
        else:
            logging.error(f"Query failed with status code {response.status_code}. {response.text}")
            break # not raising exception for now

    return snapshots

def main():
    parser = argparse.ArgumentParser(description="Retrieve snapshots for users from the Graph API.")
    parser.add_argument('--block_number', type=int, help='The block number to retrieve snapshots for (optional)')
    args = parser.parse_args()

    block_number = args.block_number

    logging.info(f'Retrieving snapshots for users from "{endpoint}"' + (f' at block number {block_number}' if block_number is not None else ''))

    # Get the net supplied amount for each user at each block
    snapshots = get_net_supplied_amount(block_number)
    
    # Prepare the data for the CSV file
    data = []
    for snapshot in snapshots:
        # if it's too big we can stream it to a file
        data.append({
            "block_number": snapshot['blockNumber'],
            "timestamp": from_timestamp(int(snapshot['timestamp'])),
            "owner_address": snapshot['user']['id'],
            "token_symbol": snapshot['token']['symbol'],
            "token_address": snapshot['token']['id'],
            "token_amount": int(snapshot['netSupplied'])
        })
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Write the DataFrame to a CSV file
    df.to_csv("output/output.csv", index=False)

    logging.info(f'Exported {len(df)} records to "output/output.csv"')

if __name__ == "__main__":
    main()
