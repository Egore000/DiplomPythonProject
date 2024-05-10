import sys

sys.path.append('C:\\Users\\egorp\\Desktop\\диплом\\файлы\\Python\\')

from Resonance import Resonance
from Services import FileService, GraphService, Tools


LABELS = {
        't': '$\it{T}$, годы',
        'i': '$\mathit{i}$, °',
        'ecc': '$\it{e}$',
        'a': '$\mathit{a}$, км',
        'megno': 'MEGNO',
        'mean_megno': 'MEGNO',
        'w': '$\mathit{\omega}$, °',
        'Omega': '$\Omega$, °',
        'M': '$\mathit{M}$, °',
        'F': '$\mathit{{Ф_{}}}$, °',
        'dF': '$\dot{{\mathit{{Ф_{}}}}}$, рад/с',
    }


class Research:

    def __init__(self, folder, file, Omega, light_effect, phi_num=1):
        self.folder = folder
        self.file = file
        self.Omega = Omega 
        self.light_effect = light_effect
        self.phi_num = phi_num

        self.init_resonance()
        self.saver = GraphService.GraphSaver()

    def init_resonance(self):
        self.res = Resonance.OrbitalResonance(folder_number=self.folder,
                                         file_number=self.file,
                                         Omega_value=self.Omega,
                                         light_effect=self.light_effect)
        self.list_data = self.res.get_data()
        self.data = self.res.data

    def orbital_single(self):
        single = GraphService.SingleGraph({
            'title': LABELS['F'].format(self.phi_num),
            'xlabel': LABELS['t'],
            'ylabel': LABELS['F'].format(self.phi_num),
            'grid': {
                'X': {
                    'X_min': 0,
                    'X_max': 100,
                    'Nx': 20,
                },
                'Y': {
                    'Y_min': 0,
                    'Y_max': 360,
                    'Ny': 12,
                }
            },
            'annotate': False,
        })        
        single.print(
            x=self.data['time'],
            y=self.data[f'F{self.phi_num}']
        ).show()

    def orbital_common_phi(self):
        common = GraphService.CommonGraph({
            'title': '$\mathit{Ф}$',
            'type': [None] * 5,
            'xlabel': LABELS['t'],
            'y1label': LABELS['F'].format(1),
            'y2label': LABELS['F'].format(2),
            'y3label': LABELS['F'].format(3),
            'y4label': LABELS['F'].format(4),
            'y5label': LABELS['F'].format(5),
            'grid': {
                'X': {'X_min': 0, 'X_max': 100, 'Nx': 20},
                'Y1': {'Y_min': 0, 'Y_max': 360, 'Ny': 12},
                'Y2': {'Y_min': 0, 'Y_max': 360, 'Ny': 12},
                'Y3': {'Y_min': 0, 'Y_max': 360, 'Ny': 12},
                'Y4': {'Y_min': 0, 'Y_max': 360, 'Ny': 12},
                'Y5': {'Y_min': 0, 'Y_max': 360, 'Ny': 12},
            },
            'annotate': True,
        })

        x = [self.data['time'] for _ in range(5)]
        y = [self.data[f'F{i + 1}'] for i in range(5)]

        common.print(x=x, y=y).show()

    
    def orbital_common_dot_phi(self):
        common = GraphService.CommonGraph({
            'title': '$\dot{\mathit{Ф}}$',
            'type': [True] * 5,
            'xlabel': LABELS['t'],
            'y1label': LABELS['dF'].format(1),
            'y2label': LABELS['dF'].format(2),
            'y3label': LABELS['dF'].format(3),
            'y4label': LABELS['dF'].format(4),
            'y5label': LABELS['dF'].format(5),
            'grid': {
                'X': {'X_min': 0, 'X_max': 100, 'Nx': 0},
                'Y1': {'Y_min': 0, 'Y_max': 360, 'Ny': 0},
                'Y2': {'Y_min': 0, 'Y_max': 360, 'Ny': 0},
                'Y3': {'Y_min': 0, 'Y_max': 360, 'Ny': 0},
                'Y4': {'Y_min': 0, 'Y_max': 360, 'Ny': 0},
                'Y5': {'Y_min': 0, 'Y_max': 360, 'Ny': 0},
            },
            'annotate': False,
            'label_on_right': True,
        })

        x = [self.data['time'] for _ in range(5)]
        y = [self.data[f'dF{i + 1}'] for i in range(5)]

        common.print(x=x, y=y).show()

    def orbital_pair(self, res=[1, 2, 3, 4, 5]):

        x = [self.data['time']] * 2
        for num in res:
            pair = GraphService.PairGraph({
                'type': [True, None],
                'title': '',
                'grid': {
                    'X1': {
                        'X_min': 0,
                        'X_max': 100,
                        'Nx': 0,
                    },
                    'X2': {
                        'X_min': 0,
                        'X_max': 100,
                        'Nx': 5,
                    },
                    'Y1': {
                        'Y_min': 0,
                        'Y_max': 360,
                        'Ny': 0,
                    },
                    'Y2': {
                        'Y_min': 0,
                        'Y_max': 360,
                        'Ny': 4,
                    },
                },
                'xlabel': LABELS['t'],
                'y1label': LABELS['dF'].format(num),
                'y2label': LABELS['F'].format(num),
            })

            y = [
                self.data[f'dF{num}'],
                self.data[f'F{num}'],
            ]
            pair.print(x=x, y=y).show()
            
    def elements(self, elems=['i', 'ecc', 'a', 'mean_megno']):
        x = [self.data['time']] * len(elems)
        y = []
        for elem in elems:
            y.append(self.data.get(elem, []))

        y_labels = {f'y{i + 1}label': LABELS[elem] for i, elem in enumerate(elems)}

        y_grids = {
            f'Y{i + 1}': {
                'Y_min': 0,
                'Y_max': 100,
                'Ny': 0,
            } for i in range(len(elems) + 1)
        }
        grid = {
            'X': {
                'X_min': 0,
                'X_max': 100,
                'Nx': 0,
            }, 
        }
        grid.update(y_grids)

        params = {
            'title': f'$\Omega$={self.Omega} {self.folder}/EPH_{self.file}.DAT',
            'type': [None] * (len(elems) - 1) + [None],
            'xlabel': LABELS['t'],
            'annotate': False,
        }
        params.update(y_labels)
        params.update({'grid': grid})

        common = GraphService.CommonGraph(params)
        common.print(x=x, y=y).show()

    def report(self, elems=['i', 'ecc', 'a', 'mean_megno']):
        # GraphService.plt.rcParams['figure.subplot.hspace'] = 0.4
        report = GraphService.ReportGraph({
            'title': '',
            '1': {
                'type': True,
                'ylabel': LABELS[elems[0]],
            },
            '2': {
                'type': True,
                'ylabel': LABELS[elems[1]],
            },
            '3': {
                'type': True,
                'ylabel': LABELS[elems[2]],
            },
            '4': {
                'type': None,
                'xlabel': LABELS['t'],
                'ylabel': LABELS[elems[3]],
            },
            '5': {
                'type': None,
                'ylabel': LABELS['F'].format(1),
            },
            '6': {
                'type': None,
                'ylabel': LABELS['F'].format(2),
            },
            '7': {
                'type': None,
                'ylabel': LABELS['F'].format(3),
            },
            '8': {
                'type': None,
                'ylabel': LABELS['F'].format(4),
            },
            '9': {
                'type': None,
                'xlabel': LABELS['t'],
                'ylabel': LABELS['F'].format(5),
            },
            'A': {
                'type': True,
                'line': True,
                'ylabel': LABELS['dF'].format(1),
            },
            'B': {
                'type': True,
                'line': True,
                'ylabel': LABELS['dF'].format(2),
            },
            'C': {
                'type': True,
                'line': True,
                'ylabel': LABELS['dF'].format(3),
            },
            'D': {
                'type': True,
                'line': True,
                'ylabel': LABELS['dF'].format(4),
            },
            'E': {
                'type': True,
                'line': True,
                'xlabel': LABELS['t'],
                'ylabel': LABELS['dF'].format(5),
            },
        })
        x_data = self.res.data.get('time')
        x = {k: x_data for k in '123456789ABCDEF'}
        y = {
            '1': self.res.data.get(elems[0]),
            '2': self.res.data.get(elems[1]),
            '3': self.res.data.get(elems[2]),
            '4': self.res.data.get(elems[3]),
            '5': self.res.data.get('F1'),
            '6': self.res.data.get('F2'),
            '7': self.res.data.get('F3'),
            '8': self.res.data.get('F4'),
            '9': self.res.data.get('F5'),
            'A': self.res.data.get('dF1'),
            'B': self.res.data.get('dF2'),
            'C': self.res.data.get('dF3'),
            'D': self.res.data.get('dF4'),
            'E': self.res.data.get('dF5'),
        }
        report.print(x, y)

        # self.saver.save(report, '.', 'test')
        report.show()

    def write_to_file(self, path: str, filename: str):
        ew = FileService.FileWriter(path)
        ew.write(filename, self.list_data)


def main():
    research = Research(2, 3134, 0, False)
    print(research.res.path_data)

    # research.orbital_single()
    # research.orbital_common_phi()
    # research.orbital_common_dot_phi()
    # research.orbital_pair([1])
    # research.elements(['ecc', 'i', 'a', 'Omega'])
    # research.elements(['w',])
    research.report()

    # print(research.find_by_folder(2, 1980))
    # print(research.find_by_elements(26560, 108))

    # research.save()

if __name__ == "__main__":
    main()