# MLOPS

deployment guide:

1. in gunicorn_config, specify port to use

2. root directory
/

3. build command
pip install --upggrade pip && pip install -r flask_application/requirements.txt

4. start command
python flask_application/gunicorn_config.py


folder structure:
cookiecutter https://github.com/khuyentran1401/data-science-template --checkout dvc-poetry 

machine_learning_operations
>> data
> models
> notebooks
> docs
> outputs
> src
> flask_application
    > config
    > py_scripts
    > static
    > templates
    gunicorn_config.py
    requirements.txt
    main.py
    logs.log
    main.log
    README.md


webapp url:
https://zsmlml.onrender.com 
