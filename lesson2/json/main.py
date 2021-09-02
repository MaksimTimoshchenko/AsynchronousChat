import getopt, sys
import json


def write_order_to_json(item, quantity, price, buyer, date):
    json_dict = {
        "Item": item,
        "Quantity": quantity,
        "Price": price,
        "Buyer": buyer,
        "Date": date
    }

    with open('order.json', 'w') as f_n:
        json.dump(json_dict, f_n, indent=4)
    return True


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:q:p:b:d:", ["item=", "quantity=", "price=", "buyer=", "date="])
        item, quantity, price, buyer, date = (None for _ in range(5))
        verbose = False
        for o, a in opts:
            if o in ("-i", "--item"):
                item = a
            elif o in ("-q", "--quantity"):
                quantity = a
            elif o in ("-p", "--price"):
                price = a
            elif o in ("-b", "--buyer"):
                buyer = a
            elif o in ("-d", "--date"):
                date = a
            else:
                assert False, "Unhandled option"

        if item and quantity and price and buyer and date:
            write_order_to_json(item, quantity, price, buyer, date)
        else:
            print('main.py -i <item:str> -q <quantity:int> -p <price:float> -b <buyer:str> -d <date:datetime>')
            sys.exit(2)
    except getopt.GetoptError as err:
        print('Error while getting options')
        sys.exit(2)