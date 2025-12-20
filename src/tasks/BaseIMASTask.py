import re

from ok import BaseTask

class BaseIMASTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def home_checking(self):
        box = self.wait_feature('home', time_out=3)
        if not box:
            self.log_debug('home_checking: home 未找到')
            self.sleep(0.5)
            if not self.wait_click_feature('homeflag_grey', raise_if_not_found=False,box = "bottom_left"):
                self.log_debug('home_checking: homeflag_grey 未找到')
                if not self.wait_click_feature('homeflag', raise_if_not_found=False,box = "bottom"):
                    self.log_debug('home_checking: homeflag 未找到')
                    return False
            self.sleep(1)
        return True
    
    def click_next_button(self):
        if not self.wait_click_feature('next_button', raise_if_not_found=False, box = "bottom"):
            self.log_debug('click_next_button: next_button 未找到')
            return False
        return True
    
    def click_yes_button(self):
        if not self.wait_click_feature('yes_button',time_out = 1, raise_if_not_found=False, box = "bottom",click_after_delay=1):
            self.log_debug('click_yes_button: yes_button 未找到')
            return False
        return True
    
    def click_no_button(self):
        self.sleep(1)
        if not self.wait_click_feature('no_button',time_out = 1, raise_if_not_found=False, box = "bottom",click_after_delay=1):
            self.log_debug('click_no_button: no_button 未找到')
            return False
        return True
    
    def click_add_button(self):
        if not self.wait_click_feature('add_button',time_out = 1, raise_if_not_found=False, box = "bottom"):
            self.log_debug('click_add_button: add_button 未找到')
            return False
        return True
    
    def click_back_button(self):
        if not self.wait_click_feature('back', time_out=1, raise_if_not_found=False, after_sleep=1,click_after_delay=1):
            self.log_debug('click_back_button: back 未找到')
            return False
        return True

    def test(self):
        return True