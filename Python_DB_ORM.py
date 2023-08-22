import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
from models import create_tables, Publisher, Sale, Book, Stock, Shop


DSN = "postgresql://postgres:905995ike@localhost:5432/book_db1"
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

with open('tests_data.json', 'r') as db:
    data = json.load(db)

for line in data:
    method = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[line['model']]
    session.add(method(id=line['pk'], **line.get('fields')))

session.commit()

def store_selections():
    writer = input('Введите имя (name) издателя или ID: ')
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(
        Shop).join(Sale)
    if writer.isdigit():
        query = query.filter(Publisher.id == writer).all()
    else:
        query = query.filter(Publisher.name == writer).all()
    for title, name, price, date_sale in query:
        print(f"{title:<40} | {name:<10} | {price:<8} | {date_sale}")


if __name__ == '__main__':
    store_selections()

session.close()