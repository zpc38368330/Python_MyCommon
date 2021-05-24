import xlrd
# from xlutils.copy import copy
import xlwt

class MyExcelOp():
    m_workbook: xlrd.book.Book=None
    m_sheet: xlrd.sheet.Sheet=None

    def __init__(self):
        pass

    def __del__(self):
        self.close()
        pass

    def openXls(self,filename)->xlrd.book.Book:
        self.m_workbook=xlrd.open_workbook(filename)
        return self.m_workbook

    def getSheet_by_index(self,index)->xlrd.sheet.Sheet:
        self.m_sheet = self.m_workbook.sheet_by_index(0)
        return self.m_sheet

    def getSheet_by_name(self,name):
        self.m_sheet=self.m_workboot.sheet_by_name(name)
        return self.m_sheet

    def getCell(self,r,c):
        return self.m_sheet.cell_value(r,c)

    def getRowLen(self):
        return self.m_sheet.nrows

    def close(self):
        if self.m_workbook!=None:
            self.m_workbook.release_resources()
            del self.m_workbook
            self.m_workbook=None

