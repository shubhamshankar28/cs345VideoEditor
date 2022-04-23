from tracemalloc import start
import moviepy.editor as mpy
videos = []
track = []
vcodec =   "libx264"

videoquality = "24"

# slow, ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
compression = "fast"


class Clips():
    def __init__(self,origVideoClip,currentVideoClip):
        self.origVideoClip = origVideoClip
        self.videoClip = currentVideoClip
        self.audioList = []
        self.textList = []
        self.imageList = []
        self.textEffectList = []
        self.imageEffectList = []

    def setTextList(self,textList):
        self.textList = textList.copy()

    def setAudioList(self,audioList):
        self.audioList = audioList.copy()

    def setImageList(self,imageList):
        self.imageList = imageList.copy()

    def setTextEffectList(self,textEffectList):
        self.textEffectList = textEffectList.copy()

    def setImageEffectList(self,imageEffectList):
        self.imageEffectList = imageEffectList.copy()

    def addText(self,textClip):

        final_clip = mpy.CompositeVideoClip([self.videoClip,textClip])
        #print(final_clip.clips)
        self.videoClip = final_clip
        self.textList.append(textClip)


    def addImage(self,imageClip):
        self.videoClip = mpy.CompositeVideoClip([self.videoClip,imageClip])
        self.imageList.append(imageClip)


    def addAudio(self,audioClip,startPosition=None,endPosition=None):
        clipLength = self.videoClip.duration
        if(startPosition == None):
            startPosition  = 0
        if(endPosition == None):
            endPosition = clipLength
        audioClip = audioClip.set_start(startPosition)
        audioClip = audioClip.set_duration(endPosition - startPosition)
        self.videoClip = self.videoClip.set_audio(audioClip)
        self.audioList.append((audioClip,startPosition,endPosition))

    def addEffectOnText(self,textListIndex,effectName,effectDuration):
        currentTextClip = self.textList[textListIndex]
        self.removeText(textListIndex)
        ## retrieve the currentTextClip and remove it from the video
        if(effectName == "crossfadein"):
            currentTextClip =  currentTextClip.crossfadein(effectDuration)
        if(effectName == "crossfadeout"):
            currentTextClip = currentTextClip.crossfadeout(effectDuration)
        ## modify the current text clip by adding the required effect to the text clip
        final_clip = mpy.CompositeVideoClip([self.videoClip,currentTextClip])
        self.videoClip = final_clip
        ## add the modified textclip to the video
        self.textList.append(currentTextClip)
        currentIndex = len(self.textList)
        self.textEffectList.append((currentIndex-1,effectName,effectDuration))
        ## add the modified textclip to the list of textclips and add the effect to the list of applied effects.
    def addEffectOnImage(self,imageListIndex,effectName,effectDuration):
        currentImageClip = self.imageList[imageListIndex]
        self.removeImage(imageListIndex)
        ## retrieve the currentImageClip and remove it from the video
        if(effectName == "crossfadein"):
            currentImageClip =  currentImageClip.crossfadein(effectDuration)
        if(effectName == "crossfadeout"):
            currentImageClip = currentImageClip.crossfadeout(effectDuration)
        ## modify the current image clip by adding the required effect to the image clip
        final_clip = mpy.CompositeVideoClip([self.videoClip,currentImageClip])
        self.videoClip = final_clip
        ## add the modified image clip to the video
        self.imageList.append(currentImageClip)
        currentIndex = len(self.imageList)
        self.imageEffectList.append((currentIndex-1,effectName,effectDuration))
        ## add the modified imageclip to the list of imageclips and add the effect to the list of applied effects.
    def removeText(self,index):
        del self.textList[index]
        effectIndex = -1

        temporaryClip =  Clips(self.origVideoClip,self.origVideoClip)
        for audios in self.audioList:
            temporaryClip.addAudio(audios[0],startPosition = audios[1],endPosition=audios[2])
        for imageClip in self.imageList:
            temporaryClip.addImage(imageClip)
        for textClip in self.textList:
            temporaryClip.addText(textClip)
        for effects in self.textEffectList:
            if(effects[0] != index):
                temporaryClip.addEffectOnText(effects[0],effects[1],effects[2])
            else:
                effectIndex = index
        for effects in self.imageEffectList:
            temporaryClip.addEffectOnImage(effects[0],effects[1],effects[2])

        if(effectIndex != -1):
            del self.textEffectList[effectIndex]

        self.videoClip = temporaryClip.output().copy()

    def removeImage(self,index):
        del self.imageList[index]
        effectIndex = -1
        temporaryClip =  Clips(self.origVideoClip,self.origVideoClip)
        for audios in self.audioList:
            temporaryClip.addAudio(audios[0],startPosition = audios[1],endPosition=audios[2])
        for imageClip in self.imageList:
            temporaryClip.addImage(imageClip)
        for textClip in self.textList:
            temporaryClip.addText(textClip)
        for effects in self.textEffectList:
            temporaryClip.addEffectOnText(effects[0],effects[1],effects[2])

        for effects in self.imageEffectList:
            if(effects[0] != index):
                temporaryClip.addEffectOnImage(effects[0],effects[1],effects[2])
            else:
                effectIndex = index

        if(effectIndex != -1):
            del self.imageEffectList[effectIndex]

        self.videoClip = temporaryClip.output().copy()

    def removeAudio(self,index):
        del self.audioList[index]
        temporaryClip =  Clips(self.origVideoClip,self.origVideoClip)
        for audios in self.audioList:
            temporaryClip.addAudio(audios[0],startPosition = audios[1],endPosition=audios[2])
        for imageClip in self.imageList:
            temporaryClip.addImage(imageClip)
        for textClip in self.textList:
            temporaryClip.addText(textClip)
        for effects in self.textEffectList:
            temporaryClip.addEffectOnText(effects[0],effects[1],effects[2])
        for effects in self.imageEffectList:
            temporaryClip.addEffectOnImage(effects[0],effects[1],effects[2])

        self.videoClip = temporaryClip.output().copy()

    def removeTextEffect(self,index):
        del self.textEffectList[index]
        ## delete the textEffect from the list of applied text effects
        temporaryClip =  Clips(self.origVideoClip,self.origVideoClip)
        ## retrieve the starting video clip with no media elements and effects added.Create a temporary clip object using this video clip.
        for audios in self.audioList:
            temporaryClip.addAudio(audios[0],startPosition = audios[1],endPosition=audios[2])
        for imageClip in self.imageList:
            temporaryClip.addImage(imageClip)
        for textClip in self.textList:
            temporaryClip.addText(textClip)
        for effect in self.textEffectList:
            temporaryClip.addEffectOnText(effect[0],effect[1],effect[2])
        for effect in self.imageEffectList:
            temporaryClip.addEffectOnImage(effect[0],effect[1],effect[2])
        ## add all the media elements and apply the effects to this temporary clip.
        self.videoClip = temporaryClip.output().copy()

    def removeImageEffect(self,index):
        del self.imageEffectList[index]
        ## delete the imageEffect from the list of applied image effects
        temporaryClip =  Clips(self.origVideoClip,self.origVideoClip)
        ## retrieve the starting video clip with no media elements and effects added.Create a temporary clip object using this video clip.
        for audios in self.audioList:
            temporaryClip.addAudio(audios[0],startPosition = audios[1],endPosition=audios[2])
        for imageClip in self.imageList:
            temporaryClip.addImage(imageClip)
        for textClip in self.textList:
            temporaryClip.addText(textClip)
        for effect in self.textEffectList:
            temporaryClip.addEffectOnText(effect[0],effect[1],effect[2])
        for effect in self.imageEffectList:
            temporaryClip.addEffectOnImage(effect[0],effect[1],effect[2])
        ## add all the media elements and apply the effects to this temporary clip
        self.videoClip = temporaryClip.output().copy()



    def constructVideoClip(self):
        temporaryClip =  Clips(self.origVideoClip,self.origVideoClip)
        ## retrieve the starting video clip with no media elements and effects added.Create a temporary clip object using this video clip.
        for audios in self.audioList:
            temporaryClip.addAudio(audios[0],startPosition = audios[1],endPosition=audios[2])
        for imageClip in self.imageList:
            temporaryClip.addImage(imageClip)
        for textClip in self.textList:
            temporaryClip.addText(textClip)
        for effect in self.textEffectList:
            temporaryClip.addEffectOnText(effect[0],effect[1],effect[2])
        for effect in self.imageEffectList:
            temporaryClip.addEffectOnImage(effect[0],effect[1],effect[2])
        self.videoClip = temporaryClip.output().copy()

    def output(self):
        return self.videoClip

