from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter import ttk
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm
from tkintermapview import TkinterMapView
import googlemaps
from datetime import datetime
import webbrowser
from functools import partial
import spam
import mimetypes
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Google Maps API 키 설정
API_KEY = 'AIzaSyD_klTk0Y3yyjkBzijIiO1-VPER1_Ao3tM'
gmaps = googlemaps.Client(key=API_KEY)

class PlanGUI:
    def __init__(self, main_window, plan_name, plan_date, plan_country, checklist1, checklist2, schedule, cost, memo):
        self.main_window = main_window
        self.window = Toplevel(main_window)
        self.window.title(f"{plan_name} / {plan_date} / {plan_country}")
        self.window.geometry("1120x680")

        self.plan_name = plan_name  # 계획 이름을 XML에서 참조하기 위해 저장

        self.schedule_frame = Frame(self.window, width=350, height=600, bg='grey')
        self.schedule_frame.place(x=20, y=60)
        self.schedule_frame.pack_propagate(False)

        self.notebook = ttk.Notebook(self.schedule_frame)
        self.notebook.pack(expand=1, fill='both')

        self.day_count = 0
        self.days = []

        self.schedule_button = Frame(self.window, bg='grey', height=30)
        self.schedule_button.place(x=20, y=20, width=350, height=30)

        self.schedule_add = Button(self.schedule_button, text='생성', command=self.add_day_schedule, width=10)
        self.schedule_add.pack(side='left', padx=5, pady=5)
        self.schedule_del = Button(self.schedule_button, text='삭제', command=self.del_day_schedule, width=10)
        self.schedule_del.pack(side='right', padx=5, pady=5)

        self.main = Frame(self.window, width=600, height=640, bg='grey')
        self.main.place(x=400, y=20)
        self.button_list = Frame(self.window, width=150, height=600)
        self.button_list.place(x=1030, y=20)

        self.memo = None
        self.checklist1_items = checklist1.split(',') if checklist1 else []
        self.checklist2_items = checklist2.split(',') if checklist2 else []
        self.cost_items = cost.split(',') if cost else []

        map_button = Button(self.button_list, text="지도", command=self.open_map, width=8, height=4)
        map_button.pack(padx=5, pady=5)

        check_list_button = Button(self.button_list, text="준비물", command=self.open_check_list, width=8, height=4)
        check_list_button.pack(padx=5, pady=5)

        memo_button = Button(self.button_list, text="메모장", command=self.open_memo, width=8, height=4)
        memo_button.pack(padx=5, pady=5)

        cost_button = Button(self.button_list, text="경비", command=self.open_cost, width=8, height=4)
        cost_button.pack(padx=5, pady=5)

        pi_chart_button = Button(self.button_list, text="차트", command=self.open_pi_chart, width=8, height=4)
        pi_chart_button.pack(padx=5, pady=5)

        gmail_button = Button(self.button_list, text="메일", command=self.entry_mail, width=8, height=4)
        gmail_button.pack(padx=5, pady=5)

        turn_back_button = Button(self.button_list, text="back", command=self.back_to_main, width=8, height=4)
        turn_back_button.pack(padx=5, pady=5)

        self.current_marker = None

        # Load the schedule from the XML file
        self.load_schedule()

    def add_day_schedule(self):
        self.day_count += 1
        day_frame = Frame(self.notebook)
        self.notebook.add(day_frame, text=f'{self.day_count}일차')

        add_place_button = Button(day_frame, text='추가', command=partial(self.add_place, day_frame, self.day_count))
        add_place_button.pack(side='top', padx=5, pady=5)

        self.days.append(day_frame)
        self.save_day_schedule()

    def del_day_schedule(self):
        if self.days:
            last_day = self.days.pop()
            last_day_index = self.notebook.index('end') - 1
            self.notebook.forget(last_day_index)
            self.day_count -= 1
            self.save_day_schedule()

    def save_day_schedule(self):
        tree = ET.parse('plans.xml')
        root = tree.getroot()
        for plan in root.findall('plan'):
            if plan.find('planname').text == self.plan_name:
                schedule = plan.find('schedule')
                if schedule is None:
                    schedule = ET.SubElement(plan, 'schedule')
                else:
                    for child in list(schedule):
                        schedule.remove(child)

                for i in range(1, self.day_count + 1):
                    day = ET.SubElement(schedule, f'day{i}')

                break
        tree.write('plans.xml')

    def load_schedule(self):
        tree = ET.parse('plans.xml')
        root = tree.getroot()
        for plan in root.findall('plan'):
            if plan.find('planname').text == self.plan_name:
                schedule = plan.find('schedule')
                if schedule is not None:
                    for day in schedule:
                        self.day_count += 1
                        day_frame = Frame(self.notebook)
                        self.notebook.add(day_frame, text=f'{self.day_count}일차')

                        add_place_button = Button(day_frame, text='추가',
                                                  command=partial(self.add_place, day_frame, self.day_count))
                        add_place_button.pack(side='top', padx=5, pady=5)

                        prev_place = None
                        for place in day.findall('place'):
                            place_frame = Frame(day_frame, bg='white', bd=2, relief=SOLID)
                            place_frame.pack(fill=X, padx=5, pady=5)

                            place_name = place.get('name')
                            place_label = Label(place_frame, text=place_name, bg='white')
                            place_label.pack(side='left', padx=5, pady=5)

                            lat = place.get('lat')
                            lng = place.get('lng')

                            edit_button = Button(place_frame, text='수정',
                                                 command=partial(self.edit_place, place_frame, self.day_count,
                                                                 place_name, lat, lng))
                            edit_button.pack(side='right', padx=5, pady=5)

                            delete_button = Button(place_frame, text='삭제',
                                                   command=partial(self.delete_place, place_frame, self.day_count,
                                                                   place_name))
                            delete_button.pack(side='right', padx=5, pady=5)

                            if prev_place:
                                route_button = Button(place_frame, text='경로 검색',
                                                      command=partial(self.search_route, prev_place, place_name))
                                route_button.pack(side='right', padx=5, pady=5)

                            prev_place = place_name

                        self.days.append(day_frame)
                break

    def add_place(self, day_frame, day_index):
        if self.current_marker:
            place_name = simpledialog.askstring("목적지 이름", "목적지 이름을 입력하세요:")
            if place_name:
                lat, lng = self.current_marker.position
                self.save_place(day_index, place_name, lat, lng)

                place_frame = Frame(day_frame, bg='white', bd=2, relief=SOLID)
                place_frame.pack(fill=X, padx=5, pady=5)

                place_label = Label(place_frame, text=place_name, bg='white')
                place_label.pack(side='left', padx=5, pady=5)

                edit_button = Button(place_frame, text='수정',
                                     command=partial(self.edit_place, place_frame, day_index, place_name, lat, lng))
                edit_button.pack(side='right', padx=5, pady=5)

                delete_button = Button(place_frame, text='삭제',
                                       command=partial(self.delete_place, place_frame, day_index, place_name))
                delete_button.pack(side='right', padx=5, pady=5)

                prev_place_frame = day_frame.winfo_children()[-2] if len(day_frame.winfo_children()) > 1 else None
                if prev_place_frame and prev_place_frame.winfo_children():
                    prev_place_label = prev_place_frame.winfo_children()[0]
                    prev_place = prev_place_label.cget("text")
                    route_button = Button(place_frame, text='경로 검색',
                                          command=partial(self.search_route, prev_place, place_name))
                    route_button.pack(side='right', padx=5, pady=5)

    def save_place(self, day_index, place_name, lat, lng):
        tree = ET.parse('plans.xml')
        root = tree.getroot()
        for plan in root.findall('plan'):
            if plan.find('planname').text == self.plan_name:
                schedule = plan.find('schedule')
                day = schedule.find(f'day{day_index}')
                place = ET.SubElement(day, 'place', name=place_name)
                place.set('lat', str(lat))
                place.set('lng', str(lng))
                break
        tree.write('plans.xml')

    def search_route(self, origin, destination):
        origin_lat, origin_lng = self.get_lat_lng(origin)
        destination_lat, destination_lng = self.get_lat_lng(destination)
        if origin_lat and origin_lng and destination_lat and destination_lng:
            url = f"https://www.google.com/maps/dir/{origin_lat},{origin_lng}/{destination_lat},{destination_lng}"
            webbrowser.open(url)

    def get_lat_lng(self, place_name):
        tree = ET.parse('plans.xml')
        root = tree.getroot()
        for plan in root.findall('plan'):
            if plan.find('planname').text == self.plan_name:
                for day in plan.find('schedule'):
                    for place in day.findall('place'):
                        if place.get('name') == place_name:
                            return place.get('lat'), place.get('lng')
        return None, None

    def edit_place(self, place_frame, day_index, old_place_name, old_lat, old_lng):
        new_place_name = simpledialog.askstring("목적지 이름", "새로운 목적지 이름을 입력하세요:", initialvalue=old_place_name)
        if new_place_name:
            self.update_place(day_index, old_place_name, new_place_name, old_lat, old_lng)
            place_frame.children['!label'].config(text=new_place_name)
            for button in place_frame.children.values():
                button.config(
                    command=partial(self.edit_place, place_frame, day_index, new_place_name, old_lat, old_lng))

    def update_place(self, day_index, old_place_name, new_place_name, lat, lng):
        tree = ET.parse('plans.xml')
        root = tree.getroot()
        for plan in root.findall('plan'):
            if plan.find('planname').text == self.plan_name:
                schedule = plan.find('schedule')
                day = schedule.find(f'day{day_index}')
                for place in day.findall('place'):
                    if place.get('name') == old_place_name:
                        place.set('name', new_place_name)
                        break
        tree.write('plans.xml')

    def delete_place(self, place_frame, day_index, place_name):
        tree = ET.parse('plans.xml')
        root = tree.getroot()
        for plan in root.findall('plan'):
            if plan.find('planname').text == self.plan_name:
                schedule = plan.find('schedule')
                day = schedule.find(f'day{day_index}')
                for place in day.findall('place'):
                    if place.get('name') == place_name:
                        day.remove(place)
                        break
        tree.write('plans.xml')
        place_frame.destroy()

    def open_memo(self):
        self.clear_main_frame()
        self.memo_frame = Frame(self.main, bg='white', bd=2, relief=SUNKEN)
        self.memo_frame.place(x=0, y=0, width=600, height=640)

        self.memo_text = Text(self.memo_frame, wrap='word')
        self.memo_text.pack(expand=True, fill='both')

        self.load_memo()

        save_button = Button(self.memo_frame, text="저장", command=self.save_memo)
        save_button.pack()

    def clear_main_frame(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def load_memo(self):
        tree = ET.parse('plans.xml')
        root = tree.getroot()
        for plan in root.findall('plan'):
            if plan.find('planname').text == self.plan_name:
                memo = plan.find('memo').text
                if memo:
                    self.memo_text.insert(1.0, memo)
                break

    def save_memo(self):
        memo_content = self.memo_text.get(1.0, END)
        tree = ET.parse('plans.xml')
        root = tree.getroot()
        for plan in root.findall('plan'):
            if plan.find('planname').text == self.plan_name:
                plan.find('memo').text = memo_content
                break
        tree.write('plans.xml')

    def open_check_list(self):
        self.clear_main_frame()
        self.checklist_frame = Frame(self.main, bg='white', bd=2, relief=SUNKEN)
        self.checklist_frame.place(x=0, y=0, width=600, height=640)

        checklist1_label = Label(self.checklist_frame, text="준비해야할 것")
        checklist1_label.pack()
        self.checklist1_listbox = Listbox(self.checklist_frame, selectmode=SINGLE)
        self.checklist1_listbox.pack(fill=BOTH, expand=True)

        checklist2_label = Label(self.checklist_frame, text="준비 완료된 것")
        checklist2_label.pack()
        self.checklist2_listbox = Listbox(self.checklist_frame, selectmode=SINGLE)
        self.checklist2_listbox.pack(fill=BOTH, expand=True)

        self.load_checklist()

        entry_frame = Frame(self.checklist_frame)
        entry_frame.pack(fill='x')

        self.checklist_entry = Entry(entry_frame)
        self.checklist_entry.pack(side='left', expand=True, fill='x')

        add_button = Button(entry_frame, text="추가", command=self.add_checklist_item)
        add_button.pack(side='right')

        move_button = Button(self.checklist_frame, text="이동", command=self.move_item)
        move_button.pack(side='left', padx=10, pady=10)

        delete_button = Button(self.checklist_frame, text="삭제", command=self.delete_item)
        delete_button.pack(side='left', padx=10, pady=10)

        save_button = Button(self.checklist_frame, text="저장", command=self.save_checklist)
        save_button.pack(side='bottom', pady=10)

    def load_checklist(self):
        self.checklist1_listbox.delete(0, END)
        self.checklist2_listbox.delete(0, END)

        tree = ET.parse('plans.xml')
        root = tree.getroot()
        for plan in root.findall('plan'):
            if plan.find('planname').text == self.plan_name:
                checklist1 = plan.find('checklist1').text
                checklist2 = plan.find('checklist2').text
                if checklist1:
                    for item in checklist1.split(','):
                        self.checklist1_listbox.insert(END, item)
                if checklist2:
                    for item in checklist2.split(','):
                        self.checklist2_listbox.insert(END, item)
                break

    def add_checklist_item(self):
        item = self.checklist_entry.get()
        if item:
            self.checklist1_listbox.insert(END, item)
            self.checklist_entry.delete(0, END)

    def move_item(self):
        if self.checklist1_listbox.curselection():
            from_listbox, to_listbox = self.checklist1_listbox, self.checklist2_listbox
        elif self.checklist2_listbox.curselection():
            from_listbox, to_listbox = self.checklist2_listbox, self.checklist1_listbox
        else:
            messagebox.showwarning("경고", "이동할 항목을 선택하세요.")
            return

        selected_index = from_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("경고", "이동할 항목을 선택하세요.")
            return

        selected_item = from_listbox.get(selected_index)
        from_listbox.delete(selected_index)
        to_listbox.insert(END, selected_item)

    def delete_item(self):
        if self.checklist1_listbox.curselection():
            listbox = self.checklist1_listbox
        elif self.checklist2_listbox.curselection():
            listbox = self.checklist2_listbox
        else:
            messagebox.showwarning("경고", "삭제할 항목을 선택하세요.")
            return

        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showwarning("경고", "삭제할 항목을 선택하세요.")
            return

        listbox.delete(selected_index)

    def save_checklist(self):
        checklist1_items = [self.checklist1_listbox.get(idx) for idx in range(self.checklist1_listbox.size())]
        checklist2_items = [self.checklist2_listbox.get(idx) for idx in range(self.checklist2_listbox.size())]

        tree = ET.parse('plans.xml')
        root = tree.getroot()
        for plan in root.findall('plan'):
            if plan.find('planname').text == self.plan_name:
                plan.find('checklist1').text = ','.join(checklist1_items)
                plan.find('checklist2').text = ','.join(checklist2_items)
                break
        tree.write('plans.xml')

    def open_pi_chart(self):
        self.clear_main_frame()
        fig, ax = plt.subplots(figsize=(7, 7))  # figsize를 사용하여 크기 조정

        # 한글 폰트 설정
        font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows에서의 폰트 경로 (예시)
        font_name = fm.FontProperties(fname=font_path).get_name()
        plt.rc('font', family=font_name)

        costs = self.get_cost_data()
        categories = list(costs.keys())
        values = list(costs.values())

        ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        plt.title('Travel Costs')

        canvas = FigureCanvasTkAgg(fig, master=self.main)
        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=0, width=600, height=640)  # place를 사용하여 크기 고정

    def get_cost_data(self):
        costs = {}
        tree = ET.parse('plans.xml')
        root = tree.getroot()
        for plan in root.findall('plan'):
            if plan.find('planname').text == self.plan_name:
                cost_data = plan.find('cost').text
                if cost_data:
                    for item in cost_data.split(','):
                        category, value = item.split(':')
                        costs[category] = float(value)
                break
        return costs

    def open_cost(self):
        self.clear_main_frame()
        self.cost_frame = Frame(self.main, bg='white', bd=2, relief=SUNKEN)
        self.cost_frame.place(x=0, y=0, width=600, height=640)

        cost_label = Label(self.cost_frame, text="경비 내역")
        cost_label.pack()

        self.cost_listbox = Listbox(self.cost_frame, selectmode=SINGLE)
        self.cost_listbox.pack(fill=BOTH, expand=True)

        self.load_cost()

        entry_frame = Frame(self.cost_frame)
        entry_frame.pack(fill='x')

        self.cost_entry = Entry(entry_frame)
        self.cost_entry.pack(side='left', expand=True, fill='x')

        def validate_cost_entry(char):
            return char.isdigit() or char == '.'

        self.cost_value_entry = Entry(entry_frame, validate="key",
                                      validatecommand=(self.window.register(validate_cost_entry), '%S'))
        self.cost_value_entry.pack(side='left', expand=True, fill='x')

        add_button = Button(entry_frame, text="추가", command=self.add_cost_item)
        add_button.pack(side='right')

        button_frame = Frame(self.cost_frame)
        button_frame.pack(side='bottom', pady=10)

        delete_button = Button(button_frame, text="삭제", command=self.delete_cost_item)
        delete_button.pack(side='left', padx=10, pady=10)

        edit_button = Button(button_frame, text="수정", command=self.edit_cost_item)
        edit_button.pack(side='left', padx=10, pady=10)

        save_button = Button(button_frame, text="저장", command=self.save_cost)
        save_button.pack(side='bottom', padx=10, pady=10)

    def load_cost(self):
        self.cost_listbox.delete(0, END)

        tree = ET.parse('plans.xml')
        root = tree.getroot()
        for plan in root.findall('plan'):
            if plan.find('planname').text == self.plan_name:
                cost_data = plan.find('cost').text
                if cost_data:
                    for item in cost_data.split(','):
                        self.cost_listbox.insert(END, item)
                break

    def add_cost_item(self):
        item = self.cost_entry.get()
        value = self.cost_value_entry.get()
        if item and value:
            self.cost_listbox.insert(END, f"{item}:{value}")
            self.cost_entry.delete(0, END)
            self.cost_value_entry.delete(0, END)

    def delete_cost_item(self):
        selected_index = self.cost_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("경고", "삭제할 항목을 선택하세요.")
            return
        self.cost_listbox.delete(selected_index)

    def edit_cost_item(self):
        selected_index = self.cost_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("경고", "수정할 항목을 선택하세요.")
            return
        item = self.cost_listbox.get(selected_index)
        name, value = item.split(':')
        self.cost_entry.delete(0, END)
        self.cost_entry.insert(0, name)
        self.cost_value_entry.delete(0, END)
        self.cost_value_entry.insert(0, value)
        self.cost_listbox.delete(selected_index)

    def save_cost(self):
        cost_items = [self.cost_listbox.get(idx) for idx in range(self.cost_listbox.size())]

        tree = ET.parse('plans.xml')
        root = tree.getroot()
        for plan in root.findall('plan'):
            if plan.find('planname').text == self.plan_name:
                plan.find('cost').text = ','.join(cost_items)
                break
        tree.write('plans.xml')

    def open_map(self):
        self.clear_main_frame()

        search_frame = Frame(self.main, bg='white', bd=2, relief=SUNKEN)
        search_frame.place(x=0, y=0, width=600, height=50)

        self.map_widget = TkinterMapView(self.main, width=600, height=640, corner_radius=0)
        self.map_widget.place(x=0, y=50)

        # OpenStreetMap 타일 서버 설정
        self.map_widget.set_tile_server("https://tile.openstreetmap.org/{z}/{x}/{y}.png", tile_size=256)

        search_entry = Entry(search_frame)
        search_entry.pack(side='left', expand=True, fill='x', padx=5, pady=5)

        search_button = Button(search_frame, text="검색,마킹", command=lambda: self.search_location(search_entry.get()))
        search_button.pack(side='right', padx=5, pady=5)

        # 기본 위치 설정 (예: 서울)
        self.map_widget.set_position(37.5665, 126.9780)  # 서울의 위도와 경도
        self.map_widget.set_zoom(12)  # 줌 레벨 설정

        # 지도 클릭 이벤트 바인딩
        self.map_widget.bind("<Button-1>", self.on_map_click)

    def search_location(self, location):
        geocode_result = gmaps.geocode(location)
        if geocode_result:
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            self.map_widget.set_position(lat, lng)
            self.add_marker((lat, lng))

    def on_map_click(self, event):
        position = self.map_widget.convert_canvas_coordinates_to_lat_lng(event.x, event.y)
        self.add_marker(position)

    def add_marker(self, position):
        if self.current_marker:
            self.map_widget.delete(self.current_marker)
        self.current_marker = self.map_widget.set_marker(position[0], position[1], text="Marker")

    def read_plan_from_xml(self, plan_name):
        tree = ET.parse('plans.xml')
        root = tree.getroot()
        plan_info = ""
        for plan in root.findall('plan'):
            if plan.find('planname').text == plan_name:
                plan_info += f"여행 이름: {plan.find('planname').text}\n"
                plan_info += f"출발 날짜: {plan.find('startdate').text}\n"
                plan_info += f"도착 날짜: {plan.find('enddate').text}\n"
                plan_info += f"방문 지역: {plan.find('plancountry').text}\n"
                plan_info += "일정:\n"
                for day in plan.find('schedule'):
                    plan_info += f"{day.tag}:\n"
                    for place in day.findall('place'):
                        plan_info += f" - {place.get('name')}\n"
                plan_info += f"준비 해야할 것: {plan.find('checklist1').text}\n"
                plan_info += f"준비 완료된 것: {plan.find('checklist2').text}\n"
                plan_info += f"비용: {plan.find('cost').text}\n"
                plan_info += f"메모: {plan.find('memo').text}\n"
                break
        return plan_info

    def send_gmail(self):
        recipientAddr = self.mail_entry.get()  # 사용자가 입력한 메일 주소를 가져옵니다.
        plan_name = self.plan_name  # 계획 이름을 가져옵니다.
        plan_info = self.read_plan_from_xml(plan_name)

        host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
        port = 587

        senderAddr = "starship8902@gmail.com"  # 보내는 사람 email 주소.

        # 이메일 메시지 생성
        msg = MIMEMultipart("alternative")
        msg['Subject'] = "여행 일정 및 방문국가 정보"
        msg['From'] = senderAddr
        msg['To'] = recipientAddr

        # MIMEText 객체 생성
        plan_part = MIMEText(plan_info, 'plain')

        # 이메일 메시지에 MIMEText 객체 추가
        msg.attach(plan_part)

        # SMTP 서버에 연결 및 이메일 전송
        try:
            server = smtplib.SMTP(host, port)
            server.starttls()
            server.login(senderAddr, spam.get_password())  # Gmail 계정 로그인
            server.sendmail(senderAddr, recipientAddr, msg.as_string())
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def entry_mail(self):
        self.mail_window = Tk()
        self.mail_window.title("메일 주소 입력")
        self.mail_window.geometry("300x200")
        Label(self.mail_window, text="메일 주소를 입력하세요.", font=("Yu Gothic UI Semibold", 14)).pack(pady=20)
        self.mail_entry = Entry(self.mail_window, width=30)
        self.mail_entry.pack()
        send_button = Button(self.mail_window, command=self.send_gmail, text="전송")
        send_button.pack(pady=10)

    def back_to_main(self):
        self.window.destroy()
        self.main_window.deiconify()

