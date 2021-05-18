import socket
import json
#client传入socket client的套接字,requestStr传入请求的字符串
#第一次使用:(c# MyH_TcpBigDataTrasferOp_V1.cs)
# requestStr格式为:{type:'get|set|et.",op:'itemnames'}
#下面为起始流程解释:(注:此函数协议可以修改算法后变为窗口滑动模式)
#服务器端会有线程接收并解析此字符串,然后传入大数据发送的函数的参数:需要发送的buf,
#客户端则调用此函数进行大数据接收
#服务器端会返回{success:0,allSize:全部大小,packageCount:发送次数,msg:'...'}
def getBigData(client,requestStr)->bytearray:
    '''
    host = '127.0.0.1'
    port = 28080
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    req={"type":"get","op":"E:\\素材相关\\1.jpg"}
    '''
    #设置阻塞超时
    client.settimeout(30)
    #发送数据请求头
    client.send(bytes(requestStr,encoding='utf-8'))
    receiveInfo=client.recv(1024)
    strrecv=str(receiveInfo,'utf-8')
    #print(strrecv)
    j=json.loads(strrecv)
    if j['success']!=0:
        print(j['msg'])
        return None
    #获取json{success:0,allSize:全部大小,packageCount:发送次数,msg:'...'}
    rcvCount=j['packageCount']
    rcvSize=j['allSize']
    sendbuf=bytearray()
    sendbuf.append(0)
    #发送5个字节,第一个字节表示是否有问题,正常为0,第2~5个字节为接收的序号,初始为0
    sendSeq=0
    sendSeq=sendSeq.to_bytes(4,'little')
    sendbuf=sendbuf+sendSeq
    #print(sendbuf)
    client.send(sendbuf)
    alldata=bytearray()
    for f in range(rcvCount):
        data =client.recv(1024) #!!!!!!python无法获取接收字节的大小....太坑了吧....
        #print("datalen=",len(data),f' data={data}')
        data=bytearray(data)
        if(len(data)<=0 or data[0]!=0):
            print("接收错误:code=",data)
            return None
        #tmpArr={data[1],data[2],data[3],data[4]}
        #print('tmpArr=',data[1:5])
        req=int.from_bytes(data[1:5],'little')
        #print("get count=",req)
        alldata+=data[5:]
        #print('get all len=',len(alldata))
        sendSeq=(b'\x00')+(f+1).to_bytes(4,'little')
        #print('sendbuf=',sendSeq)
        client.send(sendSeq)
    return alldata
    #print('get len=',len(alldata))
    #print(alldata)
    #alldata:bytearray()
    '''
    img=Image.open(io.BytesIO(alldata))
    plt.imshow(img)
    plt.show()
    '''