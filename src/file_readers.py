import pandas as pd

from typing import Any

def reading_excel(file_path: str) -> list[dict[Any, Any]]:
  dict_df_excel = pd.read_excel(file_path).to_dict(orient='records')
  return dict_df_excel