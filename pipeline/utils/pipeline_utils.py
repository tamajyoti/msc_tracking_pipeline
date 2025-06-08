import json
import hashlib
import yaml

def generate_hash_id(data: dict) -> str:
    json_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(json_str.encode('utf-8')).hexdigest()