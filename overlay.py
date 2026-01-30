import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image

PALETTE_DATA = {
    "1-1": (5, 22, 22), "1-2": (65, 69, 69), "1-3": (128, 130, 130), "1-4": (191, 192, 192), "1-5": (254, 255, 255),
    "5-1": (208, 53, 77), "5-2": (238, 110, 114), "5-3": (166, 38, 61), "5-4": (245, 172, 166), "5-5": (201, 132, 131),
    "5-6": (163, 93, 94), "5-7": (105, 49, 59), "5-8": (230, 213, 212), "5-9": (192, 172, 171), "5-10": (117, 94, 94),
    "6-1": (232, 94, 43), "6-2": (249, 131, 88), "6-3": (171, 66, 38), "6-4": (254, 186, 159), "6-5": (218, 147, 124),
    "6-6": (175, 107, 88), "6-7": (117, 59, 49), "6-8": (232, 213, 208), "6-9": (193, 172, 166), "6-10": (117, 94, 89),
    "7-1": (243, 158, 22), "7-2": (254, 174, 59), "7-3": (177, 110, 22), "7-4": (254, 206, 145), "7-5": (218, 167, 108),
    "7-6": (179, 129, 75), "7-7": (121, 81, 38), "7-8": (245, 227, 206), "7-9": (206, 188, 169), "7-10": (128, 110, 94),
    "8-1": (237, 201, 22), "8-2": (249, 216, 56), "8-3": (179, 148, 22), "8-4": (250, 230, 144), "8-5": (210, 190, 110),
    "8-6": (171, 149, 75), "8-7": (117, 99, 38), "8-8": (238, 230, 198), "8-9": (198, 191, 162), "8-10": (120, 114, 89),
    "9-1": (168, 188, 22), "9-2": (183, 200, 49), "9-3": (117, 134, 22), "9-4": (215, 223, 147), "9-5": (173, 183, 108),
    "9-6": (133, 144, 75), "9-7": (84, 94, 43), "9-8": (229, 233, 198), "9-9": (189, 194, 163), "9-10": (110, 116, 93),
    "10-1": (5, 162, 93), "10-2": (65, 185, 123), "10-3": (5, 116, 70), "10-4": (156, 217, 173), "10-5": (118, 178, 139),
    "10-6": (80, 137, 104), "10-7": (36, 86, 64), "10-8": (196, 224, 203), "10-9": (157, 183, 166), "10-10": (84, 104, 93),
    "11-1": (5, 135, 129), "11-2": (5, 171, 160), "11-3": (5, 104, 102), "11-4": (126, 204, 194), "11-5": (85, 164, 156),
    "11-6": (43, 126, 120), "11-7": (5, 75, 75), "11-8": (191, 224, 217), "11-9": (152, 183, 178), "11-10": (78, 106, 102),
    "12-1": (5, 114, 156), "12-2": (5, 153, 186), "12-3": (5, 88, 120), "12-4": (121, 187, 203), "12-5": (81, 147, 165),
    "12-6": (36, 108, 127), "12-7": (5, 73, 91), "12-8": (198, 221, 226), "12-9": (158, 181, 186), "12-10": (80, 103, 110),
    "13-1": (5, 94, 166), "13-2": (43, 131, 193), "13-3": (5, 70, 130), "13-4": (131, 168, 200), "13-5": (93, 128, 161),
    "13-6": (54, 91, 127), "13-7": (25, 59, 86), "13-8": (194, 204, 213), "13-9": (155, 166, 176), "13-10": (76, 89, 103),
    "14-1": (84, 77, 161), "14-2": (117, 119, 189), "14-3": (62, 56, 126), "14-4": (162, 160, 200), "14-5": (120, 122, 161),
    "14-6": (85, 86, 126), "14-7": (51, 53, 84), "14-8": (200, 203, 213), "14-9": (162, 163, 176), "14-10": (86, 88, 104),
    "15-1": (129, 61, 139), "15-2": (161, 103, 169), "15-3": (96, 43, 107), "15-4": (184, 155, 185), "15-5": (144, 115, 149),
    "15-6": (108, 77, 115), "15-7": (67, 46, 75), "15-8": (208, 200, 209), "15-9": (171, 161, 172), "15-10": (96, 86, 101),
    "16-1": (173, 53, 110), "16-2": (208, 106, 143), "16-3": (134, 38, 88), "16-4": (218, 161, 180), "16-5": (180, 122, 140),
    "16-6": (139, 82, 103), "16-7": (96, 53, 75), "16-8": (227, 213, 217), "16-9": (189, 173, 177), "16-10": (114, 94, 102),
}

