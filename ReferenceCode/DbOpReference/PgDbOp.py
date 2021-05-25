from MyCommon.MyPostgresqlOp import MyPostgresqlOp as pg
station_in_ini_name= 'STATION'
class PgDbOp(pg):
    def __init__(self):
        super().setConnectParams("YOUR_DB_NAME", "postgres", "YOUR_PASSWORD", "YOUR_IP", YOUR_PORT)
        pass
    def stopTiaoKongServerce(self):
        super().execNoQuery("update conf_global_params set value='stop' where type='serviceisrun'")
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