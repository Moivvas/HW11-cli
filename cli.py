from ab_classes import AddressBook, Name, Phone, Record, Birtday

ab = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ValueError as v:
            return str(v)
        except IndexError as i:
            return str(i)
        except TypeError as t:
            return str(t)
    return wrapper

@input_error
def add(*args):
    if len(args) == 2:
        name = Name(args[0])
        phone = Phone(args[1])
        rec: Record = ab.data.get(str(name))
        if rec:
            return rec.add_phone(phone)
        rec = Record(name, phone)
        return ab.add_record(rec)
    elif len(args) == 3:
        name = Name(args[0])
        phone = Phone(args[1])
        birthday = Birtday(args[2])
        rec: Record = ab.data.get(str(name))
        if rec:
            return rec.add_phone(phone)
        rec = Record(name, phone, birthday)
        return ab.add_record(rec)
    

def change_phone(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec:Record = ab.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f'{old_phone} does`t exist'

def delete_record(*args):
    name = Name(args[0])
    rec = ab.get(str(name))
    if rec:
        ab.delete_record(str(name))
        return f"Record {name} deleted"
    return f"Address book has no contact with name {name}"

def search(*args):
    if args and args[0].isdigit():
        search_field = Phone(args[0])
    else:
        search_field = Name(args[0]) if args else None
    
    if search_field:
        return ab.search(search_field)
    return 'Try again, but check your term'

def exit_command(*args):
    return "Good bye"

def hello_command(*args):
    return 'Hi! Available'

def unknow_command(*args):
    return ' Unknow command'

def show_all(*args):
    return ab

def birthday(*args):
    name = Name(args[0])
    rec:Record = ab.get(str(name))
    if rec:
        return rec.days_to_birthday(name)
        
command_dict = {
    add: ('add', '+'),
    change_phone: ('change',),
    delete_record: ('delete', 'del'),
    exit_command: ('exit', 'close', 'good bye'),
    search: ('search', 'find'),
    hello_command: ('hello',),
    show_all: ('show all',),
    birthday: ('birthday',)
}

def parser(text:str):
    for command, kwrds in command_dict.items():
        for val in kwrds:
            if text.lower().startswith(val):
                data =text[len(val):].strip().split()
                return command, data
    return unknow_command, []

def main():
    print('Print "Hello" to start')
    while True:
        user_input = input('>>>')
        command, data = parser(user_input)
        result = command(*data)
        print(result)
        if command == exit_command:
            break
        
if __name__ == '__main__':
    main()
