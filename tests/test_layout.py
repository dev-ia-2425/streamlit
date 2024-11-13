from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py").run(timeout = 30)

# Import de la BDD 
def test_database():
   # at = AppTest.from_file("app.py").run(timeout = 30)
   # Tester avec une valeur connue
   assert at.dataframe[0].value["odometer"][0] == 16639

# Champs pour les tris
def test_sorting_inputs():
   # at = AppTest.from_file("app.py").run(timeout = 30)

   sort_by = (at.selectbox[0].value == None)
   order = (at.selectbox[1].value == "Croissant")
   
   print(sort_by, order)
   valid = (sort_by) and (order)

   assert valid

# Champs pour les filtres
def test_filter_inputs():
   # at = AppTest.from_file("app.py").run(timeout = 30)

   custom_filter = (at.multiselect[0].value == [])
   first_date = (str(at.date_input[0].value) == "2014-01-01")
   last_date =  (str(at.date_input[1].value) == "2015-07-21")
   make =  (at.selectbox[2].value == None)
   model = (at.selectbox[3].value == None)
   first_price = (at.slider[0].value[0] == 1)
   last_price = (at.slider[0].value[1] == 230000)

   print( custom_filter, first_date, last_date, make, model, first_price, last_price )
   valid = (custom_filter) and (first_date) and (last_date) and (make) and (model) and (first_price) and (last_price)

   assert valid

# Champs pour le group by
def test_group_inputs():
   group_by = (at.selectbox[4].value == None)
   num_func = (at.selectbox[5].disabled == True)
   str_func = (at.selectbox[6].disabled == True)

   print(group_by, num_func, str_func)
   valid = (group_by) and (num_func) and (str_func)

   assert valid

# Champ pour l'affichage
def test_display():
   valid = (at.multiselect[1].disabled == True)

   assert valid


   