import django
django.setup()
from datamad2.models import Grant
from datetime import date
import re

g = Grant.objects.filter(importedgrant__actual_start_date__lte=date(2023, 3, 31), 
                         importedgrant__actual_end_date__gte=date(2022, 4, 1)).order_by("assigned_data_centre__name", 
                                "importedgrant__scheme", "importedgrant__call")

print(len(g))
grant_numbers = set()
schemes = {}
calls = {}

for gg in g:
    if gg.grant_ref in grant_numbers: continue
    
    ig = gg.importedgrant
    grant_numbers.add(gg.grant_ref)
    amount = ig.amount_awarded
    if amount is None: amount = 0
    period = ig.actual_end_date - ig.actual_start_date
    rate = amount/period.days
    start_in_year = min(max(date(2022, 4, 1), ig.actual_start_date), date(2023, 3, 31))
    end_in_year = max(min(date(2023, 3, 31), ig.actual_end_date), date(2022, 4, 1))
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
 
    print(DC, call, gg.grant_ref, fy_cost, in_year_period, rate, period, amount)

    if DC not in calls: calls[DC] = {}
    dc_calls = calls[DC] 
    if call in dc_calls:
        dc_calls[call]["number"] += 1
        dc_calls[call]["cost"] += fy_cost
    else:
        dc_calls[call] = {"number": 1, "cost": fy_cost, "scheme": ig.scheme, "DC": DC, "grant_type": ig.grant_type}

for s in schemes:
    print(s, schemes[s]["number"], schemes[s]["cost"])


print()
print(f'Data Centre, Scheme, Programme, Number of grants, DM cost')

for dc in calls:
    for c in calls[dc]:
        call = calls[dc][c]
        print(f'{call["DC"]}, {call["grant_type"]}, {call["scheme"]}, {c}, {call["number"]}, {call["cost"]}')