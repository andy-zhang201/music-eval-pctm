import numpy as np
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import os

import mido
import numpy as np
# import music21

fileInputPath = './data/Samples 3'
dataPaths = ['./data/cymatics','./data/baseline_generated','./data/Baseline 2','./data/Primary Samples 1','./data/Primary Samples 2','./data/Primary Samples 2']
plotOutputPath = "./plots"
matrices = []

for dataPathName in dataPaths:
    midis = os.listdir(dataPathName)

    matrix = np.zeros((12, 12))

    pitch_classes = []
    notes = []
    # Read from each midi file
    for midi_name in midis:
        try:
            midi_file = mido.MidiFile(os.path.join(dataPathName, f'{midi_name}'))

        except OSError as ose:
            continue
            
        notes = []
        for msg in midi_file:
            #When note starts playing, append the note to list
            if msg.type == 'note_on':
                notes.append(msg.note)

            #When note stops playing, also append to list
            elif msg.type == 'note_off':
                notes.append(msg.note)

        #print(notes)
        pitch_classes = [note % 12 for note in notes] #60 = C4, 
        #print(pitch_classes)

        for i in range(len(pitch_classes) - 1):
            matrix[pitch_classes[i], pitch_classes[i+1]] += 1


    #Normalization code after all files itereated 
    for i in range(12):
        row_sum = np.sum(matrix[i])
        if row_sum != 0:
            matrix[i] /= row_sum
        else:
            matrix[i] = np.nan_to_num(matrix[i])

    print(matrix)
    matrices.append(matrix)


transition_matrix_input = np.zeros((12, 12))
transition_matrix_input = matrices[0]

transition_matrix_baselineOld = np.zeros((12, 12))
transition_matrix_baselineOld = matrices[1]

transition_matrix_baselineNew = np.zeros((12, 12))
transition_matrix_baselineNew = matrices[2]

transition_matrix_primary_samples1 = np.zeros((12, 12))
transition_matrix_primary_samples1 = matrices[3]

transition_matrix_primary_samples2 = np.zeros((12, 12))
transition_matrix_primary_samples2 = matrices[4]

transition_matrix_primary_samples3 = np.zeros((12, 12))
transition_matrix_primary_samples3 = matrices[5]


# transition_matrix_primary_samples2 = np.zeros((12, 12))

#Plotting
firstNote = ["C", "C#", "D",
            "D#", "E", "F", "F#",
            "G", "G#", "A",
            "A#", "B"]

secondNote = ["C", "C#", "D",
            "D#", "E", "F", "F#",
            "G", "G#", "A",
            "A#", "B"]


fig, ax = plt.subplots()
# im = ax.imshow(matrix)

# # We want to show all ticks...
# ax.set_xticks(np.arange(len(firstNote)))
# ax.set_yticks(np.arange(len(secondNote)))
# # ... and label them with the respective list entries
# ax.set_xticklabels(firstNote)
# ax.set_yticklabels(secondNote)
# # Rotate the tick labels and set their alignment.
# plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#         rotation_mode="anchor")

# # Loop over data dimensions and create text annotations.
# for i in range(len(secondNote)):
#     for j in range(len(firstNote)):
#         text = ax.text(j, i, round(matrix[i, j],2),
#                     ha="center", va="center", color="w")

                    
# ax.set_title(f'Pitch Class Transition Matrix of Primary Model Generated Samples 2')
# plt.xlabel("Destination Pitches")
# plt.ylabel("Source Pitches")

# fig.tight_layout()

# plt.savefig(f"./plots/pctm_primary_2_generated.png")
# plt.close()


# plt.show()

def get_mse(transition_matrix_A, transition_matrix_B):
      return  np.square(np.subtract(transition_matrix_A, transition_matrix_B)).mean()

print("PCTM MSE of Input vs Baseline Old Data: ", get_mse(transition_matrix_input, transition_matrix_baselineOld))
print("PCTM MSE of Input vs Baseline New Data: ", get_mse(transition_matrix_input, transition_matrix_baselineNew))
print("PCTM MSE of Input vs Primary Samples 1: ", get_mse(transition_matrix_input, transition_matrix_primary_samples1))
print("PCTM MSE of Input vs Primary Samples 2: ", get_mse(transition_matrix_input, transition_matrix_primary_samples2))
print("PCTM MSE of Input vs Primary Samples 3: ", get_mse(transition_matrix_input, transition_matrix_primary_samples3))

# print("PCTM MSE of Input vs Primary Samples 2: ", get_mse(transition_matrix_input, transition_matrix_primary_samples2))
