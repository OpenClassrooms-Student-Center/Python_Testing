# gudlift-performance test

## Requirements :

#### Make sure that you activated the virtual environment :
```bash
./env/Script/activate  # on Windows
./env/bin/activate     # on Mac or Linux
```

#### And you have installed all dependencies from the file 'requirements.txt' :
```bash
pip install -r requirements.txt
```

#### And you have opened your terminal at :

```bash
cd P11_Python_Testing/tests/performance/
```


## Testing

#### Now you can run the performance test with this command :


```bash
locust -f locustfile1 # this file tests all competitions'retrieving 
```


```bash
locust -f locustfile2 # this file tests the total points' update
```

#### Those previous commands will automatically run the locust server :

open it in your default browser at localhost:8089

#### Add the following settings to the "Start new load test" :

- Number of users = 6
- Spawn rate = 1

then to start the test click on : Start swarming 

## Author

- By Rossignol Hanane 2022 
- Github Profile :octocat: [@Rossignol-h](https://github.com/Rossignol-h)