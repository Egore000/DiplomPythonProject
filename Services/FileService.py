import csv
import os
import sys

sys.path.append('C:\\Users\\egorp\\Desktop\\диплом\\файлы\\Python_test\\')

from config import const
from Services import Tools


class FileReader:
    def __init__(self, path: str):
        self._path = path

    def read(self):
        raise NotImplementedError()
    

class EPHFileReader(FileReader):

    @staticmethod
    def __read_time(line: list) -> float:
        return float(line[1]) / const.SecInYear

    @staticmethod
    def __read_date(line: list) -> tuple[int]:
        return (int(line[3]), int(line[4]), int(line[5]))

    @staticmethod
    def __read_coords(line: list) -> tuple[float]:
        return tuple(map(float, line[1:4]))
    
    @staticmethod
    def __read_velocities(line: list) -> tuple[float]:
        return tuple(map(float, line[:3]))
    
    @staticmethod
    def __read_megno(line: list) -> float:
        return float(line[-1])

    def read(self) -> list[dict]:
        outdata = []

        with open(self._path, 'r') as data:
            dat = Tools.batches(list(data), 3)
            
            for batch in dat:
                data_dict = {}
                batch = list(map(str.split, batch))

                data_dict['time'] = self.__read_time(batch[0])
                data_dict['date'] = self.__read_date(batch[0])
                
                data_dict['coords'] = self.__read_coords(batch[1])
                data_dict['megno'] = self.__read_megno(batch[1])
                
                data_dict['mean_megno'] = self.__read_megno(batch[2])
                data_dict['velocities'] = self.__read_velocities(batch[2])

                outdata.append(data_dict)
        
        return outdata
    

class OrbitalResonanceFileReader(FileReader):

    @staticmethod
    def __read_time(line: list) -> float:
        return line[0]

    def read(self):
        outdata = []
        with open(self._path, 'r') as data:
            for num, line in enumerate(data):
                if num == 0:
                    continue
                line = list(map(float, line.strip('()').split()))

                outdata.append({
                    'time': self.__read_time(line),
                    'F1': line[1],
                    'F2': line[2],
                    'F3': line[3],
                    'F4': line[4],
                    'F5': line[5],
                    'dF1': line[6],
                    'dF2': line[7],
                    'dF3': line[8],
                    'dF4': line[9],
                    'dF5': line[10],
                })
        return outdata


class SecondaryResonanceFileReader(OrbitalResonanceFileReader):
    pass


class FileWriter:
    def __init__(self, path: str):
        self._path = path

        self.create_folder()

    def create_folder(self):
        if not os.path.exists(self._path):
            os.makedirs(self._path)

    def write(self, filename: str, data: dict):
        path = self._path + f'\{filename}'
        with open(path, 'w', newline='') as outfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data)


class ElementsWriter(FileWriter):
    pass
        

class OrbitalWriter(FileWriter):
    pass


class SecondaryWriter(FileWriter):
    pass


def main():
    # eph = EPHFileReader('C:\\Users\\egorp\\Desktop\\диплом\\файлы\\Исходные данные\\Без светового давления\\Omega_0\\1\\EPH_0001.DAT')
    # data = eph.read()
    # print(data)
    o = OrbitalResonanceFileReader(r'C:\Users\egorp\Desktop\диплом\файлы\Выходные данные\Без светового давления\Omega_0\Орбитальные\2\2162.dat')
    data = o.read()

    w = OrbitalWriter('..')
    w.write('test.csv', data)

if __name__ == "__main__":
    main()