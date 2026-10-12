import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from styles import get_application_stylesheet

from database.db_manager import (
    init_db, get_all_subscriptions, get_all_categories,
    add_subscription, update_subscription, delete_subscription
)

def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсам (работает и для скрипта, и для .exe) """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SubDialog(QDialog):
    """Диалоговое окно для добавления или редактирования подписки (Форма 2)."""
    def __init__(self, parent=None, sub_data=None):
        super().__init__(parent)
        ui_path = resource_path(os.path.join("ui", "dialog_sub.ui"))
        uic.loadUi(ui_path, self)
        
        self.sub_data = sub_data
        self.load_categories()
        
        # Если передан sub_data, значит это режим редактирования — заполняем поля
        if self.sub_data:
            self.setWindowTitle("Редактировать подписку")
            self.nameInput.setText(str(self.sub_data[1]))
            self.priceSpin.setValue(float(self.sub_data[2]))
            self.daySpin.setValue(int(self.sub_data[3]))
            # Выбор нужной категории в ComboBox
            index = self.categoryCombo.findData(self.sub_data[5])
            if index >= 0:
                self.categoryCombo.setCurrentIndex(index)
        else:
            self.setWindowTitle("Добавить подписку")

        self.saveBtn.clicked.connect(self.accept_data)
        self.cancelBtn.clicked.connect(self.reject)

    def load_categories(self):
        """Загружаем категории из БД в выпадающий список."""
        self.categoryCombo.clear()
        categories = get_all_categories()
        for cat_id, cat_name in categories:
            self.categoryCombo.addItem(cat_name, cat_id)

    def accept_data(self):
        name = self.nameInput.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название сервиса!")
            return
        
        price = self.priceSpin.value()
        if price <= 0:
            QMessageBox.warning(self, "Ошибка", "Цена должна быть больше нуля!")
            return
            
        day = self.daySpin.value()
        if not (1 <= day <= 31):
            QMessageBox.warning(self, "Ошибка", "День списания должен быть от 1 до 31!")
            return
            
        category_id = self.categoryCombo.currentData()
        
        if self.sub_data:
            # Редактирование
            update_subscription(self.sub_data[0], category_id, name, price, day)
        else:
            # Добавление
            add_subscription(category_id, name, price, day)
            
        self.accept()


class MainWindow(QMainWindow):
    """Главное окно приложения (Форма 1)."""
    def __init__(self):
        super().__init__()
        ui_path = resource_path(os.path.join("ui", "main_window.ui"))
        uic.loadUi(ui_path, self)

        # Мультимедиа: вывод картинки в logoLabel
        icon_path = resource_path(os.path.join("assets", "icon.png"))
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            self.logoLabel.setPixmap(pixmap.scaled(self.logoLabel.width(), self.logoLabel.height()))
        
        # Инициализация БД
        init_db()
        
        # Настройка таблицы
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Название", "Категория", "Цена (руб.)", "День списания"])
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Загрузка данных
        self.load_data()
        
        # Привязка кнопок
        self.addBtn.clicked.connect(self.open_add_dialog)
        self.editBtn.clicked.connect(self.open_edit_dialog)
        self.deleteBtn.clicked.connect(self.delete_selected)
        
        # Обработка клавиатуры и мыши
        self.searchLineEdit.textChanged.connect(self.load_data)
        self.tableWidget.doubleClicked.connect(self.open_edit_dialog)

    def load_data(self):
        """Загрузка подписок в таблицу с учетом поиска и подсчет суммы."""
        rows = get_all_subscriptions()
        search_text = self.searchLineEdit.text().lower()
        
        self.tableWidget.setRowCount(0)
        total_sum = 0.0
        
        row_idx = 0
        for r in rows:
            sub_id, name, price, billing_day, cat_name, cat_id = r
            
            # Фильтрация по поиску
            if search_text and search_text not in name.lower():
                continue
                
            self.tableWidget.insertRow(row_idx)
            self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(str(name)))
            self.tableWidget.setItem(row_idx, 1, QTableWidgetItem(str(cat_name)))
            self.tableWidget.setItem(row_idx, 2, QTableWidgetItem(f"{price:.2f}"))
            self.tableWidget.setItem(row_idx, 3, QTableWidgetItem(str(billing_day)))
            
            # Сохраняем реальный ID подписки в скрытом поле первой колонки
            self.tableWidget.item(row_idx, 0).setData(Qt.UserRole, sub_id)
            # Также сохраняем полный кортеж для редактирования
            self.tableWidget.item(row_idx, 0).setData(Qt.UserRole + 1, r)
            
            total_sum += price
            row_idx += 1
            
        # Вывод общей суммы трат
        self.totalLabel.setText(f"Итого за месяц: {total_sum:.2f} руб.")

    def open_add_dialog(self):
        dialog = SubDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()

    def open_edit_dialog(self):
        selected_rows = self.tableWidget.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите подписку для редактирования!")
            return
        
        row = selected_rows[0].row()
        sub_data = self.tableWidget.item(row, 0).data(Qt.UserRole + 1)
        
        dialog = SubDialog(self, sub_data)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()

    def delete_selected(self):
        selected_rows = self.tableWidget.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите подписку для удаления!")
            return
            
        row = selected_rows[0].row()
        sub_id = self.tableWidget.item(row, 0).data(Qt.UserRole)
        name = self.tableWidget.item(row, 0).text()
        
        reply = QMessageBox.question(
            self, "Подтверждение", 
            f"Вы уверены, что хотите удалить подписку '{name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            delete_subscription(sub_id)
            self.load_data()

    def keyPressEvent(self, event):
        """Обработка нажатий клавиатуры."""
        if event.key() == Qt.Key_Delete:
            self.delete_selected()
        elif event.key() == Qt.Key_Insert:
            self.open_add_dialog()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Вот эта строчка применяет оформление из styles.py:
    app.setStyleSheet(get_application_stylesheet())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())