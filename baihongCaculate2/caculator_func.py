import itertools
import math
import threading
from math import comb
from queue import Queue
def 计算2_近似配重计算器(净重1,净重2,总重量):
    """
    :params int 净重1: 纱线净重
    :params int 净重2: 纱线净重2
    :params int 总重量: 纱线总重量
    """
    if 净重1=="":
        净重1=0
    if 净重2=="":
        净重2=0
    if 总重量=="":
        总重量=0
    if 净重1==0 and 净重2==0:
        return "净重1与净重2同时为0，无法正常配重(╥╯^╰╥)"
    try:
        总重量 = int(总重量)
        重量1 = int(净重1)
        重量2 = int(净重2)
    except ValueError:
        return "数据输入异常，请重新输入。(╯‵□′)╯︵┻━┻"
    if 总重量<=0 or 重量1<0 or 重量2<0:
        return "数据输入有问题！请重新输入！(*￣︶￣)"
    if 重量1==0:
        aa= '配货详情:'+ str(重量2) + '公斤枚举,总重量接近:' + str(总重量) + '公斤\n'
        aa=aa+ str(int(总重量/重量2))+'件' + str(重量2) + '公斤,总重量为:' + str(int(总重量/重量2) * 重量2) + '公斤,剩余' + str(总重量-int(总重量/重量2) * 重量2) + '公斤\n'
        return aa
    if 重量2==0:
        aa= '配货详情:'+ str(重量1) + '公斤枚举,总重量接近:' + str(总重量) + '公斤\n'
        aa=aa+ str(int(总重量/重量1))+'件' + str(重量1) + '公斤,总重量为:' + str(int(总重量/重量1) * 重量1) + '公斤,剩余' + str(总重量-int(总重量/重量1) * 重量1) + '公斤\n'
        return aa
    lines=""
    x = 总重量 / 重量1
    lines=lines+'配货详情:' + str(重量1) + '公斤和' + str(重量2) + '公斤枚举,总重量接近:' + str(总重量) + '公斤\n'
    arr=[]
    for i in range(int(x) + 1):
        配重 = 总重量 - i * 重量1
        j = 0
        while 配重 >= 重量2:
            j = j + 1
            配重 = 配重 - 重量2
        arr.append((i, j, 配重))
    if len(arr)==0:
        return "可能缺乏配重方案哦~请重新输入其他数值进行配重！(#^.^#)"
    for a in arr:
        lines=lines+str(a[0]) + '件' + str(重量1) + '公斤,'+ str(a[1]) + '件' + str(重量2) + '公斤 总重量为:' + str(a[0] * 重量1 + a[1] * 重量2) + '公斤,剩余' + str(a[2]) + '公斤\n'
    return lines
def 计算1_配重计算器(净重1,净重2,总重量):
    if 净重1=="":
        净重1=0
    if 净重2=="":
        净重2=0
    if 总重量=="":
        总重量=0
    if 净重1==0 and 净重2==0:
        return "净重1与净重2同时为0，无法正常配重(╥╯^╰╥)"
    try:
        总重量 = int(总重量)
        重量1 = int(净重1)
        重量2 = int(净重2)
    except ValueError:
        return "数据输入异常，请重新输入。(╯‵□′)╯︵┻━┻"
    if 总重量<=0 or 重量1<0 or 重量2<0:
        return "数据输入有问题！请重新输入！o(╥﹏╥)o"
    if 重量1 == 0:
        if  总重量%重量2==0:
            aa = '配货详情:' + str(重量2) + '公斤枚举,总重量等于:' + str(总重量) + '公斤\n'
            aa = aa + str(int(总重量 / 重量2)) + '件' + str(重量2) + '公斤,总重量为:' + str(int(总重量 / 重量2) * 重量2) + '公斤\n'
            return aa
        else:
            return "可能缺乏配重方案哦~请重新输入其他数值进行配重！(#^.^#)"
    if 重量2 == 0:
        if 总重量%重量1 == 0:
            print('221321')
            aa = '配货详情:' + str(重量1) + '公斤枚举,总重量等于:' + str(总重量) + '公斤\n'
            aa = aa + str(int(总重量 / 重量1)) + '件' + str(重量1) + '公斤,总重量为:' + str(int(总重量 / 重量1) * 重量1) + '公斤\n'
            return aa
        else:
            return "可能缺乏配重方案哦~请重新输入其他数值进行配重！(#^.^#)"
    arr = []
    x = 总重量 / 重量1
    textsArr=""
    textsArr=textsArr+'配货详情:' + str(重量1) + '公斤和' + str(重量2) + '公斤枚举,总重量为:' + str(总重量) + '公斤'+'\n'
    for i in range(int(x) + 1):
        y = 总重量 - i * 重量1
        if math.modf(y / 重量2)[0] == 0:
            arr.append((i, int(y / 重量2)))
    if len(arr)==0:
        return "可能缺乏配重方案哦~请重新输入其他数值进行配重！(#^.^#)"
    for a in arr:
        textsArr=textsArr+str(a[0]) + '件' + str(重量1) + '公斤,'+str(a[1]) + '件' + str(重量2) + '公斤 总重量为:' + str(a[0] * 重量1 + a[1] * 重量2) + '公斤'+'\n'
        # 总重量/重量1
    return textsArr
