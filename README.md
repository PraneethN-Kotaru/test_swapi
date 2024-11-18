## This is a basic version of code, which contains python, pandas and sqlite as the solution

## Pre requisits:
Python 3.12.7
pip install requests pandas
pip install sqlalchemy  # If you're working with databases

## Some of the following assumptions were made:
  There is no species information for people, so these people are considered as Human
  As script contains first name of the chanracter most of the times, we took only first name, so results may not match the expected

## How to Run:

Get the code locally from git
remove the star_wars.db
install pre-requisits
run `python main.py` from the path

Output:
<img width="1328" alt="image" src="https://github.com/user-attachments/assets/79bac0ac-886b-4c28-8f39-d03adca462f2">
To view the results, please upload the star_wars.db to https://inloop.github.io/sqlite-viewer/, you can make the queries to view all tables and results:
`SELECT * FROM result1`

## Next steps:

1. Containerisation
2. Updating code standards more and scaling
