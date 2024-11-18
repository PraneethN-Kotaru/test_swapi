import pandas as pd

def solution(session):
    person_query = "select name from person where species_id = 1"
    person_df = pd.read_sql_query(person_query, session.bind)
    person_df['first_name'] = person_df['name'].str.split(' ').str[0]

    scripts_query = "select script_name, character from scripts"
    scripts_df = pd.read_sql_query(scripts_query, session.bind)

    intermediate_df=pd.merge(
        person_df.assign(first_name=person_df['first_name'].str.lower()),
        scripts_df.assign(character=scripts_df['character'].str.lower()),
        how='inner', left_on='first_name', right_on='character').groupby('script_name').size().reset_index(name='count')

    total_counts_df = scripts_df.groupby('script_name').size().reset_index(name='count')
    print(total_counts_df)
    type(total_counts_df)

    result_df = pd.merge(
        intermediate_df,
        total_counts_df,
        on='script_name',
        how='inner',
        suffixes=('_human', '_total'))

    result_df['human_percentage'] = ((result_df['count_human'] / result_df['count_total']) * 100).round(2)
    result_df['non_human_percentage'] = (((result_df['count_total']-result_df['count_human']) / result_df['count_total']) * 100).round(2)


    return result_df