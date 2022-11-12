# gudlift-coverage test

1. REQUIREMENTS :

#### Make sure that you activated the virtual environment :
```bash
./env/Script/activate  # on Windows
./env/bin/activate     # on Mac or Linux
```

#### And you have installed all dependencies from the file 'requirements.txt' :
```bash
pip install -r requirements.txt
```

#### And you have opened your terminal at the root of the app  :

```bash
cd P11_Python_Testing
```


1. Testing

#### Now you can run the coverage test with this command :


```bash
python -m pytest --cov=. --cov-report html
```


#### The previous command will automatically generate a new folder :
```bash
htmlcov  
```

#### In this htmlcov/ there is an index.html file :

open it in your default browser, to see the report.

## Author

- By Rossignol Hanane 2022 
- Github Profile :octocat: [@Rossignol-h](https://github.com/Rossignol-h)