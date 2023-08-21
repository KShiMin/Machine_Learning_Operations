# Machine Learning Operations

## Webapp URL: https://zsmlml.onrender.com
Web Application will go idle after 15 minutes of inactivity, if you want to view please contact either Shi Min or Zowie. Thank you

## Tools used in this project
* [Poetry](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f): Dependency management - [article](https://mathdatasimplified.com/2023/06/12/poetry-a-better-way-to-manage-python-dependencies/)
* [hydra](https://hydra.cc/): Manage configuration files - [article](https://mathdatasimplified.com/2023/05/25/stop-hard-coding-in-a-data-science-project-use-configuration-files-instead/)
* [DVC](https://dvc.org/): Data version control - [Repository Here](https://github.com/zow1e/mlopsData)
* [guincorn](https://gunicorn.org): Deployment of Web Application
* Flask: Development of Web Pages
* Jinja
* HTML & CSS
* Pycaret
* MLflow

## Deployment guide:

1. Specify the desired port to use under flask_application/gunicorn_config.py
```python
    options = {
        'bind': '0.0.0.0:<port_number>',
        'workers': 4,
    }
```

2. Ensure the directory path is in the root directory /

3. build the web application
```console
c:\repo_folder_path>pip install --upgrade pip && pip install -r flask_application/requirements.txt
```

4. start the web application
```console
C:\repo_folder_path>python flask_application/gunicorn_config.py
```


## Obtain Folder Structure
```console
C:\path_to_empty_dir>cookiecutter https://github.com/khuyentran1401/data-science-template --checkout dvc-poetry
```

## Machine_Learning_Operations Folder Structure
```bash
.
├── data                
│   ├── process                     # contains processed data
│   └── raw                         # contains raw data
├── models                          # store models
├── notebooks                       # store notebooks
├── docs                            # documentation for your project
├── outputs
├── src
└── flask_application            
    ├── config                      # configuration of web applications
    ├── pyscripts                   # python scripts for web applications
    ├── static                      # stylesheets
    ├── templates                   # HTML files
    ├── README.md                  
    ├── gunicorn_config.py          
    ├── main.py                     # Application Routes
    ├── requirements.txt            # Requirements for web application
    ├── storage.db.bak
    ├── storage.db.dat              
    └── storage.db.dir              
```
