"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random

def tagsToStr(tagsList):
    tags = ""
    if tagsList:
        for tag in tagsList:
            tag.strip("()")
            tags= tags + tag        
        tags=tags[0]+tags[1:].replace('#', ' #')
    return tags

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.playing_video=None
        self.paused_video=None
        self.playlists={}
        self.flagged_videos={}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        sorted_list=self._video_library.get_all_videos().copy()
        sorted_list.sort(key=lambda x:x.title)

        print("Here's a list of all available videos:")
        for video in sorted_list:
            tags = tagsToStr(video.tags)
            if video in self.flagged_videos.keys():
                print(f"  {video.title} ({video.video_id}) [{tags}] - FLAGGED (reason: {self.flagged_videos[video]})")
            else:
                print(f"  {video.title} ({video.video_id}) [{tags}]")


    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video =self._video_library.get_video(video_id)
        if video in self.flagged_videos.keys():
            print(f"Cannot play video: Video is currently flagged (reason: {self.flagged_videos[video]})")
        elif video != None:
            if self.playing_video != None:
                print(f"Stopping video: {self.playing_video.title}")
                self.playing_video= video
                print(f"Playing video: {video.title}")
            else:
                self.playing_video= video
                print(f"Playing video: {video.title}")
            self.paused_video=None
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        if self.playing_video != None:
            print(f"Stopping video: {self.playing_video.title}")
            self.playing_video= None
            self.paused_video= None
        else:
            print(f"Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        if list(self.flagged_videos.keys()) == self._video_library.get_all_videos():
            print("No videos available")
        else:
            randVid = random.choice(self._video_library.get_all_videos())
            while randVid in self.flagged_videos.keys():
                randVid = random.choice(self._video_library.get_all_videos())

            if self.playing_video != None:
                print(f"Stopping video: {self.playing_video.title}")
                self.playing_video= randVid
                print(f"Playing video: {randVid.title}")
            else:
                self.playing_video= randVid
                print(f"Playing video: {randVid.title}")

            self.paused_video = None

    def pause_video(self):
        """Pauses the current video."""
        if self.paused_video != None:
            print(f"Video already paused: {self.paused_video.title}")
        elif self.playing_video == None:
            print("Cannot pause video: No video is currently playing")
        else:
            self.paused_video = self.playing_video
            print(f"Pausing video: {self.paused_video.title}")

    def continue_video(self):
        """Resumes playing the current video."""

        if (self.playing_video == self.paused_video) & (self.paused_video!= None):
            print(f"Continuing video: {self.playing_video.title}")
            self.paused_video == None
        elif self.playing_video == None:
            print("Cannot continue video: No video is currently playing")
        else:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        tags = ""
        if self.playing_video!=None:
            tags = tagsToStr(self.playing_video.tags)

        if self.playing_video == None:
            print("No video is currently playing")
        elif self.playing_video == self.paused_video:
            print(f"Currently playing: {self.playing_video.title} ({self.playing_video.video_id}) [{tags}] - PAUSED")
        else:
            print(f"Currently playing: {self.playing_video.title} ({self.playing_video.video_id}) [{tags}]")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in map(str.lower, self.playlists.keys()):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            newPlaylist=Playlist(playlist_name)
            self.playlists[newPlaylist.name]=[]
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        video = self._video_library.get_video(video_id)

        if playlist_name.lower() not in map(str.lower, self.playlists.keys()):
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        elif video == None:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
        else:
            for key in self.playlists.keys():
                if key.lower() == playlist_name.lower():
                    playlist_key=key
            if video in self.flagged_videos.keys():
                print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {self.flagged_videos[video]})")
            elif video in self.playlists[playlist_key]:
                print(f"Cannot add video to {playlist_name}: Video already added")
            else:
                self.playlists[playlist_key].append(video)
                print(f"Added video to {playlist_name}: {video.title}")

    def show_all_playlists(self):
        """Display all playlists."""

        lists = list(self.playlists)

        if len(lists) == 0:
            print("No playlists exist yet")
        else:
            lists.sort()
            print("Showing all playlists:")
            for list_name in lists:
                print(f"  {list_name}")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.lower() not in map(str.lower, self.playlists.keys()):
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
        else:
            for key in self.playlists.keys():
                if key.lower() == playlist_name.lower():
                    playlist_key=key

            print(f"Showing playlist: {playlist_name}")
            if len(self.playlists[playlist_key])==0:
                print("  No videos here yet")
            else:
                for video in self.playlists[playlist_key]:
                    tags = tagsToStr(video.tags)
                    if video in self.flagged_videos.keys():
                        print(f"  {video.title} ({video.video_id}) [{tags}] - FLAGGED (reason: {self.flagged_videos[video]})")
                    else:
                        print(f"  {video.title} ({video.video_id}) [{tags}]")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """

        video = self._video_library.get_video(video_id)

        if playlist_name.lower() not in map(str.lower, self.playlists.keys()):
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        elif video == None:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
        else:
            for key in self.playlists.keys():
                if key.lower() == playlist_name.lower():
                    playlist_key=key

            if video not in self.playlists[playlist_key]:
                print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            else:
                self.playlists[playlist_key].remove(video)
                print(f"Removed video from {playlist_name}: {video.title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.lower() not in map(str.lower, self.playlists.keys()):
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            for key in self.playlists.keys():
                if key.lower() == playlist_name.lower():
                    playlist_key=key
            
            self.playlists[playlist_key].clear()
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.lower() not in map(str.lower, self.playlists.keys()):
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            for key in self.playlists.keys():
                if key.lower() == playlist_name.lower():
                    playlist_key=key
            
            self.playlists.pop(playlist_key)
            print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        result_list=[]
        for video in self._video_library.get_all_videos():
            if video.title.lower().find(search_term.lower()) != -1:
                if video not in self.flagged_videos.keys():
                    result_list.append(video)

        if len(result_list)!=0:
            result_list.sort(key=lambda x:x.title)
            print(f"Here are the results for {search_term}:")
            index = 1
            for video in result_list:
                tags = tagsToStr(video.tags)
                print(f"  {index}) {video.title} ({video.video_id}) [{tags}]")
                index+=1

            print("Would you like to play any of the above? If yes, specify the number of the video. \nIf your answer is not a valid number, we will assume it's a no.")
            while True:
                command = input("> ")
                if command.isnumeric():
                    if (int(command)<=len(result_list)):
                        self.play_video(result_list[int(command)-1].video_id)
                        break
                    else:
                         break
                else:
                    break
        else:
            print(f"No search results for {search_term}")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

        result_list=[]
        for video in self._video_library.get_all_videos():
            if video_tag.lower() in map(str.lower, video.tags) :
                if video not in self.flagged_videos.keys():
                    result_list.append(video)

        if len(result_list)!=0:
            result_list.sort(key=lambda x:x.title)
            print(f"Here are the results for {video_tag}:")
            index = 1
            for video in result_list:
                tags = tagsToStr(video.tags)
                print(f"  {index}) {video.title} ({video.video_id}) [{tags}]")
                index+=1

            print("Would you like to play any of the above? If yes, specify the number of the video. \nIf your answer is not a valid number, we will assume it's a no.")
            while True:
                command = input("> ")
                if command.isnumeric():
                    if (int(command)<=len(result_list)):
                        self.play_video(result_list[int(command)-1].video_id)
                        break
                    else:
                         break
                else:
                    break
        else:
            print(f"No search results for {video_tag}")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if  video == None:
            print("Cannot flag video: Video does not exist")
        elif video in self.flagged_videos.keys():
            print("Cannot flag video: Video is already flagged")
        else:
            if (video == self.playing_video) | (video == self.paused_video):
                self.stop_video()
            if flag_reason != "":
                self.flagged_videos[video]=flag_reason
                print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")
            else:
                self.flagged_videos[video]="Not supplied"
                print(f"Successfully flagged video: {video.title} (reason: Not supplied)")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """

        video = self._video_library.get_video(video_id)
        if  video == None:
            print("Cannot remove flag from video: Video does not exist")
        elif video not in self.flagged_videos.keys():
            print("Cannot remove flag from video: Video is not flagged")
        else:
            self.flagged_videos.pop(video)
            print(f"Successfully removed flag from video: {video.title}")
