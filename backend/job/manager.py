from job.PreCacheJob import item
from configs import scheduler
import inspect


def _schedulerCacheRecommendUser():
    scheduler.add_job(
        func=item.doCacheRecommendUser,
        id='doCacheRecommendUser',
        trigger='cron',
        hour=0,
        minute=4,
        second=0
    )


def collectSchedulers():
    """
    自动收集定时任务函数，要求函数名必须以 _scheduler 下划线开头，不然会收集到错误的函数
    使用了yeild生成器，逐个生成对象，节省内存
    """
    current_module = globals()
    for name, obj in current_module.items():
        if inspect.isfunction(obj) and name.startswith('_scheduler'):
            print(f"collection [{name}] as timed task", flush=True)
            yield obj


def StartJob():
    schedulers = collectSchedulers()
    for scheduler in schedulers:
        scheduler()