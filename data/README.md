## Folder containing data for the project

This is the folder where you should put the ZIP file contain the data.

### Use of light version

You could download also use the light version of the file :
- download from https://perso.telecom-paristech.fr/nallegre-24/projet_bgdia700/recipe.zip
- put it in this folder
- verify or change path configuration of this file in `src/optimRecipes/config.py`
```python
# For the light version, this should be :
self.zip_file_path: str = r"data/recipe.zip"
```