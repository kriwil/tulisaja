#!/usr/bin/env python
import csv


reader = csv.DictReader(open("kriwil.csv", "rb"))
for row in reader:
    print row
