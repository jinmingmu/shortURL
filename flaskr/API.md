#API 说明
##当这个服务开始运行后，您可以用GET方式去得到长地址对应的短地址。  

###假设现在我们的服务运行在localhost上。现在我们希望得到一个长地址 http://www.google.com 对应的短地址。
我们可以发送一个GET请求: http://localhost?add=http://www.google.com 
如果我们希望使用curl命令，我们可以输入
<pre>curl http://localhost/?add=http://www.google.com</pre>
如果成功的话，服务会返回如下的信息：
<pre>
{
  "mimetype": "application/json", 
  "shortURL": "http://localhost/14", 
  "status": 200
}
</pre>
* mimetype:返回的是json 文件
* shortURL:返回的短地址链接
* status:状态码

如果失败的话，服务器会返回
<pre>
{
  "error": "Bad request", 
  "status": 400
}
</pre>
* error:错误的请求
* status:状态码

###现在我们希望统计一个长地址总共跳转了几次，比如http://www.google.com 是我们的长地址。
我们可以发送一个GET请求: http://localhost?counter=http://www.google.com 
如果我们希望使用curl命令，我们可以输入
<pre>curl http://localhost/?counter=http://www.google.com</pre>
如果成功的话，服务器会返回如下的信息：
<pre>
{
  "counter": 258, 
  "mimetype": "application/json", 
  "status": 200
}
</pre>
* mimetype:返回的是json 文件
* counter:长地址总共跳转的次数
* status:状态码

###现在我们希望从一个短地址跳转到一个长地址，比如 http://localhost/14 是我们的短地址。
我们可以发送一个GET请求: http://localhost/14
如果我们希望使用curl命令，我们可以输入
<pre>curl http://localhost/14</pre>
如果成功的话你将会得到302状态码并跳转至长连接的地址。如果失败的话你会得到404状态码
