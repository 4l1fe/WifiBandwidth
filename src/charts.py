from json import loads
from collections import defaultdict

import justpy as jp

from db import tresults
from bandwidth import T_INPUT, T_OUTPUT


CHART_DEF = """
{   
    chart: {
            type: 'line'
        },
    title: {
        text: 'Bandwidth',
    },
    yAxis: {
        title: {
            text: 'Recv/Sent Mbps'
        }
    },
    xAxis: {
        title: {
            text: 'try'
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle',
        title: {
            text: 'SSID'
        }
    },
}
"""


def to_Mbps(amount):
    return amount / 1000 / 1000


def signal_values():
    data = tresults.all().namedtuples()
    wp = jp.WebPage()
    chart_in, chart_out = jp.HighCharts(a=wp, options = CHART_DEF), jp.HighCharts(a=wp, options = CHART_DEF)
    series = defaultdict(lambda : defaultdict(list))
    for row in data:
        if row.ssid in ('Sunny Days 13', 'Sunny Days 3', 'Sunny Days 4', 'Sunny Days 15', 'SmallWall'):
            pass
        json = loads(row.json)
        series[row.type][row.ssid, 'recv'].append(to_Mbps(json['end']['sum_received']['bits_per_second']))
        series[row.type][row.ssid, 'sent'].append(-to_Mbps(json['end']['sum_sent']['bits_per_second']))

    chart_in.options.subtitle.text = 'Client to server direction'
    chart_in.options.series = [{'name': (ssid, type), 'data': values} for (ssid, type), values in series[T_INPUT].items()]
    chart_out.options.subtitle.text = 'Server to client direction'
    chart_out.options.series = [{'name': (ssid, type), 'data': values} for (ssid, type), values in series[T_OUTPUT].items()]
    return wp


jp.justpy(signal_values)
