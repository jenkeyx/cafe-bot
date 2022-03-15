from peewee import *

db = MySQLDatabase('telegram_bot', host='database-1.clp2dsewlpjx.us-east-2.rds.amazonaws.com', port=3306, user='admin',
                   password='Mihail2004')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Order(BaseModel):
    number = IntegerField()
    user = IntegerField()
    deadline = TimestampField()
    status = TextField()

    class Meta:
        db_table = "orders"


class Category(BaseModel):
    name = TextField()

    class Meta:
        db_table = "categories"


class Product(BaseModel):
    name = TextField()
    price = FloatField()
    category = ForeignKeyField(Category)
    image_uri = TextField()

    class Meta:
        db_table = "products"


class Item(BaseModel):
    product_id = ForeignKeyField(Product)
    order_id = ForeignKeyField(Order)
    count = IntegerField()

    class Meta:
        db_table = "items"


class Sale(BaseModel):
    product_id = ForeignKeyField(Product)
    discount = FloatField()

    class Meta:
        db_table = "sales"


class User(BaseModel):
    order_id = ForeignKeyField(Order)
    mobile_number = TextField()

    class Meta:
        db_table = "users"
