
import MyCommon.MyDatetimeOp as MyDatetimeOp
import types
def show(*msg):
    print(MyDatetimeOp.getStrCurTime_microseconds(),":")
    print(*msg)
    return
    msgs=''
    for f in  msg:
        if type('')==type(f):
            msgs+=f
        else:
            print(f)
    print(msgs)
