from collections import UserDict
from collections.abc import Iterator
from datetime import datetime, timedelta
import re,json
from dataclasses import asdict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self) -> str:
        return str(self)

class Name(Field):
    def __str__(self):
        return super().__str__()


class Phone(Field):
    ...
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, nv):
        if nv.isdigit() and (len(nv) == 10 or len(nv) == 11 or len(nv) == 12):
            self._value = nv
        else:
            raise ValueError("Phone number must have a proper length and consist only of digits")



class Birthday(Field):

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, nv):
        input_date_true = r"\d{1,2}\.\d{1,2}\.\d{4}"
        if nv == 'None':
            self._value = None
        elif re.match(input_date_true, nv):
            self._value = nv
        else:
            raise ValueError("Invalid birthday! Please input in format d.m.y")


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone: Phone, from_load=False):
        if not from_load and phone.value in [p.value for p in self.phones]:
            return f'{phone} already exists in {self.name}`s phones'
        else:
            self.phones.append(phone)
            return f'Phone {phone} added to {self.name}'    
    
    def __str__(self) -> str:

        phones = ", ".join(p.value for p in self.phones)

        if self.birthday is None:
            birthday = 'Unknown'
        else:
            birthday = self.birthday.value

        return f'{self.name}: {phones}; Birthday: {birthday}'

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        if new_phone.value in [p.value for p in self.phones]:
            return f'{new_phone} already exist in {self.name}`s phones'
        else:
            for idx, p in enumerate(self.phones):
                if old_phone.value == p.value:
                    self.phones[idx] = new_phone
                    return f"{self.name}`s {old_phone} change to {new_phone}"
            return f'{old_phone} not in {self.name}`s phones'

    def days_to_birthday(self, name: str):
        if self.birthday is None:
            return f"{name}'s birthday is unknown."
        else:
            today = datetime.now().date()
            birth = datetime.strptime(str(self.birthday), "%d.%m.%Y").date()
            
            next_birthday = datetime(today.year, birth.month, birth.day).date()
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, birth.month, birth.day).date()
            timedelta = next_birthday - today
            if timedelta.days == 0:
                return f"Today is {name}'s birthday!"
            elif timedelta.days == 1:
                return f"{name}'s birthday is tomorrow."
            else:
                return f"{name}'s birthday is in {timedelta.days} day(s)."
            
class AddressBook(UserDict):

    

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        
        return f'Success!\nContact {record} '
    
    def __str__(self) -> str:
        return '\n'.join(str(rec) for rec in self.data.values())
    
    def delete_record(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record {name} deleted"
        return f"No record found with name {name}"
    
    def search(self, search_field):
            results = []
            for record in self.values():
                if isinstance(search_field, Name) and search_field.value.lower() in record.name.value.lower():
                    phones = ', '.join(str(phone) for phone in record.phones)
                    results.append(f"{record.name} : {phones}")
                elif isinstance(search_field, Phone) and any(search_field.value == phone.value for phone in record.phones):
                    results.append(f"{record.name} : {search_field.value}")
            if results:
                return '\n'.join(results)
            return "No matching records found."
    
    def save_data(self, filename = 'phone_book.json'):
        # Серіалізуємо записи
        records = {}
        for name, record in self.data.items():
            if record.birthday is None:
                birthday = 'None'
            else:  
                birthday = record.birthday.value
            records[name] = {
                'name': str(record.name),
                'phones': [str(phone) for phone in record.phones],
                'birthday': birthday
                }

        with open(filename, 'w') as f:
            json.dump({"data": records}, f)

    @classmethod
    def load_data(cls, filename='phone_book.json'):
        with open(filename) as f:
            data = json.load(f)

        ab = cls()

        # Десеріалізуємо записи    
        for name, rec_dict in data['data'].items():
            name = Name(name)
            phones = [Phone(p) for p in rec_dict['phones']]
            birthday = None
            if 'birthday' in rec_dict and rec_dict['birthday'] != 'None':
                birthday = Birthday(rec_dict['birthday'])

            # Перевірка, чи існує запис з таким ім'ям в AddressBook
            if name in ab.data:
                record = ab.data[name]
                for phone in phones:
                    record.add_phone(phone)
            else:
                # Якщо запису немає, додати новий
                ab.add_record(Record(name, phones[0], birthday))

                # Додати інші номери телефонів (якщо вони є)
                for phone in phones[1:]:
                    ab[name].add_phone(phone)

        return ab
