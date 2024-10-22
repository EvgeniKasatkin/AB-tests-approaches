from flask import Flask, send_file, jsonify, request, render_template
import APPClasses
import time
from dotenv import load_dotenv, find_dotenv
import os
import traceback
import requests
import json

app = Flask(__name__)
load_dotenv(find_dotenv())


@app.route('/sample-size-evaluate')
def form_size_sample():
    return render_template('size_sample_template.html')

@app.route('/sample-size-evaluate', methods=['POST'])
def form_size_sample_post():
    while 'variable' not in locals():
        try:
            try:
                baseline_rate = request.form['baseline_rate']
                minimum_detectable_effect = request.form['minimum_detectable_effect']
                statistic_power = request.form['statistic_power']
                alpha_level = request.form['alpha_level']
                samples_ratio = request.form['samples_ratio']
                sample_size = APPClasses.SampleSizeEvaluation(baseline_rate = baseline_rate, minimum_detectable_effect = minimum_detectable_effect, statistic_power = statistic_power, alpha_level = alpha_level, samples_ratio = samples_ratio).sample_size_calculator()
                APPClasses.Tgmessage(chatid = os.getenv('telegram_id'), send = 'At baseline_rate: ' + str(baseline_rate) + ' and minimum_detectable_effect: ' + str(minimum_detectable_effect) + ' and statistic_power: '\
                       + str(statistic_power) + ' and alpha level: ' + str(alpha_level) + ' and samples_ratio: ' +  str(samples_ratio) + '\n' + 'SAMPLE SIZE VOLUME: ' + str(sample_size)).message_alarm()
                return 'Baseline_rate: ' + str(baseline_rate) + '\n' + 'Minimum_detectable_effect: ' + str(minimum_detectable_effect) + '\n' + 'Statistic_power: '\
                       + str(statistic_power) + '\n' + 'Alpha level: ' + str(alpha_level) + '\n' + 'Samples_ratio: ' +  str(samples_ratio) + '\n' + 'SAMPLE SIZE VOLUME: ' + str(sample_size)
            except Exception as e:
                APPClasses.Tgmessage(chatid=os.getenv('telegram_id'), send=str(traceback.format_exc())).message_alarm()
                return str(traceback.format_exc())
        except:
            return str(traceback.format_exc())


@app.route('/test-result-evaluation')
def form_test_result():
    return render_template('test_evaluation.html')

@app.route('/test-result-evaluation', methods=['POST'])
def form_test_result_post():
    while 'variable' not in locals():
        try:
            try:
                conversion_a = request.form['conversion_a']
                conversion_b = request.form['conversion_b']
                size_sample_a = request.form['size_sample_a']
                size_sample_b = request.form['size_sample_b']
                significance = request.form['significance']

                decision, p_value = APPClasses.ABTestEvaluation(conversion_a = conversion_a, conversion_b = conversion_b, size_sample_a = size_sample_a, size_sample_b = size_sample_b, significance = significance).z_test_evaluation()

                if decision == True:
                    decision = 'Positive'
                elif decision == False:
                    decision = 'Negative'

                APPClasses.Tgmessage(chatid = os.getenv('telegram_id'), send = 'Decision: ' + str(decision) + '\n' + 'P-VALUE in test: ' + str(p_value)).message_alarm()

                return 'Decision: ' + str(decision) + '\n' + 'P-VALUE in test: ' + str(p_value)
            except Exception as e:
                APPClasses.Tgmessage(chatid=os.getenv('telegram_id'), send=str(traceback.format_exc())).message_alarm()
                return str(traceback.format_exc())
        except:
            return str(traceback.format_exc())
