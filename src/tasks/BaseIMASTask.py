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
        self.sleep(1)
        if not self.wait_click_feature('next_button', raise_if_not_found=False, box = "bottom"):
            self.log_debug('click_next_button: next_button 未找到')
            return False
        return True
    
    def click_yes_button(self):
        self.sleep(1)
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
    #連點
    def clicker(self, num_clicks, x=0.5, y=0.5, delay_between_clicks=0.5):
        for _ in range(num_clicks):
            self.click(x, y)
            self.sleep(delay_between_clicks)
        return True
    #魔改 wait_click_feature 支持最小置信度參數
    def wait_click_feature_confidence(self, feature, horizontal_variance=0, vertical_variance=0, threshold=0,
                                      relative_x=0.5,relative_y=0.5, min_confidence=0.5,#配置最小置信度
                                      time_out=0, pre_action=None, post_action=None, box=None,
                                      raise_if_not_found=True,use_gray_scale=False, canny_lower=0,
                                      canny_higher=0, click_after_delay=0, settle_time=-1,
                                      after_sleep=0):
    
        def find_with_min_confidence():
            # 改用 find_feature，返回所有匹配
            boxes = self.find_feature(feature, horizontal_variance, vertical_variance,
                                      threshold, box=box,use_gray_scale=use_gray_scale,
                                      canny_lower=canny_lower, canny_higher=canny_higher)
            
            # 篩選置信度 >= min_confidence 的
            valid_boxes = [i for i in boxes if i.confidence >= min_confidence]
            
            if len(valid_boxes) > 0:
                # 返回置信度最高的那個
                return max(valid_boxes, key=lambda i: i.confidence)
            return None
        
        box = self.wait_until(
            lambda: find_with_min_confidence(),
            time_out=time_out,
            pre_action=pre_action,
            post_action=post_action,
            settle_time=settle_time)
        
        if box is not None:
            if click_after_delay > 0:
                self.sleep(click_after_delay)
            self.click_box(box, relative_x, relative_y, after_sleep=after_sleep)
            return True
        return False
    #魔改 wait_click_feature 支持RBG百分比閥值篩選
    def wait_click_feature_color(self, feature, horizontal_variance=0, vertical_variance=0,
                                 threshold=0, relative_x=0.5, relative_y=0.5,
                                 rgb={'r': (255, 255), 'g': (255, 255), 'b': (255, 255)},#配置找色區間(min,max)
                                 color_percentage=0.5,#配置RBG百分比閥值(0~1)
                                 time_out=0, pre_action=None, post_action=None, 
                                 box=None, raise_if_not_found=True,use_gray_scale=False,
                                 canny_lower=0, canny_higher=0, click_after_delay=0,
                                 settle_time=-1, after_sleep=0):
        # 根據RGB range於box所佔的百分比篩選
        def find_with_color_check():
            candidate = self.find_one(feature, horizontal_variance, vertical_variance,
                                      threshold, box=box, use_gray_scale=use_gray_scale,
                                      canny_lower=canny_lower, canny_higher=canny_higher,)
            if not candidate:
                return None
            percentage = self.calculate_color_percentage(rgb, candidate)
            return candidate if percentage > color_percentage else None

        box = self.wait_until(
            lambda: find_with_color_check(),
            time_out=time_out,
            pre_action=pre_action,
            post_action=post_action, raise_if_not_found=raise_if_not_found,
            settle_time=settle_time)
        
        if box is not None:
            if click_after_delay > 0:
                self.sleep(click_after_delay)
            self.click_box(box, relative_x, relative_y, after_sleep=after_sleep)
            return True
        return False
    def test(self):
        if self.wait_click_feature_color('challenge_skip',color_percentage=0.05,time_out=1 ,raise_if_not_found=False):
            print("found")
            return "found"
        else:
            print("not found")
            return "not found"
        return True