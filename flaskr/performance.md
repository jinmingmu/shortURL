# 性能测试报告

##本次性能测试使用的docker虚拟机，每个虚拟机有2G的内存，本机处理器为2.4 GHz Intel Core i5，虚拟机的cpu性能大概为本机的50%。

###测试软件为siege

###测试步骤

* 当配置好服务器后，运行
<pre>siege -r 50 -c 20 -b http://localhosts</pre>
访问主页1000次，因为短连接服务的主页只会返回一个含有bad request的json，其实这个访问并不会触及到很多服务逻辑，以此来测试不触碰服务逻辑的情况下每秒可以访问的次数
得到报告为
<pre>Transactions:		        1000 hits
Availability:		      100.00 %
Elapsed time:		        3.41 secs
Data transferred:	        0.04 MB
Response time:		        0.06 secs
Transaction rate:	      293.26 trans/sec
Throughput:		        0.01 MB/sec
Concurrency:		       19.01
Successful transactions:        1000
Failed transactions:	           0
Longest transaction:	        0.23
Shortest transaction:	        0.01
</pre>

* 下面我们来测试跳转的速度  
如果这是一个新的服务，那么我们需要运行<pre>curl http://localhost/?add=http://localhost</pre>来得到一个短地址，我这里得到的短地址为 http://localhost/1
运行以下链接来测试跳转的速度
<pre>siege -r 50 -c 20 -b http://localhost/1</pre>  
访问哈希值为1的短连接1000次，每次这个短连接都会跳转到我们的主页  
得到报告为
<pre>
Transactions:		        2000 hits
Availability:		      100.00 %
Elapsed time:		       17.19 secs
Data transferred:	        0.27 MB
Response time:		        0.17 secs
Transaction rate:	      116.35 trans/sec
Throughput:		        0.02 MB/sec
Concurrency:		       19.58
Successful transactions:        2000
Failed transactions:	           0
Longest transaction:	        0.81
Shortest transaction:	        0.01
</pre>

* 让我们再测试以下跳转到不存在网页的速度，我这里用了一个哈希值999，这个999对应的长地址并不在数据库中存在
<pre>siege -r 50 -c 20 -b  http://localhost/999</pre>
访问哈希值为999的短连接1000次，每次这个短连接都会返回404 no found
得到报告为
<pre>
Transactions:		        1000 hits
Availability:		      100.00 %
Elapsed time:		        6.92 secs
Data transferred:	        0.22 MB
Response time:		        0.14 secs
Transaction rate:	      144.51 trans/sec
Throughput:		        0.03 MB/sec
Concurrency:		       19.77
Successful transactions:           0
Failed transactions:	           0
Longest transaction:	        0.46
Shortest transaction:	        0.00
</pre>

* 最后让我们测试一下跳转到www.google.com的速度  
先运行
<pre>curl http://localhost/?add=http://www.google.com</pre>得到一个短地址  
我这里得到的短地址为 http://localhost/2  
运行siege来测试跳转www.google.com的速度
<pre>siege -r 50 -c 20 -b http://localhost/2</pre>  
具体速度会因为网络连接速度而改变
得到报告
<pre>
Transactions:		        3000 hits
Availability:		      100.00 %
Elapsed time:		       30.32 secs
Data transferred:	       48.70 MB
Response time:		        0.20 secs
Transaction rate:	       98.94 trans/sec
Throughput:		        1.61 MB/sec
Concurrency:		       19.35
Successful transactions:        3000
Failed transactions:	           0
Longest transaction:	        0.90
Shortest transaction:	        0.02
</pre>  
性能测试完成

##性能加强的办法
* 这里我用的虚拟器本身处理速度不够快，换成服务器的话速度会快很多
* 我们用的是mysql将数据存储的方式来得到长地址，如果搭配上memcached来做一个缓存，那么可以大大减少数据库的访问量而且不会浪费内存。
* 换成md5去哈希的方式来得到短地址与长地址，这样不需要数据库的访问
