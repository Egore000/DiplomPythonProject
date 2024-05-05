import sys
from itertools import islice

sys.path.append('C:\\Users\\egorp\\Desktop\\диплом\\файлы\\Python_test\\')

from config import const


def batches(lst: list, size: int):
    if size <= 0:
       return
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


class FileReader:
    def __init__(self, path: str):
        self._path = path

    def read(self):
        raise NotImplementedError()
    

class FileWriter:
    def __init__(self, path: str):
        self._path = path

    def write(self):
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
            dat = batches(list(data), 3)
            
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
    pass


class SecondaryResonanceFileReader(FileReader):
    pass


def main():
    eph = EPHFileReader('C:\\Users\\egorp\\Desktop\\диплом\\файлы\\Исходные данные\\Без светового давления\\Omega_0\\1\\EPH_0001.DAT')
    data = eph.read()
    print(data)

if __name__ == "__main__":
    main()