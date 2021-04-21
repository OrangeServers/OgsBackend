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
        group_count = 10
        host_count = 100
        msg_list = []
        for i in host_group:
            body_list = []
            group_count += 1
            dic = Host.query.filter_by(group=i).all()
            for y in dic:
                host_count += 1
                host_name = y.alias
                body_list.append({'title': host_name, 'id': host_count})
            dic = {'title': i, 'id': group_count, 'children': body_list}
            msg_list.append(dic)
        return jsonify({"host": [{'title': '所有资产组', 'id': 0, 'spread': 'true', 'children': msg_list}]})
