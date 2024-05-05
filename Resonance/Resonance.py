import sys

sys.path.append('C:\\Users\\egorp\\Desktop\\диплом\\файлы\\Python_test\\')

from Services import FileService, Mechanics, Tools
from config import cfg, const


class Resonance:
    _U = 1
    _V = 2

    def __init__(self, 
                 folder_number: int,
                 file_number: int,
                 Omega_value: int,
                 light_effect: bool = False):
        self._folder = folder_number
        self._file = file_number
        self._Omega = Omega_value
        self._LE = 'Со световым давлением\\' if light_effect else 'Без светового давления\\'

    @property
    def path_data(self):
        return cfg.PATH_DATA + self._LE + f'Omega_{self._Omega}\\{self._folder}\\EPH_{str(self._file).rjust(4, "0")}.DAT'
    
    @property
    def path_figure(self):
        return cfg.PATH_FIG + self._LE + f'Omega_{self._Omega}\\'
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, _data: dict):
        if not isinstance(_data, dict):
            raise TypeError()
        self._data = _data

    def _get_data_from_file(self) -> dict:
        raise NotImplementedError()
        
    def get_data(self):
        raise NotImplementedError()
    

class OrbitalResonance(Resonance):

    def _get_data_from_file(self) -> dict:
        eph = FileService.EPHFileReader(self.path_data)

        data = eph.read()
        transposed_data = Tools.transpose(data)
        return transposed_data

    def get_data(self) -> dict:
        data = self._get_data_from_file()

        time = data['time']
        coords = data['coords']
        velocities = data['velocities']
        date = data['date']
        megno = data['megno']
        mean_megno = data['mean_megno']

        outdata = []
        for idx, (x, v) in enumerate(zip(coords, velocities)):
            ecc, i, a, Omega, w, M = Mechanics.CoordsToElements(x, v)

            Y, m, d = date[idx]

            phi = Mechanics.resonance(Y, m, d, M=M, Omega=Omega, w=w, u=self._U, v=self._V)
            dot_phi = Mechanics.derivative_resonance(ecc, i, a, u=self._U, v=self._V)
            
            outdata.append({
                'time': time[idx],
                'F1': phi[0], 
                'F2': phi[1], 
                'F3': phi[2], 
                'F4': phi[3], 
                'F5': phi[4], 
                'dF1': dot_phi[0], 
                'dF2': dot_phi[1], 
                'dF3': dot_phi[2], 
                'dF4': dot_phi[3], 
                'dF5': dot_phi[4],
                
                'a': a,
                'ecc': ecc,
                'i': i * const.toDeg,
                'w': w * const.toDeg,
                'Omega': Omega * const.toDeg,
                'M': M * const.toDeg,
                'megno': megno[idx],
                'mean_megno': mean_megno[idx],  
            })

        self.data = Tools.transpose(outdata)
        return outdata


class SecondaryResonance(Resonance):

    def __init__(self, folder_number: int, file_number: int, Omega_value: int, sign: int,light_effect: bool = False):
        super().__init__(folder_number, file_number, Omega_value, light_effect)
        self._sign = 'минус' if sign < 0 else 'плюс'
    
    @property
    def path_data(self):
        return cfg.PATH_OUTDATA + self._LE + f'Omega_{self._Omega}\\Вторичные\\{self._sign}\\{self._folder}\\{str(self._file).rjust(4, "0")}.DAT'
    

    def _get_data_from_file(self) -> dict:
        reader = FileService.SecondaryResonanceFileReader(self.path_data)
        return reader.read()
        
    def get_data(self):
        outdata = self._get_data_from_file()
        self.data = Tools.transpose(outdata)
        return outdata



def main():
    res = SecondaryResonance(1, 12, 120, -1, False)
    
    print(res.get_data())
    

if __name__ == "__main__":
    main()