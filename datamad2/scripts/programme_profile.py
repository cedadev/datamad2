import django
django.setup()
from datamad2.models import Grant
from datetime import date
import re
import sys

call = sys.argv[1]

g = Grant.objects.filter(importedgrant__call__startswith=call).order_by("assigned_data_centre__name", 
                                "importedgrant__scheme", "importedgrant__call")

print(len(g))
schemes = {}
calls = {}

min_date = date(2100, 1, 1)
max_date = date(1970, 1, 1)
for gg in g:
    if gg.importedgrant.actual_start_date < min_date:
        min_date = gg.importedgrant.actual_start_date
    if gg.importedgrant.actual_end_date > max_date:
        max_date = gg.importedgrant.actual_end_date
    

print(min_date, max_date)
start_year = min_date.year
end_year = max_date.year+1
years = range(start_year, end_year)
print(start_year, end_year, years)

grant_numbers = set()

for year in years:
    for gg in g:
        if f"{gg.grant_ref}.{year}" in grant_numbers: continue
    
        ig = gg.importedgrant
        grant_numbers.add(f"{gg.grant_ref}.{year}")
        amount = ig.amount_awarded
        if amount is None: amount = 0
        period = ig.actual_end_date - ig.actual_start_date
        rate = amount/period.days
        start_in_year = min(max(date(year, 4, 1), ig.actual_start_date), date(year+1, 3, 31))
        end_in_year = max(min(date(year+1, 3, 31), ig.actual_end_date), date(year, 4, 1))
        in_year_period = end_in_year-start_in_year 
        fy_cost = in_year_period.days * rate * 0.021   

        if ig.scheme in schemes:
            schemes[ig.scheme]["number"] += 1
            schemes[ig.scheme]["cost"] += fy_cost
        else:
            schemes[ig.scheme] = {"number": 1, "cost": fy_cost}

        call = ig.call.strip()
        call = re.sub('\s+(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\d\d$', '', call)

        DC = gg.assigned_data_centre
        if DC: DC = DC.name
        else: DC = "unassigned"
 
        print(DC, call, gg.grant_ref, fy_cost, in_year_period, rate)

        if DC not in calls: calls[DC] = {}
        if year not in calls[DC]: calls[DC][year] = {}
        dc_calls = calls[DC][year] 
        if call in dc_calls:
            dc_calls[call]["number"] += 1
            dc_calls[call]["cost"] += fy_cost
        else:
            dc_calls[call] = {"number": 1, "cost": fy_cost, "scheme": ig.scheme, "DC": DC, "grant_type": ig.grant_type}

for s in schemes:
    print(s, schemes[s]["number"], schemes[s]["cost"])


print()
print(f'Data Centre, Scheme, Programme, Number of grants, DM cost')

print(calls)

for dc in calls:
    print(dc)
    for year in calls[dc]:
        print(year)         
        for c in calls[dc][year]:
            call = calls[dc][year][c]
            print(f'{call["DC"]}, {call["grant_type"]}, {call["scheme"]}, {c}, {call["number"]}, {call["cost"]}')