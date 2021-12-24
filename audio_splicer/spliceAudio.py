import os, pydub
import matplotlib.pyplot as plt
from inspect import getsourcefile

inputFilenames = ['clap', 'snap', 'tap', 'clap_noisered_compr', 'tap_noisered_compr', 'snap_noisered_compr']

for inputFilename in inputFilenames:

    cwd = os.path.abspath(getsourcefile(lambda:0) + '/..')
    exportPath = os.path.join(cwd,'export')

    if not os.path.isdir(f'{exportPath}/{inputFilename}'):
        os.mkdir(f'{exportPath}/{inputFilename}')


    audioInput = pydub.AudioSegment.from_file(f"{cwd}/{inputFilename}.wav" , "wav") 
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

    for n, frame in enumerate(timeStamps):
        start = int(1000*frame/audioInput.frame_rate)-100
        stop = start + 500

        au = audioInput[start:stop]
        with open(f'{cwd}/export/{inputFilename}/tr_{inputFilename}_{n}.wav','wb') as fh:
            au.export(fh, format='wav')
        