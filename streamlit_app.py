import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
#pandas
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#display df
streamlit.dataframe(fruits_to_show)

#New Section to display API Response
streamlit.header('Fruityvice Fruit Advice')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','kiwi')
  if not fruit_choice:
      streamlit.write("The user entered", fruit_choice)
  else:
      #import requests
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
      # show jason fruit
      #-- streamlit.text(fruityvice_response.json())

      #take json
      fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
      #output table
      streamlit.dataframe(fruityvice_normalized)
      
except URLError as e:
    streamlit.error()

#lesson 12 stop
streamlit.stop()
import snowflake.connector
#account connector part
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall() #fetchone()
streamlit.header("The Fruit Load List Contains:")
streamlit.dataframe(my_data_rows)

#choice
fruit_choice = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write("Thanks for adding ", fruit_choice)

#insert
my_cur.execute("insert into fruit_load_list values ('from streamlit')")

