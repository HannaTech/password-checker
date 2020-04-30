import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res


def get_password_leaks_data(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, v in hashes:
        if h == hash_to_check:
            return v
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_data(response, tail)


def read_passwords(file):
    with open(file) as f:
        return f.readlines()


def main(passwords_file):
    passwords = read_passwords(passwords_file)
    for password in passwords:
        count = pwned_api_check(password)
        if count:
            print(f'"{password}" was found {count} times...')
        else:
            print(f'"{password} "was not found! Carry on!')
    return 'done!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))

print(pwned_api_check('123'))