def 等级品计算器_迭代计算(src_datas,remove_datas,limitWeight,num=-1,receiver=None):
    def preHandle(datas,remove_datas):
        """
        对数据进行预处理
        """
        for remove in remove_datas:
            for i in range(len(datas)):
                if datas[i] == remove:
                    break
            del datas[i]
        datas = sorted(datas)
        return datas
    def getRangeArr(datas, limitWeight):
        # 2.进行范围数组的确定
        # tiny=sum(datas)/len(datas)
        range_arr = []
        for i in range(1, len(datas) + 1):
            _sum_min = sum(datas[0:i])
            _sum_max = sum(datas[len(datas) - i:len(datas)])
            if _sum_min <= limitWeight and _sum_max >= limitWeight:
                range_arr.append((i, _sum_min, _sum_max))
        return range_arr
    def cauculateSendRateFate(iterNUM):
        fate = 0
        if iterNUM <= 30:
            fate = 1
        elif iterNUM > 30 and iterNUM < 1000:
            fate = 10
        elif iterNUM >= 1000 and iterNUM < 10000:
            fate = 100
        elif iterNUM >= 10000 and iterNUM <= 100000:
            fate = 1000
        else:
            fate = 5000
        q = Queue(maxsize=fate)
        return (q,fate)
    def reduceSendRate(receiver,q,fate):
        #开启一条多线程
        def send(receiver,q):
            arr=[]
            while True:
                recv=q.get()
                if recv=='end':
                    if len(arr)!=0:
                        receiver.put(arr[-1])
                    receiver.put(('end',))
                    break
                else:
                    arr.append(recv)
                    if len(arr)>=fate-1:
                        receiver.put(arr[-1])
                        arr=[]
        t=threading.Thread(target=send,args=[receiver,q])
        # t.setDaemon(True)
        t.start()
    #通知receiver，要开始运算了
    receiver.put(('start',))
    items = []
    src_datas=preHandle(src_datas,remove_datas)
    if len(src_datas) == 0 or sum(src_datas)<limitWeight:
        receiver.put(('end',))
        return
    range_arr=getRangeArr(src_datas,limitWeight)
    tiny=sum(src_datas)/len(src_datas)
    print_num=50
    #计算要迭代多少数据
    # print(range_arr)
    iterNUM=0
    if num>0:
        iterNUM = comb(len(src_datas),num)
    else:
        for i in range(len(range_arr)):
            a = comb(len(src_datas), range_arr[i][0])
            iterNUM=iterNUM+a
    q,fate=cauculateSendRateFate(iterNUM)
    reduceSendRate(receiver,q,fate)
    for i in range(len(range_arr)):
        if num == range_arr[i][0] or num <=0:
            pass
        else:
            continue
        # a = comb(len(src_datas), i)
        # if a >= 100000:
        #     assert 1 / 0
        comb_iter = itertools.combinations(src_datas, range_arr[i][0])
        while True:
            try:
                datas=next(comb_iter)
            except StopIteration:
                break
            _s=sum(datas)
            if _s<=limitWeight and _s>=limitWeight-tiny:
                if len(items)!=0:
                    # print(items[len(items) - 1][2])
                    if _s >= items[len(items) - 1][2]:
                        items = sorted(items, key=lambda x: x[0])
                        if len(items)>print_num:
                            items=items[0:print_num]
                            for item in items:
                                s = '要求重量不超过:' + str(limitWeight) +\
                                      '; 实际重量为:'+str(item[2])+\
                                      '; 重量差为:'+str(item[0])+ ';'+\
                                      ' 托数为:'+str(item[1])+ ';'+\
                                      '具体数据为:'+str( item[3])+ ';'
                                q.put((等级品计算器_迭代计算, s))

                        items.append((round(limitWeight - _s, 5), len(datas), round(_s, 5), datas))  # 重量差,托数，重量和，重量的原始数据
                else:
                    items.append((round(limitWeight - _s, 5), len(datas), round(_s, 5), datas))  # 重量差,托数，重量和，重量的原始数据
    items = sorted(items, key=lambda x: x[0])
    items = items[0:print_num]
    for item in items:
        s = '要求重量不超过:' + str(limitWeight) + \
            '; 实际重量为:' + str(item[2]) + \
            '; 重量差为:' + str(item[0]) + ';' + \
            ' 托数为:' + str(item[1]) + ';' + \
            '具体数据为:' + str(item[3]) + ';'
        q.put((等级品计算器_迭代计算, s))
    q.put('end')
