import csv
import os
BILLS_CSV = 'bills.csv'
def read_bills():
    if not os.path.exists(BILLS_CSV):
        return []
    with open(BILLS_CSV, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)
cosmic = read_bills()
#print(cosmic)

dynamite = []
for bill in cosmic:
    kepler = []
    for pic in bill[3::]:
        if "RK" in pic:
           z =  pic.split(":")
           kepler.append(bill[0])
           kepler.append(z[1])
           dynamite.append(kepler)
print(dynamite)

