if __name__ == "__main__" and __package__ is None:
    __package__ = "package.tests"

    from package.module import circuitOld as cc
else:
    from package.module import circuitOld as cc

if __name__ == '__main__':
    drop = cc.Tank("gunnar")
    loop = cc.PipeBend("srt", 10)

    print(drop)
    pool = cc.Circuit()
    '''
    pool.canvas_resize_height(1)
    pool.canvas_resize_height(-1)
    pool.canvas_resize_height(-1)
    pool.canvas_resize_length(1)
    pool.canvas_resize_length(1)
    '''
    #pool.canvas_creator()

    pool.canvas[0][0] = drop
   # pool.canvas_placer(drop)
    pool.canvas_placer(loop)

    print(pool)
    pass
