
import re
import time
from collections import Counter
from functools import reduce

def find_max_(s):
    ss = reduce(lambda x, y: x + y, [re.findall(rf"{i}+", s) for i in Counter(s).keys()])
    max_number = max([len(i) for i in ss])
    return max_number




def find_AB(s_str):
    # 有限长
    star_time = time.time()
    ss = re.split(r"\*", re.sub("(B{2,})", r"B*B", re.sub("(A{2,})", r"A*A", s_str)))
    ss_dic = {len(item): item for item in ss}
    max_number = ss_dic[max(ss_dic)]
    # print(f"use re::::\t{time.time() - star_time}")
    return time.time() - star_time


def find_AB_(s_str):
    start_time = time.time()
    max_str, last_str = "", ''
    for i in s_str:
        if last_str:
            if i != last_str[-1]:
                last_str += i
            else:
                if len(max_str) <= len(last_str):
                    max_str = last_str
                    last_str = i
                else:
                    last_str = i
        else:
            last_str += i

    if last_str and len(max_str) <= len(last_str):
        max_str = last_str
    # print(f"use for::::\t{time.time() - start_time}")
    return time.time() - start_time


sss = "ABABABABBABAABAABABABABABABABABABABABAABBBBBABABABABABABABABABABABABABABABABABABBAABABABABABABABBABAABAABABABABABABABABABABABAABBBBBABABABABABABABABABABABABABABABABABABBAABAB"
t1 = sum([find_AB(sss * 100000) for i in range(10)]) / 10
t2 = sum([find_AB_(sss * 100000) for i in range(10)]) / 10

print(f"use re: {t1}")
print(f"use for: {t2}")




