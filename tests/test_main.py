import unittest
import tempfile
import os
import yaml
from unittest.mock import Mock, patch, MagicMock
from argparse import Namespace

from main import load_config, get_args, main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.test_config_data = {
            'general': {
                'downloads': '/test/downloads'
            },
            'paths': {
                'sci': 'science',
                'tech': 'technology',
                'df': 'default'
            }
        }
        
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml')
        yaml.dump(self.test_config_data, self.temp_file)
        self.temp_file.close()
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    @patch('main.os.path.dirname')
    @patch('main.os.path.abspath')
    @patch('main.os.path.join')
    @patch('main.Config')
    def test_load_config(self, mock_config, mock_join, mock_abspath, mock_dirname):
        mock_abspath.return_value = '/current/dir/main.py'
        mock_dirname.return_value = '/current/dir'
        mock_join.return_value = '/current/dir/config/config.yaml'
        mock_config_instance = Mock()
        mock_config.return_value = mock_config_instance
        
        result = load_config('config/config.yaml')
        
        mock_abspath.assert_called_once()
        mock_dirname.assert_called_once_with('/current/dir/main.py')
        mock_join.assert_called_once_with('/current/dir', 'config/config.yaml')
        mock_config.assert_called_once_with('/current/dir/config/config.yaml')
        self.assertEqual(result, mock_config_instance)
    
    def test_get_args_with_defaults(self):
        mock_config = Mock()
        mock_config.get.return_value = 'default_category'
        
        with patch('sys.argv', ['main.py', 'http://test.url']):
            args = get_args(mock_config)
        
        self.assertEqual(args.url, 'http://test.url')
        self.assertEqual(args.category, 'default_category')
        self.assertEqual(args.only_audio, False)
        self.assertEqual(args.container, 'mp4')
        mock_config.get.assert_called_once_with("paths", "df")
    
    def test_get_args_with_category_provided(self):
        mock_config = Mock()
        mock_config.get.return_value = 'default_category'
        
        with patch('sys.argv', ['main.py', 'http://test.url', 'tech']):
            args = get_args(mock_config)
        
        self.assertEqual(args.url, 'http://test.url')
        self.assertEqual(args.category, 'tech')
        self.assertEqual(args.only_audio, False)
        self.assertEqual(args.container, 'mp4')

    def test_get_args_with_mkv_container(self):
        mock_config = Mock()
        mock_config.get.return_value = 'default_category'

        with patch('sys.argv', ['main.py', 'http://test.url', '--container', 'mkv']):
            args = get_args(mock_config)

        self.assertEqual(args.url, 'http://test.url')
        self.assertEqual(args.category, 'default_category')
        self.assertEqual(args.only_audio, False)
        self.assertEqual(args.container, 'mkv')
    
    def test_get_args_with_audio_only(self):
        mock_config = Mock()
        mock_config.get.return_value = 'default_category'
        
        with patch('sys.argv', ['main.py', 'http://test.url', 'tech', 'True']):
            args = get_args(mock_config)
        
        self.assertEqual(args.url, 'http://test.url')
        self.assertEqual(args.category, 'tech')
        self.assertEqual(args.only_audio, True)
        self.assertEqual(args.container, 'mp4')
    
    @patch('main.download_video')
    @patch('main.get_args')
    @patch('main.load_config')
    def test_main_function_flow(self, mock_load_config, mock_get_args, mock_download_video):
        mock_config = Mock()
        mock_load_config.return_value = mock_config
        
        mock_args = Namespace(url='http://test.url', category='tech', only_audio=False, container='mp4')
        mock_get_args.return_value = mock_args
        
        main()
        
        mock_load_config.assert_called_once_with("config/config.yaml")
        mock_get_args.assert_called_once_with(mock_config)
        mock_download_video.assert_called_once_with(mock_config, 'http://test.url', 'tech', False, 'mp4')
    
    @patch('main.download_video')
    @patch('main.get_args')
    @patch('main.load_config')
    def test_main_function_with_audio_only(self, mock_load_config, mock_get_args, mock_download_video):
        mock_config = Mock()
        mock_load_config.return_value = mock_config
        
        mock_args = Namespace(url='http://test.url', category='sci', only_audio=True, container='mp4')
        mock_get_args.return_value = mock_args
        
        main()
        
        mock_download_video.assert_called_once_with(mock_config, 'http://test.url', 'sci', True, 'mp4')


if __name__ == '__main__':
    unittest.main()
