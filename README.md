# pdbDB
搭建分为三步
创表，解压，导入

数据库相关资料在db文件夹中。创建语句在molecule的创建语句

案例中未解压的文件在JF里

解压文件unzip.sh，会解压脚本所在位置的所有文件。

chmod +x db/unzip.sh

db/unzip.sh

解压后文件会放在~/output中。

导入文件为db/insert.py

python3 db/insert.py
