import os, pydub
import matplotlib.pyplot as plt
from inspect import getsourcefile

# import tensorflow_datasets as tfds
cwd = os.path.abspath(getsourcefile(lambda:0) + '/..')

def write_on_new_file(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + "-" + str(counter) + extension
        counter += 1

    return path

parent = ['test', 'train']
sourcePath = [os.path.join(cwd, 'source', i) for i in parent]

filePaths = {}

for n,i in enumerate(sourcePath):
    par = parent[n]
    temp = os.listdir(i)
    paths = {}
    for j in temp: 
        paths[j] = [os.path.join(cwd, 'source', i, j, x) for x in os.listdir(os.path.join(cwd, 'source', i, j))]
    filePaths[par] = paths

for pa in filePaths.keys():

    exportPath = os.path.join(cwd,'dataset')
    if not os.path.isdir(f'{exportPath}'):
        os.mkdir(f'{exportPath}')

    exportPath = os.path.join(cwd,'dataset', pa)
    if not os.path.isdir(f'{exportPath}'):
        os.mkdir(f'{exportPath}')
    for cl in filePaths[pa].keys():

        exportPath = os.path.join(cwd,'dataset',pa, cl)
        if not os.path.isdir(f'{exportPath}'):
            os.mkdir(f'{exportPath}')

        audioPaths = filePaths[pa][cl]

        fhnum = 0
        for p in audioPaths:
            audioInput = pydub.AudioSegment.from_file(p, "wav") 
            # audioInput = audioInput.set_frame_rate(audioInput.frame_rate)
            channel_audio = audioInput.split_to_mono()

            samples = channel_audio[0].get_array_of_samples()

            maxval = max(samples)
            samples = [i/maxval for i in samples]
            samples_iterator = iter(samples)
            thresh = .5
            skips = 1000
            timeStamps = []

            temp = []
            t = 0
            while True:
                t += 1
                try:
                    val = next(samples_iterator)
                    if val>=thresh:
                        temp.append(1)
                        timeStamps.append(t)
                        ttemp = []
                        for _ in range(skips):
                            t += 1
                            next(samples_iterator)
                            ttemp.append(1)
                        temp += ttemp
                    else:
                        temp.append(0)
                except StopIteration:
                    break

            # plt.plot([i for i in range(len(samples))], samples, label='a')
            # plt.plot([i for i in range(len(samples))], temp, label='b')
            # plt.show()

            for frame in timeStamps:
                fhnum += 1
                start = int(1000*frame/audioInput.frame_rate)-100
                stop = start + 500

                au = audioInput[start:stop]
                
                with open(f'{cwd}/dataset/{pa}/{cl}/tr_{cl}-{fhnum}.wav','wb') as fh:
                    au.export(fh, format='wav')
                