def 等级品计算器_快速计算(src_datas,remove_datas,limitWeight,num=-1,receiver=None):
    def changeArr(arr1, arr2, i1, i2):
        mid = arr1.pop(i1)
        arr1.append(arr2.pop(i2))
        arr2.append(mid)
        arr1.sort()
        arr2.sort()
    def preHandle(datas,remove_datas):
        """
        对数据进行预处理
        """
        for remove in remove_datas:
            for i in range(len(datas)):
                if datas[i] == remove:
                    break
            del datas[i]
        datas = sorted(datas)
        return datas
    def getRangeArr(datas,limitWeight):
        # 2.进行范围数组的确定
        # tiny=sum(datas)/len(datas)
        range_arr = []
        for i in range(1, len(datas) + 1):
            _sum_min = sum(datas[0:i])
            _sum_max = sum(datas[len(datas)-i:len(datas)])
            if _sum_min <= limitWeight and _sum_max  >= limitWeight:
                range_arr.append((i, _sum_min, _sum_max))
        return range_arr
    def limit_init(trr,trr_,limitWeight):
        # 1.初步收敛
        limit_arr = []
        limit_arr.append(limitWeight- sum(trr))
        while abs(limit_arr[-1]) > 0:
            min = trr.pop(0)
            # print(trr_)
            trr.append(trr_.pop())
            trr_.insert(0, min)
            limit_arr.append(limitWeight - sum(trr))
            if limit_arr[-1] >= limit_arr[-2] or limit_arr[-1] <= 0:
                min = trr_.pop(0)
                trr_.append(trr.pop())
                trr.insert(0, min)
                limit_arr.pop()
                break
        # print('1步收敛:'+str(sum(trr)))

        di = sum(trr) - limitWeight
        return (di,0,0)
    def limit_cauculate(trr,trr_,index, limit,limitWeight):
        # index:收敛等级。最低为1级，2级，逐级上升
        limit_dig_2 = []
        di = limitWeight - sum(trr)
        a = comb(len(trr)+len(trr_), index)
        if a >= 100000:
            assert 1 / 0
        if index == 1:
            arr_trr = trr
            arr_trr_ = trr_
        else:
            # 470.5, 474.5, 486.5, 584.5, 658.5, 658.5
            arr_trr = list(itertools.combinations(trr, index))
            arr_trr_ = list(itertools.combinations(trr_, index))
        for i in arr_trr_:  # 外数据
            for j in arr_trr:  # 内数据
                if index == 1:
                    if i - j - di <= 0:
                        limit_dig_2.append((i - j - di, i, j))
                else:
                    if sum(i) - sum(j) - di <= 0:
                        limit_dig_2.append((sum(i) - sum(j) - di, i, j))
                        if len(limit_dig_2)>=500:
                            limit_dig_2 = sorted(limit_dig_2, key=lambda x: x[0])
                            limit_dig_2=limit_dig_2[-101:-1]

        # print(len(limit_dig_2))
        limit_dig_2 = sorted(limit_dig_2, key=lambda x: x[0])
        if len(limit_dig_2)!=0:
            if limit > limit_dig_2[-1][0]:
                return None
            else:
                return limit_dig_2[-1]
    def limit_cauculate_by_托数(datas,托数):
        trr = src_datas[0:托数]
        trr_ = src_datas[托数:len(datas)]
        if len(trr_)!=0:
            limit_fate = limit_init(trr, trr_, limitWeight)[0]
        s = '初步收敛:要求重量不超过:' + str(limitWeight) + '; 实际重量为:' + str(sum(trr)) + \
            '; 重量差为:' + str(limitWeight - sum(trr)) + '; 托数为:' + str(len(trr)) + ';具体数据为:' + str(trr) + ';'
        receiver.put((limit_cauculate_by_托数, s))
        if len(trr_) != 0:
            for _i in range(1, 20):
                try:
                    result = limit_cauculate(trr, trr_, _i, limit_fate, limitWeight)
                except ZeroDivisionError as e:
                    break
                # 判断是否收敛成功
                if result != None:
                    if type(result[1]) == float:
                        changeArr(trr, trr_, trr.index(result[2]), trr_.index(result[1]))
                    else:
                        for i in range(len(result[1])):
                            changeArr(trr, trr_, trr.index(result[2][i]), trr_.index(result[1][i]))
                    s=str(_i) + '步收敛:要求重量不超过:' + str(limitWeight) +'; 实际重量为:'+ str(sum(trr))+\
                      '; 重量差为:'+str(limitWeight - sum(trr))+'; 托数为:'+str(len(trr))+ ';具体数据为:'+str(trr)+';'
                    receiver.put((limit_cauculate_by_托数,s))
    receiver.put(('start',))
    src_datas = preHandle(src_datas, remove_datas)
    if len(src_datas)==0 or sum(src_datas)<limitWeight:
        receiver.put(('end',))
        return
    range_arr = getRangeArr(src_datas, limitWeight)
    if num<=0:
        for r in range_arr:
            limit_cauculate_by_托数(src_datas,r[0])
    else:
        limit_cauculate_by_托数(src_datas,num)
    receiver.put(('end',))
if __name__ == '__main__':
    a=计算2_近似配重计算器(6100,720,30240)
    # 470.5, 474.5, 486.5, 584.5, 658.5, 658.5
    print(a)