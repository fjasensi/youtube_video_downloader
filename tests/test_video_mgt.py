import unittest
import os
import shutil
import tempfile
from unittest.mock import Mock, patch, MagicMock

from video_mgt import download_video


class TestVideoMgt(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.mock_config = Mock()
        self.mock_config.get.side_effect = self._mock_config_get
        
        self.test_url = "https://www.youtube.com/watch?v=test"
        self.test_category = "tech"
        self.base_downloads = self.temp_dir
        self.category_path = "technology"

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _mock_config_get(self, *args):
        if args == ("general", "downloads"):
            return self.base_downloads
        elif args == ("paths", "tech"):
            return self.category_path
        elif args == ("paths", "df"):
            return "default"
        elif args == ("paths", "nonexistent"):
            return None
        return None
    
    @patch('video_mgt.yt_dlp.YoutubeDL')
    def test_download_video_with_video_and_audio(self, mock_yt_dlp):
        mock_ydl_instance = MagicMock()
        mock_yt_dlp.return_value.__enter__.return_value = mock_ydl_instance
        
        download_video(self.mock_config, self.test_url, self.test_category, False)
        
        expected_path = os.path.join(self.base_downloads, self.category_path)
        expected_options = {
            'ignoreerrors': True,
            'noprogress': True,
            'remote_components': ['ejs:github'],
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'merge_output_format': 'mp4',
            'outtmpl': f'{expected_path}/%(title)s.%(ext)s',
            'writesubtitles': True,
            'subtitleslangs': ['en'],
        }
        
        mock_yt_dlp.assert_called_once_with(expected_options)
        mock_ydl_instance.download.assert_called_once_with([self.test_url])

    @patch('video_mgt.yt_dlp.YoutubeDL')
    def test_download_video_with_mkv_container(self, mock_yt_dlp):
        mock_ydl_instance = MagicMock()
        mock_yt_dlp.return_value.__enter__.return_value = mock_ydl_instance

        download_video(self.mock_config, self.test_url, self.test_category, False, "mkv")

        expected_path = os.path.join(self.base_downloads, self.category_path)
        expected_options = {
            'ignoreerrors': True,
            'noprogress': True,
            'remote_components': ['ejs:github'],
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mkv',
            'outtmpl': f'{expected_path}/%(title)s.%(ext)s',
            'writesubtitles': True,
            'subtitleslangs': ['en'],
        }

        mock_yt_dlp.assert_called_once_with(expected_options)
        mock_ydl_instance.download.assert_called_once_with([self.test_url])
    
    @patch('video_mgt.yt_dlp.YoutubeDL')
    def test_download_video_audio_only(self, mock_yt_dlp):
        mock_ydl_instance = MagicMock()
        mock_yt_dlp.return_value.__enter__.return_value = mock_ydl_instance
        
        download_video(self.mock_config, self.test_url, self.test_category, True)
        
        expected_path = os.path.join(self.base_downloads, self.category_path)
        expected_options = {
            'ignoreerrors': True,
            'noprogress': True,
            'remote_components': ['ejs:github'],
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{expected_path}/%(title)s.%(ext)s',
        }
        
        mock_yt_dlp.assert_called_once_with(expected_options)
        mock_ydl_instance.download.assert_called_once_with([self.test_url])
    
    @patch('video_mgt.yt_dlp.YoutubeDL')
    def test_download_video_fallback_to_default_category(self, mock_yt_dlp):
        mock_ydl_instance = MagicMock()
        mock_yt_dlp.return_value.__enter__.return_value = mock_ydl_instance
        
        download_video(self.mock_config, self.test_url, "nonexistent", False)
        
        expected_path = os.path.join(self.base_downloads, "default")
        mock_ydl_instance.download.assert_called_once_with([self.test_url])
        
        call_args = mock_yt_dlp.call_args[0][0]
        self.assertIn(expected_path, call_args['outtmpl'])
    
    @patch('video_mgt.yt_dlp.YoutubeDL')
    @patch('builtins.print')
    def test_download_video_handles_exception(self, mock_print, mock_yt_dlp):
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.download.side_effect = Exception("Download failed")
        mock_yt_dlp.return_value.__enter__.return_value = mock_ydl_instance
        
        download_video(self.mock_config, self.test_url, self.test_category, False)
        
        mock_print.assert_called_once_with("Error: Download failed")
    
    @patch('video_mgt.yt_dlp.YoutubeDL')
    def test_download_video_uses_youtube_title_in_filename(self, mock_yt_dlp):
        mock_ydl_instance = MagicMock()
        mock_yt_dlp.return_value.__enter__.return_value = mock_ydl_instance
        
        download_video(self.mock_config, self.test_url, self.test_category, False)
        
        call_args = mock_yt_dlp.call_args[0][0]
        self.assertEqual(
            call_args['outtmpl'],
            os.path.join(self.base_downloads, self.category_path, '%(title)s.%(ext)s'),
        )


if __name__ == '__main__':
    unittest.main()
