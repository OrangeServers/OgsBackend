import itertools


class ListTool:
    def __init__(self):
        pass

    # 列表集合整合成一个列表
    @staticmethod
    def list_gather(ls_str):
        msg = list(itertools.chain.from_iterable(ls_str))
        return msg

    # 去重整合
    @staticmethod
    def list_rep_gather(ls_str):
        msg = list(itertools.chain.from_iterable(set(ls_str)))
        return msg

    # 查询的dict传list
    @staticmethod
    def dict_reset_list(one_dict):
        msg = list(one_dict.__dict__.values())
        msg.pop(0)
        return msg

    # bug待修复
    @staticmethod
    def dict_reset_pop(one_dict):
        msg = one_dict.__dict__
        msg.pop('_sa_instance_state')
        msg.pop('host_password')
        return msg

    # 查询的dict组传list组
    @staticmethod
    def dict_ls_reset_list(ls_dict):
        msg = []
        for ds in ls_dict:
            res_ls = list(ds.__dict__.values())
            res_ls.pop(0)
            msg.append(res_ls)
        return msg

    # 查询的dict组传list内dict组 针对查询主机列表
    @staticmethod
    def dict_ls_reset_dict(ls_dict):
        msg = []
        for ds in ls_dict:
            ds_ls = ds.__dict__
            ds_ls.pop('_sa_instance_state')
            ds_ls.pop('host_password')
            msg.append(ds_ls)
        return msg
