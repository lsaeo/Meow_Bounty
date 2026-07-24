from .task_manager import quest_today

DIFFICULTY_REWARDS = {
    '普通': {'exp': 20, 'gold': 10},
    '困难': {'exp': 50, 'gold': 25},
    '史诗': {'exp': 100, 'gold': 50},
}

DIFFICULTY_HP_PENALTY = {
    '普通': 5,
    '困难': 10,
    '史诗': 20,
}

ALL_CLEAR_BONUS_RATE = 0.2


class RPGEngine:
    def __init__(self, adventurer):
        self.adventurer = adventurer

    def complete_task(self, task):
        diff = task.get('difficulty', '普通')
        rewards = DIFFICULTY_REWARDS.get(diff, DIFFICULTY_REWARDS['普通'])

        exp = rewards['exp']
        gold = rewards['gold']

        leveled_up = self.adventurer.add_exp(exp)
        self.adventurer.add_gold(gold)
        self.adventurer.save()

        msg = f'任务完成！EXP +{exp}  金币 +{gold}'
        if leveled_up:
            msg += f'\n\u2728 升级！Lv.{self.adventurer.level} {self.adventurer.title}'

        return msg, leveled_up, exp, gold

    def apply_all_clear_bonus(self, today_tasks):
        total_exp = 0
        total_gold = 0
        for t in today_tasks:
            diff = t.get('difficulty', '普通')
            r = DIFFICULTY_REWARDS.get(diff, DIFFICULTY_REWARDS['普通'])
            total_exp += r['exp']
            total_gold += r['gold']

        bonus_exp = int(total_exp * ALL_CLEAR_BONUS_RATE)
        bonus_gold = int(total_gold * ALL_CLEAR_BONUS_RATE)

        leveled_up = self.adventurer.add_exp(bonus_exp)
        self.adventurer.add_gold(bonus_gold)
        self.adventurer.streak += 1
        self.adventurer.save()

        msg = (f'\U0001f389 今日悬赏全部清除！'
               f'\n全清奖励：EXP +{bonus_exp}  金币 +{bonus_gold}'
               f'\n\u2b50 连续完成 {self.adventurer.streak} 天！')

        if leveled_up:
            msg += f'\n\u2728 升级！Lv.{self.adventurer.level} {self.adventurer.title}'

        return msg, leveled_up, bonus_exp, bonus_gold

    def daily_settlement(self, yesterday_incomplete):
        total_hp_loss = 0
        for t in yesterday_incomplete:
            diff = t.get('difficulty', '普通')
            hp_loss = DIFFICULTY_HP_PENALTY.get(diff, 5)
            self.adventurer.take_damage(hp_loss)
            total_hp_loss += hp_loss

        if yesterday_incomplete:
            self.adventurer.streak = 0

        self.adventurer.last_login = quest_today()
        self.adventurer.save()

        return total_hp_loss, len(yesterday_incomplete)
