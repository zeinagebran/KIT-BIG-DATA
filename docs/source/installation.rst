Installation
============

This document explains how to install the KIT-BIG-DATA project.

**Installation via Poetry:**

.. code-block:: bash

    git clone https://github.com/zeinagebran/KIT-BIG-DATA.git
    cd KIT-BIG-DATA
    poetry install

Make sure you have the correct version of Python installed.

**Manual installation:**

.. code-block:: bash

    git clone https://github.com/zeinagebran/KIT-BIG-DATA.git
    
    virtualenv venv
    .\venv\Scripts\activate
    
    cd KIT-BIG-DATA
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install -r requirements.txt
    python -m nltk.downloader stopwords

For development and use our unit test add this action :

.. code-block:: bash

    python -m pip install -r requirements-dev.txt
