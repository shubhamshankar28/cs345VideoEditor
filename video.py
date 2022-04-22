from tracemalloc import start
import moviepy.editor as mpy
videos = []
track = []
vcodec =   "libx264"

videoquality = "24"

# slow, ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
compression = "slow"


class Clips():
    def __init__(self,videoClip):
        self.origVideoClip = videoClip
        self.videoClip = videoClip
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

        if(startPosition==0):
            if(endPosition == clipLength):
                self.videoClip = self.videoClip.set_audio(audioClip)
            else:
                firstClip = self.videoClip.subclip(startPosition,endPosition).set_audio(audioClip)
                secondClip = self.videoClip.subclip(endPosition,clipLength)
                self.videoClip = mpy.concatenate_videoclips([firstClip,secondClip])
        else:
            if(endPosition == clipLength):
                firstClip = self.videoClip.subclip(startPosition,endPosition)
                secondClip = self.videoClip.subclip(endPosition,clipLength).set_audio(audioClip)
                self.videoClip = mpy.concatenate_videoclips([firstClip,secondClip])
                ##self.videoClip = self.videoClip.set_audio(audioClip)
            else:
                firstClip = self.videoClip.subclip(0,startPosition)
                secondClip = self.videoClip.subclip(startPosition,endPosition).set_audio(audioClip)
                thirdClip = self.videoClip.subclip(endPosition,clipLength)
                self.videoClip = mpy.concatenate_videoclips([firstClip,secondClip,thirdClip])

        self.audioList.append((audioClip,startPosition,endPosition))

    def addEffectOnText(self,textListIndex,effectName,effectDuration):
        currentTextClip = self.textList[textListIndex]
        self.removeText(textListIndex)
        if(effectName == "crossfadein"):
            currentTextClip =  currentTextClip.crossfadein(effectDuration)
        if(effectName == "crossfadeout"):
            currentTextClip = currentTextClip.crossfadeout(effectDuration)

        final_clip = mpy.CompositeVideoClip([self.videoClip,currentTextClip])
        self.videoClip = final_clip
        self.textList.append(currentTextClip)
        currentIndex = len(self.textList)
        self.textEffectList.append((currentIndex-1,effectName,effectDuration))

    def addEffectOnImage(self,imageListIndex,effectName,effectDuration):
        currentImageClip = self.imageList[imageListIndex]
        self.removeImage(imageListIndex)
        if(effectName == "crossfadein"):
            currentImageClip =  currentImageClip.crossfadein(effectDuration)
        if(effectName == "crossfadeout"):
            currentImageClip = currentImageClip.crossfadeout(effectDuration)

        final_clip = mpy.CompositeVideoClip([self.videoClip,currentImageClip])
        self.videoClip = final_clip
        self.imageList.append(currentImageClip)
        currentIndex = len(self.imageList)
        self.imageEffectList.append((currentIndex-1,effectName,effectDuration))

    def removeText(self,index):
        del self.textList[index]
        effectIndex = -1

        temporaryClip =  Clips(self.origVideoClip)
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
        temporaryClip =  Clips(self.origVideoClip)
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
        temporaryClip =  Clips(self.origVideoClip)
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
        temporaryClip =  Clips(self.origVideoClip)
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

    def removeImageEffect(self,index):
        del self.imageEffectList[index]
        temporaryClip =  Clips(self.origVideoClip)
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
        clip = Clips(videos[videoIndex])
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

def swapClips(sourceTrackIndex,targetTrackIndex):
    tempClip = track[sourceTrackIndex]
    track[sourceTrackIndex] = track[targetTrackIndex]
    track[targetTrackIndex] = tempClip


def handleAudio(clip,subClip1,subClip2,splitTime):
    currentAudioList = clip.audioList
    subClip1AudioList = []
    subClip2AudioList = []
    audioClip1 = None
    audioClip2 = None
    for audio in currentAudioList:
        startTime = audio[1]
        endTime = audio[2]
        if(endTime <= splitTime):
            subClip1AudioList.append(audio)
        elif(startTime >= splitTime):
            audioClip2 = audio[0].copy()
            audioClip2 = audioClip2.set_start(startTime-splitTime)
            subClip2AudioList.append((audioClip2,startTime - splitTime,endTime - splitTime))

        else:
            audioClip1 = audio[0].copy()
            audioClip1 = audioClip1.set_start(startTime)
            audioClip1 = audioClip1.set_duration(splitTime-startTime)
            audioClip2 = audio[0].copy()
            audioClip2 = audioClip2.set_start(splitTime)
            audioClip2 = audioClip2.set_duration(endTime-splitTime)
            subClip1AudioList.append((audioClip1,startTime,splitTime))
            subClip2AudioList.append((audioClip2,splitTime,endTime))

    subClip1.setAudioList(subClip1AudioList)
    subClip2.setAudioList(subClip2AudioList)


