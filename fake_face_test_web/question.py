import random
import time
from datetime import datetime
from functools import partial

from nicegui import ui, app

from csv_funcs import (
    read_question_csv,
    init_result_file,
    record_result,
)
from defs import questions_dir, images_dir, results_dir

app.add_static_files("/images", images_dir())  # serve all files in this folder

class SessionData:
    def __init__(self, p_id, params, section):
        # self.session_id = session_id
        self.params = params
        self.p_id = p_id
        self.section = section
        self.session = self.params["condition"]
        self.datetime = "{:%Y%m%d-%H%M}".format(datetime.now())
        self.show_ai_results = self.params["show_ai_results"]
        self.show_shap = self.params["show_shap"]
        self.image_dir = images_dir()
        self.save_name = f"{self.p_id}-{self.session}-{self.datetime}.csv"
        self.save_path = results_dir() / self.save_name

        self.image_id = None
        self.image_name = ""
        self.ai_results = ""
        self.ai_confidence = 0
        self.ai_accuracy = 0
        self.true_answer = ""
        self.Age = ""
        self.workclass = ""
        self.education = ""
        self.marital = ""
        self.occupation = ""
        self.relation = ""
        self.race = ""
        self.sex = ""
        self.gain = ""
        self.loss = ""
        self.hpw = ""
        self.country = ""

        self.shap_values = ""

        self.ques_count = 0
        self.ques_start_time = time.time()

        self.ques_num_label = ""
        self.ai_result_label = ""
        self.ai_confidence_label = ""
        self.image_item = None
        self.human_img = None

        question_header, self.questions = read_question_csv(
            questions_dir() / self.params["question_file"], add_index=False
        )

        assert question_header == [
            "ai_results",
            "true_answer",
            "shap_values",
            "Age",
            "workclass",
            "Education-num",
            "Martial-status",
            "Occupation",
            "relationship",
            "Race",
            "Sex",
            "Capital-gain",
            "Capital-loss",
            "Hour-per-week",
            "Country",
        ], "invalid file!"
        random.shuffle(self.questions)

        self.results_header = [
            "p_id",
            "session",
            "datetime",
            "show_ai_results",
            "show_shap",
            "question_number",
            "answer",
            "answered_conf",
            "duration",
        ] + question_header

    def start_test(self):
        if self.ques_count == 0:
            init_result_file(self.save_path, self.results_header)
        self.next_question()

    def next_question(self):
        if self.ques_count >= len(self.questions):
            app.storage.user[f"ques_count-{self.section}"] = self.ques_count
            ui.navigate.to("/end")
            return

        app.storage.user[f"ques_count-{self.section}"] = self.ques_count

        (
            self.ai_results,
            self.true_answer,
            self.shap_values,
            self.Age,
            self.workclass,
            self.education,
            self.marital,
            self.occupation,
            self.relation,
            self.race,
            self.sex,
            self.gain,
            self.loss,
            self.hpw,
            self.country,
        ) = self.questions[self.ques_count]
        self.ques_count += 1
        self.ques_num_label = f"Q{self.ques_count}"
        self.ai_result_label = f"AI Result: {self.ai_results}"
        self.image_item = f"/images/{self.shap_values}"
        self.human_img = "/images/human.png"
        self.Age_label = f"{self.Age}歳"
        self.workclass_label = self.workclass
        self.education_label = self.education
        self.marital_label = self.marital
        self.occupation_label = self.occupation
        self.relation_label = self.relation
        self.race_label = self.race
        self.sex_label = self.sex
        self.gain_label = f"{self.gain}ドル"
        self.loss_label = f"{self.loss}ドル"
        self.hpw_label = f"{self.hpw}時間"
        self.country_label = self.country
        self.ques_start_time = time.time()

    def real_clicked(self, conf):
        self.answered("real", conf)
        # print(conf)

    def fake_clicked(self, conf):
        self.answered("fake", conf)
        # print(conf)

    def answered(self, answer, ans_conf):
        now = time.time()
        duration = now - self.ques_start_time
        self.record_result(
            (
                self.p_id,
                self.section,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.show_ai_results,
                self.show_shap,
                self.ques_count,
                answer,
                ans_conf,
                duration,
                self.shap_values,
                self.ai_results,
                self.true_answer,
                self.Age,
                self.workclass,
                self.education,
                self.marital,
                self.occupation,
                self.relation,
                self.race,
                self.sex,
                self.gain,
                self.loss,
                self.hpw,
                self.country,
            )
        )
        self.next_question()

    def record_result(self, result):
        record_result(self.save_path, result)


