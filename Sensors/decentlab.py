# MIT License
#
# Copyright (c) 2016 Decentlab GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import json

import requests
import pandas as pd


def query(domain, api_key, time_filter='',
          device='//', location='//',
          sensor='//', include_network_sensors=False,
          channel='//',
          agg_func=None, agg_interval=None,
          do_unstack=True,
          convert_timestamp=True, timezone='UTC'):

    select_var = 'value'
    fill = ''
    interval = ''

    if agg_func is not None:
        select_var = agg_func + '("value") as value'
        fill = 'fill(null)'

    if agg_interval is not None:
        interval = ', time(%s)' % agg_interval

    if time_filter != '':
        time_filter = ' AND ' + time_filter

    filter_ = (' location =~ %s'
               ' AND node =~ %s'
               ' AND sensor =~ %s'
               ' AND ((channel =~ %s OR channel !~ /.+/)'
               ' %s)') % (location,
                          device,
                          sensor,
                          channel,
                          ('' if include_network_sensors
                           else 'AND channel !~ /^link-/'))

    q = ('SELECT %s FROM "measurements" '
         ' WHERE %s %s'
         ' GROUP BY "uqk" %s %s') % (select_var,
                                     filter_,
                                     time_filter,
                                     interval,
                                     fill)

    r = requests.get('https://%s/api/datasources/proxy/1/query' % domain,
                     params={'db': 'main',
                             'epoch': 'ms',
                             'q': q},
                     headers={'Authorization': 'Bearer %s' % api_key})

    data = json.loads(r.text)

    if 'results' not in data or 'series' not in data['results'][0]:
        raise ValueError("No series returned: %s" % r.text)

    def _ix2df(series):
        df = pd.DataFrame(series['values'], columns=series['columns'])
        df['series'] = series['tags']['uqk']
        return df

    df = pd.concat(_ix2df(s)
                   for s
                   in data['results'][0]['series'])

    if convert_timestamp:
        df['time'] = pd.to_datetime(df['time'], unit='ms', utc=True)
        try:
            df['time'] = df['time'].dt.tz_localize('UTC')
        except TypeError:
            pass
        df['time'] = df['time'].dt.tz_convert(timezone)

    df = df.set_index(['time', 'series'])
    df = df.sort_index()

    if do_unstack:
        df = df.unstack(level='series')
        df.columns = df.columns.droplevel(0)

    return df