def uploadVideo(inputVideos):
    if (len(inputVideos) == 0):
        print("Error: list cannot be empty")
    else:
        for video in inputVideos:
            videos.append(mpy.VideoFileClip(video))

def addVideo(videoIndex, position):
    if(position > len(track)):
        print("Error: invalid position")
    else:
        clip = Clips(videos[videoIndex],videos[videoIndex])
        track.insert(position, clip)

def addSound(audioFilePath,trackIndex,startPosition=None,endPosition=None):
    audioClip = mpy.AudioFileClip(audioFilePath)
    track[trackIndex].addAudio(audioClip,startPosition,endPosition)

def addTextualContent(content,startTime,displayDuration,x,y,trackIndex,font=None,color=None,bg_color=None,size = None):
#    print("entered add text")
    textClip = mpy.TextClip(content)
    textClip = textClip.set_start(startTime)
    textClip = textClip.set_duration(displayDuration)
    textClip = textClip.set_position((x,y))
    track[trackIndex].addText(textClip)
    print(textClip.start)
#    print("addition of text over")
def addImage(image,startTime,displayDuration,x,y,trackIndex):
#    print("entered add image")
    imageClip = mpy.ImageClip(image)
    imageClip = imageClip.set_start(startTime)
    imageClip = imageClip.set_duration(displayDuration)
    imageClip = imageClip.set_position((x,y))
    track[trackIndex].addImage(imageClip)
