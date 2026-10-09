# Import python packages
import streamlit as st
import os
import requests
from snowflake.snowpark.functions import col



# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose fruits you want in your custom smoothie! """
)


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your will be', name_on_order)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('search_on'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop

# Convert the Snowspark Dataframe to pandas dataframe so we can use LOC function
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '
      
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_choosen,' is ', search_on, '.')
      
        st.subheader(fruit_choosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
      

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(NAME_ON_ORDER, ingredients)
                    values ('""" + name_on_order + "','" + ingredients_string + """')"""

    # st.write(my_insert_stmt)    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

# smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  

