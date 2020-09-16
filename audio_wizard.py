import sys
from scipy.io import wavfile
import numpy as np

from typing import List, Tuple


class AudioWizard:
    def __init__(self):
        pass

    def load_file(self,
                  filename: str) -> Tuple[int, np.ndarray]:
        sample_rate, samples = wavfile.read(filename)
        return sample_rate, samples

    def save_file(self,
                  filename: str,
                  sample_rate: int,
                  samples: np.ndarray) -> None:
        wavfile.write(filename, sample_rate, samples)

    def merge(self,
              input_files: List[str],
              output_file: str) -> None:
        '''
        В заданном порядке соединить файлы в один и сохранить результат.
        '''
        sample_rate, merged_samples = self.load_file(input_files[0])
        for f in input_files[1:]:
            _, samples = self.load_file(f)
            merged_samples = np.concatenate((merged_samples, samples))
        self.save_file(output_file, sample_rate, merged_samples)

    def crop(self,
             input_file: str,
             intervals: List[Tuple[int, int]]) -> None:
        '''
        Разбить файл на несколько по заданным границам (в миллисекундах)
        и сохранить результат.
        '''
        sample_rate, samples = self.load_file(input_file)
        for start_ms, stop_ms in intervals:
            start, stop = list(map(lambda x: x * sample_rate // 1000,
                                   [start_ms, stop_ms]))

            cropped_samples = samples[start:stop]
            self.save_file(input_file[:-4] + f'_{start_ms}_{stop_ms}.wav',
                           sample_rate, cropped_samples)

    def invert(self,
               input_file: str,
               output_file: str = None) -> None:
        '''
        Инвертировать файл и сохранить результат.
        '''
        if output_file is None:
            output_file = f'{input_file[:-4]}_inv.wav'

        sample_rate, samples = self.load_file(input_file)
        inv_samples = np.flip(samples)
        self.save_file(output_file, sample_rate, inv_samples)

    def exec(self, args: List[str]) -> None:
        '''
        Спарсить аргументы командной строки в команду.
        '''
        command = args[0]
        if command == '-m':
            # merge
            input_files, output_file = args[1:-1], args[-1]
            self.merge(input_files, output_file)
        elif command == '-c':
            # crop
            input_file = args[1]
            starts, stops = map(int, args[2::2]), map(int, args[3::2])
            intervals = list(zip(starts, stops))
            self.crop(input_file, intervals)
        elif command == '-i':
            # invert
            input_file, output_file = args[1:]
            self.invert(input_file, output_file)


if __name__ == '__main__':
    aw = AudioWizard()
    aw.exec(sys.argv[1:])

    # Прямой доступ к методам:
    # aw.merge(filenames, 'merged.wav')
    # aw.crop(filename, [(100, 800), (600, 2800)])
    # aw.invert(filename)
