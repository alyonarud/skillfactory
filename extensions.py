import json
import requests
from config import keys, keys_more


class APIException(Exception):
    pass

# [name for name, age in mydict.items() if age == search_age]
# condition_if_true if condition else condition_if_false

class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            if base in keys.values():
                base_key = base
            else:
                base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            if sym in keys.values():
                sym_key = sym
            else:
                sym_key = keys[sym.lower()]

        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        #r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key=fd894c54262d04c12144fa038ee2d25d&base={base_key}&symbols={sym_key}")
        r = requests.get(
            f"https://min-api.cryptocompare.com/data/pricemulti?api_key=8f2d6e2ab4be8be2b015f3d76ca88f9e90169ccf70c2d2b434c8830851f1eec0&fsyms={base_key}&tsyms={sym_key}")

        resp = json.loads(r.content)
        new_price = resp[base_key][sym_key] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message


def key_get(dict1,search_value):
    for key,keyv in dict1.items():
        if keyv == search_value:
            return key

class Convertor_more:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            if base in keys_more.values():
                #base_key = keys_more[base.lower()]
                # по значению получить индекс
                base_key = key_get(keys_more, base)
            else:
                base_key = base.upper()

        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            if sym in keys_more.values():
                sym_key = key_get(keys_more, sym)
            else:
                sym_key = sym.upper()

        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        #r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key=fd894c54262d04c12144fa038ee2d25d&base={base_key}&symbols={sym_key}")
        r = requests.get(
            f"https://min-api.cryptocompare.com/data/pricemulti?api_key=8f2d6e2ab4be8be2b015f3d76ca88f9e90169ccf70c2d2b434c8830851f1eec0&fsyms={base_key}&tsyms={sym_key}")

        resp = json.loads(r.content)
        new_price = resp[base_key][sym_key] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message