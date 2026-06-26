import unittest
import tempfile
import os
import shutil
from unittest.mock import Mock, patch

from paths_mgt import create_paths, create_folder_if_not_exists


class TestPathsMgt(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        
        self.mock_config = Mock()
        self.mock_config.get.side_effect = self._mock_config_get
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _mock_config_get(self, *args):
        if args == ("general", "downloads"):
            return self.temp_dir
        elif args == ("paths",):
            return {
                'sci': 'science',
                'tech': 'technology',
                'df': 'default'
            }
        return None
    
    def test_create_folder_if_not_exists_creates_new_folder(self):
        test_path = os.path.join(self.temp_dir, 'new_folder')
        self.assertFalse(os.path.exists(test_path))
        
        create_folder_if_not_exists(test_path)
        
        self.assertTrue(os.path.exists(test_path))
        self.assertTrue(os.path.isdir(test_path))
    
    def test_create_folder_if_not_exists_with_existing_folder(self):
        test_path = os.path.join(self.temp_dir, 'existing_folder')
        os.makedirs(test_path)
        self.assertTrue(os.path.exists(test_path))
        
        create_folder_if_not_exists(test_path)
        
        self.assertTrue(os.path.exists(test_path))
        self.assertTrue(os.path.isdir(test_path))
    
    def test_create_folder_if_not_exists_creates_nested_folders(self):
        test_path = os.path.join(self.temp_dir, 'parent', 'child', 'grandchild')
        self.assertFalse(os.path.exists(test_path))
        
        create_folder_if_not_exists(test_path)
        
        self.assertTrue(os.path.exists(test_path))
        self.assertTrue(os.path.isdir(test_path))
    
    def test_create_paths_creates_base_download_folder(self):
        base_path = os.path.join(self.temp_dir, 'downloads')
        self.mock_config.get.side_effect = lambda *args: base_path if args == ("general", "downloads") else {'df': 'default'}
        
        create_paths(self.mock_config)
        
        self.assertTrue(os.path.exists(base_path))
    
    def test_create_paths_creates_all_category_folders(self):
        create_paths(self.mock_config)
        
        expected_paths = [
            os.path.join(self.temp_dir, 'science'),
            os.path.join(self.temp_dir, 'technology'),
            os.path.join(self.temp_dir, 'default')
        ]
        
        for path in expected_paths:
            self.assertTrue(os.path.exists(path), f"Path {path} should exist")
            self.assertTrue(os.path.isdir(path), f"Path {path} should be a directory")
    
    def test_create_paths_calls_config_get_correctly(self):
        create_paths(self.mock_config)
        
        self.mock_config.get.assert_any_call("general", "downloads")
        self.mock_config.get.assert_any_call("paths")


if __name__ == '__main__':
    unittest.main()