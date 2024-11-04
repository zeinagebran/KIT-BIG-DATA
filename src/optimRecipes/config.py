from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Union


@dataclass
class Config:
    # Path to the zip file containing project resources
    zip_file_path: Path = Path(
        r"C:\Users\User\Desktop\MASTERE SPECIALISE IA\KIT BIG DATA BGDIA700\RESOURCES PROJET\archive.zip")

    # Directory for storing logs
    logging_dir: Path = Path("logs")

    # Directory for storing output configurations and results
    run_cfg_dir: Path = Path("outputs")

    # Minimum rating threshold for filtering recipes
    min_rating: float = 4.5

    # Minimum number of ratings a recipe must have to be considered
    min_num_ratings: int = 0

    # Number of top recipes to retrieve based on filters
    num_top_recipes: int = 20

    # Filter recipes by a minimum year of creation
    min_year: int = 1999

    # Filter recipes by a maximum year of creation
    max_year: int = 2019
