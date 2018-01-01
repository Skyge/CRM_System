from django.shortcuts import HttpResponse, redirect
from django.core.urlresolvers import resolve
from .import permission_list


def perm_check(*args, **kwargs):
    request = args[0]
    if request.user.is_authenticated():
        for permission_name, v in permission_list.perm_dic.items():
            url_matched = False
            if v["url_type"] == 1:  # absolute
                if v["url"] == request.path:  # 绝对url匹配上了
                    url_matched = True
            else:
                resolve_url_obj = resolve(request.path)
                if resolve_url_obj.url_name == v["url"]:  # 相对的url 别名匹配上了
                    url_matched = True

            if url_matched:
                if v["method"] == request.method:  # 请求方法也匹配上了
                    arg_matched = True
                    for request_arg in v["args"]:
                        request_method_func = getattr(request, v["method"])
                        if not request_method_func.get(request_arg):
                            arg_matched = False

                    if arg_matched:  # 走到这里，仅代表这个请求 和这条权限的定义规则 匹配上了
                        if request.user.has_perm(permission_name):
                            # 有权限
                            return True
    else:
        return redirect("/account/login/")


def check_permission(func):
    def inner(*args, **kwargs):
        # print("--permission:",*args,**kwargs)
        # print("--func:",func)
        if perm_check(*args, **kwargs) is True:
            return func(*args, **kwargs)
        else:
            return HttpResponse("没权限")
    return inner
