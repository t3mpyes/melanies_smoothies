# Import python packages
import streamlit as st
import requests
import pandas as pd
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
#st.stop()

ingredient_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredient_list:
    st.write(ingredient_list)
    st.text(ingredient_list)

    ingredient_string = ''

    for each_fruit in ingredient_list:
        ingredient_string += each_fruit + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', each_fruit,' is ', search_on, '.')

        st.subheader(each_fruit + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + each_fruit)
        jv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    #st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredient_string + """', '"""+name_on_order+"""')"""

    
    insert_order = st.button('Submit Order')
    
    if insert_order:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

