# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Smoothie App :cup_with_straw:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

name_on_order = st.text_input("Name on smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredient_list:
    st.write(ingredient_list)
    st.text(ingredient_list)

    ingredient_string = ''

    for each_fruit in ingredient_list:
        ingredient_string += each_fruit + ' '
    #st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredient_string + """', '"""+name_on_order+"""')"""

    
    insert_order = st.button('Submit Order')
    
    if insert_order:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
