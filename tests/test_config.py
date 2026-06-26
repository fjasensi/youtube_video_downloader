import unittest
import tempfile
import os
import yaml
from unittest.mock import patch

from config import Config


class TestConfig(unittest.TestCase):
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
        
        self.config = Config(self.temp_file.name)
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    def test_init_loads_config(self):
        self.assertIsNotNone(self.config.config)
        self.assertEqual(self.config.config, self.test_config_data)
    
    def test_get_single_key(self):
        result = self.config.get('general')
        self.assertEqual(result, {'downloads': '/test/downloads'})
    
    def test_get_nested_keys(self):
        result = self.config.get('general', 'downloads')
        self.assertEqual(result, '/test/downloads')
    
    def test_get_nested_dict(self):
        result = self.config.get('paths')
        expected = {'sci': 'science', 'tech': 'technology', 'df': 'default'}
        self.assertEqual(result, expected)
    
    def test_get_nested_value(self):
        result = self.config.get('paths', 'sci')
        self.assertEqual(result, 'science')
    
    def test_get_nonexistent_key_returns_none(self):
        result = self.config.get('nonexistent')
        self.assertIsNone(result)
    
    def test_get_nonexistent_nested_key_returns_none(self):
        result = self.config.get('general', 'nonexistent')
        self.assertIsNone(result)
    
    def test_get_with_default_value(self):
        result = self.config.get('nonexistent', default='default_value')
        self.assertEqual(result, 'default_value')
    
    def test_get_nested_with_default_value(self):
        result = self.config.get('paths', 'nonexistent', default='default_path')
        self.assertEqual(result, 'default_path')
    
    def test_get_partial_path_returns_default(self):
        result = self.config.get('paths', 'nonexistent', default='default')
        self.assertEqual(result, 'default')


if __name__ == '__main__':
    unittest.main()