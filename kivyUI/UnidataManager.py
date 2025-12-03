import os
import ctypes
import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.core.text import LabelBase
from kivy.uix.popup import Popup

from kivyDataTrans.file_converter import convert_file   # 데이터 변환 모듈 불러오기 (패키지 방식)

font_path = os.path.join(os.path.dirname(__file__), "[KOR]NanumGothic", "NanumGothic.ttf")  # 한글 폰트 등록
LabelBase.register(name="Nanum", fn_regular=font_path)

DLL_PATH = os.path.join(os.path.dirname(__file__), "..", "kivyC", "UnidataManager.dll") # C DLL 로드
clib = ctypes.CDLL(DLL_PATH)

clib.sum_array.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int)  # C 함수 시그니처 정의
clib.sum_array.restype = ctypes.c_int
clib.average_array.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int)
clib.average_array.restype = ctypes.c_double


class TableView(GridLayout):
    def __init__(self, df: pd.DataFrame, **kwargs):
        super().__init__(cols=len(df.columns), spacing=5, padding=5, **kwargs)
        for col in df.columns:
            self.add_widget(Label(text=str(col), font_name="Nanum"))
        for _, row in df.iterrows():
            for cell in row:
                self.add_widget(Label(text=str(cell), font_name="Nanum"))


class ManagerUI(App):
    title = "UnidataManager"

    def build(self):
        root = BoxLayout(orientation="vertical", spacing=8, padding=8)

        # 버튼 바
        btns = BoxLayout(size_hint_y=None, height=50, spacing=8)
        btn_load = Button(text="불러오기", font_name="Nanum")
        btn_save = Button(text="저장", font_name="Nanum")
        btn_convert = Button(text="변환", font_name="Nanum")
        btn_csum = Button(text="C합계", font_name="Nanum")
        btn_cavg = Button(text="C평균", font_name="Nanum")

        btn_load.bind(on_press=self.on_load)
        btn_save.bind(on_press=self.on_save)
        btn_convert.bind(on_press=self.on_convert)
        btn_csum.bind(on_press=self.on_csum)
        btn_cavg.bind(on_press=self.on_cavg)

        for b in [btn_load, btn_save, btn_convert, btn_csum, btn_cavg]:
            btns.add_widget(b)
        root.add_widget(btns)

        # 기본 데이터 표시
        self.df = pd.DataFrame([["홍길동", 25, 90], ["김철수", 30, 85]], columns=["이름", "나이", "점수"])
        self.table_container = BoxLayout()
        self.refresh_table()
        root.add_widget(self.table_container)

        return root

    def refresh_table(self):
        self.table_container.clear_widgets()
        self.table_container.add_widget(TableView(self.df))

    def show_popup(self, title, content_text):
        popup = Popup(title=title, content=Label(text=content_text, font_name="Nanum"), size_hint=(0.6, 0.4))
        popup.open()

    def on_load(self, instance):
        chooser = FileChooserListView(filters=["*.xlsx", "*.csv", "*.json"])
        popup = Popup(title="파일 불러오기", content=chooser, size_hint=(0.9, 0.9))
        def on_select(instance, selection):
            if selection:
                path = selection[0]
                try:
                    if path.lower().endswith(".xlsx"):
                        self.df = pd.read_excel(path)
                    elif path.lower().endswith(".csv"):
                        self.df = pd.read_csv(path)
                    elif path.lower().endswith(".json"):
                        self.df = pd.read_json(path)
                    else:
                        self.show_popup("오류", "지원하지 않는 형식입니다.")
                        return
                    self.refresh_table()
                    popup.dismiss()
                except Exception as e:
                    self.show_popup("불러오기 오류", str(e))
        chooser.bind(on_submit=lambda inst, sel, touch: on_select(inst, sel))
        popup.open()

    def on_save(self, instance):
        out = os.path.join(os.path.dirname(__file__), "..", "output.xlsx")
        self.df.to_excel(out, index=False)
        self.show_popup("저장 완료", f"파일 저장: {out}")

    def on_convert(self, instance):
        try:
            base = os.path.join(os.path.dirname(__file__), "..")
            input_file = os.path.join(base, "output.xlsx")
            output_file = os.path.join(base, "output.json")
            convert_file(input_file, output_file)
            self.show_popup("변환 완료", f"{input_file} → {output_file}")
        except Exception as e:
            self.show_popup("변환 오류", str(e))

    def on_csum(self, instance):
        scores = self.df["점수"].astype(int).tolist()
        arr = (ctypes.c_int * len(scores))(*scores)
        total = clib.sum_array(arr, len(scores))
        self.show_popup("C 합계 결과", f"점수 합계: {total}")

    def on_cavg(self, instance):
        scores = self.df["점수"].astype(int).tolist()
        arr = (ctypes.c_int * len(scores))(*scores)
        avg = clib.average_array(arr, len(scores))
        self.show_popup("C 평균 결과", f"점수 평균: {avg:.2f}")


if __name__ == "__main__":
    ManagerUI().run()
