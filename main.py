import requests
from urllib.parse import quote
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from bs4 import BeautifulSoup
from iso_codes import get_iso_code
import os
import subprocess
from plan import PlanGUI
<<<<<<< HEAD
from PIL import Image, ImageTk
=======
<<<<<<< HEAD
from PIL import Image,ImageTk
=======
>>>>>>> 6c9a44f8ebc7aac4976e76f48b5839a4caaa766e
>>>>>>> bbaf0f0e19f491d2b4ae56293e6d609df2a4ccde

class MainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("여행 플래너")
        self.window.geometry("930x450")
<<<<<<< HEAD
        self.window.configure(bg='white')

=======
<<<<<<< HEAD
        self.window.configure(bg='white')
=======

>>>>>>> 6c9a44f8ebc7aac4976e76f48b5839a4caaa766e
>>>>>>> bbaf0f0e19f491d2b4ae56293e6d609df2a4ccde
        self.plans_frame = Frame(self.window, bg="light sky blue")
        self.plans_frame.place(x=20, y=190, width=900, height=180)
        self.plans_frame.pack_propagate(False)

<<<<<<< HEAD
        self.mainlabel = Label(self.window, text="여행 플래너", font=("Yu Gothic UI Semibold", 45), fg="light sky blue", bg='white')
        self.mainlabel.place(x=10, y=10)

        self.imgframe = Frame(self.window, width=150, height=150, bg='white', highlightbackground="white")
        self.imgframe.place(x=350, y=10)

=======
<<<<<<< HEAD
        self.mainlabel = Label(self.window, text="여행 플래너", font=("Yu Gothic UI Semibold", 45), fg="light sky blue",bg='white')
        self.mainlabel.place(x=10, y=10)

        self.imgframe = Frame(self.window, width=150, height=150, bg='white', highlightbackground="white"
                                )
        self.imgframe.place(x=350, y=10)


>>>>>>> bbaf0f0e19f491d2b4ae56293e6d609df2a4ccde
        self.image_path = 'trip.jpg'  # 이미지 경로
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((150, 150), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)

<<<<<<< HEAD
        self.img_label = Label(self.imgframe, image=self.photo, width=150, height=150)
        self.img_label.pack()

        self.image = self.image.resize((150, 150), Image.LANCZOS)
        self.img_f = Label(self.imgframe, image=self.photo, width=150, height=150)
        self.img_f.place(x=350, y=10)

=======

        self.img_label = Label(self.imgframe, image=self.photo, width=150, height=150)
        self.img_label.pack()


        self.image = self.image.resize((150, 150), Image.LANCZOS)
        self.img_f = Label(self.imgframe, image=self.photo,width=150,height=150)
        self.img_f.place(x=350, y=10)

=======
        self.mainlabel = Label(self.window, text="여행 플래너", font=("Yu Gothic UI Semibold", 45), fg="light sky blue")
        self.mainlabel.place(x=10, y=10)

>>>>>>> 6c9a44f8ebc7aac4976e76f48b5839a4caaa766e
>>>>>>> bbaf0f0e19f491d2b4ae56293e6d609df2a4ccde
        self.searchbutton = Button(self.window, text="해외국가 정보 검색", font=("Yu Gothic UI Semibold", 25), bd=4,
                                   command=self.open_search_window)
        self.searchbutton.place(x=570, y=10)

        self.add_button = Button(self.window, text="플랜 생성", font=("Yu Gothic UI Semibold", 25), bd=4,
                                 command=self.choose_plan_type)
        self.add_button.place(x=570, y=100)

        self.load_plans()
<<<<<<< HEAD
        self.start_teller_bot()
=======


        self.start_teller_bot()

