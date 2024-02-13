import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
from ..NUMPY.mathematics import Mathematics
from KERNEL.SCRIPT.python.classes.basic import PYBASE

class Plot(PYBASE):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        self.set_style()
        self.set_plt()
        self.mathematics = Mathematics()
        
    def set_style(self):
        self.map_style = dict(
            neon = '@MATPLOTLIB/import/style/neon.mplstyle'
        )
        self._style = str(self.kwargs.get('style', 'neon')) # OPTIONAL
        self._style = self.map_style.get(self._style, self._style)
        if self.fspath(self._style, isfile=True):
            self.style = self.fspath(self._style)
        else:
            self.style = self._style
        plt.style.use(self.style)

    def set_plt(self):
        self.config = dict(
            grid = self.kwargs.get('config_grid', dict(zorder=0.5, alpha=.02, color='#D9D9D9')), # OPTIONAL
            # fontdict = self.kwargs.get('config_font', dict(family=[font, 'Purisa', 'sans-serif', 'serif'], color=color, weight='bold', fontsize='x-large')), # OPTIONAL
        )
        self.fig = plt.figure(figsize=self.kwargs.get('figsize', (10,8)), facecolor=None)
        if self.kwargs.get('hide_axis', False): # OPTIONAL
            plt.axis('off')
        plt.grid(**self.config.get('grid', dict()))
        plt.xlabel(self.kwargs.get('xlabel', 'x'), fontdict=self.config.get('fontdict', dict())) # OPTIONAL
        plt.ylabel(self.kwargs.get('ylabel', 'y'), fontdict=self.config.get('fontdict', dict())) # OPTIONAL
        # plt.xticks(fontname=font)
        # plt.yticks(fontname=font)

    # def save(self):
    #     savefig_result = self.fig.savefig(self.fspath(self.kwargs.get('save', '@MATPLOTLIB/export/fig.png'), makedirs=True), dpi=int(self.kwargs.get('dpi', 1200)), bbox_inches=self.kwargs.get('bbox_inches', 'tight'), **self.kwargs.get('save_params', dict()))
    #     plt.close(self.fig)
    #     return savefig_result
    
    def sampler(self, xmin, xmax, xres=1e-2):
        """number of independent variables"""
        xmin, xmax, xres= float(xmin), float(xmax), float((xres or 1e-2))
        nsamples = int((xmax - xmin) / xres)
        return np.linspace(xmin, xmax, nsamples)

    def grid(self):
        pass # TODO call plot1d/nd multi times and create grid of that plots!!
    
    def plot(self, X, Y, Θ=None, **kwargs):
        if not isinstance(X, (list, tuple)):
            X = [X]
        if not isinstance(Y, (list, tuple)):
            Y = [Y]
        if Θ == None:
            Θ = [None for yidx in range(len(Y))]

        assert len(Y) > 0
        for yidx in range(len(Y)):
            x = X[yidx]
            y = Y[yidx]
            θ = Θ[yidx]

            if not isinstance(x, dict):
                x = dict(x1 = x)
            
            d = len(x)
            
            xlist = []
            for xk in x:
                if isinstance(xk, str) and ':' in x[xk]:
                    xkmin, xkres, xkmax = x[xk].split(':')
                    x[xk] = self.sampler(xkmin, xkmax, xkres)
                xlist.append(x[xk])
            
            if isinstance(y, str):
                y = getattr(self.mathematics, y)(*np.meshgrid(*xlist))
            
            if θ == None:
                θ = [
                    [],
                    dict(label='')
                ]
            
            if d == 1:
                if len(θ[0]) > 0:
                    plt.plot(xlist[0], y, *θ[0], **θ[1])
                else:
                    plt.plot(xlist[0], y, **θ[1])
                plt.legend(loc=self.kwargs.get('loc', 'best'))
            elif d == 2:
                meshgrid = np.meshgrid(*xlist)
                ax = self.fig.add_subplot(projection='3d')
                # ax.plot_surface(meshgrid[0], meshgrid[1], y)
                # ax.set_zlabel(self.kwargs.get('zlabel', 'y'))
                surf = ax.plot_surface(meshgrid[0], meshgrid[1], y, cmap=cm.coolwarm, linewidth=0, antialiased=False)
                ax.set_zlim(np.min(y), np.max(y))
                ax.zaxis.set_major_locator(LinearLocator(10))
                # A StrMethodFormatter is used automatically
                ax.zaxis.set_major_formatter('{x:.02f}')

                # Add a color bar which maps values to colors.
                self.fig.colorbar(surf, shrink=0.5, aspect=5)
            else:
                assert False, 'code bezan star cordinates!!'
                
        if kwargs.get('show', True):
            plt.show()
            

