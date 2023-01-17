import json
import collections
import itertools


class SortingAlgorithm:
    def __init__(self, products):
        self.products = self.sort_by_price(products)
        searched = []
        for product in self.products:
            if product['nazwa'] not in searched:
                searched.append(product['nazwa'])

        self.isFound = {item: 0 for item in searched}
        self.productsInBlocks = {}
        self.searchedQTY = len(searched)

    def resetSearched(self):
        temp = self.isFound.keys()
        self.isFound = {item: 0 for item in temp}
        self.productsInBlocks = {}

    def agregateBy(self, key):
        for product in self.products:
            if self.productsInBlocks.get(product[key]) != None:
                self.productsInBlocks[product[key]].append(product)
            else:
                self.productsInBlocks[product[key]] = []
                self.productsInBlocks[product[key]].append(product)

    def sort_by_price(self, products):
        sorted_products = sorted(products, key=lambda x: x["cena"])
        for i, product in enumerate(sorted_products):
            product["ID"] = i
        return sorted_products

    def show(self):
        print(json.dumps(self.productsInBlocks, indent=2))

    def dataIntoSets(self):
        ### the fewest shops
        self.resetSearched()
        DataTFS = {}
        self.agregateBy("sklep")

        tempDict = {
            tempVendorName: len(self.productsInBlocks[tempVendorName])
            for tempVendorName in self.productsInBlocks
        }
        tempDict = collections.OrderedDict(sorted(tempDict.items()))
        tempDict = {
            tempVendorName: self.productsInBlocks[tempVendorName]
            for tempVendorName in tempDict
        }

        self.productsInBlocks = tempDict
        itemsCounter = 0

        tempList = []
        DataTFS["products"] = []
        for _, vendorItems in self.productsInBlocks.items():
            for item in vendorItems:
                if not self.isFound[item["nazwa"]]:
                    self.isFound[item["nazwa"]] = 1
                    itemsCounter += 1
                    DataTFS["products"].append(item)
            if itemsCounter == self.searchedQTY:
                break
        

        # print(json.dumps(DataTFS,indent=2))

        ### the lowest price

        self.resetSearched()
        self.agregateBy("nazwa")

        tempList = [
            [item["ID"] for item in self.productsInBlocks[nazwa]]
            for nazwa in self.productsInBlocks
        ]
        combinationsOfItems = list(itertools.product(*tempList))

        DataTLP = {}
        listOfVendors = []

        for combination in combinationsOfItems:
            fullPrice = 0
            for itemId in combination:
                fullPrice += self.products[itemId]["cena"]
                if not self.products[itemId]["sklep"] in listOfVendors:
                    listOfVendors.append(self.products[itemId]["sklep"])
                    fullPrice += self.products[itemId]["cena dostawy"]
            DataTLP[combination] = fullPrice
        DataTLP = sorted(DataTLP.items(), key=lambda x: x[1])[0]
        products = []
        for id in DataTLP[0]:
            products.append(self.products[id])
        DataTLP = {}
        DataTLP["products"] = products
        sorted(products, key=lambda x: x["cena"])
        return {"TFS": sorted(DataTFS["products"], key=lambda x: x["sklep"]), "TLP":sorted(DataTLP["products"], key=lambda x: x["sklep"])}


if __name__ == "__main__":
    searchingFor = ["Klocki Lego 123456", "Motorek", "Book"]
    f = open("./produkty.json")
    products = json.load(f)["products"]
    f.close()
    #print(products)
    sortowanie = SortingAlgorithm(products)
    # sortowanie.agregateBy("vendor")
    # sortowanie.show()
    print(json.dumps(sortowanie.dataIntoSets(), indent=2))
