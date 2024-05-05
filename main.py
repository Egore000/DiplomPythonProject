import sys

sys.path.append('C:\\Users\\egorp\\Desktop\\диплом\\файлы\\Python_test\\')

from Resonance import Resonance
from Services import FileService, GraphService


class Research:
    def __init__(self, folder, file, Omega, light_effect, phi_num=1):
        self.folder = folder
        self.file = file
        self.Omega = Omega 
        self.light_effect = light_effect
        self.phi_num = phi_num

        self.init_resonance()

    def init_resonance(self):
        self.res = Resonance.OrbitalResonance(folder_number=self.folder,
                                         file_number=self.file,
                                         Omega_value=self.Omega,
                                         light_effect=self.light_effect)
        self.res.get_data()
        self.data = self.res.data

    def orbital_single(self):
        single = GraphService.SingleGraph({
            'title': f'$\mathit{{Ф_{self.phi_num}}}$',
            'xlabel': '$\it{T}$, годы',
            'ylabel': f'$\mathit{{Ф_{self.phi_num}}}$, °',
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
            'xlabel': '$\it{T}$, годы',
            'y1label': '$\mathit{Ф_1}$, °',
            'y2label': '$\mathit{Ф_2}$, °',
            'y3label': '$\mathit{Ф_3}$, °',
            'y4label': '$\mathit{Ф_4}$, °',
            'y5label': '$\mathit{Ф_5}$, °',
            'grid': {
                'X': {'X_min': 0, 'X_max': 100, 'Nx': 20},
                'Y1': {'Y_min': 0, 'Y_max': 360, 'Ny': 12},
                'Y2': {'Y_min': 0, 'Y_max': 360, 'Ny': 12},
                'Y3': {'Y_min': 0, 'Y_max': 360, 'Ny': 12},
                'Y4': {'Y_min': 0, 'Y_max': 360, 'Ny': 12},
                'Y5': {'Y_min': 0, 'Y_max': 360, 'Ny': 12},
            },
            'annotate': False,
        })

        x = [self.data['time'] for _ in range(5)]
        y = [self.data[f'F{i + 1}'] for i in range(5)]

        common.print(x=x, y=y).show()

    
    def orbital_common_dot_phi(self):
        common = GraphService.CommonGraph({
            'title': '$\dot{\mathit{Ф}}$',
            'type': [True] * 5,
            'xlabel': '$\it{T}$, годы',
            'y1label': '$\dot{\mathit{Ф_1}}$, рад/с',
            'y2label': '$\dot{\mathit{Ф_2}}$, рад/с',
            'y3label': '$\dot{\mathit{Ф_3}}$, рад/с',
            'y4label': '$\dot{\mathit{Ф_4}}$, рад/с',
            'y5label': '$\dot{\mathit{Ф_5}}$, рад/с',
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
                'xlabel': '$\it{T}$, годы',
                'y1label': f'$\dot{{\mathit{{Ф_{num}}}}}$, рад/с',
                'y2label': f'$\mathit{{Ф_{num}}}$, °',
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

        labels = {
            'i': '$\mathit{i}$, °',
            'ecc': '$\it{e}$',
            'a': '$\mathit{a}$, км',
            'megno': 'MEGNO',
            'mean_megno': 'MEGNO',
            'w': '$\mathit{\omega}$, °',
            'Omega': '$\Omega$, °',
            'M': '$\mathit{M}$, °',
        }
        y_labels = {f'y{i + 1}label': labels[elem] for i, elem in enumerate(elems)}

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
            'title': '',
            'type': [None] * len(elems),
            'xlabel': '$\it{T}$, годы',
            'annotate': False,
        }
        params.update(y_labels)
        params.update({'grid': grid})

        common = GraphService.CommonGraph(params)
        common.print(x=x, y=y).show()




def main():
    research = Research(2, 1945, 120, False)
    print(research.res.path_data)

    research.orbital_single()
    research.orbital_common_phi()
    research.orbital_common_dot_phi()
    research.orbital_pair([1])
    research.elements()

if __name__ == "__main__":
    main()