import json

def load_json_data(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_pricing_representation(data):
    """Flatten the JSON structure and generate text representation for all categories."""
    flat_data = []
    for category, services_data in data.items():
        for service, details in services_data.items():
            for detail in details:
                detail_text = ', '.join([f"{k}: {v}" for k, v in detail.items()])
                text_representation = f"Category: {category}, Service: {service}, Details: {detail_text}"
                flat_data.append(text_representation)
    return flat_data

def extract_details_representation(data):
    """Flatten the JSON structure and generate text representation for details."""
    flat_data = []
    for entry in data:
        name = entry.get("name", "Unnamed")
        new_text = entry.get("newText", "No text available")
        text_representation = f"Name: {name}, Text: {new_text}"
        flat_data.append(text_representation)
    return flat_data

def formatter(data_type, file):
    """Format data based on the specified type."""
    data = load_json_data(file)
    
    if data_type == 'pricing':
        text_data = extract_pricing_representation(data)
    elif data_type == 'details':
        text_data = extract_details_representation(data)  # Placeholder function
    else:
        raise ValueError("Invalid data type. Choose 'pricing' or 'details'.")
    
    return text_data
