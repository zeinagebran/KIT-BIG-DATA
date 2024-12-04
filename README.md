# **🍴 optimRecipes: User Interaction Analysis for Recipe Platform 🍴**

[![Github build and verify](https://github.com/zeinagebran/KIT-BIG-DATA/actions/workflows/python-app.yml/badge.svg)](https://github.com/zeinagebran/KIT-BIG-DATA/actions/workflows/python-app.yml)
[![Github test, coverage](https://github.com/zeinagebran/KIT-BIG-DATA/actions/workflows/sonarcloud.yml/badge.svg)](https://github.com/zeinagebran/KIT-BIG-DATA/actions/workflows/sonarcloud.yml)
[![Github documentation](https://github.com/zeinagebran/KIT-BIG-DATA/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/zeinagebran/KIT-BIG-DATA/actions/workflows/pages/pages-build-deployment)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=zeinagebran_KIT-BIG-DATA&metric=alert_status)](https://sonarcloud.io/summary/overall?id=zeinagebran_KIT-BIG-DATA)

[![Kaggle](https://img.shields.io/badge/Dataset-Kaggle-yellow)](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)
[![Licence EUPL 1.2](https://img.shields.io/badge/licence-EUPL_1.2-blue)](https://interoperable-europe.ec.europa.eu/collection/eupl/eupl-text-eupl-12)


## **Description:**

### ***Project overview***

`optimRecipes` is a Python-based data analysis project designed to enhance user engagement on a recipe platform.
By analyzing user interactions and recipe feedback, this project uncovers trends and patterns to:
- Optimize content strategy.
- Improve the user experience.

### ***Project objectives***

1. Analyze temporal trends to determine high-activity periods.
2. Identify popular recipes and their defining features.
3. Use insights to optimize platform engagement and satisfaction.

### ***Dataset source***

This project uses data from **Food.com Recipes and User Interactions**.  
[📁 Access the dataset on Kaggle](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)

### ***Documentation***

Comprehensive project documentation is available :

**Automatic generation :**
- Documentation on [📘 Read the Docs](https://kit-big-data.readthedocs.io/en/latest/)
- Documentation on [GitHub.io](https://zeinagebran.github.io/KIT-BIG-DATA/)

**Manual/semi-manual generation :**
- Documentation on [Telecom-Paris website](https://perso.telecom-paristech.fr/nallegre-24/projet_bgdia700/html/)

### ***📷 Dashboard Preview***

_Example of the interactive dashboard:_

![image](https://github.com/user-attachments/assets/e23f5ee2-fc48-4a32-aa31-22c9b0ad4a71)


## **Technical informations:**

### ***Code Quality and Testing***

The **Quality Gate badge** (![Github build and test](https://github.com/zeinagebran/KIT-BIG-DATA/actions/workflows/python-app.yml/badge.svg)
![Quality Gate Status])) reflects that the project meets predefined criteria for code quality, including:
- High unit test coverage.
- Low technical debt.
- Reliable, maintainable, and secure code.

The **Github Action Python** (![Github build and verify](https://github.com/zeinagebran/KIT-BIG-DATA/actions/workflows/python-app.yml/badge.svg)) reflects that the project could be build without problem and has basic code quality:
- Build the project with the requirements.
- Basic code quality (with flake8).
- Run unit tests (ok if no error).

The **Github Action sonarcloud** (![Github test, coverage](https://github.com/zeinagebran/KIT-BIG-DATA/actions/workflows/sonarcloud.yml/badge.svg)) reflects that the project has coverage and critical commit issues.
- Run code coverage with unit tests.
- Transfert results to Sonarcloud server for avanced and standard code quality and security verification.


### ***Installation***

```shell
git clone https://github.com/zeinagebran/KIT-BIG-DATA.git
cd KIT-BIG-DATA
python -m pip install -r requirements.txt
python -m nltk.downloader stopwords
curl https://perso.telecom-paristech.fr/nallegre-24/projet_bgdia700/recipe.zip -o data/recipe.zip
```

### ***Usage***

```shell
set PYTHONPATH=src
streamlit run src/optimRecipes/main.py
```

### ***Development environment***

Firstly, you should build an environment for development and all requirements :
- Installation requirements :
```python
git clone https://github.com/zeinagebran/KIT-BIG-DATA.git
cd KIT-BIG-DATA
python -m pip install -r requirements.txt -r requirements-dev.txt
```

Then you can do testing, coverage or building documentation :
- Runing test :
```shell
python -m pytest
```
- Running coverage :
```shell
coverage run -m pytest
coverage report
```
- Building documentation :
```shell
make
firefox build/html/index.html
```

### ***Developers***

| Name               | GitHub Profile                              |
|--------------------|---------------------------------------------|
| **Habibata Samaké**| [habibatasamake](https://github.com/habibatasamake) |
| **Matthieu Larnouhet**| [mlarnouhet](https://github.com/mlarnouhet) |
| **Nicolas Allègre**| [nicolas-allegre](https://github.com/nicolas-allegre) |
| **Zeina Gebran**   | [zeinagebran](https://github.com/zeinagebran) |
