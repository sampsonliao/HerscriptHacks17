import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter
from bokeh.models import HoverTool
from bokeh.embed import components

from data_generator import convert_todatetime, convert_totimestamp, gen_liter


def get_tags(filename):
    df = pd.read_csv(filename, header=0, names=['month_num'])

    date = pd.date_range(start='1-01-17', end='12-01-17', freq='MS')
    df['liter'] = df['month_num'].apply(gen_liter)
    df['datetime'] = df['month_num'].apply(convert_todatetime)
    df['timestamp'] = df['datetime'].apply(convert_totimestamp)

    df_liter = pd.DataFrame({'liter': df['liter'], 'month_num': df['month_num'], 'datetime': df['datetime'],
                             'timestamp': df['timestamp']}, columns=['liter', 'month_num', 'timestamp'])
    df_liter.sort_values('month_num', inplace=True)
    df_liter_grouped = df_liter.groupby('month_num').mean()
    df_liter_grouped['datetime'] = date
    output_file("line.html")

    df['timestamp'] = df['timestamp'].apply(lambda x: (x * 1000))
    df_liter_grouped['timestamp'] = df_liter_grouped['timestamp'].apply(lambda x: (x * 1000))

    TOOLS = ['box_zoom', 'box_select', 'crosshair', 'resize', 'reset']

    colors = [
        "#%02x%02x%02x" % (int(r), int(g), 0) for r,g in zip((df['liter']-100)*.8,0.2*(df['liter']+250))
    ]
    p = figure(plot_width=1100, plot_height=500, title="Water usage, Liters Per Kilo Produce", tools=TOOLS)
    cr = p.circle(df['timestamp'], df['liter'], size=20, color=colors, alpha=0.5, hover_fill_color="firebrick",
             hover_alpha=0.3, hover_line_color="white")

    p.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='hline'))
    p.line(df_liter_grouped['timestamp'], df_liter_grouped['liter'], line_width=2)
    p.xaxis[0].formatter = DatetimeTickFormatter(months="%b")

    p.xaxis.axis_label = "Month"
    p.yaxis.axis_label = "L/kg"
    script_div = components(p)


    return script_div


if __name__ == "__main__":
    script, div = get_tags('Data/randmonth.csv')