CANVAS_SPECS = {
    "16:9 XL (150x84)": (150, 84), "16:9 Big (100x56)": (100, 56), "16:9 Mid (50x28)": (50, 28), "16:9 Small (30x18)": (30, 18),
    "4:3 XL (150x114)": (150, 114), "4:3 Big (100x76)": (100, 76), "4:3 Mid (50x38)": (50, 38), "4:3 Small (30x24)": (30, 24),
    "1:1 XL (150x150)": (150, 150), "1:1 Big (100x100)": (100, 100), "1:1 Mid (50x50)": (50, 50), "1:1 Small (30x30)": (30, 30),
    "3:4 XL (114x150)": (114, 150), "3:4 Big (76x100)": (76, 100), "3:4 Mid (38x50)": (38, 50), "3:4 Small (24x30)": (24, 30),
    "9:16 XL (84x150)": (84, 150), "9:16 Big (56x100)": (56, 100), "9:16 Mid (28x50)": (28, 50), "9:16 Small (18x30)": (18, 30)
}

class OverlayWindow(QWidget):
    def __init__(self, parent_panel):
        super().__init__()
        self.panel = parent_panel
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.original_pil_img = None
        self.is_locked = False
        self.target_color_rgb = None
        self.show_grid = False
        self.grid_color = QColor(255, 255, 255, 180)
        self.dot_w, self.dot_h = 100, 100
        self.pixmap = None
        self.start_pos = None
        self.start_geometry = None
        self.blink_on = True
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.toggle_blink)
        self.blink_timer.start(500)

    def toggle_blink(self):
        if self.target_color_rgb:
            self.blink_on = not self.blink_on
            self.update_display()
        else:
            if not self.blink_on:
                self.blink_on = True
                self.update_display()

    def set_always_on_top(self, stay_on_top):
        flags = Qt.FramelessWindowHint | Qt.Tool
        if stay_on_top: flags |= Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()

    def set_lock(self, lock):
        self.is_locked = lock
        self.setWindowFlag(Qt.WindowTransparentForInput, lock)
        self.show()

    def update_display(self, pil_img=None, color_rgb=None):
        if pil_img: self.original_pil_img = pil_img.convert("RGBA")
        if color_rgb == -1: self.target_color_rgb = None
        elif color_rgb: self.target_color_rgb = color_rgb
            
        if not self.original_pil_img: return

        data = np.array(self.original_pil_img).astype(np.float64)
        
        if self.target_color_rgb:
            r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
            tr, tg, tb = self.target_color_rgb
            mask = (r == tr) & (g == tg) & (b == tb)
            
            if self.blink_on:
                data[mask, 0] = 255 - data[mask, 0]
                data[mask, 1] = 255 - data[mask, 1]
                data[mask, 2] = 255 - data[mask, 2]
                data[mask, 3] = 255 
            else:
                data[mask, 3] = 255 
            
            data[~mask, 0:3] *= 0.1
            data[~mask, 3] = 20

        final_data = data.astype(np.uint8)
        filtered_img = Image.fromarray(final_data)
        
        qimg = QImage(filtered_img.tobytes(), filtered_img.size[0], filtered_img.size[1], QImage.Format_RGBA8888)
        self.pixmap = QPixmap.fromImage(qimg).scaled(self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.pixmap: painter.drawPixmap(0, 0, self.pixmap)
        if self.show_grid and self.original_pil_img:
            painter.setPen(QPen(self.grid_color, 1))
            step_x, step_y = self.width() / self.dot_w, self.height() / self.dot_h
            for x in range(self.dot_w + 1):
                curr_x = int(x * step_x); painter.drawLine(curr_x, 0, curr_x, self.height())
            for y in range(self.dot_h + 1):
                curr_y = int(y * step_y); painter.drawLine(0, curr_y, self.width(), curr_y)

    def mousePressEvent(self, event):
        if not self.is_locked: self.start_pos, self.start_geometry = event.globalPos(), self.geometry()

    def mouseMoveEvent(self, event):
        if self.is_locked or self.start_pos is None: return
        delta = event.globalPos() - self.start_pos
        if self.panel.mode_move.isChecked():
            self.move(self.start_geometry.topLeft() + delta)
        else:
            self.resize(max(30, self.start_geometry.width() + delta.x()), max(30, self.start_geometry.height() + delta.y()))
        self.panel.update_ui_from_overlay(); self.update_display()

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.overlay = OverlayWindow(self)
        self.specs = CANVAS_SPECS
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Art Helper v1.0")
        self.setGeometry(1200, 100, 350, 850)
        layout = QVBoxLayout()

        win_group = QGroupBox("Window Settings")
        win_lay = QVBoxLayout()
        self.chk_ontop = QCheckBox("Always on Top")
        self.chk_ontop.setChecked(True)
        self.chk_ontop.toggled.connect(self.overlay.set_always_on_top)
        win_lay.addWidget(self.chk_ontop)
        
        self.op_slider = QSlider(Qt.Horizontal); self.op_slider.setRange(10, 100); self.op_slider.setValue(70)
        self.op_slider.valueChanged.connect(lambda v: self.overlay.setWindowOpacity(v/100))
        win_lay.addWidget(QLabel("Opacity"))
        win_lay.addWidget(self.op_slider)
        win_group.setLayout(win_lay); layout.addWidget(win_group)

        layout.addWidget(QLabel("▣ Canvas Specification"))
        self.combo = QComboBox(); self.combo.addItems(self.specs.keys()); layout.addWidget(self.combo)
        
        mode_lay = QHBoxLayout()
        self.mode_move = QRadioButton("Move"); self.mode_resize = QRadioButton("Resize")
        self.mode_move.setChecked(True); mode_lay.addWidget(self.mode_move); mode_lay.addWidget(self.mode_resize)
        layout.addLayout(mode_lay)

        grid_lay = QHBoxLayout()
        self.chk_grid = QCheckBox("Show Grid"); self.chk_grid.toggled.connect(lambda c: (setattr(self.overlay, 'show_grid', c), self.overlay.update()))
        self.btn_grid_clr = QPushButton("Grid B/W"); self.btn_grid_clr.clicked.connect(self.switch_grid_color)
        grid_lay.addWidget(self.chk_grid); grid_lay.addWidget(self.btn_grid_clr); layout.addLayout(grid_lay)

        self.btn_load = QPushButton("Load Image (Auto Palette)"); self.btn_load.clicked.connect(self.load_image); layout.addWidget(self.btn_load)
        self.btn_lock = QPushButton("Lock Position"); self.btn_lock.setCheckable(True); self.btn_lock.clicked.connect(self.toggle_lock); layout.addWidget(self.btn_lock)

        layout.addWidget(QLabel("▣ Palette List (Used Colors):"))
        self.color_list = QListWidget(); self.color_list.addItem("View All (Clear Filter)")
        self.color_list.currentRowChanged.connect(self.apply_filter)
        layout.addWidget(self.color_list)

        self.setLayout(layout); self.show()

    def switch_grid_color(self):
        self.overlay.grid_color = QColor(0,0,0,180) if self.overlay.grid_color == QColor(255,255,255,180) else QColor(255,255,255,180)
        self.overlay.update()

    def load_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Select Image', './')
        if fname[0]:
            w_dots, h_dots = self.specs[self.combo.currentText()]
            self.overlay.dot_w, self.overlay.dot_h = w_dots, h_dots
            
            img = Image.open(fname[0]).convert("RGB").resize((w_dots, h_dots), Image.Resampling.NEAREST)
            img_data = np.array(img)
            palette_colors = np.array(list(PALETTE_DATA.values()))
            
            flat_img = img_data.reshape(-1, 3)
            distances = np.sqrt(np.sum((flat_img[:, np.newaxis] - palette_colors) ** 2, axis=2))
            nearest_indices = np.argmin(distances, axis=1)
            
            new_img_data = palette_colors[nearest_indices].reshape(h_dots, w_dots, 3).astype(np.uint8)
            self.pil_img = Image.fromarray(new_img_data)
            
            self.overlay.update_display(self.pil_img)
            self.overlay.show()
            self.refresh_color_list()

    def refresh_color_list(self):
        try: self.color_list.currentRowChanged.disconnect()
        except: pass
            
        self.color_list.clear()
        self.color_list.addItem("View All (Clear Filter)")
        
        pixels = np.array(self.pil_img).reshape(-1, 3)
        unique_colors = {tuple(map(int, c)) for c in np.unique(pixels, axis=0)}
        
        found_keys = []
        for key, rgb in PALETTE_DATA.items():
            if tuple(map(int, rgb)) in unique_colors:
                found_keys.append(key)
        
        found_keys.sort(key=lambda x: [int(p) for p in x.split('-')])

        for key in found_keys:
            item = QListWidgetItem(key)
            pix = QPixmap(18, 18); pix.fill(QColor(*PALETTE_DATA[key]))
            item.setIcon(QIcon(pix))
            self.color_list.addItem(item)
        
        self.color_list.currentRowChanged.connect(self.apply_filter)

    def apply_filter(self, row):
        if row <= 0: self.overlay.update_display(color_rgb=-1)
        else:
            key = self.color_list.item(row).text()
            self.overlay.update_display(color_rgb=PALETTE_DATA[key])

    def toggle_lock(self):
        locked = self.btn_lock.isChecked()
        self.overlay.set_lock(locked)
        self.btn_lock.setText("Unlock" if locked else "Lock Position")

    def update_ui_from_overlay(self): pass

if __name__ == '__main__':
    app = QApplication(sys.argv); ex = ControlPanel(); sys.exit(app.exec_())