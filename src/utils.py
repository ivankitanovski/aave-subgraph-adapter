from datetime import datetime

def from_timestamp(timestamp):
    """Helper function to convert timestamp to datetime object and format it to string"""
    # Convert timestamp to datetime object
    dt_object = datetime.fromtimestamp(timestamp)
    # Format datetime object to string
    date_string = dt_object.strftime("%Y-%m-%d %H:%M:%S")   
    return date_string