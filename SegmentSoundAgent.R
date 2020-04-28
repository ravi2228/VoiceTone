# install.packages('tuneR', repos = "http://cran.us.r-project.org")

list.of.packages <- c("tuneR")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages, repos = "http://cran.us.r-project.org")

library(tuneR)
xml = read.csv('output/xmlParsed.csv')
breaksound=function (sound){

  nme = substr(sound,23 , nchar(sound)-8)
  # print(nme)
  if (xml[which(xml$name == nme),]$direction == 'Outbound'){
          # print('right')
  test <- tryCatch({
  channel(readWave(sound),which = "right")
  },
  error=function(cond) {
            message("Here's the original error message:")
            # Choose a return value in case of error
            return(channel(readWave(sound),which = "left"))
            },
   warning=function(cond) {
            message("Here's the original warning message:")
            # Choose a return value in case of warning
            return(channel(readWave(sound),which = "left"))
        },
  finally={
  # NOTE:
  # Here goes everything that should be executed at the end,
  # regardless of success or error.
  # If you want more than one expression to be executed, then you 
  # need to wrap them in curly brackets ({...}); otherwise you could
  # just have written 'finally=<expression>' 
      message("Process Successful")
        }
        )
  
  }
  else {
          # print('left')
  test = channel(readWave(sound),which = "left")
  }

  #test=channel(readWave(sound),which = "left")
  i=1  #define starting frame
  d=40000  #define length of each snippet. With 8000 Hz sampling rate, 40000 frames equal 5 seconds.
  leg=trunc(length(test)/d) ###define the number of sample for each call
  
  # print(sound)
 
  if (length(test) > 40000) {
  for (i in 1:leg) {
    writeWave(test[((i-1)*d+1):(i*d)],filename = paste0('data/wavDataSegmented/',substr(sound,23 , nchar(sound)-8),'_fno_' ,i, ".wav"))
  } 
  }
  ### file.remove(sound) ###delete file to save space in EC2
}
filenames <- list.files(path = "data/wavDataProcessed", pattern="*.wav", full.names=TRUE) ###get all the .wav files in your EC2 folder
# print(filenames)
invisible(lapply(filenames,breaksound)) ###apply the function to all .wav files and suppress output messages