def setup_question_page(session_id, params, section):
    @ui.page(f"/question-{section}")
    def question_page() -> None:
        # print(session_id, params)
        session_data = SessionData(session_id, params, section)

        # if f"questions-{session_id}" in app.storage.user:
        #     session_data.questions = app.storage.user[f"questions-{session_id}"]
        # else:
        app.storage.user[f"questions-{section}"] = session_data.questions

        # if f"ques_count-{session_id}" in app.storage.user:
        #     session_data.ques_count = app.storage.user[f"ques_count-{session_id}"]
        # else:
        app.storage.user[f"ques_count-{section}"] = session_data.ques_count
        
        if session_data.ques_count >= len(session_data.questions):
            print("aaa")
            ui.navigate.to("/end")
            return

        session_data.start_test()

        with ui.column().classes("w-full items-center"):
            ques_label = (
                ui.label()
                .bind_text_from(session_data, "ques_num_label")
                .style("font-size: 3em; font-weight: bold")
            )
            with ui.grid(columns=3).classes('w-full items-center'):
                with ui.card():
                    with ui.column().classes('w-full items-center'):
                        title_label = (
                            ui.label("データ")
                            .style("font-size: 2em; font-weight: bold")
                        )
                        ui.separator()
                        with ui.grid(columns=2).classes("w-full items-left").style("font-size: 1.5em; font-weight: bold"):
                            ui.label('年齢')               
                            ui.label().bind_text_from(session_data, "Age_label")             
                            
                            ui.label('雇用形態')           
                            ui.label().bind_text_from(session_data, "workclass_label")   
                            
                            ui.label('教育年数')         
                            ui.label().bind_text_from(session_data, "education_label")  
                            
                            ui.label('婚姻状況')              
                            ui.label().bind_text_from(session_data, "marital_label")     
                            
                            ui.label('職業')                
                            ui.label().bind_text_from(session_data, "occupation_label")     
                            
                            ui.label('続柄')                
                            ui.label().bind_text_from(session_data, "relation_label") 

                            ui.label('人種')                
                            ui.label().bind_text_from(session_data, "race_label") 

                            ui.label('性別')                
                            ui.label().bind_text_from(session_data, "sex_label") 

                            ui.label('資本獲得')                
                            ui.label().bind_text_from(session_data, "gain_label") 

                            ui.label('資本減少')                
                            ui.label().bind_text_from(session_data, "loss_label") 

                            ui.label('週間労働時間')                
                            ui.label().bind_text_from(session_data, "hpw_label") 

                            ui.label('出身国')                
                            ui.label().bind_text_from(session_data, "country_label")

                with ui.column().classes("w-full items-center"):
                    image_label = (
                        ui.image()
                        .style("width: 40em")
                        .bind_source_from(session_data, "human_img")
                    )   

                with ui.column():
                    if session_data.show_ai_results:
                        ai_result_label = (
                            ui.label()
                            .bind_text_from(session_data, "ai_result_label")
                            .style("font-size: 1.5em")
                        )

                    if session_data.show_shap:
                        shap_label = (
                            ui.image()
                            .style("width: 30em")
                            .bind_source_from(session_data, "image_item")
                        )

            ui.label("年収が５万ドルを")

            with ui.row():
                ui.label("超えていない").style("font-size: 1.5em; font-weight: bold; color: #000000")
                for i in range(100, 54, -5):
                    if (i >= 95):
                        ui.button(str(i), color='#666666').on('click', partial(session_data.fake_clicked, i))
                    elif(i >=85):
                        ui.button(str(i), color='#777777').on('click', partial(session_data.fake_clicked, i))
                    elif(i >=75):
                        ui.button(str(i), color='#888888').on('click', partial(session_data.fake_clicked, i))
                    elif(i >= 65):
                        ui.button(str(i), color='#999999').on('click', partial(session_data.fake_clicked, i))
                    else:
                        ui.button(str(i), color='#AAAAAA').on('click', partial(session_data.fake_clicked, i))
                
                ui.button('50', color='#CCCCCC').disable()

                for j in range(55, 101, 5):
                    if (j <= 60):
                        ui.button(str(j), color='#AAAAAA').on('click', partial(session_data.real_clicked, j))
                    elif(j <=70):
                        ui.button(str(j), color='#999999').on('click', partial(session_data.real_clicked, j))
                    elif(j <=80):
                        ui.button(str(j), color='#888888').on('click', partial(session_data.real_clicked, j))
                    elif(j <= 90):
                        ui.button(str(j), color='#777777').on('click', partial(session_data.real_clicked, j))
                    else:
                        ui.button(str(j), color='#666666').on('click', partial(session_data.real_clicked, j))
                ui.label("超えている").style("font-size: 1.5em; font-weight: bold; color: #000000")