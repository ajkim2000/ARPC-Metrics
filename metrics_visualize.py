import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import calendar

def create_dateTime(date: str):
    if(date == 'nan'):
        return date

    month, date = find_and_cut(date, '/')
    day, date = find_and_cut(date, '/')
    year, date = find_and_cut(date, ' ')
    hour, date = find_and_cut(date, ':')
    minute, date = find_and_cut(date, ':')
    second, date = find_and_cut(date, ' ')

    if date == 'PM' and hour != 12:
        hour += 12

    # datetime(year, month, day, hour, minute ,second)
    return datetime.datetime(year, month, day, hour, minute, second)

def find_and_cut(to_cut: str, cut_at_char: str):

    index = to_cut.find(cut_at_char)
    cut_value = to_cut[0:index]
    to_cut = to_cut[index+1:]

    return int(cut_value), str(to_cut)

def metrics(info):
  cp = data.drop_duplicates(subset=[info], keep='first')
  cp = cp.dropna(subset=[info])
  cp = cp[[info]]
  cp = cp.reset_index(drop=True)
  length = len(cp.index)
  cp.insert(1, "Average_Time", np.zeros(length), True)
  cp.insert(2, "Total_Tickets", np.zeros(length), True)
  cp.loc[cp[info] == "Anthony J Buono", "Average_Time"] = 1
  close_t = np.zeros(length)
  close_avg = np.zeros(length)
  cnt = 0
  for index, row in cp.iterrows():
      current = closed.loc[closed[info] == row[info]]
      for index, row in current.iterrows():
          submit_time = create_dateTime(str(row['TICKET_SUBMIT_DATE']))
          resolved_time = create_dateTime(str(row['LAST_RESOLVED_DATE']))
          diff = resolved_time - submit_time
          diff = diff.total_seconds() / 3600
          close_avg[cnt] += diff
          close_t[cnt] += 1
      if close_t[cnt] != 0:
          close_avg[cnt] = close_avg[cnt] / close_t[cnt]
      cp.loc[cp[info] == row[info], "Average_Time"] = close_avg[cnt]
      cp.loc[cp[info] == row[info], "Total_Tickets"] = close_t[cnt]
      cnt += 1
  return cp

def visualizeV(lst, name, measure, asc):
    sorted = lst
    if asc:
        sorted = lst.sort_values(measure)
    plt.figure(figsize=(40,20))
    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    plt.xlabel(name, fontsize=20)
    if measure == "Average_Time":
        plt.ylabel("Average Time for Ticket Resolution (HOURS)", fontsize=20)
    elif measure == "Total_Tickets":
        plt.ylabel("Total Number of Resolved/Closed Tickets", fontsize=20)
    else:
        plt.ylabel(measure, fontsize=20)
    plt.bar(np.array(sorted[name]), np.array(sorted[measure]), color ='darkviolet', width = 0.3)

def visualizeH(lst, name, measure, asc):
    sorted = lst.sort_values(measure, ascending=asc)
    plt.figure(figsize=(40,20))
    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    if measure == "Average_Time":
        plt.xlabel("Average Time for Ticket Resolution (HOURS)", fontsize=20)
    elif measure == "Total_Tickets":
        plt.xlabel("Total Number of Resolved/Closed Tickets", fontsize=20)
    else:
        plt.xlabel(measure, fontsize=20)
    plt.ylabel(name, fontsize=20)
    plt.barh(np.array(sorted[name]), np.array(sorted[measure]).astype(int), align='center')

def visualizeTime():
    tems = data.dropna(subset=["TICKET_SUBMIT_DATE"])
    sub = []
    res = []
    first = True
    for index, row in tems.iterrows():
        sub.append(create_dateTime(str(row['TICKET_SUBMIT_DATE'])))
        res.append(create_dateTime(str(row['LAST_RESOLVED_DATE'])))
    sub = np.array(sub)
    res = np.array(res)
    begin = sub[0]
    end = sub[0]
    for id in range(len(res)):
        if begin > sub[id]:
            begin = sub[id]
        if res[id] == res[id] and res[id] != "nan":
            if end < res[id]:
                end = res[id]
        if end < sub[id]:
            end = sub[id]
    begin = datetime.datetime(begin.year, begin.month, 1, 0, 0, 0)
    end = datetime.datetime(end.year, end.month, calendar.monthrange(end.year, end.month)[1], 23, 59, 59)
    rng = round((end - begin).total_seconds() / 2592000)
    
    tnames = []
    yr = 0
    cl = 0
    for i in range(rng-1):
        tnames.append(datetime.datetime(begin.year+yr, begin.month+i+cl, 1, 0, 0, 0))
        if begin.month+1 == 12:
            yr += 1
            cl -= 12
    tnames.append(end)
    zeros = np.zeros(rng)
    threes = np.zeros(rng)
    sixs = np.zeros(rng)
    for j in range(len(sub)):
        for k in range(len(tnames)):
            if res[j] == res[j] and res[j] != "nan":
                if res[j] > tnames[k]:
                    if sub[j] < tnames[k]:
                        dif = tnames[k] - sub[j]
                        dif = dif.total_seconds() / 3600
                        if dif <= 720:
                            zeros[k] += 1
                        elif dif <= 1440:
                            threes[k] += 1
                        elif dif > 1440:
                            sixs[k] += 1
            else:
                if sub[j] < tnames[k]:
                    dif2 = tnames[k] - sub[j]
                    dif2 = dif2.total_seconds() / 3600
                    if dif2 <= 720:
                        zeros[k] += 1
                    elif dif2 <= 1440:
                        threes[k] += 1
                    elif dif2 > 1440:
                        sixs[k] += 1
    out = pd.DataFrame({'0-30 Days': zeros,
                   '31-60 Days': threes,
                   'Greater Than 60 Days' : sixs}, index=tnames)

    out.plot.barh(stacked=True, figsize=(40,20))


data = pd.read_csv("ARPC.csv")
data = data.drop_duplicates(subset=['INCIDENT_NUMBER'], keep='first')
data = data.reset_index(drop=True)
closed = data[data.LAST_RESOLVED_DATE.notnull()]


asc = metrics("ASSIGNED_SUPPORT_COMPANY")
aso = metrics("ASSIGNED_SUPPORT_ORGANIZATION")
asg = metrics("ASSIGNED_GROUP")
ase = metrics("ASSIGNEE")

#visualizeV(asg, "ASSIGNED_GROUP", "Average_Time", False)
#visualizeV(asg, "ASSIGNED_GROUP", "Total_Tickets", False)
#visualizeH(ase, "ASSIGNEE", "Average_Time", False)
#visualizeH(ase, "ASSIGNEE", "Total_Tickets", True)
visualizeTime()
