from collections import UserDict
from collections.abc import Iterator
from datetime import datetime, timedelta
import re


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



class Birtday(Field):

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, nv):
        input_date_true = r"\d{1,2}\.\d{1,2}\.\d{4}"
        if re.match(input_date_true, nv):
            self._value = nv
        else:
            raise ValueError("Invalid birthday! Please input in format d.m.y")


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birtday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f'phone {phone} add to {self.name}'
        return f'{phone} already exist in {self.name}`s phones'
    
    def __str__(self) -> str:
        return f'{self.name}: {", ".join(str(p) for p in self.phones)}; Birthday: {self.birthday}'

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

    def __init__(self, N=1):
        super().__init__()
        self.N = N

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
    
    def __iter__(self):
        self.items = list(self.data.items())
        self.stop_iter = len(self.items) // self.N
        self.start_iter = 0
        self.start = 0
        self.stop = self.N
        return self

    def __next__(self):
        if self.start_iter < self.stop_iter:
            result = self.items[self.start:self.stop]
            self.start += self.N
            self.stop += self.N
            self.start_iter += 1
            return ', '.join([f'{key}: {str(value)}' for key, value in result])
        else:
            raise StopIteration

    

if __name__ =="__main__":
    ab = AddressBook()
    name = Name('bill')
    phone = Phone('23456')
    rec = Record(name, phone)
    name1 = Name('LOL')
    phone1 = Phone('11111')
    rec1 = Record(name, phone)
    ab[name] = phone
    ab[name1] = phone1

    name3 = Name('GFF')
    phone3 = Phone('999999')
    rec3 = Record(name, phone)
    name4 = Name('NONO')
    phone4 = Phone('00000')
    rec4 = Record(name, phone)
    ab[name3] = phone3
    ab[name4] = phone4
    
    for i in ab:
        print(i)