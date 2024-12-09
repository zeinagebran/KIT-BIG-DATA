"""optimRecipes/config.py file.

Sub-module Streamlit and entry point of webapp streamlit.

"""
###############################################################################
# IMPORTS :
# /* Standard includes. */
# /* Extern modules */
# /* Intern modules */


###############################################################################
# CLASS :
class Config:
    """Class for configuraiton parameter of module and webapp."""

    def __init__(self):
        """Initialise default configuration or current configuration."""
        # Standard path for project resources we used for this project (you should relative path)
        # !!! NE PAS COMMIT LA VERSION LOCALE !!!
        self.zip_file_path: str = r"C:\Users\User\Desktop\MASTERE SPECIALISE IA\KIT BIG DATA BGDIA700\RESOURCES PROJET/archive.zip"

        # Directory of extracted_data
        self.extracted_data_path: str = 'extracted_data'

        # Directory for storing logs
        self.logging_dir: str = "logs"

        # Directory for storing output configurations and results
        self.run_cfg_dir: str = "outputs"

        # Minimum rating threshold for filtering recipes
        self.min_rating: float = 4.5

        # Minimum number of ratings a recipe must have to be considered
        self.min_num_ratings: int = 0

        # Number of top recipes to retrieve based on filters
        self.num_top_recipes: int = 20

        # Filter recipes by a minimum year of creation
        self.min_year: int = 1999

        # Filter recipes by a maximum year of creation
        self.max_year: int = 2019

        # URL where data are
        self.url: str = 'https://perso.telecom-paristech.fr/nallegre-24/projet_bgdia700/recipe.zip'
