from MyCommon.MyPostgresqlOp import MyPostgresqlOp as pg
import MyCommon.MyDatetimeOp as MyDatetimeOp
# import OpcJsonOp as OpcJsonOp
station_in_ini_name= 'STATION'
class PgDbOp(pg):
    def __init__(self):
        # super().setConnectParams("HeatSystem", "postgres", "pgSql_510=11@$", "10.10.18.151", 6132)
        super().setConnectParams("HeatSystem", "postgres", "pgSql_510=11@$", "192.168.9.206", 6132)
        #super().__init__()
        pass
        # super().connect("zhaoyuan", "postgres", "sql510115", "127.0.0.1", 5432)
    # def _chk_connect(self):
    #     if super().conn==None:
    #         super().connect("HeatSystem", "postgres", "pgSql_510=11@$", "192.168.9.206", 6132)
    #seciton是Opc json对象的section节点
    #返回两个值:第一个值,为执行是否正确,第二个值,为错误消息,或TID的值
    def getTidFromSection(self,sec):
        db_row_name=''
        for f in sec['items']:
            if(f['field']==station_in_ini_name):
                db_row_name=f['value']
                break;
        #如果名称字段未找到,则退出
        if(db_row_name==''):
            msg='错误:未找到数据库中行为'+db_row_name+'的配置'
            return False,msg
        # 通过数据库查找此名称对应的TID
        rows = super().select("select * from mapping_station_tid where name='" + db_row_name + "'")
        if len(rows) <= 0:
            msg="错误:未找到[" + db_row_name + \
                "]在mapping数据库中对应的id,请检查是否数据库中未注册此ID"
            return False,msg
        return True,rows[0]['tid']
        pass
    def stopTiaoKongServerce(self):
    #第一参为服务器OpcJsond的data下的各项,第二个参数是时间间隔,单位分钟
        super().execNoQuery("update conf_global_params set value='stop' where type='serviceisrun'")
    #返回值为两个,第一个是bool型,表示查询是否成功
    #如果第一个值为True,返回记录,如果为False,返回错误信息
    def getOpcSec_StationLastTimeRecord(self,sec,interval):
        isok,result=self.getTidFromSection(sec)
        if isok!=True:
            return False,result
            pass
        row = super().select(
            "select * from history_table where did=" + str(result)
            + " and updatetime<=current_timestamp - interval '" + str(interval) + " minute'"
            + " order by updatetime desc limit 1")
        if len(row) <= 0:
            msg="错误:查询" + sec + "在" + str(interval) + "分钟前没有数据."
            return False,msg
        return True,row

    # #section是json对象中 section的节点
    # #返回两个值,第一个值为执行是否成功,第二个值如果成功返回的是插入的记录数,不成功,返回的是错误信息
    # def saveOutFlowStation(self,section):
    #     isok,result=self.getTidFromSection(section)
    #     if isok!=True:
    #         return False,result
    #
    #     sql='insert into alarm_outflow_station (did,create_time,flow_cur,flow_upper_limit,flow_lower_limit,flow_basis,alarm_level)' \
    #         +" values("\
    #         +str(result)+","\
    #         +"'"+MyDatetimeOp.getSqlStringTime()+"',"\
    #         +str(OpcJsonOp.getValueFromField(section,'瞬时流量'))+","\
    #         +str(OpcJsonOp.getValueFromField(section,'流量限定上限'))+"," \
    #         + str(OpcJsonOp.getValueFromField(section, '流量限定上限')) +"," \
    #         + str(OpcJsonOp.getValueFromField(section, '流量限定下限')) + "," \
    #         + str(OpcJsonOp.getValueFromField(section, '流量限定基数')) + "," \
    #         + '1)'
    #     result=super().execNoQuery(sql)
    #     return True,result
    #     pass

    #返回rows
    def selectStationOutflowRecordCount(self,section,minuteInterval):
        isok, result = self.getTidFromSection(section)
        if isok != True:
            return False, result
        sql="select * from alarm_outflow_station where did=" + str(result)\
            + " and create_time<=current_timestamp - interval '" + str(minuteInterval) + " minute'"
        return super().select(sql)
        pass
    '''
    将station_real表数据读出并组合成已name(站点名称)为key的key value字典对象
    '''
    def getObjectFromStationReal(self):
        rows=super().select("select * from view_real_station")
        result={}
        for f in rows:
            result[f["name"]]=f
        return result;
    def addRunCount(self):
        rows = super().select("select * from conf_global_params where type='runcount'")
        if (len(rows) <= 0):
            print('数据库中未设置runcount')
            return 0
        cur=int(rows[0]['value'])+1
        return super().execNoQuery("update conf_global_params set value='"+str(cur)+"' where type='runcount'")