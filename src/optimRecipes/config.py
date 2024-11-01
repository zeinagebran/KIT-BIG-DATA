from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Union

@dataclass
class Config:
    zip_file_path: Path = Path("archive.zip")

    logging_dir: Path = Path("logs")
    run_cfg_dir: Path = Path("outputs")

    min_rating: float = 4.5
    min_num_ratings: int = 0
    num_top_recipes: int = 20
    min_year: int = 1999
    max_year: int = 2019



