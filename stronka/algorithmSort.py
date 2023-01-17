# import json
# import collections
# import itertools as it
# import operator as op


# class SortingAlgorithm:
#     def __init__(self, products):
#         self.products = products
#         searched = []
#         for product in self.products:
#             if product['nazwa'] not in searched:
#                 searched.append(product['nazwa'])

#         self.isFound = {item: 0 for item in searched}
#         self.productsInBlocks = {}
#         self.searchedQTY = len(searched)

#     def resetSearched(self):
#         temp = self.isFound.keys()
#         self.isFound = {item: 0 for item in temp}
#         self.productsInBlocks = {}

#     def agregateBy(self, key):
#         for product in self.products:
#             if self.productsInBlocks.get(product[key]) != None:
#                 self.productsInBlocks[product[key]].append(product)
#             else:
#                 self.productsInBlocks[product[key]] = []
#                 self.productsInBlocks[product[key]].append(product)

#     def sort_by_price(self, products):
#         sorted_products = sorted(products, key=lambda x: x["cena"])
#         print(json.dumps(sorted_products, indent=2))
#         return sorted_products

#     def show(self):
#         print(json.dumps(self.productsInBlocks, indent=2))

#     def dataIntoSets(self):
#         ### the fewest shops
#         self.resetSearched()
#         DataTFS = {}
#         grouped_products = {sklep: list(group) for sklep, group in it.groupby(self.products, key=lambda x: x["sklep"])}
#         sorted_groups = {sklep: group for sklep, group in sorted(grouped_products.items(), key=lambda x: len(x[1]), reverse=True)}
#         sorted_group_by_sum = {sklep: group for sklep, group in sorted(sorted_groups.items(), key=lambda x: sum(item['cena'] for item in x[1]))}
#         self.productsInBlocks = sorted_group_by_sum

#         tempList = []
#         itemsCounter = 0
#         DataTFS["products"] = []
#         for _, vendorItems in self.productsInBlocks.items():
#             for item in vendorItems:
#                 if not self.isFound[item["nazwa"]]:
#                     self.isFound[item["nazwa"]] = 1
#                     itemsCounter += 1
#                     DataTFS["products"].append(item)
#             if itemsCounter == self.searchedQTY:
#                 break

#         ### the lowest price

#         self.resetSearched()
#         self.agregateBy("nazwa")

#         tempList = [
#             [item["ID"] for item in self.productsInBlocks[nazwa]]
#             for nazwa in self.productsInBlocks
#         ]
#         combinationsOfItems = list(it.product(*tempList))

#         DataTLP = {}
#         listOfVendors = []

#         for combination in combinationsOfItems:
#             fullPrice = 0
#             for itemId in combination:
#                 fullPrice += self.products[itemId]["cena"]
#                 if not self.products[itemId]["sklep"] in listOfVendors:
#                     listOfVendors.append(self.products[itemId]["sklep"])
#                     fullPrice += self.products[itemId]["cena dostawy"]
#             DataTLP[combination] = fullPrice
#         DataTLP = sorted(DataTLP.items(), key=lambda x: x[1])[0]
#         products = []
#         for id in DataTLP[0]:
#             products.append(self.products[id])
#         DataTLP = {}
#         DataTLP["products"] = products
#         sorted(products, key=lambda x: x["cena"])
#         return {"TFS": DataTFS["products"], "TLP":sorted(DataTLP["products"], key=lambda x: x["sklep"])}


# if __name__ == "__main__":
#     searchingFor = ["Klocki Lego 123456", "Motorek", "Book"]
#     f = open("./produkty.json")
#     products = json.load(f)["products"]
#     f.close()
#     #print(products)
#     sortowanie = SortingAlgorithm(products)
#     # sortowanie.agregateBy("vendor")
#     # sortowanie.show()
#     sortowanie.dataIntoSets()
#     #print(json.dumps(sortowanie.dataIntoSets(), indent=2))


###############################


import json
import itertools as it

class ProductGrouping:
    def __init__(self, products):
        self.products = products

    def group_by(self, key_e):
        return {key: list(group) for key, group in it.groupby(self.products, key=lambda x: x[key_e])}

    def sort_by_price(self, products):
        return sorted(products, key=lambda x: x["cena"])

    def sort_by_shop_count(self, group_by_shop):
        return {shop: group for shop, group in sorted(group_by_shop.items(), key=lambda x: len(x[1]), reverse=True)}

    def sort_by_shop_sum(self, group_by_shop):
        return {shop: group for shop, group in sorted(group_by_shop.items(), key=lambda x: sum(item['cena'] for item in x[1]))}

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
        group_by_shop = ProductGrouping(self.products).sort_by_shop_count(ProductGrouping(self.products).group_by("sklep"))
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
                    fullPrice += self.products[itemId]["cena dostawy"]
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
    print("TLP")
    print(json.dumps(TLP.get_products(),indent=2))
    print("TFS")
    print(json.dumps(TFS.get_products(),indent=2))
