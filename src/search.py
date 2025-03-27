import re
import os
from typing import List, Dict, Any
from config import DATA_DIR

operations =

def filter_operations(operations: List[Dict[str, Any]], search_pattern: str) -> List[Dict[str, Any]]:
    """
    Фильтрует банковские операции по наличию строки в описании и возвращает
    список отфильтрованных операций, где description содержит search_pattern

    Пример использования:
        >>> operations = [
        ...     {'description': 'Payment to John', 'amount': 100},
        ...     {'description': 'Transfer to bank', 'amount': 200},
        ...     {'description': 'Grocery store', 'amount': 50}
        ... ]
        >>> filter_operations(operations, 'to')
        [
            {'description': 'Payment to John', 'amount': 100},
            {'description': 'Transfer to bank', 'amount': 200}
        ]
    """

    try:
        pattern = re.compile(search_pattern, re.IGNORECASE)
        return [
            op for op in operations
            if 'description' in op and pattern.search(op['description'])
        ]

    except re.error as e:
        raise ValueError(f"Invalid regular expression pattern: {e}") from e