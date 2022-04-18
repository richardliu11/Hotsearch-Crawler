# [爬虫]抓取新浪微博热搜相关数据项
在用户未登录状态下，访问微博热搜页（https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6) 抓取[热搜话题排名]，[热搜话题]，[热搜话题热度]，[热搜链接]。通过二次访问热搜链接，跳转至该热搜话题页，抓取[话题主持人]，[今日阅读]，[今日讨论]，[分类]，[地区]。

## 反爬机制说明

### 微博临时cookie 

### 访问IP限制
通过代理IP规避 （http://FQWH123.v4.dailiyun.com/query.txt?key=NPA2F4B388&word=&count=17&rand=false&ltime=0&norepeat=false&detail=false）。

## 实现步骤

### ①获取临时cookie
携带cb和fp数据requests请求验证页（https://passport.weibo.com/visitor/genvisitor） 返回params数据，携带并再次请求验证页，返回cookie。携带该cookie访问热搜页。

### ②请求热搜页面
携带临时cookie、代理IP的API返回的IP地址，requests请求热搜页。

### ③获取热搜页数据
通过正则表达式，夹出[热搜话题排名]，[热搜话题]，[热搜话题热度]，[热搜链接]；存储在dict中。append方法。

### ⑥二次请求：热搜话题页 
遍历循环（50个左右）请求（requests）热搜页获取的热搜话题链接（携带proxy、headers）；注意time.sleep间隔

### ⑤获取热搜话题页数据
通过正则表达式，夹出[话题主持人]，[今日阅读]，[今日讨论]，[分类]，[地区]；存储在dict中。append方法。

### 数据写入
建立本地数据库链接，写入MySQL。
