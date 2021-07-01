"""A video player class."""
from src.video_playlist import Playlist
from .video_library import VideoLibrary
import random
import enum

class video_state(enum.Enum):
    Playing = 1
    Pause = 2
    Stop = 3
    Continue = 4

class video_under_process:
    def __init__(self):
        self.video = None
        self.status = video_state.Stop

    def set_video(self, video, state):
        self.video = video
        self.set_status(state)

    def set_status(self, state):
        self.status = state

        if self.status == video_state.Playing:
            print("Playing video: " + self.video._title)
        elif self.status == video_state.Pause:
            print("Pausing video: " + self.video._title)
        elif self.status == video_state.Stop:
            print("Stopping video: " + self.video._title)
            self.video = None
        elif self.status == video_state.Continue:
            print("Continuing video: " + self.video._title)

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        #info about all videos
        self._video_library = VideoLibrary()
        #currently playing video
        self.video_under_process = video_under_process()

        self.playlists = dict()
        self.userWrittenStylePlaylists = dict()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        for vid in self.Sort_video_titles( self._video_library.get_all_videos() ):
            print( "  ", self.get_video_details(vid) )
    # print("show_all_videos needs implementation")

    def play_video(self, video_id):
        """Plays the respective video.
        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video != None:

            if(video.flagged == None):
                if self.video_under_process.status != video_state.Stop:
                    self.stop_video()

                self.video_under_process.set_video(video, video_state.Playing)
            else:
                print("Cannot play video: Video is currently flagged (reason: "+ video.flagged +")")

        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        if self.video_under_process.status != video_state.Stop:
            self.video_under_process.set_status(video_state.Stop)

        else:
            print("Cannot stop video: No video is currently playing")
        # print("stop_video needs implementation")

    def play_random_video(self):
        """Plays a random video from the video library."""
        videos = self._video_library.get_all_videos()

        if len([x for x in videos if x.flagged == None]) == 0:
            print("No videos available")
            return

        vid = videos[ random.randint(0, len(videos)-1) ]
        self.play_video(vid._video_id)
        # print("play_random_video needs implementation")

    def pause_video(self):
        """Pauses the current video."""
        if self.video_under_process.video != None:
            if( self.video_under_process.status != video_state.Pause ):
                self.video_under_process.set_status(video_state.Pause)
            else:
                print("Video already paused:", self.video_under_process.video._title)

        else:
            print("Cannot pause video: No video is currently playing")
    # print("pause_video needs implementation")

    def continue_video(self):
        """Resumes playing the current video."""
        print("continue_video needs implementation")

    def show_playing(self):
        """Displays video currently playing."""
        if self.video_under_process.video != None:
            if self.video_under_process.status != video_state.Pause:
                print("Currently playing:", self.get_video_details(self.video_under_process.video))
            else:
                print("Currently playing:", self.get_video_details(self.video_under_process.video), "- PAUSED")

        else:
            print("No video is currently playing")
        # print("show_playing needs implementation")

    def is_playlist_exist(self, name):
        return name in self.playlists.keys()

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        pln = playlist_name.lower()
        if pln in self.playlists.keys():
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self.playlists[pln] = []
            self.userWrittenStylePlaylists[pln] = playlist_name  # for later user to display the playlist
            print("Successfully created new playlist:", self.userWrittenStylePlaylists[pln])

        # if playlist_name.lower() not in (name.lower() for name in self.playlist_dict.keys()):
        #     pl = Playlist(playlist_name)
        #     self.playlist_dict[playlist_name] = pl
        #     print("Successfully created new playlist:", pl._name)
        # else:
        #     print("Cannot create playlist: A playlist with the same name already exists")
        #print("create_playlist needs implementation")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        pln = playlist_name.lower()
        video = self._video_library.get_video(video_id)

        if self.is_playlist_exist(pln):

            if video != None:
                if (video.flagged == None):
                    if video in self.playlists[pln]:
                        print("Cannot add video to " + playlist_name + ": Video already added")
                    else:
                        self.playlists[pln].append(video)
                        print("Added video to " + playlist_name + ":", video._title)
                else:
                    print("Cannot add video to " + playlist_name + ": Video is currently flagged (reason: " + \
                          video.flagged + ")")
            else:
                print("Cannot add video to " + playlist_name + ": Video does not exist")

        else:
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")

        #print("add_to_playlist needs implementation")

    def show_all_playlists(self):
        """Display all playlists."""
        if (len(self.playlists.keys()) == 0):  # means no playlist added
            print("No playlists exist yet")

        else:
            print("Showing all playlists: ")
            for playlist in sorted(self.playlists.keys()):
                print("   " + self.userWrittenStylePlaylists[playlist.lower()])

        #print("show_all_playlists needs implementation")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        pln = playlist_name.lower()

        if self.is_playlist_exist(pln):
            videos = self.playlists[pln]
            print("Showing playlist:", playlist_name)

            if len(videos) != 0:
                for vid in videos:
                    print("  ", self.get_video_details(vid))

            else:
                print("  ", "No videos here yet")
        else:
            print("Cannot show playlist " + playlist_name + ": Playlist does not exist")

        #print("show_playlist needs implementation")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist_name_old = playlist_name
        if playlist_name.lower() not in (name.lower() for name in self.playlist_dict.keys()):
            print("Cannot remove video from", playlist_name + ":", "Playlist does not exist")
        else:
            for key in self.playlist_dict.keys():
                if key.lower() == playlist_name.lower():
                    playlist_name = key
            obj = self.playlist_dict[playlist_name]
            video_list = obj.videos
            try:
                video_name = self._video_library.get_video(video_id)._titile
            except:
                video_name =""
            if video_id in video_list:
                video_list.remove(video_id)
                obj.x(video_list)
                print("Removed video from", playlist_name_old + ":", video_name)
            else:
                if not video_name:
                    print("Cannot remove video from", playlist_name_old + ":", "Video does not exist")
                else:
                    print("Cannot remove video from", playlist_name_old + ":", "Video is not in playlist")
        #print("remove_from_playlist needs implementation")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        pln = playlist_name.lower()
        if self.is_playlist_exist(pln):
            self.playlists[pln] = []
            print("Successfully removed all videos from " + playlist_name)
        else:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")
        #print("clears_playlist needs implementation")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        pln = playlist_name.lower()
        if self.is_playlist_exist(pln):
            self.playlists.pop( pln )
            print("Deleted playlist: " + pln )
        else:
            print("Cannot delete playlist " + pln + ": Playlist does not exist")

        #print("deletes_playlist needs implementation")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        #print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        #print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.
        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")