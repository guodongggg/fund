def timer(func):
    """
    装饰器：打印func函数执行耗时
    :param func:
    :return:
    """
    import time
    def wrapper(*args, **kwargs):
        t1 = time.time()
        f = func(*args, **kwargs)
        t2 = time.time()
        cost_time = t2-t1
        print('{}：{:.2f}s'.format(func.__name__, cost_time))
        return f
    return wrapper


if __name__ == '__main__':
    pass