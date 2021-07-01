from flask import request, jsonify
from app.sqldb.SqlAlchemyDB import t_settings, db
from app.tools.SqlListTool import ListTool


class OgsSettings:
    def __init__(self):
        self.name = request.values.get('name')
        self.lt = ListTool()

    def settings_info(self):
        query_msg = t_settings.query.filter_by(name=self.name).first()
        st_msg = self.lt.dict_reset_pop_auto(query_msg)
        print(st_msg)
        return jsonify(st_msg)

    def settings_change(self):
        try:
            login_time = request.values.get('login_time')
            rsgister_status = request.values.get('rsgister_status')
            t_settings.query.filter_by(name=self.name).update({'name': self.name, 'login_time': login_time, 'rsgister_status': rsgister_status})
            db.session.commit()
            return jsonify({'status': 'true'})
        except IOError:
            return jsonify({'status': 'fail'})