def addTextEffect(textListIndex,effectName,effectDuration,trackIndex):
    track[trackIndex].addEffectOnText(textListIndex,effectName,effectDuration)
def addImageEffect(imageListIndex,effectName,effectDuration,trackIndex):
    track[trackIndex].addEffectOnImage(imageListIndex,effectName,effectDuration)
#    print("image addition over")

def removeSound(trackIndex,audioListIndex):
    track[trackIndex].removeAudio(audioListIndex)

def removeText(trackIndex,textListIndex):
    track[trackIndex].removeText(textListIndex)

def removeImage(trackIndex,imageListIndex):
    track[trackIndex].removeImage(imageListIndex)

def deleteClip(trackIndex):
    del track[trackIndex]
    ## Delete the clip located at trackIndex

def swapClips(sourceTrackIndex,targetTrackIndex):

    tempClip = track[sourceTrackIndex]
    track[sourceTrackIndex] = track[targetTrackIndex]
    track[targetTrackIndex] = tempClip
    for texts in track[sourceTrackIndex].textList:
        print("source text start: %d duration : %d" % (texts.start,texts.duration))
    for audios in track[sourceTrackIndex].audioList:
        print("source audio start: %d duration: %d" % (audios[0].start,audios[0].duration))
    for images in track[sourceTrackIndex].imageList:
        print("source images start: %d duration: %d" % (images.start,images.duration))

    for texts in track[targetTrackIndex].textList:
        print("target text start: %d duration : %d" % (texts.start,texts.duration))
    for audios in track[targetTrackIndex].audioList:
        print("target audio start: %d duration: %d" % (audios[0].start,audios[0].duration))
    for images in track[targetTrackIndex].imageList:
        print("target images start: %d duration: %d" % (images.start,images.duration))

    # Swap the clip at sourceTrackIndex with the clip at targetTrackIndex

def modifyAudioClip(origAudio,startTime,duration):
    modifiedAudio = origAudio.copy()
    modifiedAudio = modifiedAudio.set_start(startTime)
    modifiedAudio = modifiedAudio.set_duration(duration)
    ##  create a new audio clip and set it's attributes appropriately
    return modifiedAudio


