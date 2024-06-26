# # Import python packages
# import streamlit as st
# from snowflake.snowpark.context import get_active_session
# from snowflake.snowpark.functions import col  # Import col function
# # Write directly to the app
# st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw: ")

# st.write(
#     """Choose the fruits you want in your custom Smoothiel!
#     """
# )
# # import streamlit as st

# name_on_order= st.text_input("Name On Smoothie:")
# st.write("The name on your Smoothie will be", name_on_order)


# # st.write("You selected:", option)

# session = get_active_session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))    
# # st.dataframe(data=my_dataframe, use_container_width=True)

# #st.dataframe (data-my_dataframe, use_contai
# ingredients_list =st.multiselect(
# 'Choose up to 5 ingredients:'
# , my_dataframe
# )
# # if ingredients_list:
# #  st.write(ingredients_list)   
# #  st.text(ingredients_list)
# # time_to_insert =st.button('Submit Order')
# ingredients_string = ""  # Initialize ingredients_string
# if ingredients_list :
 
 
#  for fruit_chosen in ingredients_list: 
#    ingredients_string += fruit_chosen + ' '
#  # st.write(ingredients_string)
    
 
# #  my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
# #                       values ('""" + ingredients_string + """','"""+name_on_order+""")"""
        

# #  st.write(my_insert_stmt)
# #  st.stop()

 
# # # time_to_insert =st.button('Submit Order')


# my_insert_stmt = """ INSERT INTO smoothies.public.orders(ingredients,name_on_order)
#                         VALUES ('{}', '{}') """.format(ingredients_string, name_on_order)
# time_to_insert =st.button('Submit Order')
# session.sql(my_insert_stmt).collect()
# st.success('Your Smoothie is ordered!', icon="✅")













import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:") 
st.write("Orders that need to be filled.")

# Get active Snowflake session
session = get_active_session()

# Retrieve pending orders
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == False).collect()

# Display orders in a data editor
editable_df = st.experimental_data_editor(my_dataframe)

# Submit button
submitted = st.button('Submit')

if submitted:
    st.success("Someone clicked the button",icon='👍')
    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)
    try:
     og_dataset.merge(edited_dataset
                     , (og_dataset['order_uid'] == edited_dataset['order_uid'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
     # st.success("Someone clicked the button",icon='👍')
    except:
        st.write("Something went wrong.")
    
