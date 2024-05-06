import random


def random_terminal_data():
    data = {
        'terminalHandlerId': ''.join(random.choices('0123456789', k=5)),
        'terminalId': ''.join(random.choices('0123456789', k=8)),
        'enabled': random.choice([True, False]),
        'payeeCode': ''.join(random.choices('0123456789', k=11)),
        'slave': random.choice([True, False]),
        'pagoPa': False,
        'idpay': random.choice([True, False]),
    }
    return data