def handleAudio(clip,subClip1,subClip2,splitTime):
    currentAudioList = clip.audioList
    subClip1AudioList = []
    subClip2AudioList = []
    ## retrieve the current audio list and initialize the audioLists of the subclips,
    audioClip1 = None
    audioClip2 = None
    ## initialize two temporary clips which will be used later
    for audio in currentAudioList:
        startTime = audio[1]
        endTime = audio[2]
        ## retrieve start and end time of current audio clip
        if(endTime <= splitTime):
            subClip1AudioList.append(audio)
            ## Complete audio clip is inserted in subClip1's audio list
        elif(startTime >= splitTime):
            audioClip2 = modifyAudioClip(audio[0],startTime-splitTime,endTime-startTime)
            subClip2AudioList.append((audioClip2,startTime - splitTime,endTime - splitTime))
            ## startTime of  audio clip is modified and then it is inserted in subClip2's audio list
        else:
            ## this is is the case where the current audioClip needs to be split
            audioClip1 = modifyAudioClip(audio[0],startTime,splitTime-startTime)
            audioClip2 = modifyAudioClip(audio[0],0,endTime-splitTime)
            subClip1AudioList.append((audioClip1,startTime,splitTime))
            subClip2AudioList.append((audioClip2,splitTime,endTime))
            ## the startTime and duration of the two parts into which the audioClip is split is initialized and then the parts are added into the appropriate list.

    subClip1.setAudioList(subClip1AudioList)
    subClip2.setAudioList(subClip2AudioList)
    # the audioLists of both the subClips are set appropriately


def modifyTextClip(origTextClip,startTime,duration):
    modifiedTextClip = origTextClip.copy()
    modifiedTextClip = modifiedTextClip.set_start(startTime)
    modifiedTextClip = modifiedTextClip.set_duration(duration)
    ##  create a new text clip and set it's attributes appropriately
    return modifiedTextClip

def handleTextClipSplit(startTime,endTime,effectListIndex,splitTime,index,currentTextClip,effectListToTextListMapping,currentTextEffectList,subClip1TextList,subClip2TextList,subClip1TextEffectList,subClip2TextEffectList):
    textClip1 = modifyTextClip(currentTextClip,startTime,splitTime-startTime)
    textClip2 = modifyTextClip(currentTextClip,0,endTime-splitTime)
    subClip1TextList.append(textClip1)
    subClip2TextList.append(textClip2)
    print("for first text clip: duration: %d start : %d" % (textClip1.duration,textClip1.start))
    print("for second text clip: duration: %d start : %d" % (textClip2.duration,textClip2.start))

    ## The text clip is set into two parts , these parts are added to the appropriate textList
    if(effectListIndex!=-1):
        if(currentTextEffectList[effectListIndex] == "crossfadein"):
            subClip1TextEffectList.append((len(subClip1TextList)-1,currentTextEffectList[effectListIndex][1],currentTextEffectList[effectListIndex][2]))
        else:
            subClip2TextEffectList.append((len(subClip2TextList)-1,currentTextEffectList[effectListIndex][1],currentTextEffectList[effectListIndex][2]))


def modifySubClipTextList(splitTime,index,currentTextClip,effectListToTextListMapping,currentTextEffectList,subClip1TextList,subClip2TextList,subClip1TextEffectList,subClip2TextEffectList):
    #print("index is %d" % (index))
    textClip1 = None
    textClip2 = None
    ## temporary textCips that will be used later.
    startTime = currentTextClip.start
    endTime = currentTextClip.start + currentTextClip.duration
    if(index in effectListToTextListMapping):
        effectListIndex = effectListToTextListMapping[index]
    else:
        effectListIndex = -1
    ## find the startTime , endTime and corresponding effectListIndex,
    if(endTime <= splitTime):
        subClip1TextList.append(currentTextClip)
        print("for current text clip: duration: %d start : %d" % (currentTextClip.duration,currentTextClip.start))
        if(effectListIndex != -1):
            subClip1TextEffectList.append((len(subClip1TextList)-1,currentTextEffectList[effectListIndex][1],currentTextEffectList[effectListIndex][2]))
        ## Complete text clip is inserted in subClip1's text list
    elif(startTime >= splitTime):

        textClip2 = modifyTextClip(currentTextClip,startTime-splitTime,endTime-startTime)
        print("for rear end text clip: duration: %d start : %d" % (textClip2.duration,textClip2.start))
        subClip2TextList.append(textClip2)
        if(effectListIndex != -1):
            subClip2TextEffectList.append((len(subClip2TextList)-1,currentTextEffectList[effectListIndex][1],currentTextEffectList[effectListIndex][2]))
        ## Complete text clip is inserted in subClip2's text list
    else:
        handleTextClipSplit(startTime,endTime,effectListIndex,splitTime,index,currentTextClip,effectListToTextListMapping,currentTextEffectList,subClip1TextList,subClip2TextList,subClip1TextEffectList,subClip2TextEffectList)


