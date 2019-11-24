from typing import Generator, List, Dict
import time

import requests
from sqlalchemy.exc import OperationalError

from storage.base import (
    Base,
    engine,
    Session,
)
from storage.numbers import (
    Diaposon,
    Operator,
    Location,
)


def get_data() -> Generator[List[str], None, None]:
    """
    Getting csv numbers data from rossvyaz.ru
    """
    links = (
        'https://rossvyaz.ru/data/ABC-3xx.csv',
        'https://rossvyaz.ru/data/ABC-4xx.csv',
        'https://rossvyaz.ru/data/ABC-8xx.csv',
        'https://rossvyaz.ru/data/DEF-9xx.csv',
    )
    for link in links:
        print(link)
        response = requests.get(link)
        response.raise_for_status()
        data = response.content.decode('utf-8').splitlines()
        for row in data:
            yield row.split(';')


def reparse() -> None:
    """
    Reparsing numbers, locations and operators
    """
    Base.metadata.create_all(engine)
    # Есть косяк в том, что в период между очисткой базы и новым заполнением сервис будет
    # работать некорректно. Это можно исправить временной базой, либо, если точно знать правила
    # перераспределения адресов между операторами, обновлением текущей без полной очистки.
    Diaposon.truncate()
    INDEX_OF_LOCATION = 5
    INDEX_OF_OPERATOR = 4
    INDEX_OF_CODE = 0
    INDEX_OF_START = 1
    INDEX_OF_END = 2
    operators: Dict[str, int] = {}
    locations: Dict[str, int] = {}
    session = Session()
    counter = 0
    total_counter = 0
    time_start = time.time()
    for record in get_data():
        try:
            start = int(record[INDEX_OF_CODE] + record[INDEX_OF_START])
            end = int(record[INDEX_OF_CODE] + record[INDEX_OF_END])
            record_location = record[INDEX_OF_LOCATION]
            record_operator = record[INDEX_OF_OPERATOR]
            if record_operator not in operators:
                phone_operator = Operator(name=record_operator)
                session.add(phone_operator)
                session.flush()
                session.refresh(phone_operator)
                operators[phone_operator.name] = phone_operator.id
            if record_location not in locations:
                phone_location = Location(name=record_location)
                session.add(phone_location)
                session.flush()
                session.refresh(phone_location)
                locations[phone_location.name] = phone_location.id
            session.add(
                Diaposon(
                    start=start,
                    end=end,
                    operator=operators[record_operator],
                    location=locations[record_location]
                ),
            )
            counter += 1
            total_counter += 1
            print(str(total_counter))
            if counter >= 100000:
                print("commit...")
                counter = 0
                session.commit()
        except OperationalError:
            print("OperationalError")
            time.sleep(10)
            continue
    session.commit()
    session.close()
    print("total records in %s seconds" % (time.time() - time_start))


if __name__ == '__main__':
    print("reparse start...")
    reparse()
    print("reparce end. Waiting...")
    time.sleep(60 * 60 * 24)
