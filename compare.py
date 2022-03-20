#!/usr/bin/env python3
import collections

f_pred = open("pred.txt", "r")
f_ref = open("ref.txt", "r")

tp = 0
tn = 0
fp = 0
fn = 0
g = 0
gn = 0

recall_freq = collections.defaultdict(lambda: 0)
wrong_freq = collections.defaultdict(lambda: 0)
total_freq = collections.defaultdict(lambda: 0)

for pred, ref in zip(f_pred, f_ref):
    p_words = pred.split()
    r_words = ref.split()
    if "get" in r_words:
        g += 1
    if "set" in r_words:
        g += 1
    gn += len(list(x for x in r_words if x != "get" and x != "set"))
    for p in set(p_words):
        if p in r_words:
            tp += 1
            recall_freq[p] += 1
        else:
            fp += 1
            wrong_freq[p] += 1
    for r in r_words:
        if r not in p_words:
            fn += 1
        total_freq[r] += 1

prec = tp / (tp + fp)
recall = tp / (tp + fn)
prec_g = 1
recall_g = g / (g + gn)
print(f"precision {tp / (tp + fp)}")
print(f"recall {tp / (tp + fn)}")
print(f"f1 {2/(1/prec + 1/recall)}")
print(f"precisiong {prec_g}")
print(f"recallg {recall_g}")
print(f"f1g {2/(1/prec_g + 1/recall_g)}")
t = 0
xs = []
ys = []
for k, v in reversed(sorted(filter(lambda x: x[1] > 1000, recall_freq.items()), key=lambda x: x[1] / total_freq[x[0]])):
    print(k, v, total_freq[k])
    xs += [k]
    ys += [v / total_freq[k]]
    if t > 30:
        break
    t += 1


import matplotlib.pyplot as plt

plt.figure(figsize=(20, 10))
plt.bar(x=xs, height=ys)
#plt.tick_params(rotation=60, axis="x")
plt.savefig("dist.png")