def handleText(clip,subClip1,subClip2,splitTime):
    #print("handling text")
    currentTextList = clip.textList
    currentTextEffectList = clip.textEffectList
    subClip1TextList = []
    subClip2TextList = []
    ## retrieve the currentTextList and currentTextEffectList and initialize subClip1's and subClip2's textList appropriately
    subClip1TextEffectList = []
    subClip2TextEffectList = []
    effectListToTextListMapping = dict()
    for index,effects in enumerate(currentTextEffectList):
        effectListToTextListMapping[effects[0]] = index
    ## store the index of the effect that corresponds to a particular textClip

    for index,currentTextClip in enumerate(currentTextList):
        modifySubClipTextList(splitTime,index,currentTextClip,effectListToTextListMapping,currentTextEffectList,subClip1TextList,subClip2TextList,subClip1TextEffectList,subClip2TextEffectList)

    subClip1.setTextList(subClip1TextList)
    subClip2.setTextList(subClip2TextList)
    subClip1.setTextEffectList(subClip1TextEffectList)
    subClip2.setTextEffectList(subClip2TextEffectList)
    ## The text list and text effect lists of subClip1 and subClip2 are initialized appropriately.




def modifyImageClip(origImageClip,startTime,duration):
    modifiedImageClip = origImageClip.copy()
    modifiedImageClip = modifiedImageClip.set_start(startTime)
    modifiedImageClip = modifiedImageClip.set_duration(duration)
    ##  create a new image clip and set it's attributes appropriately
    return modifiedImageClip


def handleImageClipSplit(startTime,endTime,effectListIndex,splitTime,index,currentImageClip,effectListToImageListMapping,currentImageEffectList,subClip1ImageList,subClip2ImageList,subClip1ImageEffectList,subClip2ImageEffectList):
    imageClip1 = None
    imageClip2 = None
    ## temporary imageCips that will be used later.
    imageClip1 = modifyImageClip(currentImageClip,startTime,splitTime-startTime)
    imageClip2 = modifyImageClip(currentImageClip,0,endTime-splitTime)
    subClip1ImageList.append(imageClip1)
    subClip2ImageList.append(imageClip2)
    ## The image clip is set into two parts , these parts are added to the appropriate imageList
    if(effectListIndex!=-1):
        if(currentImageEffectList[effectListIndex] == "crossfadein"):
            subClip1ImageEffectList.append((len(subClip1ImageList)-1,currentImageEffectList[effectListIndex][1],currentImageEffectList[effectListIndex][2]))
        else:
            subClip2ImageEffectList.append((len(subClip2ImageList)-1,currentImageEffectList[effectListIndex][1],currentImageEffectList[effectListIndex][2]))


def modifySubClipImageList(splitTime,index,currentImageClip,effectListToImageListMapping,currentImageEffectList,subClip1ImageList,subClip2ImageList,subClip1ImageEffectList,subClip2ImageEffectList):
    imageClip1 = None
    imageClip2 = None
    ## temporary imageCips that will be used later.
    startTime = currentImageClip.start
    endTime = currentImageClip.start + currentImageClip.duration
    if(index in effectListToImageListMapping):
        effectListIndex = effectListToImageListMapping[index]
    else:
        effectListIndex = -1
    ## find the startTime , endTime and corresponding effectListIndex,
    if(endTime <= splitTime):
        subClip1ImageList.append(currentImageClip)
        if(effectListIndex != -1):
            subClip1ImageEffectList.append((len(subClip1ImageList)-1,currentImageEffectList[effectListIndex][1],currentImageEffectList[effectListIndex][2]))
        ## Complete image clip is inserted in subClip1's image list
    elif(startTime >= splitTime):
        imageClip2 = modifyImageClip(currentImageClip,startTime-splitTime,endTime-startTime)
        subClip2ImageList.append(imageClip2)
        if(effectListIndex != -1):
            subClip2ImageEffectList.append((len(subClip2ImageList)-1,currentImageEffectList[effectListIndex][1],currentImageEffectList[effectListIndex][2]))
        ## Complete image clip is inserted in subClip2's image list
    else:
        handleImageClipSplit(startTime,endTime,effectListIndex,splitTime,index,currentImageClip,effectListToImageListMapping,currentImageEffectList,subClip1ImageList,subClip2ImageList,subClip1ImageEffectList,subClip2ImageEffectList)



