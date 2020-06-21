from collections import defaultdict

import justpy as jp

from db import tresults


CHART_DEF = """
{   
    chart: {
            type: 'line'
        },
    title: {
        text: 'Signal value'
    },
    yAxis: {
        title: {
            text: 'Signal value'
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


def signal_values():
    data = tresults.all().namedtuples()
    wp = jp.WebPage()
    chart_in = jp.HighCharts(a=wp, options = CHART_DEF)
    series = defaultdict(list)
    for row in data:
        series[row.ssid].append(row.sig_value)

    chart_in.options.xaxis.categories = [row.id for row in data]
    chart_in.options.series = [{'name': ssid, 'data': values} for ssid, values in series.items()]
    return wp


jp.justpy(signal_values)
