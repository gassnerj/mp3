from mutagen.id3 import ID3
import os
import shutil
import re

class mp3():
    def __init__(self):
        self.mp3Path = 'D:\\OneDrive\\Music\\iTunes Music'
        self.newPath = 'D:\\MyMusic'
        self.audio = None
    def print_tags(self):
        self.audio = ID3('D:\\OneDrive\\Music\\iTunes Music\\F00\\Avalon - Adonai.mp3')
        keys = self.audio.keys()
        for k in keys:
            print(self.audio.getall(k))

    def get_tags(self, file):
        audioData = {}
        if os.path.isfile(file):
            audio = ID3(file)
            if audio.get('TALB') and audio.get('TPE1') and audio.get('TCON') and audio.get('TIT2'):
                audioData['album'] = audio.get('TALB').text[0]
                audioData['artist'] = audio.get('TPE1').text[0]
                audioData['genre'] = audio.get('TCON').text[0]
                audioData['title'] = audio.get('TIT2').text[0]
                return audioData

    def main(self):
        for dirName, subdirList, fileList in os.walk(self.mp3Path):
            for file in fileList:
                fpath = dirName + "\\" + file
                filename, file_extension = os.path.splitext(fpath)
                if file_extension == '.mp3':
                    tags = self.get_tags(fpath)
                    newPath = self.make_path(tags)
                    try:
                        self.move_files(fpath, newPath)
                    except Exception as e:
                        print(e)


    def first_upper(self, string):
        string = string[:1].upper() + string[1:]
        return string

    def make_path(self, tags):
        newRootDir = self.newPath
        if tags is not None:
            genre = tags.get('genre')
            artist = tags.get('artist')
            album = tags.get('album')

            genre = self.first_upper(genre)
            artist = self.first_upper(artist)
            album = self.first_upper(album)

            regex = '[?.!/;:,""<>|-]'
            regex2 = r'\s+$'
            genre = re.sub(regex, '', genre)
            artist = re.sub(regex, '', artist)
            album = re.sub(regex, '', album)

            genre = re.sub(regex2, '_', genre)
            artist = re.sub(regex2, '_', artist)
            album = re.sub(regex2, '_', album)

            newDir = newRootDir + "\\" + genre + "\\" + artist + "\\" + album
            if not os.path.exists(newDir):
                os.makedirs(newDir)
            return newDir
        else:
            newDir = newRootDir + "\\" + "noID3tags"
            return newDir

    def move_files(self, srce, dest):
        shutil.move(srce, dest)
        print("Moved " + srce + " to " + dest)

m3 = mp3()

m3.main()