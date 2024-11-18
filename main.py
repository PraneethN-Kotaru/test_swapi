from src.load.load_df import load_df_to_sql
from src.models.models import create_session
from src.extract.swapi import insert_planets, insert_people, insert_starships
from src.extract.scripts import read_and_insert_files_from_directory
from src.transform.problem1 import solution

def main():
    session = create_session()

    insert_people(session)
    # insert_planets(session)
    # insert_starships(session)
    read_and_insert_files_from_directory("data/SW_scripts", session)
    print("Data extraction and insertion complete!")


    result1 = solution(session)
    print("transformation complete!")

    load_df_to_sql(session, result1)
    print("load complete!")


if __name__ == '__main__':
    main()