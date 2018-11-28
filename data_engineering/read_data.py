import datetime
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

original_path = "original_data/"
objective_path = "data/"

all_info = []
heart_info = []
human_info = []
keys = ["good", "bad", "normal", "reject"]
human_dict = {key:value for key,value in zip(keys, [1, -1, 0, 0])}
with open(original_path+"data.txt") as f:
    for line in f:
        value = json.loads(line)
        info = [datetime.datetime.strptime(value["time"], '%Y-%m-%d %H:%M:%S.%f'),
                value["ip"], value["port"], value["value"]]
        if info[3] not in ["good", "bad", "normal", "reject"]:
            info[3] = np.float(info[3])
            heart_info.append(info)
        else:
            info[3] = human_dict[info[3]]
            human_info.append(info)
        all_info.append(info)

all_info = np.asarray(all_info)
heart_info = np.asarray(heart_info)
human_info = np.asarray(human_info)

all_df = pd.DataFrame(all_info, columns=["time", "ip", "port", "value"])
all_df.to_csv(objective_path+"all_info.csv", encoding = "utf-8", index=False)
heart_df = pd.DataFrame(heart_info, columns=["time", "ip", "port", "value"])
heart_df.to_csv(objective_path+"heart_info.csv", encoding = "utf-8", index=False)
human_df = pd.DataFrame(human_info, columns=["time", "ip", "port", "value"])
human_df.to_csv(objective_path+"human_info.csv", encoding = "utf-8", index=False)

plt.figure(figsize=(16, 9))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %H:%M:%S'))
#plt.plot(all_info.T[0], all_info.T[3], label="all")
plt.plot(heart_info.T[0], heart_info.T[3], label="heart")
plt.plot(human_info.T[0], human_info.T[3], label="human")
plt.legend()
plt.xlabel("time")
plt.ylabel("magnitude")
plt.title("all magnitude")
plt.show()
plt.savefig(objective_path+"all_info.png")


plt.figure(figsize=(16, 9))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %H:%M:%S'))
plt.plot(heart_info.T[0], heart_info.T[3], label="heart")
plt.legend()
plt.xlabel("time")
plt.ylabel("magnitude")
plt.title("heart magnitude")
plt.show()
plt.savefig(objective_path+"heart magnitude.png")


plt.figure(figsize=(16, 9))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %H:%M:%S'))
plt.plot(human_info.T[0], human_info.T[3], label="human")
plt.legend()
plt.xlabel("time")
plt.ylabel("evaluation")
plt.title("human info")
plt.show()
plt.savefig(objective_path+"human infomation.png")