def handleImage(clip,subClip1,subClip2,splitTime):
    currentImageList = clip.imageList
    currentImageEffectList = clip.imageEffectList
    subClip1ImageList = []
    subClip2ImageList = []
    ## retrieve the currentImageList and currentImageEffectList and initialize subClip1's and subClip2's imageList appropriately
    subClip1ImageEffectList = []
    subClip2ImageEffectList = []
    ## initialize two temporary imageClip objects which will be used later.
    effectListToImageListMapping = dict()
    for index,effects in enumerate(currentImageEffectList):
        effectListToImageListMapping[effects[0]] = index
    ## store the index of the effect that corresponds to a particular imageClip
    for index,currentImageClip in enumerate(currentImageList):
        modifySubClipImageList(splitTime,index,currentImageClip,effectListToImageListMapping,currentImageEffectList,subClip1ImageList,subClip2ImageList,subClip1ImageEffectList,subClip2ImageEffectList)
    subClip1.setImageList(subClip1ImageList)
    subClip2.setImageList(subClip2ImageList)
    subClip1.setImageEffectList(subClip1ImageEffectList)
    subClip2.setImageEffectList(subClip2ImageEffectList)
    ## The image list and image effect lists of subClip1 and subClip2 are initialized appropriately.

def sliceClip(trackIndex,splitTime):
    clip = track[trackIndex]
    origVideoClip = clip.output()
    umVideoClip = clip.origVideoClip
    startTime = origVideoClip.start
    duration = origVideoClip.duration
    print(startTime)
    print(duration)
    ## retrieve original Clip and store the length of the original video clip
    del track[trackIndex]
    subClip1 = Clips(umVideoClip.subclip(startTime,splitTime),origVideoClip.subclip(startTime,splitTime))
    subClip2 = Clips(umVideoClip.subclip(splitTime,duration),origVideoClip.subclip(splitTime,duration))
    ## delete original clip and create the necessary subclips
    handleAudio(clip,subClip1,subClip2,splitTime)
    ## Splitting audio Clips
    handleText(clip,subClip1,subClip2,splitTime)
    ## Splitting textClips and textEffects
    handleImage(clip,subClip1,subClip2,splitTime)
    ## Splitting imageClips and imageEffects
    subClip1.constructVideoClip()
    subClip2.constructVideoClip()
    track.insert(trackIndex,subClip1)
    track.insert(trackIndex+1,subClip2)
    ## place the subclips at the appropriate position in the track.


def output(trackIndex,outputFileName):
    final_clip = track[trackIndex].output()
    final_clip.write_videofile(outputFileName, threads=4, fps=24,codec=vcodec,preset=compression,ffmpeg_params=["-crf",videoquality])

def fullVideo(outputFileName):
    clips = []
    for clip in track:
        clips.append(clip.output())
    finalClip = mpy.concatenate_videoclips(clips)
    finalClip.write_videofile(outputFileName, threads=4, fps=24,codec=vcodec,preset=compression,ffmpeg_params=["-crf",videoquality])

uploadVideo(["inputVid.mkv"])
addVideo(0, 0)
print(track[0].output().duration)
# print(mpy.TextClip.list('color'))
# print(mpy.TextClip.list('font'))
addSound("inputAudio.wav", 0, 0,20)
print(track[0].output().duration)
addTextualContent("Divyam teaches OS",0,40,100,200,0)
print(track[0].output().duration)
print("adding effect text Effect!!")
#addTextEffect(0,"crossfadein",5,0)
print("text effect added")

addImage("monkey.jpg",0,20,200,200,0)
print(track[0].output().duration)
addImage("monkey.jpg",40,10,700,700,0)
print(track[0].output().duration)
sliceClip(0,20)
sliceClip(1,20)
swapClips(0,2)
# removeImage(2,0)

#addImageEffect(1,"crossfadeout",5,0)

fullVideo("outputSAnewApp.mp4")
# removeSound(0,0)
# print("removed sound!!")
# removeText(0,0)
# print("removed text!!")
# removeImage(0,1)
# print("removed Image!!")



# addImage("dfd" , 25,30,2,2,0)


#output(0,"outputSA.mp4")
#removeSound(0,0)
#output(0,"outputSR.mp4")
