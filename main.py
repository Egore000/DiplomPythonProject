import sys

sys.path.append('C:\\Users\\egorp\\Desktop\\диплом\\файлы\\Python_test\\')

from Resonance import Resonance
from Services import Tools, FileService, GraphService


class Research:
    def __init__(self, folder, file, Omega, light_effect, phi_num):
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
            'title': f'$\Phi_{self.phi_num}$',
            'xlabel': '$\it{T}, годы$',
            'ylabel': f'$\Phi_{self.phi_num}$, град',
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
            'title': '$\Phi$',
            'type': [None] * 5,
            'xlabel': '$\it{T}$, годы',
            'y1label': '$\Phi_1$, град',
            'y2label': '$\Phi_2$, град',
            'y3label': '$\Phi_3$, град',
            'y4label': '$\Phi_4$, град',
            'y5label': '$\Phi_5$, град',
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
            'title': '$\dot{\Phi}$',
            'type': [True] * 5,
            'xlabel': '$\it{T}$, годы',
            'y1label': '$\dot{\Phi}_1$, рад/с',
            'y2label': '$\dot{\Phi}_2$, рад/с',
            'y3label': '$\dot{\Phi}_3$, рад/с',
            'y4label': '$\dot{\Phi}_4$, рад/с',
            'y5label': '$\dot{\Phi}_5$, рад/с',
            'grid': {
                'X': {'X_min': 0, 'X_max': 100, 'Nx': 0},
                'Y1': {'Y_min': 0, 'Y_max': 360, 'Ny': 0},
                'Y2': {'Y_min': 0, 'Y_max': 360, 'Ny': 0},
                'Y3': {'Y_min': 0, 'Y_max': 360, 'Ny': 0},
                'Y4': {'Y_min': 0, 'Y_max': 360, 'Ny': 0},
                'Y5': {'Y_min': 0, 'Y_max': 360, 'Ny': 0},
            },
            'annotate': False,
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
                        'Nx': 20,
                    },
                    'Y1': {
                        'Y_min': 0,
                        'Y_max': 360,
                        'Ny': 0,
                    },
                    'Y2': {
                        'Y_min': 0,
                        'Y_max': 360,
                        'Ny': 20,
                    },
                },
                'xlabel': '$\it{T}$, годы',
                'y1label': f'$\dot{{\Phi_{num}}}$, рад/с',
                'y2label': f'$\Phi_{num}$, град',
            })

            y = [
                self.data[f'dF{num}'],
                self.data[f'F{num}'],
            ]
            p = pair.print(x=x, y=y).show()
            


def main():
    research = Research(2, 1945, 120, False, 2)

    # research.orbital_single()
    # research.orbital_common_phi()
    # research.orbital_common_dot_phi()
    research.orbital_pair([1])

if __name__ == "__main__":
    main()