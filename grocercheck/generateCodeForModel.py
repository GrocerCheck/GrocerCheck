days = ["mon",'tue','wed','thu','fri','sat','sun']

for day in days:
    for i in range(0,24):
        if(i<10):
            i = '0'+str(i)
        else:
            i = str(i)
        print(day+i+' = models.IntegerField(null=True)')
