from flask import request, jsonify
from app.sqldb.SqlAlchemyDB import Host, db, t_group, t_sys_user, User2
from app.tools.SqlListTool import ListTool


class CountList:
    def __init__(self):
        self.ls_tool = ListTool()

    @property
    def server_count_all(self):
        try:
            host_len_msg = Host.query.count()
            user_len_msg = User2.query.count()
            group_len_msg = t_group.query.count()
            return jsonify({
                'code': 0,
                'host_len': host_len_msg,
                'user_len': user_len_msg,
                'group_len': group_len_msg,
                'container_len': 0
            })
        except IOError:
            return jsonify({'code': 1})


class DataList:
    def __init__(self):
        self.lt = ListTool()

    def get_list(self):
        que_group = Host.query.with_entities(Host.group).all()
        host_group = self.lt.list_rep_gather(que_group)
        msg_list = []
        count = 0
        for i in host_group:
            count += 1
            dic = Host.query.filter_by(group=i).all()
            for y in dic:
                host_name = y.alias
                dic = {'title': i, 'id': count, 'children': [{'title': host_name, 'id': count}]}
                msg_list.append(dic)
        return jsonify({"host": msg_list})
