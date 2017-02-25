# shortURL

##这个项目有三个主要的功能
1. 当你发送一个包含很长URL的请求时，这个服务会返回一个短URL
2. 当你把这个短URL输入到浏览器时，这个服务会跳转至你以前请求的长URL的地址
3. 这个服务会统计短地址跳转的次数
  
##思路
网上有几种解决方案，第一种是利用md5算法，有极小几率会产生碰撞。第二种是用数据库id作为唯一值然后将id转为62进制作为短地址的哈希值。  
  
我采用是第二种方法，因为觉得相对较好实现而且可以接触到数据库的应用。后续有时间的话也会用第一种方法实现。
  
##现在项目的流程为:
* 当用户发送web query后，先判断长URL是否合法，判断是用一个最基本的正则表达式判断的，如果不合法返回包含400 state code的json文件。

* 然后判断query是哪一种，现在支持两种query：'add'和'counter'。
  
* 如果是'add'，那么查找数据库中有没有这个长URL。数据库中有这个长URL的话返回包含短地址和status code 200的json。没有的话将长地址加入到数据库，然后将长地址的数据库id哈希为62进制，返回包含短地址和status code 200的jason。（短地址的例子： localhost/abc  abc就是哈希后的值）

* 如果是'counter'，那么查找数据库中有没有这个长URL。数据库中有这个长URL的话返回包含这个URL统计次数和statu code 200的json。没有的话返回包含统计次数为0 和status code 200的json。

* 当用户访问短URL，比如localhost/abc，先判断短URL中的哈希值是否合法，不合法的话跳转404页面。合法的话，短URL的哈希值转换为10进制，然后在数据库中查找id是否存在，如果不存在跳转404页面，如果存在则跳转至长地址的连接。

##遇到的问题：
* 一开始我是用 localhost/add 去增加长地址，用localhost/counter去得到长地址的跳转次数，然后发现如果哈希的结果是add和counter，那么这个地址便会默认为请求命令而不是长地址。后来用web query的方式便避免了这个问题。 localhost/?add=

* 在选择post 还是 get的时候我一开始是将add请求用post，counter请求用get，这个不是非常好测试于是将两种都换为了get请求

* 如果长地址不合法的话，比如fdsfd.qe，存储进数据库后拿出来的数据不好跳转。后来加入了正则表达式判断长URL是否合法

* 如果短地址不合法的话，比如在哈希值中加入一些特殊符号，那么便无法转得有效的长地址id，解决办法是检测短地址是否只包含26个大小写字母与数字

* mysql在window下环境设置出错，在mac下也出现各种路径问题，查找了很多资料最后解决了

* docker容器的链接问题，需要两个容器通信，ip如何得到，最后用docker -inspect container 得到ip。

* python 2.7 site package有时因为path没有设定好无法加载，需要在.bash_profile里面加入 
  <pre>export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages</pre>
