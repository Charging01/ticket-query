"""Train tickets query via command-line.
   火车票通过命令行查询。
Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets beijing shanghai 2020-01-25

"""
import json

import colorama
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style
from station import station
import requests
from colorama import init, Fore
from docopt import docopt

init()                                  # 使用colorama前的初始化

def cli():

    arguments = docopt(__doc__)
    from_station = station.get(arguments['<from>'])        # station是个字典
    to_station = station.get(arguments['<to>'])
    date = arguments['<date>']

    # 构建url,输入车站名字，直接从station字典中获得相对应的字母代码
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date={}' \
          '&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date, from_station, to_station)
    # print("这是网址:", url)
    options = ''.join([
        key for key, value in arguments.items() if value is True])
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, '
                     'like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Cookie': 'JSESSIONID=0FCBD07FA01EA1713255920101896AC0;'
                 ' route=c5c62a339e7744272a54643b3be5bf64;'
                 ' BIGipServerpool_passport=384631306.50215.0000; RAIL_EXPIRATION=1582955512068; '
                 'RAIL_DEVICEID=qUANl2BZU-iRhsSMlPYc2Ut5AU-XbI_'
                 'XGAWLMc6T1MVYaIeLtvh3KoZuNsAM4fIIznGMn7Z5bx246WADUQl2C2AZhqvnwJmYH-3DRnXMvWRItWlMtwfayV6YckM8VU7UMhb5'
                  'R6cJChWUeBOyEDz-LP_GYdUBPGZ7; '
                 '_jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; '
                 '_jc_save_toDate=2020-02-26; '
                 '_jc_save_wfdc_flag=dc; BIGipServerotn=2062024970.64545.0000; _jc_save_fromDate=2020-02-27'
    }
    r = requests.get(url, verify=False, headers=headers)    # 添加verify=False参数不验证证书
    available_trains = r.json()['data']['result']           # 返回列表
    station_map = r.json()['data']['map']                  # 返回的是字典形式，地名和代号一一对应,下面要用到

    # print(station_map)  # {'AOH': '上海虹桥', 'VNP': '北京南', 'SNH': '上海南', 'BJP': '北京', 'SHH': '上海'}

    # 做表格，设置表头
    table = PrettyTable(["车次", "出发站", "到达站", "出发时间", "到达时间", "历时", "特等座", "一等座", "二等座", "软卧",
                         "硬卧", "软座", "硬座", "无座"])

    for data in available_trains:
        list = data.split("|")        # 按照“|” 切分
        # print(list)
        if list[1] == '列车停运':      # 以列车停运开头的那几行均不是
            continue
        line_nun = list[3]    # 车次
        from_sta = list[6]
        to_sta = list[7]
        start_time = list[8]
        stop_time = list[9]
        cost_time = list[10]

        TDZ = list[32] or "--"   # 特等座     # 如果没有信息，用--显示
        YDZ = list[31] or "--"  # 一等座
        EDZ = list[30] or "--"  # 二等座
        RW = list[23] or "--"  # 软卧
        YW = list[28] or "--"  # 硬卧
        RZ = list[27] or "--"  # 软座
        YZ = list[29] or "--"  # 硬座
        WZ = list[26] or "--"  # 无座

        # 表格添加列 按照表格方式整齐地输出+对输出的每个字符和“|”进行着色
        table.add_row([line_nun, Fore.LIGHTRED_EX+station_map[from_sta]+Fore.RESET,
                       Fore.LIGHTBLUE_EX + station_map[to_sta]+Fore.RESET,
                       Fore.LIGHTRED_EX+start_time+Fore.RESET, Fore.LIGHTGREEN_EX+stop_time+Fore.RESET,
                       cost_time, TDZ, YDZ, EDZ, RW, YW, RZ, YZ, WZ])
    print(table)


if __name__ == '__main__':
    cli()



