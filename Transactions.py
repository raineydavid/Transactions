import json
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import Counter


#gives the frequency of all suppliers from the data
def supplier_freq(data):
    #gets the suppliers from the data
    suppliers = [entry["Supplier"] for entry in data]
    #uses the counter library to create a dictionary of the suppliers and number of times used
    count = dict(zip(Counter(suppliers).keys(),Counter(suppliers).values()))
    #sorts the count dictionary from smallest to largest
    count = {k: v for k, v in sorted(count.items(), key=lambda item: item[1],reverse=True)}
    return count

def cum_spend_per_date(_dict,supplier,dates):
    spending = {date:0 for date in dates}
    for sup in _dict[supplier]:
        #try:
        spending[sup["Date"]] = sup["Transaction value (Â£)"]
        #except:
               #pass
    cum_spend=list(np.cumsum(list(spending.values())))
    spending = {list(spending.keys())[i]:cum_spend[i] for i in range(0,len(cum_spend))}
    return spending          

def spending_per_supplier(data):
    spending = [{x:entry[x] for x in ["Date","Transaction value (Â£)","Supplier"]} for entry in data]
    suppliers = supplier_freq(data).keys()
    dates = list(dict.fromkeys([entry["Date"] for entry in data]))
    _dict = {supplier:[{x:entry[x] for x in ["Date","Transaction value (Â£)"]} for entry in data if entry["Supplier"] == supplier] for supplier in suppliers}
    for supplier in suppliers:
        for d in _dict[supplier]:
            d["Transaction value (Â£)"] = float(d["Transaction value (Â£)"].replace(',',''))
    date_cum_spend_per_supplier = {x:cum_spend_per_date(_dict,x,dates) for x in suppliers}
    return date_cum_spend_per_supplier

def main():
    #load in the JSON file
    with open("sqlify-export-d009c6ceb1ef4.json","r") as read_file:
        data = json.load(read_file)
    suppliers=spending_per_supplier(data)


main()