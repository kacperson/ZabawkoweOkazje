import json

class SortingAlgorithm:

    def __init__(self, products=None, searched=None):
        self.searched = searched
        f = open("produkty.json")
        self.products = json.load(f)["products"]
        self.productsInBlocks = {}

    def agregateBy(self, key):
        for product in self.products:
            if self.productsInBlocks.get(product[key]) != None:
                self.productsInBlocks[product[key]].append(product)
            else:
                self.productsInBlocks[product[key]] = []
                self.productsInBlocks[product[key]].append(product)

    
    
    def show(self):
        print(json.dumps(self.productsInBlocks,indent=2))
if __name__ == "__main__":

    sortowanie = SortingAlgorithm()
    sortowanie.show()
    sortowanie.agregateBy("vendor")
    sortowanie.show()