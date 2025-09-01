import matplotlib.pyplot as plt
from typing import List, Optional

class ValueImporter:
    
    def __init__(self, filepath: str, delimiter: str = ';'):
        self.filepath = filepath
        self.delimiter = delimiter

    def load_prices(self) -> List[float]:
        prices: List[float] = []
        with open(self.filepath, encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split(self.delimiter)
            if len(parts) < 2:
                continue
            value_str = parts[1].replace('"', '').replace(',', '.').strip()
            if not value_str:
                continue
            try:
                prices.append(float(value_str))
            except ValueError:
                continue
        return prices
