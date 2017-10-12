
def try_int(args,default):
    try:
        page = int(args)
    except Exception,e:
        page = default
    return page