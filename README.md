# 1.’raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)'
出现以上的错误，我收集了大概这几种情况
## 1）没加请求头
## 2）url有误
url = https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'
url有问题，一直在更新的，其他博客的url现在再访问，会出现‘客服中心’界面的错误
修改： query?变成 queryO?
## 3）自己输入错误
日期2020-01-25 输成 2020-1-25
  或者 日期没有修改  执行命令时 python3 tickets.py 北京 上海 2020-02-28，日期要保证是今天及以后的日期 
# 2.时间判断
输入时间必须在当天及以后15天内，可以进行输入判断，当前时间获取 now=datetime.date.today()，15天后的时间 last=now+datetime.timedelta(days=14)  #15天后的日期
