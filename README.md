
# HvacController-Python

## How to use MiniConda to create a virtual environment

### Create environment
```conda create --name <name> python=3.8```
```conda create --name <name> --file requirements.txt python=3.8```

### Activate environment
```activate <name>```

Select the python interpreter of this virtual environment
### To install new package
```conda install <package>```

### To generate requirements.txt
```conda list -e > requirements.txt```


## To run project
In terminal: ```python3 main.py```

if using virtual environnment, in terminal: ```<path>/python.exe main.py```
## Unit Test

### To run unit test
At the root folder: run ```python -m unittest discover -v```
