import pandas as pd
from sqlalchemy.orm.util import aliased
from app.cmm.models import *
from app import db

def find_menu_by_root_id(root_id):
    included_parts = db.session \
                        .query(CM_MENU_ITEM) \
                        .filter(CM_MENU_ITEM.menu_id==root_id, CM_MENU_ITEM.use_yn == 'Y') \
                        .cte(name='included_parts', recursive=True)

    incl_alias = aliased(included_parts, name="pr")
    parts_alias = aliased(CM_MENU_ITEM, name='p')
    
    included_parts = included_parts.union_all(
        db.session.query(parts_alias).filter(parts_alias.pmenu_id==incl_alias.c.menu_id , parts_alias.use_yn == 'Y')
    )
    
    try:
        rs = db.session.query(included_parts).all()
        df = pd.DataFrame(rs)
        df = df.fillna(0)
#         print(df)
        df['pmenu_id'] = df['pmenu_id'].astype(int)
        tree = {'top' : None, 'sub_1' : [], 'sub_2' : [] }
        rank = []
        sub1_id = []
        for x, g in df.groupby('pmenu_id'):
            rank.append(x)
            rank.sort()
#             print("  ")
#             print(rank)
#             print("x->",x)
            if x == 0:
                tree['top'] = g.to_dict(orient='records')[0]
            elif x == root_id:
                tree['sub_1'] = g.to_dict(orient='records')
                for k in tree['sub_1']:
                    sub1_id.append(k['menu_id'])
            elif x in sub1_id:
#                 print("sub2 - > {} -- ")
                tree['sub_2'] += g.to_dict(orient='records')
            else:
                pass
            
            '''
            if x == list(rank)[0] and len(rank) >= 1:
                tree['top'] = g.to_dict(orient='records')[0]
            elif x == list(rank)[1] and len(rank) >= 2:
                tree['sub_1'] = g.to_dict(orient='records')
#             elif x == list(rank)[2]:
#                 tree['sub_2'] = g.to_dict(orient='records')
            else:
                tree['sub_2'] = g.to_dict(orient='records')
            
            '''

        for x in tree['sub_1']:
            x['hasChild'] = False
            for y in tree['sub_2']:
#                 print('   > ',y)
                if x['menu_id'] == y['pmenu_id']:
                    x['hasChild'] = True
        return tree
    except Exception as e:
        print('err',e)
        return {}
    
def find_menu():    
    rs = db.session.query(CM_MENU_ITEM).filter(CM_MENU_ITEM.pmenu_id == 0, CM_MENU_ITEM.use_yn == 'Y').all()
    buf = []
    for x in rs:
#         buf.append(find_menu_by_root_id(root_id[0]))
        buf.append(find_menu_by_root_id(x.menu_id))
        
#     print("----------")
#     print(buf)
#     print("----------")
    return buf

if __name__ == '__main__':
    from pprint import pprint 
    pprint(find_menu_by_root_id(1))