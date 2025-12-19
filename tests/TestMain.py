# Test case
import unittest

from src.config import config
from ok.test.TaskTestCase import TaskTestCase



class TestMyOneTimeTask(TaskTestCase):

    config = config

    def test_ocr1(self):
        # Create a BattleReport object
        self.set_image('tests/images/4.png')
        text = self.task.ocr(match="1回10", log=True)
        print("1@@@:")
        self.assertEqual(text[0].name, '1回10')

    def test_scenario_from_user_screenshot(self):
        # Create a BattleReport object
        self.set_image('tests/images/4.png')
        feature = self.task.find_feature("shopping_coin_button")
        print("2@@@:", feature)
        self.assertIsNotNone(feature)


if __name__ == '__main__':
    unittest.main()
