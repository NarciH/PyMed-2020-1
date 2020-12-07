import ipywidgets as ipw
from ipywidgets import widgets, interactive_output
import numpy as np

import plotly.graph_objects as go
import matplotlib.pyplot as plt

def get_app(dict_parameters_coef_1 = {'min':1,'max':10,'step':1,'value':1},dict_parameters_coef_2 = {'min':1,'max':10,'step':1,'value':1},dict_parameters_coef_3 = {'min':1,'max':10,'step':1,'value':1}):
    
    def process_edo(a,b,c,r_x,condition_1,condition_2,tf,n):
    
        from scipy.integrate import odeint

        def df(y,x):
            y1, y2= y[0], y[1] #variables de paso
            dy1 = y2 
            dy2 = (eval(r_x)-b*y2-c*y1)/a
            return [dy1,dy2]

        try:
            y0 = [float(eval(i)) for i in [condition_1.split('=')[1],condition_2.split('=')[1]]]
            x_vector = np.linspace(0,tf,n)


            sol = odeint(df, y0, x_vector)

            y_sol = sol[:,0] #toma el vector correspondiente a la solucion de y1
            dy_sol = sol[:,1]
            with fig_y.batch_update():
                fig_y.data[0].x = x_vector
                fig_y.data[0].y = y_sol
            with fig_Dy.batch_update():
                fig_Dy.data[0].x = x_vector
                fig_Dy.data[0].y = dy_sol
            with fig_y_vs_Dy.batch_update():
                fig_y_vs_Dy.data[0].x = y_sol
                fig_y_vs_Dy.data[0].y = dy_sol
            print('Operación finalizada con exito')
        except:
            print('Revise bien los indicadores.')

    box_layout = widgets.Layout(display='flex',flex_flow='column',align_items='center')

    wid_coef_1 = widgets.FloatSlider(min = dict_parameters_coef_1['min'],
                                   max = dict_parameters_coef_1['max'],
                                   step = dict_parameters_coef_1['step'],
                                   value = dict_parameters_coef_1['value'],
                                   description=r'$a:$')
    
    wid_coef_2 = widgets.FloatSlider(min = dict_parameters_coef_2['min'],
                                   max = dict_parameters_coef_2['max'],
                                   step = dict_parameters_coef_2['step'],
                                   value = dict_parameters_coef_2['value'],
                                   description=r'$b:$',readout_format='.3f')
    
    wid_coef_3 = widgets.FloatSlider(min = dict_parameters_coef_3['min'],
                                   max = dict_parameters_coef_3['max'],
                                   step = dict_parameters_coef_3['step'],
                                   value = dict_parameters_coef_3['value'],
                                   description=r'$c:$')

    wid_tf = widgets.IntSlider(min = 10,max = 100,step = 10,value = 20,description=r'$t:$')
    wid_n = widgets.IntSlider(min = 10,max = 500,step = 10,value = 100,description=r'$n:$')

    wid_rx = widgets.Text(value='np.sin(x)',placeholder='Type something',description=r'$r(x):$')

    wid_cond_1 = widgets.Text(value='y(0)=0',placeholder='Type something',description="$y(x_0)=y_0$")
    wid_cond_2 = widgets.Text(value='Dy(0)=0',placeholder='Type something',description="$y'(x_0)=y_0$")

    fig_y = go.FigureWidget([go.Scatter(x = [1,2,3],y = [1,2,3])]).update_layout(template = 'plotly_white',width = 400,margin = {'l':20,'r':10,'b':20,'t':20},title = '<br>Solución de la EDO',xaxis_title = r'$x$',yaxis_title = r'$y$')
    fig_Dy = go.FigureWidget([go.Scatter(x = [1,2,3],y = [1,2,3])]).update_layout(template = 'plotly_white',width = 400,margin = {'l':20,'r':10,'b':20,'t':20},title = '<br>Derivada de la EDO',xaxis_title = r'$x$',yaxis_title = r'$\dot{y}$')
    fig_y_vs_Dy = go.FigureWidget([go.Scatter(x = [1,2,3],y = [1,2,3])]).update_layout(template = 'plotly_white',width = 400,margin = {'l':20,'r':10,'b':20,'t':20},title = '<br>Derivada vs Solución de la EDO',xaxis_title = r'$y$',yaxis_title = r'$\dot{y}$')
    
    dict_widgets = {'a':wid_coef_1,'b':wid_coef_2,'c':wid_coef_3,'r_x':wid_rx,'condition_1':wid_cond_1,'condition_2':wid_cond_2,'tf':wid_tf,'n':wid_n}
    
    output = interactive_output(process_edo,dict_widgets)
    
    ui = widgets.VBox([
        widgets.HBox([widgets.Label(value="$(aD^2+bD+c)y(x) = r(x)$")]),
        widgets.HBox([wid_cond_1,wid_cond_2,wid_tf,wid_n]),
        widgets.HBox([wid_coef_1,wid_coef_2,wid_coef_3,wid_rx]),
        widgets.HBox([fig_y,fig_Dy,fig_y_vs_Dy]),
        widgets.HBox([output])
    ])
    return(ui)