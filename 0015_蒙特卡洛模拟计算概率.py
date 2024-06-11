import random
import time

begin_time = time.perf_counter()

result_num = []

cards_num = list(range(54))

for i in range(1000000):
    result = []
    count = 0
    while len(result) < 54:
        num = random.choice(cards_num)
        if num not in result:
            result.append(num)
        count += 1
    result_num.append(count)
end_time = time.perf_counter()
print("运算耗费的时间为：{}".format(end_time - begin_time))
print("平均期望为:{}".format(sum(result_num)/len(result_num)))