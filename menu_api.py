from models import *

with db:
    db.create_tables([Order, Product, Category, Item, Sale, User])

    print('Tables created')

with db:
    products = Product.select()
    categories = Category.select()

    productData = [
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
            'name': 'Сырный',
            'price': 40,
            'category_id': 3,
            'image_uri': 'classic.webp'
        },
        {
            'name': 'Карри',
            'price': 40,
            'category_id': 3,
            'image_uri': 'classic.webp'
        },
        {
            'name': 'Кетчуп',
            'price': 40,
            'category_id': 3,
            'image_uri': 'classic.webp'
        },
    ]

    categoriesData = [
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
        Category.insert_many(categoriesData).execute()
        print('Categories uploaded')

    if len(products) == 0:
        Product.insert_many(productData).execute()
        print('Products uploaded')


def get_categories():
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


get_categories()
