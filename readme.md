#### 遇到的问题 (以下问题出现在Mac环境)
1. 安装过程中, `pipenv install scrapy ` 一直卡在`locking...`中
    
    通过命令`pipenv lock --clear`，然后一切恢复正常

2. 通过上面的步骤，出现 如下错误
            
       ["ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied: '/Users/weibolei/.local/share/virtualenvs/quant-spider-JVGi8YHg/lib/python3.7/site-packages/_cffi_backend.cpython-37m-darwin.so'", 'Consider using the `--user` option or check the permissions.']

    解决方法： 
    `cd /Users/weibolei/.local/share/virtualenvs/` 查看quant-spider-xxx对应的user和权限，发现目录的创建者是root，这就很好解释没有权限的问题，将这个文件删除，重新运行 `pipenv sync ` 和 `pipenv install xxx`命令。
