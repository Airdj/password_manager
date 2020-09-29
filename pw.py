#!/usr/bin/python3
#pw.py simple password manager

import sys
import pyperclip
import pickle
import os.path
import getpass

def load_data(path):
    with open(r'{}'.format(path), 'rb') as file:
        loaded_dict = pickle.load(file)
        return loaded_dict


def save_data(path, passwords):
    with open(r'{}'.format(path), 'wb') as file:
        pickle.dump(passwords, file)


def file_checker(path, passwords):
    if os.path.isfile(path):
        pass
    else:
        save_data(path, passwords)


def add_acc(passwords):
    forbidden_words = ('menu', 'add', 'list', 'quit', 'remove')
    account_name = input('Please write your account name: ')
    account_password = input('Please write your account password: ')
    if account_name not in forbidden_words:
        passwords[account_name] = account_password
    else:
        print(f'Sorry but you cant use: {forbidden_words} as an account name.')


def list_acc(passwords):
    for k in passwords.keys():
        print(f'Account name: {k}')


def remove_acc(passwords):
    account_name = input('What account would you like to remove? ')
    if account_name in passwords:
        del passwords[account_name]
        print(f'Account: {account_name} - removed.')
    else:
        print(f'No account called: {account_name}.')


def get_arg(passwords):
    account = sys.argv[1]

    if account in passwords:
        pyperclip.copy(passwords[account])
        print(f'Password for {account} copied to clippboard.')
    elif account == 'menu':
        show_menu(passwords)
    else:
        print(f'There is no account named {account}')


def menu(option, passwords):
    menu_dict = {'add': add_acc, 'list': list_acc, 'remove': remove_acc, 'quit': sys.exit}
    if option not in menu_dict:
        print('Wrong option.')
        sys.exit()
    elif option == 'quit':
        menu_dict[option]()
    else:
        return menu_dict[option](passwords)


def show_menu(passwords):
    while 1:
        print('''
        Menu:
        add - adding account and password.
        list - list existing accounts.
        remove - remove chosen account.
        quit - quit.
        ''')
        option = input('What would you like to do ? ')
        menu(option, passwords)


def main():
    user = getpass.getuser()
    path = f'/home/{user}/pickled_passwords'
    my_passwords = {}

    file_checker(path, my_passwords)

    try:
        my_passwords = load_data(path)

    except Exception as e:
        print(f'Error loading file. Message:{e}')
        sys.exit()

    if len(sys.argv) < 2:
        print('Usage: pw [account] - copy account password.')
        print('Write: pw menu - to see available options.')
        sys.exit()
    try:
        get_arg(my_passwords)
    except Exception as e:
        print(f'Ooops something went wrong.Error code: {e}')
    finally:
        save_data(path, my_passwords)


if __name__ == '__main__':
    main()
