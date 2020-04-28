clearinfo
directory$ = "../data/wavDataSegmented/"

list = Create Strings as file list: "list", directory$ + "/*.wav"

n = Get number of strings
print name'tab$'group'tab$'duration'tab$'intensity'tab$'f0Mean'tab$'f0Med'tab$'f0SD'tab$'f0Min'tab$'f0Max'tab$'unvoiced'tab$'HNR'tab$'jitter'tab$'shimmer'newline$'

for i to n

  selectObject: list
  filename$ = Get string: i
  print 'filename$'
  head$ = mid$(filename$, 1, rindex(filename$,"_fno_")-1)
  #change this following path
  fileID = Read from file: directory$ + filename$
    # select and process sound object

  select fileID
    int = Get intensity (dB)

    # Make the remaining objects to get voiceReport

    selectObject: fileID
    pitch = To Pitch: 0, 75, 500
    selectObject: fileID
    pulses = To PointProcess (periodic, cc): 75, 500
    dur = Get total duration
  selectObject: fileID, pitch, pulses
  voiceReport$ = Voice report: 0,0, 75, 500, 1.3, 1.6, 0.03, 0.45
    f0Mean=extractNumber (voiceReport$, "Mean pitch: ")
    f0Med=extractNumber (voiceReport$, "Median pitch: ")
    f0SD=extractNumber (voiceReport$, "Standard deviation: ")
    f0Min=extractNumber (voiceReport$, "Minimum pitch: ")
    f0Max=extractNumber (voiceReport$, "Maximum pitch: ")
    unvoiced=extractNumber (voiceReport$, "Fraction of locally unvoiced frames: ")
    hnr=extractNumber(voiceReport$, "Mean harmonics-to-noise ratio: ")
    jitter = extractNumber (voiceReport$, "Jitter (local): ")
    shimmer = extractNumber (voiceReport$, "Shimmer (local): ")

print 'tab$''head$''tab$''dur:3''tab$''int:3''tab$''f0Mean:3''tab$''f0Med:3''tab$''f0SD:3''tab$''f0Min:3''tab$''f0Max:3''tab$''unvoiced:3''tab$''hnr:3''tab$''jitter:3''tab$''shimmer:3''newline$'

# Clean up
removeObject:  pitch, pulses
# remove sound object
removeObject: fileID
endfor
removeObject: list
