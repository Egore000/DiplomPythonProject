import os
import sys

sys.path.append('C:\\Users\\egorp\\Desktop\\диплом\\файлы\\Python\\')

import numpy as np
import matplotlib.pyplot as plt

from Services import Tools
from config import cfg, graphcfg

plt.rcParams.update(graphcfg.custom_rcParams)


class Graph:
    x_ticks = np.linspace(0, 100, 11) 
    y_ticks = np.linspace(0, 360, 24)

    def __init__(self, params=graphcfg.custom_rcParams):
        self._fig = plt.figure()
        self.params = params

    def print(self, x, y):
        raise NotImplementedError('Abstract method need to be overloaded')

    def show(self):
        mngr = plt.get_current_fig_manager()
        mngr.window.geometry('+0+0')
        plt.show()
    
    @classmethod
    def _line(cls, ax, x, y):
        if max(y) * min(y) < 0:
            ax.plot([min(x), max(x)], [0, 0], '--', color='black')
        return ax

    @classmethod
    def _annotate(cls, axes, x, y):
        text = list(zip(*Tools.enum(x)))[0]
        for n, txt in enumerate(text):
            axes.annotate(txt, (x[n], y[n] + 0.2), size=4)

    def _grid(self, axes: plt.Axes, x_key: str = 'X', y_key: str = 'Y'):
        x_grid = self.params.get('grid').get(x_key)
        y_grid = self.params.get('grid').get(y_key)

        x_min = x_grid.get('X_min', 0)
        x_max = x_grid.get('X_max', 100)
        
        y_min = y_grid.get('Y_min', 0)
        y_max = y_grid.get('Y_max', 360)

        nx = x_grid.get('Nx', 10)
        ny = y_grid.get('Ny', 10)
        
        x_ticks = np.linspace(x_min, x_max, nx + 1)
        y_ticks = np.linspace(y_min, y_max, ny + 1)

        axes.set_xticks(x_ticks, minor=True)
        axes.set_yticks(y_ticks, minor=True)

        axes.grid(which='minor', axis='y')
        if nx != 0:
            axes.grid(which='both', axis='x')

    @property
    def params(self):
        return self._params
    
    @params.setter
    def params(self, prms: dict):
        self._params = prms

    def _print_axes(self, ax, x, y, type=None):        
        if type:
            ax.plot(x, y, **graphcfg.line_style)
        else:
            ax.scatter(x, y, **graphcfg.marker_style)
        return ax

    def _set_params(self):
        self._fig.suptitle(self.params.get('title'))


class SingleGraph(Graph):

    def print(self, x, y):
        self._ax = self._fig.subplots(sharex=True)
        self._ax = super()._print_axes(self._ax, x, y)
        
        if self.params.get('annotate'):
            self._annotate(self._ax, x, y)
        
        if self.params.get('grid'):
            self._grid(self._ax)

        if self.params.get('line'):
            self._line(self._ax, x, y)
        
        self._set_params()
        return self
    
    def _set_params(self):
        super()._set_params()
        self._ax.set_xlabel(self.params.get('xlabel', 'x'))
        self._ax.set_ylabel(self.params.get('ylabel', 'y'))
    

class CommonGraph(SingleGraph):

    def print(self, x, y):
        if hasattr(y[0], '__iter__'):
            self._ax = self._fig.subplots(len(y), sharex=True)
            self._ax = self._print_axes(self._ax, x, y)
            self._set_params()
            return self
        else:
            return super().print(x, y)

    def _print_axes(self, ax: list[plt.Axes], x, y, type_=None):
        if type_ is None:
            type_ = self.params['type']

        if not hasattr(ax, '__iter__'):
            ax = [ax]

        for i, axes in enumerate(list(ax)):
            if self.params.get('annotate'):
                self._annotate(axes, x[i], y[i])
            
            x_key = f'X{i + 1}'
            y_key = f'Y{i + 1}'

            if self.params.get('line', {}).get(y_key):
                self._line(axes, x, y)

            if self.params.get('grid', {}).get(y_key):
                if self.params.get('grid').get(x_key):
                    self._grid(axes, x_key=x_key, y_key=y_key)
                else:
                    self._grid(axes, y_key=y_key)

            axes = super()._print_axes(axes, x[i], y[i], type_[i])
            
            if i % 2 and len(ax) > 2:
                axes.yaxis.tick_right()
                axes.yaxis.labelpad = 30
                if self.params.get('label_on_right'):
                    axes.yaxis.label.set_rotation(-90)
                    axes.yaxis.set_label_position('right')
        return ax

    def _set_params(self):
        try:
            self._ax[-1].set_xlabel(self.params.get('xlabel', 'x'))
            
            for i, axes in enumerate(self._ax):
                axes.set_ylabel(self.params.get(f'y{i + 1}label', f'y{i + 1}'))

        except TypeError:
            super()._set_params()
        Graph._set_params(self)


class PairGraph(CommonGraph):
    pass


class ReportGraph(Graph):
    def __init__(self, params=graphcfg.custom_rcParams):
        self._params = params
        self._mosaic = '.5A;16B;27C;38D;49E'
        self._clear_mosaic = '15726839B4ACDE'
        self._fig, self._axes = plt.subplot_mosaic(self._mosaic, sharex=True)

    def _set_params(self):
        super()._set_params()
        for key in self._axes.keys():
            self._axes[key].set_xlabel(self.params.get(key).get('xlabel'))
            self._axes[key].set_ylabel(self.params.get(key).get('ylabel'))


    def _print_axes(self, ax: dict[plt.Text, plt.Axes], x: dict[str, list], y: dict[str, list], type_=None):
        for key in self._clear_mosaic:
            axes = ax.get(key)
            data_x = x.get(key)
            data_y = y.get(key)

            if self.params.get(key).get('line'):
                self._line(axes, data_x, data_y)

            if key in '2468BD':
                axes.yaxis.tick_right()

            if key in '56789':
                if 180 <= max(y[key]) <= 360:
                    axes.set_yticks([0, 180, 360])
                elif max(y[key]) <= 180:
                    axes.set_yticks([0, 90, 180])

            axes = super()._print_axes(axes, data_x, data_y, self.params.get(key).get('type'))
            ax[key] = axes
        return ax
        
    def print(self, x, y):
        self._ax = self._print_axes(self._axes, x, y)
        self._set_params()
        return self


class GraphSaver:
    @staticmethod
    def save(graph: Graph, path: str, title: str):
        if not os.path.exists(path):
            os.makedirs(path)
        graph._fig.savefig(path + f"\\{title}.png", dpi=100)


def main():
    pass

if __name__ == "__main__":
    main()