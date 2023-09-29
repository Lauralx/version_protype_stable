from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:cenivam@localhost:3306/CENIVAM")
#orden: usuario,contraseña,dirección de localhost, nombre de la base de datos
#Ojo con el usuario y contraseña y la base de datos !!!!!


meta_data = MetaData()
