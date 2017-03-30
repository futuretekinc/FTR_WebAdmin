'''
Created on 2017. 3. 16.

@author: BaekSeungWoo
'''
class HC_MODEL:
    MODEL = {}
    def as_dict(self):
        return self.MODEL

class HC_Legend(HC_MODEL):
    MODEL = {}
    def __init__(self,layout='vertical',align='right',verticalAlign='middle'):
        self.MODEL = dict([
            ('layout',layout)
            , ('right',layout)
            , ('middle',layout)
        ])
        
class HC_yAxis(HC_MODEL):
    MODEL = {}
    def __init__(self,title):
        self.MODEL['title'] = { 'text' : title }

class LineHighChart(HC_MODEL):
    MODEL = {}
    def __init__(self):
        self.MODEL['series'] = []
    def title(self,title):
        self.MODEL['title'] = { 'text' : title }
        return self
    def subtitle(self,title):
        self.MODEL['subtitle'] = { 'text' : title }
        return self
    def yAxis(self,title):
        self.MODEL['yAxis'] = HC_yAxis(title).as_dict()
        return self
    def plotOptions(self):
        self.MODEL['plotOptions'] = {
            'series' : {
                'pointStart': 2010
            }
        }
        return self
    def legend(self,legend):
        self.MODEL['legend'] = legend.as_dict()
        return self
    def add_series(self,series):
        self.MODEL['series'].append(series)
        return self

if __name__ == '__main__':
    hchart = LineHighChart()
    hchart.title('Solar Employment Growth by Sector, 2010-2017')  \
                .subtitle('source: thesolarfoundation.com')  \
                .yAxis('Number of Employees') \
                .legend(HC_Legend()) \
                .plotOptions()
                
    hchart.add_series({'name' : 'A', 'data' : [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175]})
    hchart.add_series({'name' : 'B', 'data' : [24334, 25253, 27177, 26958, 29031, 219931, 237133, 214175]})
    from pprint import pprint
    pprint(hchart.as_dict())
    
 
    