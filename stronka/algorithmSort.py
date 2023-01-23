import json
import itertools as it


class ProductGrouping:
    def __init__(self, products):
        self.products = products

    def group_by(self, key_e):
        return {key: list(group) for key, group in it.groupby(sorted(self.products, key=lambda x: x[key_e]), key=lambda x: x[key_e])}

    def sort_by_price(self, products):
        return sorted(products, key=lambda x: x["cena"])

    def sort_by_shop_count(self, group_by_shop):
        return {shop: group for shop, group in sorted(group_by_shop.items(), key=lambda x: len(x[1]), reverse=True)}

    def sort_by_shop_sum(self, group_by_shop):
        new_data = {}
        for shop, products in group_by_shop.items():
            size = len(products)
            if size not in new_data:
                new_data[size] = {}
            new_data[size][shop] = products

        for size, shops in new_data.items():
            new_data[size] = {shop: products for shop, products in sorted(shops.items(), key=lambda x: sum(p["cena"] for p in x[1]))}

        original_data = {}
        for size, shops in new_data.items():
            for shop, products in shops.items():
                original_data[shop] = products
        return original_data


class ProductsWithFewestShops:
    def __init__(self, products):
        self.products = products
        self.searched = []
        self.searchedQTY = 0
        self.isFound = {}

    def get_unique_products(self):
        for product in self.products:
            if product['nazwa'] not in self.searched:
                self.searched.append(product['nazwa'])
        self.searchedQTY = len(self.searched)
        self.isFound = {item: 0 for item in self.searched}

    def get_products(self):
        self.get_unique_products()
        group_by_shop = ProductGrouping(self.products).sort_by_shop_count(
            ProductGrouping(self.products).group_by("sklep"))
        print(json.dumps(group_by_shop, indent=2))
        group_by_shop = ProductGrouping(self.products).sort_by_shop_sum(group_by_shop)
        tempList = []
        itemsCounter = 0
        for _, vendorItems in group_by_shop.items():
            for item in vendorItems:
                if not self.isFound[item["nazwa"]]:
                    self.isFound[item["nazwa"]] = 1
                    itemsCounter += 1
                    tempList.append(item)
            if itemsCounter == self.searchedQTY:
                break
        return tempList


class ProductsWithLowestPrice:

    def __init__(self, products):
        self.products = products
        self.combinationsOfItems = []
        self.DataTLP = {}
        self.listOfVendors = []

    def get_combinations(self):
        group_by_name = ProductGrouping(self.products).group_by("nazwa")
        tempList = [
            [item["ID"] for item in group_by_name[nazwa]]
            for nazwa in group_by_name
        ]
        self.combinationsOfItems = list(it.product(*tempList))

    def get_products(self):
        self.get_combinations()
        for combination in self.combinationsOfItems:
            fullPrice = 0
            for itemId in combination:
                fullPrice += self.products[itemId]["cena"]
                if not self.products[itemId]["sklep"] in self.listOfVendors:
                    self.listOfVendors.append(self.products[itemId]["sklep"])
                    fullPrice += self.products[itemId]["cena_dostawy"]
            self.DataTLP[combination] = fullPrice
        self.DataTLP = sorted(self.DataTLP.items(), key=lambda x: x[1])[0]
        products = []
        for id in self.DataTLP[0]:
            products.append(self.products[id])
        return ProductGrouping(products).sort_by_price(products)


if __name__ == "__main__":
    f = open("./produkty.json")
    products = json.load(f)["products"]
    f.close()
    TLP = ProductsWithLowestPrice(products)
    TFS = ProductsWithFewestShops(products)
    # print("TLP")
    # print(json.dumps(TLP.get_products(), indent=2))
    print("TFS")
    print(json.dumps(TFS.get_products(), indent=2))
