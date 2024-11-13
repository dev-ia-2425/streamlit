from streamlit.testing.v1 import AppTest

# Tester le tri
def test_sorting():
   at = AppTest.from_file("app.py").run(timeout = 30)

   at.selectbox[0].set_value("year")
   at.selectbox[1].set_value("Croissant").run(timeout = 30)
   
   index = at.dataframe[0].value.index[0]

   assert (index == 78058)

# Tester les filtres de base
def test_filter():
   from datetime import date
   at = AppTest.from_file("app.py").run(timeout = 30)

   date = date(2014, 1, 1)
   at.date_input[0].set_value(date)
   at.date_input[1].set_value(date)

   at.selectbox[2].set_value("ford")
   at.selectbox[3].set_value("F-150")

   at.slider[0].set_range(5000, 10000).run(timeout = 30)
   
   assert (len(at.dataframe[0].value) == 3)

# Tester les filtres customs 
def test_custom_filter():
   at = AppTest.from_file("app.py").run(timeout = 30)

   container = at.get("vertical")[0]
   
   container.multiselect[0].select("condition")
   container.multiselect[0].select("body").run(timeout = 30)

   container = at.get("vertical")[0]
   container.slider[0].set_range(30, 49).run(timeout = 30)

   container = at.get("vertical")[0]
   container.multiselect[1].select("SuperCab").run(timeout = 30)
   
   index = at.dataframe[0].value.index[0]

   print(at.dataframe[0].value.index)
   assert (index == 1066)

# Tester le group by
def test_group():
   at = AppTest.from_file("app.py").run(timeout = 30)

   at.selectbox

   at.selectbox[4].select("odometer").run(timeout = 30)
   at.selectbox[5].select("Min")
   at.selectbox[6].select("Premier").run(timeout = 30)

   year = (at.database[0].value["year"][0] == 1984)
   make = (at.database[0].value["make"][0] == "chevrolet")

   valid = (year) and (make)
   assert valid


   