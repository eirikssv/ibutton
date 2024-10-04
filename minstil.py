import plotly.io as pio


pio.templates['simple_white_cust'] = pio.templates['simple_white']

#ORIGINALT FARGEKART
# pio.templates['simple_white_cust']['layout']['colorway'] = ['#003C65', '#14B978', '#CDFAE1', '#004628', '#C89B14', '#BE3C37', '#780050']

#ENDRET FARGEKART FOR DENNE PUBLIKASJON
pio.templates['simple_white_cust']['layout']['colorway'] = ['#003C65', '#14B978', '#C89B14', '#BE3C37', '#780050']
pio.templates['simple_white_cust']['layout']['xaxis']['showgrid'] = True
pio.templates['simple_white_cust']['layout']['yaxis']['showgrid'] = True
pio.templates['simple_white_cust']['layout']['font'] = {'color': 'rgb(0,0,0)', 'size': 12, 'family': 'Calibri'}
pio.templates['simple_white_cust']['layout']['title']['x'] = 0.05
pio.templates['sintef'] = pio.templates['simple_white_cust']


def gen_title(title: str, subtitle = False, fontsize = 12, bold = True):

    if subtitle == False:
        tittel = '<span style="font-size: ' + str(fontsize) + 'px;"><b>' + str(title) + '</b></span>'
    else:
        tittel = '<span style="font-size: ' + str(fontsize) + 'px;"><b>' + str(title) + '</b><br>' + str(subtitle) + '</span>'
    return tittel

def colormaps(x, turnOn=False):
    if x == 1:
        colorlist = ['#003C65', '#14B978', '#CDFAE1', '#004628', '#C89B14', '#BE3C37', '#780050']
    elif x == 2:
        colorlist = ['#003C65', '#14B978', '#C89B14', '#BE3C37', '#780050']
    if turnOn:
        pio.templates['sintef']['layout']['colorway'] = colorlist
        
    return colorlist

