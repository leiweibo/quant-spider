#### 简介
1. 通过xueqiu.com/p/discover去获取热门组合列表
2. 通过组合列表的创建者字段，获取该创建者的创建的组合和关注的组合
3. 对创建的组合进行解析以及落库，如果组合已经存在，则不进行重复存储
4. 在#3步完成之后，开始通过组合列表去获取
    - 收益列表 api
    - 调仓记录 api
    - 股票配置 web
    - 调仓记录 api




#### 遇到的问题 (以下问题出现在Mac环境)
1. 安装过程中, `pipenv install ` 一直卡在`locking...`中
    
    通过命令`pipenv lock --clear`，然后一切恢复正常

2. 通过上面的步骤，出现 如下错误
```      
["ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied: '/Users/weibolei/.local/share/virtualenvs/quant-spider-JVGi8YHg/lib/python3.7/site-packages/_cffi_backend.cpython-37m-darwin.so'", 'Consider using the `--user` option or check the permissions.']
```

解决方法： 
`cd /Users/weibolei/.local/share/virtualenvs/` 查看quant-spider-xxx对应的user和权限，发现目录的创建者是root，这就很好解释没有权限的问题，将这个文件删除，重新运行 `pipenv sync ` 和 `pipenv install xxx`命令。


#### urls
- 组合持仓

https://xueqiu.com/service/v5/stock/batch/quote?symbol=SH600585%2CSH601318%2CSH603288%2CSZ000568%2CSZ002714%2CSZ000333%2CSZ002179%2CSH600177%2CSH600563%2CSZ000895%2CSZ000651%2CSZ002458%2CSH600660%2CSH600519%2CSH600176

- 仓位调整历史
https://xueqiu.com/cubes/rebalancing/history.json?cube_symbol=ZH1067693&count=20&page=1

- 跑赢组合数

(年)
https://xueqiu.com/cubes/data/rank_percent.json?cube_symbol=ZH1067693&cube_id=1084166&market=cn&dimension=annual&_=1574490138794
(月)
https://xueqiu.com/cubes/data/rank_percent.json?cube_symbol=ZH1067693&cube_id=1084166&market=cn&dimension=month&_=1574490138795
(日)
https://xueqiu.com/cubes/data/rank_percent.json?cube_symbol=ZH1067693&cube_id=1084166&market=cn&dimension=daily&_=1574490138795



- 收益走势
https://xueqiu.com/cubes/nav_daily/all.json?cube_symbol=ZH1067693&since=1566714139000&until=1574490139000

- 组合评分
https://xueqiu.com/cubes/rank/summary.json?symbol=ZH1067693&ua=web

- 最新调仓
https://xueqiu.com/cubes/rebalancing/show_origin.json?rb_id=63222854&cube_symbol=ZH1067693

