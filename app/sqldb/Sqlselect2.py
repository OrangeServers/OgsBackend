from app.sqldb.SqlAlchemySettings import User2 as t_user
from app.sqldb.SqlAlchemySettings import Host
from app.tools.SqlListTool import ListTool

user_chk = t_user.query.filter_by(name='dasd').first()
print(user_chk)
query_msg = Host.query.all()
list1_msg = ListTool().dict_ls_reset_list(query_msg)
list2_msg = ListTool().dict_ls_reset_dict(query_msg)

# print(group_list)
print(list1_msg)
print(list2_msg)
