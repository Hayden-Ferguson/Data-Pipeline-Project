<h1>Data Pipeline Project</h1>


<h2>Introduction</h2>
This project aims to use read HR attrition data from https://www.kaggle.com/datasets/rishikeshkonapure/hr-analytics-prediction and clean and enter it into the Employees table in a postgreSQL server,
as well as perform simple operations on the table.

<h2>Requirements</h2>
Python 3.11 or higher

<h2>Installation</h2>
1. Install the requiremed dependencies:

```pip install -r requirements.txt```

<h2>Usage</h2>
This program works by taking the arguements sent while running main.py and going through them sequentially.

To read data into the postgreSQL Employees table, simply put the filename as one of the arguements, like so:

```python .\main.py .\HR-Employee-Attrition.csv```

To print the data currently in the Employees table to the terminal and sql_reader.txt, pass 'read' as one of the arguments:

```python .\main.py read```

To remove all data in the Employees table, pass 'clear' or 'truncate as one of the arguments:

```python .\main.py clear```

To drop the Employees table, pass 'drop' as one of the arguments:

```python .\main.py drop```

<h2>License</h2>
This project is provided "as is" under the MIT License. Feel free to use, modify, and distribute it as you wish.
