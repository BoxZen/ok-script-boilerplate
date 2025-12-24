import re

from qfluentwidgets import FluentIcon

from src.tasks.BaseIMASTask import BaseIMASTask


class DailyTask(BaseIMASTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "每日任務"
        self.description = "將需要的行程開啟即可"
        self.icon = FluentIcon.SYNC
        self.default_config.update({
            '禮物': True,
            '活動費': True,
            '工作': True,
            '挑戰': True,
            '每日商店': True,
            'AP商店': True,
            '扭蛋': True,
            '任務': True,
        })

    def run(self):
        self.log_info('任務開始!', notify=True)
        if self.config.get('禮物'):
            self.log_info('正在執行: 禮物')
            self.home_checking()
            self.gift()
        if self.config.get('活動費'):
            self.log_info('正在執行: 活動費')
            self.home_checking()
            self.daily_coin()
        if self.config.get('工作'):
            self.log_info('正在執行: 工作')
            self.home_checking()
            self.work()
            self.click(0.5,0.9)
        if self.config.get('挑戰'):
            self.log_info('正在執行: 挑戰')
            self.home_checking()
            self.challenge()
        if self.config.get('每日商店'):
            self.log_info('正在執行: 每日商店')
            self.home_checking()
            self.shopping()
            self.daily_exchange()
            if self.config.get('AP商店'):
                self.log_info('正在執行: AP商店')
                self.ap_exchange()
            if self.config.get('扭蛋'):
                self.log_info('正在執行: 扭蛋')
                self.gacha()
        if self.config.get('任務'):
            self.log_info('正在執行: 任務')
            self.home_checking()
            self.mission()
        self.home_checking()
        self.log_info('任務完成!', notify=True)
    #商店
    def shopping(self):
        if not self.wait_click_feature('shopping', time_out=1, raise_if_not_found=False, click_after_delay=1,after_sleep=1):
            self.log_debug('shopping: shopping 未找到')
            self.log_info('任務:商店失敗')
            return False
        return True
    #每日商店
    def daily_exchange(self):
        
        recommend = True

        if not self.wait_click_feature('shopping_daily_exchange', time_out=1, raise_if_not_found=False, click_after_delay=1,after_sleep=2):
            self.log_debug('daily_exchange: shopping_daily_exchange 未找到')
            self.log_info('任務:每日商店失敗')
            return False
        while(recommend):
            self.sleep(1)
            box = self.find_one('shopping_recommend',box="top")
            if not box:
                self.log_debug('daily_exchange: shopping_recommend 未找到')
                recommend = False
                break

            try:
                x = box.x
                y = box.y
                w = box.width
                h = box.height
                # 點擊正下方
                self.click(int(x+w/2), int(y+h*2),after_sleep=1)
            except Exception:
                self.log_debug('test: 無法對 shopping_recommend 執行點擊')
                pass

            self.click_yes_button()

        if not self.config.get('AP商店'):
            self.click_back_button()

        return True
    #AP商店
    def ap_exchange(self):
        if not self.wait_click_feature('shopping_ap', time_out=1, raise_if_not_found=False, click_after_delay=1,after_sleep=1):
            self.log_debug('daily_exchange: shopping_ap 未找到')
            self.log_info('任務:AP商店失敗')
            return False
        if not self.wait_click_feature('support_point_increased', time_out=1, raise_if_not_found=False, click_after_delay=1,after_sleep=1):
            self.log_debug('daily_exchange: support_point_increased 未找到')
        self.click_yes_button()
        if not self.wait_click_feature('note_increased', time_out=1, raise_if_not_found=False, click_after_delay=1,after_sleep=1):
            self.log_debug('daily_exchange: note_increased 未找到')
        self.click_yes_button()
        if not self.wait_click_feature('memory_ticket', time_out=1, raise_if_not_found=False, click_after_delay=1,after_sleep=1):
            self.log_debug('daily_exchange: memory_ticket 未找到')
        self.click_yes_button()

        self.click_back_button()
        return True
    #扭蛋
    def gacha(self):
        if not self.wait_click_feature('shopping_coin_gacha', time_out=1, raise_if_not_found=False, click_after_delay=1):
            self.log_debug('gacha: shopping_coin_gacha 未找到')
            self.log_info('任務:扭蛋失敗')
            return False
        if not self.wait_click_feature('shopping_coin_button', time_out=1, raise_if_not_found=False, click_after_delay=1):
            self.log_debug('gacha: shopping_coin_button 未找到')
        self.click_yes_button()
        self.click_no_button()
        self.click_back_button()
        return True
    #工作
    def work(self):
        if not self.wait_click_feature('work', time_out=1, raise_if_not_found=False, click_after_delay=3):
            self.log_debug('work: work 未找到')
            self.log_info('任務:工作失敗')
            return False
        self.clicker(10)
        self.click_yes_button()
        self.clicker(5)
        self.click_yes_button()
        if self.wait_click_feature('work_left', time_out=1, raise_if_not_found=False, click_after_delay=1):
            self.click_next_button()
            self.click_yes_button()
            self.click_next_button()
            self.click_yes_button()
        else:
            self.log_debug('work: work_left 未找到')
        self.clicker(4,0.5,0.1,0.25)
        if self.wait_click_feature('work_right', time_out=1, raise_if_not_found=False, click_after_delay=1):
            self.click_next_button()
            self.click_yes_button()
            self.click_next_button()
            self.click_yes_button()
        else:
            self.log_debug('work: work_right 未找到')
        return True
    #活動費
    def daily_coin(self):
        if not self.wait_click_feature('daily_coin', time_out=1, raise_if_not_found=False, click_after_delay=1):
            self.log_debug('daily_coin: daily_coin 未找到')
            self.log_info('任務:活動費失敗')
            return False
        self.click_no_button()
        return True
    #禮物
    def gift(self):
        if not self.wait_click_feature('gift', time_out=1, raise_if_not_found=False, click_after_delay=1):
            self.log_debug('gift: gift 未找到')
            self.log_info('任務:禮物失敗')
            return False
        self.click_next_button()
        self.click_no_button()
        return True
    #任務
    def mission(self):
        if not self.wait_click_feature('mission', time_out=1, raise_if_not_found=False, click_after_delay=1):
            self.log_debug('mission: mission 未找到')
            self.log_info('任務:任務失敗')
            return False
        self.sleep(1)
        self.click_next_button()
        self.click_no_button()
        self.sleep(3)
        self.click(0.5,0.9)
        self.sleep(1)
        self.click(0.3,0.75)
        self.click_next_button()
        self.click_no_button()
        self.sleep(3)
        self.click(0.5,0.9)
        if self.wait_click_feature('pass', time_out=1, raise_if_not_found=False, click_after_delay=1):
            self.sleep(1)
            if self.wait_click_feature('pass_get', time_out=1,box="left", raise_if_not_found=False, click_after_delay=1,after_sleep=1):
                self.sleep(1)
                self.click_no_button()
            else:
                self.log_debug('mission: pass_get 未找到')
        else:
            self.log_debug('mission: pass 未找到')
        return True
    #挑戰
    def challenge(self):
        if not self.wait_click_feature('challenge', time_out=1, raise_if_not_found=False, click_after_delay=1):
            self.log_debug('challenge: challenge 未找到')

        if not self.wait_click_feature('challenge_button', time_out=1, raise_if_not_found=False, click_after_delay=1):
            self.log_debug('challenge: challenge_button 未找到')
            self.log_info('任務:挑戰失敗')
            return False
        self.sleep(2)
        while(self.wait_click_feature('challenge_battle_total', time_out=5, raise_if_not_found=False,click_after_delay=1)):
            self.wait_click_feature('challenge_start', time_out=5, raise_if_not_found=False,click_after_delay=2)
            self.sleep(2)
            self.wait_click_feature_color('challenge_skip',color_percentage=0.05 ,time_out=10, raise_if_not_found=False,settle_time=1)
            while(self.wait_click_feature('challenge_finish', raise_if_not_found=False, after_sleep=1) == False):
                self.clicker(4,0.5,0.9,0.25)
        
        return True