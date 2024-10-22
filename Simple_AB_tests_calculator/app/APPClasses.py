import telebot
from telebot import types
from dotenv import load_dotenv, find_dotenv
import os
import numpy as np
from statsmodels.stats.proportion import proportions_ztest, proportion_effectsize
from statsmodels.stats.power import NormalIndPower

load_dotenv(find_dotenv())

class Tgmessage:
    def __init__(self, send, chatid):
        self.send = send
        self.chatid = chatid

    def message_alarm(self):
        bot = telebot.TeleBot(str(os.getenv('bot_id')))
        bot.send_message(self.chatid, self.send)

class SampleSizeEvaluation:
    def __init__(self, baseline_rate, minimum_detectable_effect, statistic_power, alpha_level, samples_ratio):
        self.baseline_rate = float(baseline_rate)
        self.minimum_detectable_effect = float(minimum_detectable_effect)
        self.statistic_power = float(statistic_power)
        self.alpha_level = float(alpha_level)
        self.samples_ratio = float(samples_ratio)

    def sample_size_calculator(self):
        effect_size = proportion_effectsize(self.baseline_rate, self.baseline_rate + self.minimum_detectable_effect)
        sample_size = NormalIndPower().solve_power(effect_size = effect_size, power = self.statistic_power, alpha = self.alpha_level, ratio = self.samples_ratio)
        return round(sample_size)

class ABTestEvaluation:
    def __init__(self, conversion_a, conversion_b, size_sample_a, size_sample_b, significance):
        self.conversion_a = int(conversion_a)
        self.conversion_b = int(conversion_b)
        self.size_sample_a = int(size_sample_a)
        self.size_sample_b = int(size_sample_b)
        self.significance = float(significance)

    def z_test_evaluation(self):
        _, p_value = proportions_ztest([self.conversion_a, self.conversion_b], [self.size_sample_a, self.size_sample_b], alternative = 'two-sided')
        return p_value < self.significance, p_value

