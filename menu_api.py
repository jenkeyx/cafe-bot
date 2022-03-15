from models import *


def fill_tables():
    db.create_tables([Order, Product, Category, Item, Sale, User])

    print('Tables created')


def fill_products():
    products = Product.select()
    categories = Category.select()

    product_data = [
        {
            'name': 'Классическая',
            'price': 209,
            'category_id': 1,
            'image_uri': 'classic.webp'
        },
        {
            'name': 'Двойная',
            'price': 269,
            'category_id': 1,
            'image_uri': 'double.webp'
        },
        {
            'name': 'Фалафель',
            'price': 199,
            'category_id': 1,
            'image_uri': 'falafel.webp'
        },
        {
            'name': 'Coca-Cola 0.3 ',
            'price': 75,
            'category_id': 2,
            'image_uri': 'coke.jpeg'
        },
        {
            'name': 'Fanta 0.3 ',
            'price': 75,
            'category_id': 2,
            'image_uri': 'fanta.jpg'
        },
        {
            'name': 'Sprite 0.3 ',
            'price': 75,
            'category_id': 2,
            'image_uri': 'sprite.jpg'
        },
        {
            'name': 'Сырный',
            'price': 40,
            'category_id': 3,
            'image_uri': 'cheesy.jpg'
        },
        {
            'name': 'Карри',
            'price': 40,
            'category_id': 3,
            'image_uri': 'curry.jpg'
        },
        {
            'name': 'Кетчуп',
            'price': 40,
            'category_id': 3,
            'image_uri': 'ketchup.jpg'
        },
        {
            'name': 'Мороженое',
            'price': 80,
            'category_id': 4,
            'image_uri': 'ice_cream.jpg'
        },
        {
            'name': 'Пончики ассорти',
            'price': 60,
            'category_id': 4,
            'image_uri': 'donuts_set.jpg'
        },
    ]

    categories_data = [
        {
            'id': 1,
            'name': 'Шаверма'
        },
        {
            'id': 2,
            'name': 'Напитки'
        },
        {
            'id': 3,
            'name': 'Соусы'
        },
        {
            'id': 4,
            'name': 'Десерты'
        },
    ]

    if len(categories) == 0:
        Category.insert_many(categories_data).execute()
        print('Categories uploaded')

    if len(products) == 0:
        Product.insert_many(product_data).execute()
        print('Products uploaded')


def get_categories():
    categories = Category.select()

    categories_names = list(map(lambda item: item.name, categories))
    return categories_names


def get_products_by_category(category):
    if category == 'Напитки':
        return Product.select().where(Product.category_id == '2')
    elif category == 'Соусы':
        return Product.select().where(Product.category_id == '3')
    elif category == 'Десерты':
        return Product.select().where(Product.category_id == '4')
    elif category == 'Шаверма':
        return Product.select().where(Product.category_id == '1')


def get_order_by_chat_id(chat_id):
    return Order.get(Order.number == chat_id)


def create_order(chat_id):
    new_order = Order(number=chat_id, deadline=1, satus="created")
    new_order.save()
