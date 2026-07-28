from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import random

# ابعاد شبکه بازی (Grid)
GRID_SIZE = 15

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self.snake = [(5, 5), (4, 5), (3, 5)] # مختصات ابتدایی بدن مار
        self.direction = (1, 0)               # جهت حرکت اولیه (به سمت راست)
        self.food = (10, 10)                  # مختصات اولیه غذا
        self.score = 0
        self.game_over = False
        
        # اجرای حلقه اصلی بازی هر 0.2 ثانیه یک‌بار (سرعت حرکت مار)
        Clock.schedule_interval(self.update, 0.2)

    def generate_food(self):
        """تولید غذا در یک نقطه تصادفی که مار روی آن قرار ندارد"""
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def update(self, dt):
        """حلقه اصلی حرکت و منطق بازی"""
        if self.game_over:
            return

        # محاسبه مختصات سر جدید مار
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # ۱. بررسی برخورد با دیوارها
        if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
            self.game_over = True
            return

        # ۲. بررسی برخورد مار با خودش
        if new_head in self.snake:
            self.game_over = True
            return

        # اضافه کردن سر جدید به ابتدای مار
        self.snake.insert(0, new_head)

        # ۳. بررسی خوردن غذا
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            # به دکمه/لیبل امتیاز آپدیت بده
            if hasattr(self, 'score_label'):
                self.score_label.text = f"Score: {self.score}"
        else:
            # اگر غذا نخورده، دم مار را حذف کن (حرکت عادی)
            self.snake.pop()

        # رسم مجدد گرافیک بازی
        self.draw()

    def draw(self):
        """رسم تمام عناصر روی صفحه"""
        self.canvas.clear()
        cell_size = self.width / GRID_SIZE if self.width > 0 else 20

        with self.canvas:
            # رسم پس‌زمینه زمین بازی (سبز تیره)
            Color(0.1, 0.15, 0.1, 1)
            Rectangle(pos=self.pos, size=self.size)

            # رسم غذا (قرمز)
            Color(0.9, 0.2, 0.2, 1)
            Rectangle(
                pos=(self.x + self.food[0] * cell_size, self.y + self.food[1] * cell_size),
                size=(cell_size - 1, cell_size - 1)
            )

            # رسم مار (سبز روشن برای سر، سبز معمولی برای بدن)
            for i, segment in enumerate(self.snake):
                if i == 0:
                    Color(0.3, 0.9, 0.3, 1) # سر مار
                else:
                    Color(0.2, 0.7, 0.2, 1) # بدن
                Rectangle(
                    pos=(self.x + segment[0] * cell_size, self.y + segment[1] * cell_size),
                    size=(cell_size - 1, cell_size - 1)
                )

            # پیام باخت در صورت پایان بازی
            if self.game_over:
                Color(1, 0, 0, 0.5)
                Rectangle(pos=self.pos, size=self.size)

    def change_direction(self, new_dir):
        """تغییر جهت حرکت (جلوگیری از چرخش ۱۸۰ درجه ناگهانی)"""
        if self.game_over:
            self.reset_game()
            return

        # جلوگیـری از برگشتن روی خود مار (مثلاً وقتی به راست می‌رود نتواند چپ بزند)
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def reset_game(self):
        """شروع مجدد بازی پس از باخت"""
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.food = (10, 10)
        self.score = 0
        self.game_over = False
        if hasattr(self, 'score_label'):
            self.score_label.text = "Score: 0"


class SnakeApp(App):
    def build(self):
        # چیدمان اصلی عمودی
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # زمین بازی
        self.game = SnakeGame(size_hint=(1, 0.6))
        
        # نمایش امتیاز
        self.score_label = Label(text="Score: 0", size_hint=(1, 0.05), font_size='20sp', bold=True)
        self.game.score_label = self.score_label

        # پنل دکمه‌های کنترلی روی صفحه (D-Pad لمسی)
        controls = GridLayout(cols=3, rows=3, size_hint=(1, 0.35), spacing=5)

        # ساخت دکمه‌ها
        btn_up = Button(text="▲", font_size='24sp', on_press=lambda x: self.game.change_direction((0, 1)))
        btn_down = Button(text="▼", font_size='24sp', on_press=lambda x: self.game.change_direction((0, -1)))
        btn_left = Button(text="◀", font_size='24sp', on_press=lambda x: self.game.change_direction((-1, 0)))
        btn_right = Button(text="▶", font_size='24sp', on_press=lambda x: self.game.change_direction((1, 0)))
        btn_restart = Button(text="Reset", font_size='14sp', on_press=lambda x: self.game.reset_game())

        # چیدمان ۹ خانه کنترل لمسی (فلش‌ها به شکل D-Pad)
        controls.add_widget(Widget())       # خالی
        controls.add_widget(btn_up)         # بالا
        controls.add_widget(Widget())       # خالی
        
        controls.add_widget(btn_left)       # چپ
        controls.add_widget(btn_restart)    # ریست
        controls.add_widget(btn_right)      # راست
        
        controls.add_widget(Widget())       # خالی
        controls.add_widget(btn_down)       # پایین
        controls.add_widget(Widget())       # خالی

        # افزودن بخش‌ها به لایه اصلی
        root.add_widget(self.score_label)
        root.add_widget(self.game)
        root.add_widget(controls)

        # به‌روزرسانی ابعاد رسم گرافیک هنگام تغییر سایز صفحه
        self.game.bind(size=lambda x, y: self.game.draw(), pos=lambda x, y: self.game.draw())

        return root


if __name__ == '__main__':
    SnakeApp().run()
