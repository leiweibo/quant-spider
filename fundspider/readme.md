#### 使用方法
1. 安装pipenv，可以参考 [这里](https://www.jianshu.com/p/d06684101a3d)
2. pipenv 安装完成之后，执行`pipenv shell` 进入到pipenv虚拟环境中，然后执行`pipenv sync` 安装依赖，这里需要修改一下 Pipfile.lock里面taos的依赖，我写的是本地的路径，暂时先手动去修改，暂时我本地的python是3.6版本，如果版本不一致需要修改一下里面的python version
3. 执行quant.sql文件里面的脚本
4. 依赖安装完成之后，进入到fundspider/fundspider 目录下，然后执行scrapy crawl fund-spider 这样就可以运行

### TODO
    [] scrapy层进行去重处理
    [] 插入数据的时候，将基金代码，基金净值+时间存入到redis，用来进行数据去重处理

#### 其他
[基金列表的链接](http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery18307254792960855634_1567851101932&fundCode=501307&pageIndex=3&pageSize=20&startDate=&endDate=&_=1567852435843)

[基金净值的链接](http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=002620&page=1&per=20)

#### 参考网址 
 -  https://zhuanlan.zhihu.com/p/58264923
 -  https://blog.csdn.net/yuzhucu/article/details/55261024
 -  https://www.zhihu.com/question/57734780
 -  https://duanqz.github.io/2018-08-01-Fund-Crawler