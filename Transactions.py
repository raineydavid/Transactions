import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.animation import FuncAnimation
from collections import Counter
from datetime import datetime


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
        spending[sup["Date"]] = sup["Transaction value (Â£)"]
    cum_spend=list(np.cumsum(list(spending.values())))
    spending = {list(spending.keys())[i]:cum_spend[i] for i in range(0,len(cum_spend))}
    return spending          



def main():
    data = pd.read_csv("25000_spend_dataset.csv",usecols = ["Date","Supplier","Transaction value"])
    data["Date"] = [datetime.strptime(date, '%d/%m/%Y') for date in data["Date"]]
    dates = data["Date"]
    #dates.drop_duplicates(inplace=True)
    suppliers = list(data["Supplier"].drop_duplicates())
    frames=[]
    for supplier in suppliers:
        sup_data = data[data['Supplier'].eq(supplier)]
        cum=sup_data['Transaction value'].cumsum()
        sup_data['Cummulative'] = cum
        df = pd.DataFrame({'Supplier':[supplier]*len(dates),'Date':dates,'Cummulative': sup_data[dates.eq(sup_data['Date'])]["Cummulative"]})
        df.fillna(method='ffill',inplace=True)
        df.fillna(value=0,inplace=True)
        frames.append(df)
    cum_data = pd.DataFrame(pd.concat(frames)).reset_index(drop=True)
    def draw_barchart(date):
        dff = cum_data[cum_data['Date'].eq(date)].sort_values(by='Cummulative', ascending=True).tail(10)
        ax.clear()
        ax.barh(dff['Supplier'], dff['Cummulative'])
        dx = dff['Cummulative'].max() / 200
        for i, (value, name) in enumerate(zip(dff['Cummulative'], dff['Supplier'])):
            ax.text(value-dx, i,     name,           size=14, weight=600, ha='right', va='bottom')
            ax.text(value+dx, i,     f'{value:,.0f}',  size=14, ha='left',  va='center')
        # ... polished styles
        ax.text(1, 0.4, date, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
        ax.text(0, 1.06, 'Total transactions value (£)', transform=ax.transAxes, size=12, color='#777777')
        ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        ax.xaxis.set_ticks_position('top')
        ax.tick_params(axis='x', colors='#777777', labelsize=12)
        ax.set_yticks([])
        ax.margins(0, 0.01)
        ax.grid(which='major', axis='x', linestyle='-')
        ax.set_axisbelow(True)
        ax.text(0, 1.12, 'The most expensed suppliers from April 2016 to Feb 2020',
                transform=ax.transAxes, size=24, weight=600, ha='left')
        plt.box(False)
    fig, ax = plt.subplots(figsize=(15, 8))
    animator = FuncAnimation(fig, draw_barchart, frames=dates)
    plt.show()


main()