import re
import json


class cart:
    # file: file contain cart info
    # catalogue: json file contain list of item and its corresponding category
    def __init__(self, cart_file, catalogue):
        self.items = []
        self.discounts = []
        self.coupons = []
        self.sum = 0

        # from catalogue file, generate inverted index for searching category of item
        self.inverted_cata = dict()
        catalogue = json.load(catalogue)
        for key in catalogue.keys():
            for value in catalogue[key]:
                self.inverted_cata[value] = key

        # parsing every line of cart_file, store its contents into corresponding key of cart object
        for line in cart_file:
            print(line)
            self.parsing(line)

        # calculate grand total of items in cart
        self.checkout()

    def parsing(self, line):
        # check if line contain discount message
        dpattern = r"(?P<year>\d{4})\.(?:0*)(?P<month>[1-9]|1[012])\.(?:0*)(?P<day>[1-9]|[12][0-9]|3[01])\|(?P<rate>0\.\d)\|(?P<category>[\u4e00-\u9fff]+)"
        discount = re.search(
            dpattern,
            line,
        )

        # check if line contain item message
        ipattern = r"(?P<quantity>\d+)(?P<name>.+)\:(?P<price>\d+.\d{2})"
        item = re.search(
            ipattern,
            line,
        )

        # check if line contain coupon message
        cpattern = r"(?P<year>\d{4})\.(?:0*)(?P<month>[1-9]|1[012])\.(?:0*)(?P<day>[1-9]|[12][0-9]|3[01])\s(?P<min>\d+)\s(?P<denomination>\d+)"
        coupon = re.search(
            cpattern,
            line,
        )
        if discount:
            discount = discount.groupdict()
            discount["rate"] = float(discount["rate"])
            print(discount)
            self.discounts.append(discount)
        elif item:
            item = item.groupdict()
            # searching name of item in inverted index for it's category
            item["category"] = self.inverted_cata[item["name"]]
            item["price"] = float(item["price"])
            item["quantity"] = int(item["quantity"])
            self.items.append(item)
        elif coupon:
            coupon = coupon.groupdict()
            coupon["min"] = float(coupon["min"])
            coupon["denomination"] = float(coupon["denomination"])
            self.coupons.append(coupon)

    def checkout(self):

        # calculate total of each item, then add to sum
        for item in self.items:
            # check if any appliable discount
            for discount in self.discounts:
                if item["category"] == discount["category"]:
                    item["price"] *= discount["rate"]
            self.sum += item["price"] * item["quantity"]

        # apply coupon
        for coupon in self.coupons:
            if self.sum >= coupon["min"]:
                self.sum -= coupon["denomination"]
