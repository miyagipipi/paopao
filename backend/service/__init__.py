from service.UserService import userService
from service.AdminService import adminService
from service.TeamService import teamService
from service.UserTeamService import userTeamService
from service.TeamPlanService import teamPlanService

"""
这里有一个设计问题：
    service中的模块，理论上是平级的，尽量避免相互调用所导致的循环引入
    但是目前不可避免的发生了调用，例如在TeamService中调用了UserService
    如果后续开发中需要在UserService中调用TeamService，则会发生循环引入

    虽然将公共方法放入Base是一个可取的设计方案，但是在实际设计和调用中还是不可避免上面的问题
    
"""