if __name__ == '__main__':
    # plot_tanh = Plot(ylabel='y(x)', loc='upper left')
    # plot_tanh.plot(
    #     [
    #         '-20::20',
    #         '-20:1:20',
    #         [0, -3, 3],
    #         [-1/2, 1/2],
    #     ], 
    #     [
    #         'tanh',
    #         'tanh',
    #         [0, -1, 1],
    #         [-1/2, 1/2],
    #     ],
    #     [
    #         (['-'], dict(label='y = Tanh(x)')),
    #         (['--'], dict(label='‌Bad Mapping By f: $\dot{\Theta}_f$ does not have a good density')),
    #         (['o'], dict(color='red', label='‌Bad Mapping By f: $\dot{\Theta}_f$ ~ uniform/sharp density')),
    #         (['o'], dict(color='green', label='Good Mapping By f: $\dot{\Theta}_f$ ~ smooth density')),
    #     ]
    # )
    
    
    # plot_tanh_sx = Plot(ylabel='s(x)', loc='lower left')
    # plot_tanh_sx.plot(
    #     [
    #         '-20::20',
    #         [0],
    #         [-3, 3],
    #         [-1/2, 1/2],
    #     ], 
    #     [
    #         'tanh_sx',
    #         [1],
    #         [1, 1],
    #         [0, 0],
    #     ],
    #     [
    #         (['-'], dict(label='s(x) # Tanh satisfaction loss function')),
    #         (['s'], dict(color='red', label='‌$\dot{\Theta}_f$ ~ uniform density')),
    #         (['o'], dict(color='red', label='$\dot{\Theta}_f$ ~ sharp density')),
    #         (['o'], dict(color='green', label='$\dot{\Theta}_f$ ~ smooth density')),
    #     ]
    # )
    
    
    plot_tanh_sx = Plot(xlabel='grad | resolution=0.1', ylabel='λgs . GS(grad) | λgs=3', loc='upper left')
    plot_tanh_sx.plot(
        [
            '-100:0.1:100',
        ], 
        [
            'tanh_gsl0',
        ],
        [
            (['-'], dict(label='λgs . GS(grad)')),
        ]
    )


    # plot_tanh_sx = Plot(xlabel='grad | resolution=0.1', ylabel='λgs . GS(grad) | λgs=3', loc='upper left')
    # plot_tanh_sx.plot(
    #     [
    #         '-100:0.1:100',
    #         [0.0],
    #     ], 
    #     [
    #         'tanh_gsl0',
    #         'tanh_gsl0',
    #     ],
    #     [
    #         (['.'], dict(label='λgs . GS(grad≢0)')),
    #         (['.'], dict(label='λgs . GS(grad=0)')),
    #     ]
    # )
    
    
    # plot_gsl = Plot(xlabel='grad', ylabel='x', zlabel='GSL(grad,x)', loc='upper left', hide_axis=True)
    # plot_gsl.plot(
    #     [
    #         dict(x1 = '-5:0.25:5', x2 = '-5:0.25:5'),
    #     ], 
    #     [
    #         'tanh_gsl',
    #     ],
    #     [
    #         (['-'], dict(label='GSL(grad, x; grad=1) = grad * (1 + s(x)/2) # gradient scaler loss function by Tanh properties')),
    #     ]
    # )

    pass

    