>>>>>>> bbaf0f0e19f491d2b4ae56293e6d609df2a4ccde
        self.window.mainloop()

    def start_teller_bot(self):
        try:
            subprocess.Popen(["python", "teller.py"])
        except Exception as e:
            print(f"텔레그램 봇을 시작하는 중 오류가 발생했습니다: {e}")

    def get_plan_count(self):
        try:
            tree = ET.parse('plans.xml')
            root = tree.getroot()
            return len(root.findall('plan'))
        except (ET.ParseError, FileNotFoundError):
            return 0

    def open_search_window(self):
        search_window = Toplevel(self.window)
        search_window.title("해외국가 정보 검색")
        search_window.geometry("600x400")

        Label(search_window, text="해외국가 정보 검색", font=("Yu Gothic UI Semibold", 25)).pack(pady=20)
        search_entry = Entry(search_window, width=40)
        search_entry.pack(pady=10)

        search_button = Button(search_window, text="검색",
                               command=lambda: self.search_country_info(search_entry.get(), search_window))
        search_button.pack(pady=10)

        self.search_results = Text(search_window, width=70, height=15, wrap=WORD)
        self.search_results.pack(pady=10)

        scrollbar = Scrollbar(search_window, command=self.search_results.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.search_results.config(yscrollcommand=scrollbar.set)

    def search_country_info(self, country_name, output_window=None):
        api_key = "iM%2B5OYQQSMdcWfhPLplO76%2FH6N49AujG%2FmmOXOanS9NnbU12XeWhcMlNILeAwsn4g9%2FdVBe7ppJECUDKiGGaIw%3D%3D"
        encoded_country_name = quote(country_name)
        iso_code = get_iso_code(country_name)
        url = f"http://apis.data.go.kr/1262000/CountryBasicService/getCountryBasicList?serviceKey={api_key}&countryName={encoded_country_name}&numOfRows=1&pageNo=1&resultType=xml"
        url_warning = f"http://apis.data.go.kr/1262000/TravelWarningService/getTravelWarningList?serviceKey={api_key}&isoCode1={iso_code}&numOfRows=1&pageNo=1&resultType=xml"
        url_ban = f"http://apis.data.go.kr/1262000/TravelBanService/getTravelBanList?serviceKey={api_key}&isoCode1={iso_code}&numOfRows=1&pageNo=1&resultType=xml"

        try:
            response = requests.get(url)
            response_warning = requests.get(url_warning)
            response_ban = requests.get(url_ban)

            if response.status_code == 200 and response_warning.status_code == 200 and response_ban.status_code == 200:
                response.encoding = 'utf-8'
                tree = ET.ElementTree(ET.fromstring(response.content))
                tree_warning = ET.ElementTree(ET.fromstring(response_warning.content))
                tree_ban = ET.ElementTree(ET.fromstring(response_ban.content))
                root = tree.getroot()
                root_warning = tree_warning.getroot()
                root_ban = tree_ban.getroot()

                item = root.find('.//item')
                warning_item = root_warning.find('.//item')
                ban_item = root_ban.find('.//item')

                if item is not None:
                    country_name = item.find('countryName').text if item.find('countryName') is not None else "N/A"
                    basic = self.clean_html(item.find('basic').text if item.find('basic') is not None else "N/A")

                    warning_info = ""
                    if warning_item is not None:
                        control_note = self.clean_html(warning_item.find('controlNote').text if warning_item.find('controlNote') is not None else "N/A")
<<<<<<< HEAD
                        limit_note = self.clean_html(warning_item.find('limitaNote').text if warning_item.find('limitaNote') is not None else "N/A")
                        warning_info = f"\n여행 자제: {control_note}\n\n출국 권고: {limit_note}"
=======
                        limita_note = self.clean_html(warning_item.find('limitaNote').text if warning_item.find('limitaNote') is not None else "N/A")
                        warning_info = f"\n여행 자제: {control_note}\n\n출국 권고: {limita_note}"
>>>>>>> bbaf0f0e19f491d2b4ae56293e6d609df2a4ccde

                    ban_info = ""
                    if ban_item is not None and ban_item.find('countryName').text == country_name:
                        ban_note = self.clean_html(ban_item.find('banNote').text if ban_item.find('banNote') is not None else "N/A")
                        ban_info = f"\n여행 금지: {ban_note}"
                    else:
                        ban_info = "\n여행 금지: N/A"

                    info = f"국가: {country_name}\n{basic}\n{warning_info}\n{ban_info}"

                    if output_window:
                        self.search_results.delete(1.0, END)
                        self.search_results.insert(END, info)
                    else:
                        self.show_info_window(info)
                else:
                    if output_window:
                        self.search_results.delete(1.0, END)
                        self.search_results.insert(END, "국가 정보를 찾을 수 없습니다.")
                    else:
                        self.show_info_window("국가 정보를 찾을 수 없습니다.")
            else:
                error_msg = f"오류가 발생했습니다. 상태 코드: {response.status_code}, {response_warning.status_code}, {response_ban.status_code}\n상세 오류: {response.text}, {response_warning.text}, {response_ban.text}"
                if output_window:
                    self.search_results.delete(1.0, END)
                    self.search_results.insert(END, error_msg)
                else:
                    self.show_info_window(error_msg)

        except Exception as e:
            print(f"Exception: {e}")
            error_msg = f"요청 중 오류가 발생했습니다: {e}"
            if output_window:
                self.search_results.delete(1.0, END)
                self.search_results.insert(END, error_msg)
            else:
                self.show_info_window(error_msg)

    def clean_html(self, raw_html):
        if os.path.isfile(raw_html):
            return raw_html
        if raw_html.startswith("<"):
            soup = BeautifulSoup(raw_html, "html.parser")
            return soup.get_text(separator="\n")
        return raw_html

    def show_info_window(self, info):
        info_window = Toplevel(self.window)
        info_window.title("국가 정보")
        info_window.geometry("600x400")

        info_text = Text(info_window, width=70, height=15, wrap=WORD)
        info_text.insert(END, info)
        info_text.config(state=DISABLED)
        info_text.pack(pady=10)

        scrollbar = Scrollbar(info_window, command=info_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        info_text.config(yscrollcommand=scrollbar.set)

    def choose_plan_type(self):
        if self.get_plan_count() >= 5:
            messagebox.showwarning("경고", "최대 5개의 플랜만 생성할 수 있습니다.")
            return

        self.plan_type_window = Tk()
        self.plan_type_window.title("여행 유형 선택")
        self.plan_type_window.geometry("300x200")

        Label(self.plan_type_window, text="여행 유형을 선택하세요", font=("Yu Gothic UI Semibold", 14)).pack(pady=20)
        Button(self.plan_type_window, text="국내 여행", font=("Yu Gothic UI Semibold", 12),
               command=lambda: self.addplan("domestic")).pack(pady=10)
        Button(self.plan_type_window, text="해외 여행", font=("Yu Gothic UI Semibold", 12),
               command=lambda: self.addplan("international")).pack(pady=10)

    def addplan(self, plan_type):
        self.plan_type_window.destroy()
        self.plan_type = plan_type
        self.addplan_window = Tk()
        self.addplan_window.title("여행 계획 추가")
        self.addplan_window.geometry("400x450")

        Label(self.addplan_window, text="여행 이름(최대 12글자)").pack(pady=5)
        self.name_var = StringVar()
        self.name_var.trace('w', self.limit_size)
        self.name_entry = Entry(self.addplan_window, textvariable=self.name_var, width=30)
        self.name_entry.pack(pady=5)

        Label(self.addplan_window, text="출발 날짜").pack(pady=5)
        self.start_date_entry = DateEntry(self.addplan_window, width=30, background='darkblue', foreground='white',
                                          borderwidth=2, date_pattern='yyyy/mm/dd')
        self.start_date_entry.pack(pady=5)
        self.start_date_entry.bind("<<DateEntrySelected>>", self.update_end_date)

        Label(self.addplan_window, text="도착 날짜").pack(pady=5)
        self.end_date_entry = DateEntry(self.addplan_window, width=30, background='darkblue', foreground='white',
                                        borderwidth=2, date_pattern='yyyy/mm/dd')
        self.end_date_entry.pack(pady=5)

        if plan_type == "international":
            Label(self.addplan_window, text="여행 국가").pack(pady=5)
            self.country_entry = Entry(self.addplan_window, width=25)
            self.country_entry.pack(pady=5)
            addbutton = Button(self.addplan_window, text="추가", command=self.addlistbox)
            addbutton.place(x=293, y=217)

            countries_frame = Frame(self.addplan_window)
            countries_frame.pack(pady=5)
            self.countries_listbox = Listbox(countries_frame, height=5, selectmode=SINGLE)
            self.countries_listbox.pack(side=LEFT, fill=BOTH, expand=True)

            scrollbar = Scrollbar(countries_frame)
            scrollbar.pack(side=RIGHT, fill=Y)

            self.countries_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.countries_listbox.yview)

            delbutton = Button(self.addplan_window, text="삭제", command=self.deletelistbox)
            delbutton.place(x=335, y=217)

        else:
            self.country_entry = "국내"

        Button(self.addplan_window, text="추가", command=self.add_plan_from_dialog).pack(pady=10)

    def update_end_date(self, event):
        start_date = self.start_date_entry.get_date()
        self.end_date_entry.config(mindate=start_date)

    def add_plan_from_dialog(self):
        plan_name = self.name_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if self.plan_type == "international":
            plan_country = self.countries_listbox.size()
            if not plan_name or not start_date or not end_date or plan_country == 0:
                messagebox.showwarning("경고", "모든 필드를 입력하세요.")
                return
            countries = self.countries_listbox.get(0, self.countries_listbox.size())
            data = {'planname': plan_name, 'startdate': str(start_date), 'enddate': str(end_date),
                    'plancountry': ', '.join(countries), 'schedule': '', 'checklist1': '', 'checklist2': '', 'cost': '',
                    'memo': ''}
        else:
            if not plan_name or not start_date or not end_date:
                messagebox.showwarning("경고", "모든 필드를 입력하세요.")
                return
            data = {'planname': plan_name, 'startdate': str(start_date), 'enddate': str(end_date),
                    'plancountry': '국내', 'schedule': '', 'checklist1': '', 'checklist2': '', 'cost': '', 'memo': ''}

        self.save_plan_to_xml(data)
        plan_date = f"{start_date} ~ {end_date}"
        self.addplanbutton(plan_name, plan_date, data['plancountry'])
        self.addplan_window.destroy()

    def addplanbutton(self, name, date, country):
        plan_index = len(self.plans_frame.grid_slaves(row=0))

        if plan_index >= 5:
            messagebox.showwarning("경고", "최대 5개의 플랜만 생성할 수 있습니다.")
            return

        plan_frame = Frame(self.plans_frame, bg="steel blue", padx=10, pady=10, width=150, height=150)
        plan_frame.grid(row=0, column=plan_index, padx=5, pady=5)
        plan_frame.grid_propagate(False)

<<<<<<< HEAD
=======

>>>>>>> bbaf0f0e19f491d2b4ae56293e6d609df2a4ccde
        plan_button = Button(plan_frame, text=f"{name}\n{date}\n방문 지역: {country}", width=20, height=7,
                             command=lambda: self.show_plan_details(name, date, country))
        plan_button.pack(fill='both', expand=True)

<<<<<<< HEAD
=======

>>>>>>> bbaf0f0e19f491d2b4ae56293e6d609df2a4ccde
        edit_button = Button(plan_frame, text="✎", command=lambda: self.edit_plan(name, date, country, plan_button))
        edit_button.pack(side="left")

        if country != '국내':
<<<<<<< HEAD
            show_button = Button(plan_frame, text="🔎", command=lambda: self.show_country_info(country))
            show_button.pack(side="left")

=======

            show_button = Button(plan_frame, text="🔎", command=lambda: self.show_country_info(country))
            show_button.pack(side="left")


>>>>>>> bbaf0f0e19f491d2b4ae56293e6d609df2a4ccde
        delete_button = Button(plan_frame, text="🗑", command=lambda: self.delete_plan(plan_frame, name))
        delete_button.pack(side="right")

    def addlistbox(self):
        country = self.country_entry.get().strip()
        if country:
            self.countries_listbox.insert(END, country)
        self.country_entry.delete(0, len(self.country_entry.get()))

    def deletelistbox(self):
        selected_indices = self.countries_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("경고", "삭제할 항목을 선택하세요.")
            return
        for index in reversed(selected_indices):
            self.countries_listbox.delete(index)

    def limit_size(self, *args):
        value = self.name_var.get()
        if len(value) > 12:
            self.name_var.set(value[:12])

    def edit_plan(self, name, date, country, plan_button):
        edit_window = Toplevel(self.window)
        edit_window.title("계획 수정")
        edit_window.geometry("400x450")

        Label(edit_window, text="여행 이름(최대 12글자)").pack(pady=5)
        name_var = StringVar(value=name)
        name_var.trace('w', lambda *args: self.limit_size_edit(name_var))
        name_entry = Entry(edit_window, textvariable=name_var, width=30)
        name_entry.pack(pady=5)

        Label(edit_window, text="출발 날짜").pack(pady=5)
        start_date_entry = DateEntry(edit_window, width=30, background='darkblue', foreground='white',
                                     borderwidth=2, date_pattern='yyyy/mm/dd')
        start_date_entry.set_date(date.split(' ~ ')[0])
        start_date_entry.pack(pady=5)
        start_date_entry.bind("<<DateEntrySelected>>", lambda event: self.update_end_date_edit(event, end_date_entry))

        Label(edit_window, text="도착 날짜").pack(pady=5)
        end_date_entry = DateEntry(edit_window, width=30, background='darkblue', foreground='white',
                                   borderwidth=2, date_pattern='yyyy/mm/dd')
        end_date_entry.set_date(date.split(' ~ ')[1])
        end_date_entry.pack(pady=5)
        end_date_entry.config(mindate=start_date_entry.get_date())

        if country == '국내':
            Label(edit_window, text="여행 국가: 국내").pack(pady=5)
        else:
            Label(edit_window, text="여행 국가").pack(pady=5)
            country_entry = Entry(edit_window, width=25)
            country_entry.pack(pady=5)
            addbutton = Button(edit_window, text="추가",
                               command=lambda: self.addlistbox_edit(countries_listbox, country_entry))
            addbutton.place(x=293, y=217)

            countries_frame = Frame(edit_window)
            countries_frame.pack(pady=5)
            countries_listbox = Listbox(countries_frame, height=5, selectmode=SINGLE)
            countries_listbox.pack(side=LEFT, fill=BOTH, expand=True)

            scrollbar = Scrollbar(countries_frame)
            scrollbar.pack(side=RIGHT, fill=Y)

            countries_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=countries_listbox.yview)

            for item in country.split(', '):
                countries_listbox.insert(END, item)

            delbutton = Button(edit_window, text="삭제", command=lambda: self.deletelistbox_edit(countries_listbox))
            delbutton.place(x=335, y=217)

        def save_changes():
            new_name = name_entry.get()
            new_start_date = start_date_entry.get()
            new_end_date = end_date_entry.get()
            if country == '국내':
                new_country = '국내'
            else:
                new_country = ', '.join(countries_listbox.get(0, END))

            if not new_name or not new_start_date or not new_end_date or (new_country != '국내' and not new_country):
                messagebox.showwarning("경고", "모든 필드를 입력하세요.")
                return

            self.update_plan_in_xml(name, new_name, new_start_date, new_end_date, new_country)

            plan_date = f"{new_start_date} ~ {new_end_date}"
            plan_button.config(text=f"{new_name}\n{plan_date}\n방문 국가: {new_country}")

            edit_window.destroy()

        Button(edit_window, text="저장", command=save_changes).pack(pady=10)

    def update_end_date_edit(self, event, end_date_entry):
        start_date = event.widget.get_date()
        end_date_entry.config(mindate=start_date)

    def addlistbox_edit(self, countries_listbox, country_entry):
        country = country_entry.get().strip()
        if country:
            countries_listbox.insert(END, country)
        country_entry.delete(0, len(country_entry.get()))

    def deletelistbox_edit(self, countries_listbox):
        selected_indices = countries_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("경고", "삭제할 항목을 선택하세요.")
            return
        for index in selected_indices[::-1]:
            countries_listbox.delete(index)

    def limit_size_edit(self, name_var):
        value = name_var.get()
        if len(value) > 12:
            name_var.set(value[:12])

    def show_country_info(self, country):
        countries = country.split(', ')
        info_text = ""
        for country_name in countries:
            info_text += self.get_country_info(country_name) + "\n\n"

        self.show_info_window(info_text)

    def get_country_info(self, country_name):
        api_key = "iM%2B5OYQQSMdcWfhPLplO76%2FH6N49AujG%2FmmOXOanS9NnbU12XeWhcMlNILeAwsn4g9%2FdVBe7ppJECUDKiGGaIw%3D%3D"
        encoded_country_name = quote(country_name)
        iso_code = get_iso_code(country_name)
        url = f"http://apis.data.go.kr/1262000/CountryBasicService/getCountryBasicList?serviceKey={api_key}&countryName={encoded_country_name}&numOfRows=1&pageNo=1&resultType=xml"
        url_warning = f"http://apis.data.go.kr/1262000/TravelWarningService/getTravelWarningList?serviceKey={api_key}&isoCode1={iso_code}&numOfRows=1&pageNo=1&resultType=xml"
        url_ban = f"http://apis.data.go.kr/1262000/TravelBanService/getTravelBanList?serviceKey={api_key}&isoCode1={iso_code}&numOfRows=1&pageNo=1&resultType=xml"

        try:
            response = requests.get(url)
            response_warning = requests.get(url_warning)
            response_ban = requests.get(url_ban)

            if response.status_code == 200 and response_warning.status_code == 200 and response_ban.status_code == 200:
                response.encoding = 'utf-8'
                tree = ET.ElementTree(ET.fromstring(response.content))
                tree_warning = ET.ElementTree(ET.fromstring(response_warning.content))
                tree_ban = ET.ElementTree(ET.fromstring(response_ban.content))
                root = tree.getroot()
                root_warning = tree_warning.getroot()
                root_ban = tree_ban.getroot()

                item = root.find('.//item')
                warning_item = root_warning.find('.//item')
                ban_item = root_ban.find('.//item')

                if item is not None:
                    country_name = item.find('countryName').text if item.find('countryName') is not None else "N/A"
                    basic = self.clean_html(item.find('basic').text if item.find('basic') is not None else "N/A")

                    warning_info = ""
                    if warning_item is not None:
                        control_note = self.clean_html(warning_item.find('controlNote').text if warning_item.find('controlNote') is not None else "N/A")
                        limita_note = self.clean_html(warning_item.find('limitaNote').text if warning_item.find('limitaNote') is not None else "N/A")
                        warning_info = f"\n여행 자제: {control_note}\n\n출국 권고: {limita_note}"

                    ban_info = ""
                    if ban_item is not None and ban_item.find('countryName').text == country_name:
                        ban_note = self.clean_html(ban_item.find('banNote').text if ban_item.find('banNote') is not None else "N/A")
                        ban_info = f"\n여행 금지: {ban_note}"
                    else:
                        ban_info = "\n여행 금지: N/A"

                    info = f"국가: {country_name}\n{basic}\n{warning_info}\n{ban_info}"

                    return info
                else:
                    return "국가 정보를 찾을 수 없습니다."
            else:
                error_msg = f"오류가 발생했습니다. 상태 코드: {response.status_code}, {response_warning.status_code}, {response_ban.status_code}\n상세 오류: {response.text}, {response_warning.text}, {response_ban.text}"
                return error_msg

        except Exception as e:
            print(f"Exception: {e}")  # 예외 출력
            error_msg = f"요청 중 오류가 발생했습니다: {e}"
            return error_msg

    def save_plan_to_xml(self, plan):
        try:
            tree = ET.parse('plans.xml')
            root = tree.getroot()
        except (ET.ParseError, FileNotFoundError):
            root = ET.Element("plans")
            tree = ET.ElementTree(root)

        plan_element = ET.Element("plan")
        for key, value in plan.items():
            child = ET.Element(key)
            child.text = value
            plan_element.append(child)

        root.append(plan_element)
        self.prettify_xml(tree, 'plans.xml')

    def update_plan_in_xml(self, old_name, new_name, start_date, end_date, country):
        tree = ET.parse('plans.xml')
        root = tree.getroot()

        for plan in root.findall('plan'):
            if plan.find('planname').text == old_name:
                plan.find('planname').text = new_name
                plan.find('startdate').text = start_date
                plan.find('enddate').text = end_date
                plan.find('plancountry').text = country
                if plan.find('schedule') is None:
                    ET.SubElement(plan, 'schedule')
                if plan.find('checklist1') is None:
                    ET.SubElement(plan, 'checklist1')
                if plan.find('checklist2') is None:
                    ET.SubElement(plan, 'checklist2')
                if plan.find('cost') is None:
                    ET.SubElement(plan, 'cost')
                if plan.find('memo') is None:
                    ET.SubElement(plan, 'memo')
                break

        self.prettify_xml(tree, 'plans.xml')

    def delete_plan(self, plan_frame, name):
        if messagebox.askyesno("삭제 확인", "정말로 이 계획을 삭제하시겠습니까?"):
            plan_frame.destroy()
            self.delete_plan_from_xml(name)

    def delete_plan_from_xml(self, name):
        tree = ET.parse('plans.xml')
        root = tree.getroot()

        for plan in root.findall('plan'):
            if plan.find('planname').text == name:
                root.remove(plan)
                break

        self.prettify_xml(tree, 'plans.xml')

    def load_plans(self):
        try:
            tree = ET.parse('plans.xml')
            root = tree.getroot()
            for plan in root.findall('plan'):
                name = plan.find('planname').text
                start_date = plan.find('startdate').text
                end_date = plan.find('enddate').text
                country = plan.find('plancountry').text
                plan_date = f"{start_date} ~ {end_date}"
                self.addplanbutton(name, plan_date, country)
        except (ET.ParseError, FileNotFoundError):
            pass

    def prettify_xml(self, tree, filename):
        rough_string = ET.tostring(tree.getroot(), 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_str = reparsed.toprettyxml(indent="  ")

        pretty_str = "\n".join([line for line in pretty_str.split("\n") if line.strip()])

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(pretty_str)

    def show_plan_details(self, name, date, country):
        tree = ET.parse('plans.xml')
        root = tree.getroot()
        checklist1 = checklist2 = schedule = cost = memo = ""
        for plan in root.findall('plan'):
            if plan.find('planname').text == name:
                checklist1 = plan.find('checklist1').text if plan.find('checklist1') is not None else ""
                checklist2 = plan.find('checklist2').text if plan.find('checklist2') is not None else ""
                schedule = plan.find('schedule').text if plan.find('schedule') is not None else ""
                cost = plan.find('cost').text if plan.find('cost') is not None else ""
                memo = plan.find('memo').text if plan.find('memo') is not None else ""
                break

<<<<<<< HEAD
        self.window.withdraw()
        PlanGUI(self.window, name, date, country, checklist1, checklist2, schedule, cost, memo)

=======

        self.window.withdraw()
        PlanGUI(self.window, name, date, country, checklist1, checklist2, schedule, cost, memo)


>>>>>>> bbaf0f0e19f491d2b4ae56293e6d609df2a4ccde
MainGUI()
