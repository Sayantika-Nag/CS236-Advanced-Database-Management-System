import streamlit as st
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from math import ceil
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

def connect():
  # conn = st.connection("postgresql+psycopg2", type="sql")
  from sqlalchemy.orm import sessionmaker
  SERVER = st.secrets["database"]["host"]
  USERNAME = st.secrets["database"]["username"]
  PASSWORD = st.secrets["database"]["password"]
  DATABASE = st.secrets["database"]["database"]

  connection_url = URL.create(
      drivername="postgresql+psycopg2",
      username=USERNAME,
      password=PASSWORD,
      host=SERVER,
      port=5432,
      database=DATABASE,
  )
  sqlengine = create_engine(connection_url)
  conn = sqlengine.connect()
  return conn

def load_data_from_table(conn, table_name: str) -> pd.DataFrame:
  """
  Loads and caches data from a database table.

  Args:
      conn (SQLAlchemy Connection): SQLAlchemy connection to database
      table_name (str): Name of the table to retrieve data from

  Returns:
      pd.DataFrame: Pandas Dataframe that contains all data in the table
  """
  # query = f"SELECT * FROM {table_name}"
  return pd.read_sql(table_name, con=conn)

def split_frame(input_df: pd.DataFrame, num_rows: int) -> list[pd.DataFrame]: 
  """
  Split a Pandas Dataframe into a list of Dataframes each containing a maximum number of rows

  Args: 
      input_df (pd.Dataframe): Original Dataframe to be split
      num_rows (int): Maximum number of rows in each Dataframe to split input_df into
  
  Returns:
      list[pd.Dataframe]: List of dataframes each containing maximum num_rows
  """
  df = [input_df.loc[i : i + num_rows - 1, :] for i in range(0, len(input_df), num_rows)]
  return df

def paginate_dataframe(filtered_df: pd.DataFrame) -> list[pd.DataFrame] :
  """
  Add UI on dataframe to create pagination for viewers

  Args:
      filtered_df (pd.DataFrame): Original dataframe

  Returns:
      List[pd.Dataframe]: List of paginated dataframes
  """
  top_menu = st.columns(3)
  with top_menu[0]:
      sort = st.radio("Sort Data:", options=["Yes", "No"], horizontal=True, index=1)
  if sort == "Yes":
      with top_menu[1]:
          sort_field = st.selectbox("Sort By", options=filtered_df.columns)
      with top_menu[2]:
          sort_direction = st.radio(
              "Direction", options=["Ascending", "Descending"], horizontal=True
          )
      # dataset is sorted dataframe
      dataset = filtered_df.sort_values(
          by=sort_field, ascending=sort_direction == "Ascending", ignore_index=True
      )
  else:
      # no sorting requested
      dataset = filtered_df
  pagination = st.container()

  bottom_menu = st.columns((4, 1, 1))
  with bottom_menu[2]:
      batch_size = st.selectbox("Page Size", options=[25, 50, 100], key="page_size")
  with bottom_menu[1]:
      factor = 1 if len(dataset) % batch_size > 0 else 0
      total_pages = ceil(len(dataset) / batch_size) + factor
  
      current_page = st.number_input(
          "Page", min_value=1, max_value=total_pages, step=1
      )
  with bottom_menu[0]:
      st.markdown(f"Page **{current_page}** of **{total_pages}** ")

  pages = split_frame(dataset, batch_size)
  # Create read-only table
  pagination.dataframe(data=pages[current_page - 1], hide_index=True, use_container_width=True)

  return pages
    
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add UI to let viewers filter columns of a Dataframe

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    df = df.copy()
    # Try to convert timestamps to datetime objects
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    filterable = st.container() # stremlit container

    with filterable:
        to_filter_columns = st.multiselect("Filter on Column(s):", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]
    return df

def main():
    conn = connect()
    tables = pd.read_sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';", conn)
    tablepicker = st.container()
    select_table = st.selectbox("Choose Table:", tables['table_name'], key="table") # First column of dataframe is used to populate the selectbox
    table_name = select_table.replace("'","")
    df = load_data_from_table(conn=conn, table_name=table_name)
    filtered_df = filter_dataframe(df)
    pages = paginate_dataframe(filtered_df=filtered_df)

if __name__ == "__main__":
    main()
