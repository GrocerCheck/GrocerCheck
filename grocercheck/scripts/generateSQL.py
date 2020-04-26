import json
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
od = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
data = json.load(open("/home/ihasdapie/Grocer_Check_Project/Org/LivePopularTimes/example_output(get_populartimes_by_PlaceID).json"))

out = ""
for d in range(7):
    for h in range(24):
        out = out + ", {daystr}{hourint} = data['populartimes'][{daynum}]['data'][{hourint}]".format(daystr=od[d], hourint = h, daynum = d)
print(out)