def handleText(clip,subClip1,subClip2,splitTime):
    currentTextList = clip.textList
    currentTextEffectList = clip.textEffectList
    subClip1TextList = []
    subClip2TextList = []
    textClip1 = None
    textClip2 = None
    subClip1TextEffectList = []
    subClip2TextEffectList = []
    effectIndex = -1
    effectToListMapping = dict()
    for index,effects in enumerate(currentTextEffectList):
        effectToListMapping[effects[0]] = index


    for index,text in enumerate(currentTextList):
        startTime = text.start
        endTime = text.start + text.duration
        if(index in effectToListMapping):
            effectIndex = effectToListMapping[index]
        else:
            effectIndex = -1
        if(endTime <= splitTime):
            subClip1TextList.append(text)
            if(effectIndex != -1):
                subClip1TextEffectList.append((len(subClip1TextList)-1,currentTextEffectList[effectIndex][1],currentTextEffectList[effectIndex][2]))

        elif(startTime >= splitTime):
            textClip2 = text.copy()
            textClip2  = textClip2.set_start(startTime - splitTime)
            subClip2TextList.append(text)
            if(effectIndex != -1):
                subClip2TextEffectList.append((len(subClip2TextList)-1,currentTextEffectList[effectIndex][1],currentTextEffectList[effectIndex][2]))
        else:
            textClip1 = text.copy()
            textClip1 = textClip1.set_start(startTime)
            textClip1 = textClip1.set_duration(splitTime-startTime)
            textClip2 = text.copy()
            textClip2 = textClip2.set_start(splitTime)
            textClip2 = textClip2.set_duration(endTime-splitTime)
            subClip1TextList.append(textClip1)
            subClip2TextList.append(textClip2)
            if(effectIndex!=-1):
                if(currentTextEffectList[effectIndex] == "crossfadein"):
                    subClip1TextEffectList.append((len(subClip1TextList)-1,currentTextEffectList[effectIndex][1],currentTextEffectList[effectIndex][2]))
                else:
                    subClip2TextEffectList.append((len(subClip2TextList)-1,currentTextEffectList[effectIndex][1],currentTextEffectList[effectIndex][2]))

    subClip1.setTextList(subClip1TextList)
    subClip2.setTextList(subClip2TextList)
    subClip1.setTextEffectList(subClip1TextEffectList)
    subClip2.setTextEffectList(subClip2TextEffectList)


def handleImage(clip,subClip1,subClip2,splitTime):
    currentImageList = clip.imageList
    currentImageEffectList = clip.imageEffectList
    subClip1ImageList = []
    subClip2ImageList = []
    imageClip1 = None
    imageClip2 = None
    subClip1ImageEffectList = []
    subClip2ImageEffectList = []
    effectIndex = -1
    effectToListMapping = dict()
    for index,effects in enumerate(currentImageEffectList):
        effectToListMapping[effects[0]] = index


    for index,image in enumerate(currentImageList):
        startTime = image.start
        endTime = image.start + image.duration
        if(index in effectToListMapping):
            effectIndex = effectToListMapping[index]
        else:
            effectIndex = -1
        if(endTime <= splitTime):
            subClip1ImageList.append(image)
            if(effectIndex != -1):
                subClip1ImageEffectList.append((len(subClip1ImageList)-1,currentImageEffectList[effectIndex][1],currentImageEffectList[effectIndex][2]))

        elif(startTime >= splitTime):
            imageClip2 = image.copy()
            imageClip2.set_start(startTime-splitTime)
            subClip2ImageList.append(imageClip2)
            if(effectIndex != -1):
                subClip2ImageEffectList.append((len(subClip2ImageList)-1,currentImageEffectList[effectIndex][1],currentImageEffectList[effectIndex][2]))
        else:
            imageClip1 = image.copy()
            imageClip1.set_start(startTime)
            imageClip1.set_duration(splitTime-startTime)
            imageClip2 = image.copy()
            imageClip2.set_start(splitTime)
            imageClip2.set_duration(endTime-splitTime)
            subClip1ImageList.append(imageClip1)
            subClip2ImageList.append(imageClip2)
            if(effectIndex!=-1):
                if(currentImageEffectList[effectIndex] == "crossfadein"):
                     subClip1ImageEffectList.append((len(subClip1ImageList)-1,currentImageEffectList[effectIndex][1],currentImageEffectList[effectIndex][2]))
                else:
                    subClip2ImageEffectList.append((len(subClip2ImageList)-1,currentImageEffectList[effectIndex][1],currentImageEffectList[effectIndex][2]))

    subClip1.setImageList(subClip1ImageList)
    subClip2.setImageList(subClip2ImageList)
    subClip1.setImageEffectList(subClip1ImageEffectList)
    subClip2.setImageEffectList(subClip2ImageEffectList)

def sliceClip(trackIndex,splitTime):
    clip = track[trackIndex]
    origVideoClip = clip.output()
    duration = origVideoClip.duration
    print(splitTime)
    print(duration)
    del track[trackIndex]
    subClip1 = Clips(origVideoClip.subclip(0,splitTime))
    subClip2 = Clips(origVideoClip.subclip(splitTime,duration))
    startTime = 0
    endTime = 0
    ## Splitting audio Clips
    handleAudio(clip,subClip1,subClip2,splitTime)

    ## Splitting textClips and textEffects
    handleText(clip,subClip1,subClip2,splitTime)
    ## Splitting imageClips and imageEffects
    handleImage(clip,subClip1,subClip2,splitTime)


    track.insert(trackIndex,subClip1)
    track.insert(trackIndex+1,subClip2)


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


#addImageEffect(1,"crossfadeout",5,0)

fullVideo("outputSA.mp4")
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
