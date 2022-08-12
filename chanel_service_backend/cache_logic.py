CACHED_DATA = []
FIRST_REQUEST = True
CHANGES = {'new': [], 'update': [], 'delete': []}


def table_cacher(func):
    """Декоратор для получения данных об изменениях в гугл-таблице для записи в кэш"""
    def wrapper(*args, **kwargs):
        global CACHED_DATA, FIRST_REQUEST, CHANGES
        data = func(*args, **kwargs)[1:]
        if FIRST_REQUEST:
            CACHED_DATA = data
            CHANGES['new'] = data
            FIRST_REQUEST = False
            return CHANGES
        elif CACHED_DATA != data:
            changes = {'new': [], 'update': [], 'delete': []}
            list_of_orders_nums = list(map(lambda x: x[1], CACHED_DATA))
            for row in data:
                if row[1] not in list_of_orders_nums:
                    changes['new'].append(row)
                elif (row[1] in list_of_orders_nums) and \
                        (row != CACHED_DATA[list_of_orders_nums.index(row[1])]):
                    changes['update'].append(row)
                    list_of_orders_nums[list_of_orders_nums.index(row[1])] = None
                else:
                    list_of_orders_nums[list_of_orders_nums.index(row[1])] = None
            deleted_order = [CACHED_DATA[list_of_orders_nums.index(_)] for _ in list_of_orders_nums if _]
            changes['delete'].extend(deleted_order)
            CACHED_DATA = data
            CHANGES = changes
            return changes
        else:
            CHANGES = {'new': [], 'update': [], 'delete': []}
            return False
    return wrapper
