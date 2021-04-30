from flask import request, jsonify
from app.tools.shellcmd import RemoteConnection
import os, sys

sys.path.append('../..')


class LocalShell:
    def __init__(self):
        pass

    @staticmethod
    def cmd_shell(cmd):
        zx = os.popen(cmd)
        msg = zx.read().replace('\n', '')
        zx.close()
        return msg

    @staticmethod
    def cmdlist_shell(cmd):
        zx = os.popen(cmd)
        msg = zx.read().replace('\n', ',')
        list1 = msg.strip(',').split(',')
        zx.close()
        return list1


class LocalDirList(LocalShell):
    def __init__(self, dir1path=None, dir2path=None, rscmd=None):
        super(LocalDirList, self).__init__()
        self.dir1path = dir1path
        self.dir2path = dir2path
        self.rscmd = rscmd
        self.group_dir = request.values.get('group_dir', 'err not group_dir key', type=str)

    def getdir1(self):
        dir1 = self.cmdlist_shell(self.dir1path)
        if self.group_dir in dir1:
            dir2_path = (self.dir2path % self.group_dir)
            dir2 = self.cmdlist_shell(dir2_path)
            return jsonify({
                'status': 'sucessfuly',
                "msg": dir2
            })
        else:
            return jsonify({
                'status': 'error',
                'msg': ("server is not group_dir %s !" % self.group_dir)
            })

    def getdir2(self):
        project_dir = request.values.get('project_dir', 'err not project_dir key', type=str)
        dir1 = self.cmdlist_shell(self.dir1path)
        if self.group_dir in dir1:
            dir2_path = (self.dir2path % self.group_dir)
            dir2 = self.cmdlist_shell(dir2_path)
            if project_dir in dir2:
                rsync_dir = (self.rscmd % (self.group_dir, project_dir))
                try:
                    msg_out = LocalShell().cmdlist_shell(rsync_dir)
                    print(msg_out)
                    return jsonify({
                        'status': 'sucessfuly',
                        # 'msg': ("rsync %s %s is ok!" % (self.group_dir, project_dir))
                        'msg': msg_out
                    })
                except Exception:
                    return jsonify({
                        'status': 'fail',
                        'msg': ("rsync %s %s is fail!" % (self.group_dir, project_dir))
                    })
            else:
                return jsonify({
                    'status': 'error',
                    'msg': ("server is not project_dir %s !" % project_dir)
                })
        else:
            return jsonify({
                'status': 'error',
                'msg': ("server is not group_dir %s !" % self.group_dir)
            })

