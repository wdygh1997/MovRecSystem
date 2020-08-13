# MovRecSystem

## 这是什么？

本项目是一个小型的电影推荐系统，使用MovieLens数据集，根据数据集中的评分数据来挖掘电影之间相似度并进行推荐。项目采用潜在语义分析（LSA），使用奇异值分解（SVD）和非负矩阵分解（NMF）两种具体算法实现。推荐分为统计推荐、离线推荐、相似推荐、实时推荐四种，同时系统提供登陆注册和电影搜索功能，GUI基于Tkinter。

## 如何运行？

### 1、运行环境

项目使用python3编写，另需numpy、pandas、requests、pillow、lxml包，数据库为MySQL，请事先配置上述环境

### 2、训练数据

运行algorithm.svd文件，会在data文件夹下生成similaritySVD文件和simSVD.csv、pdtSVD.csv两个数据文件；

运行algorithm.nmf文件，会在data文件夹下生成similarityNMF文件和
simNMF.csv、pdtNMF.csv两个数据文件；

运行algorithm.online文件，会在data文件夹下生成simOL.csv、
pdtOL.csv两个数据文件；

运行algorithm.readrating文件，会在data文件夹下生成movieidlist文件

### 3、加载数据

运行dbcon.dbcreate文件，会在MySQL中创建movrecsystem数据库（连接账户和密码在dbcon.mysqlcon中修改）；

运行loaddata.loadbefore文件，会将links、movies、ratings、tags、users数据表载入数据库；

运行loaddata.loadafter文件，会将simsvd、pdtsvd、simnmf、pdtnmf、simol、pdtol数据表载入数据库

### 4、运行项目

运行gui.mian文件，进入电影推荐系统

## 附录（原理介绍）

基于ratings数据表生成<用户-电影>评分矩阵，使用SVD分解和NMF分解两种方法得到电影特征向量组成的矩阵（参考《统计学习方法第2版李航》第17、15章）；

统计被评分次数最多的若干热门电影，得到统计推荐；

由电影特征向量，计算电影之间的余弦相似度，得到相似推荐；

以相似度为权重，由已评分电影的评分计算未评分电影的预测分数，得到离线推荐；

生成待推荐队列（老用户为离线推荐+最新评分电影的相似推荐、对新用户为统计推荐），计算最近评分电影与之相似度x最近评分电影评分为推荐优先级，得到在线实时推荐
