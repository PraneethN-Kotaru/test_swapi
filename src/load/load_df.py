
def load_df_to_sql(session, df):
    df.to_sql('result1', con=session.bind, if_exists='replace', index=False)
    session.commit()
    session.close()
