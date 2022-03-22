import django
django.setup()
from datamad2.models import Grant
from datetime import date, timedelta
import re

g = Grant.objects.filter(importedgrant__actual_start_date__lte=date(2023, 3, 31), 
                         importedgrant__actual_end_date__gte=date(2022, 4, 1)).order_by("assigned_data_centre__name", 
                                "importedgrant__scheme", "importedgrant__call")

max_ingest_period = timedelta(days = 400)
year = 2022
vol_cost = 537             # per TB cost
dataset_cost = 720         # per dataset cost
dmp_support_rate = 939.0   # per year support cost
fy_start = date(year, 4, 1)
fy_end = date(year+1, 3, 31)

print(len(g))
grant_numbers = set()
schemes = {}
calls = {}

for gg in g:
    if gg.grant_ref in grant_numbers: continue
    
    ig = gg.importedgrant
    grant_numbers.add(gg.grant_ref)

    # calculate costings
    period = ig.actual_end_date - ig.actual_start_date
    ingest_period = min(max_ingest_period, period)
    ingest_start = ig.actual_end_date - ingest_period 
    start_in_year = min(max(fy_start, ig.actual_start_date), fy_end)
    ingest_start_in_year = min(max(fy_start, ingest_start), fy_end)
    end_in_year = max(min(fy_end, ig.actual_end_date), fy_start)
    in_year_period = end_in_year-start_in_year 
    in_year_ingest_period = end_in_year - ingest_start_in_year 
    print(start_in_year, ingest_start_in_year, end_in_year)

    # costs by 2.1% method
    amount = ig.amount_awarded
    if amount is None: amount = 0
    rate = amount/period.days
    fy_cost = in_year_period.days * rate * 0.021   

    # costs by cost model
    dataproducts = gg.dataproduct_set.all()
    ndatasets = len(dataproducts)
    vol = sum(map(lambda dp: dp.data_volume * 1e-12, dataproducts))
    daily_vol_rate = vol / ingest_period.days 
    daily_dataset_rate = ndatasets / ingest_period.days 
    vol_cost_in_year = daily_vol_rate * in_year_ingest_period.days * vol_cost
    dataset_cost_in_year = daily_dataset_rate * in_year_ingest_period.days * dataset_cost

    dmp_support = in_year_period.days/365. * dmp_support_rate
    print(dmp_support, vol_cost_in_year, dataset_cost_in_year)
    cost2 = dmp_support + vol_cost_in_year + dataset_cost_in_year

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
 
    print(DC, call, gg.grant_ref, fy_cost, in_year_period, rate, period, amount, cost2, dmp_support, vol_cost_in_year, dataset_cost_in_year)

    if DC not in calls: calls[DC] = {}
    dc_calls = calls[DC] 
    if call in dc_calls:
        dc_calls[call]["number"] += 1
        dc_calls[call]["cost"] += fy_cost
        dc_calls[call]["cost2"] += cost2
    else:
        dc_calls[call] = {"number": 1, "cost": fy_cost, "cost2": cost2, "scheme": ig.scheme, "DC": DC, "grant_type": ig.grant_type}

for s in schemes:
    print(s, schemes[s]["number"], schemes[s]["cost"])


print()
print(f'Data Centre, Scheme, Programme, Number of grants, DM cost')

for dc in calls:
    for c in calls[dc]:
        call = calls[dc][c]
        print(f'{call["DC"]}, {call["grant_type"]}, {call["scheme"]}, {c}, {call["number"]}, {call["cost"]}, {call["cost2"]}')