"""
Модуль стилей интерфейса (QSS - Qt Style Sheets).
Содержит глобальные палитры цветов, правила оформления виджетов,
кнопок, таблиц и диалоговых окон в современном корпоративном стиле.
"""

# Палитра цветов (Светлая тема)
COLOR_BACKGROUND = "#f8fafc"
COLOR_PRIMARY = "#2563eb"
COLOR_PRIMARY_HOVER = "#1d4ed8"
COLOR_PRIMARY_PRESSED = "#1e40af"
COLOR_TEXT_MAIN = "#1e293b"
COLOR_TEXT_MUTED = "#64748b"
COLOR_BORDER = "#cbd5e1"
COLOR_CARD_BG = "#ffffff"
COLOR_ROW_ALT = "#f1f5f9"
COLOR_DANGER = "#ef4444"
COLOR_DANGER_HOVER = "#dc2626"


def get_application_stylesheet():
    """
    Возвращает полную таблицу стилей (QSS) для кастомизации интерфейса приложения.
    """
    return f"""
        /* Общий стиль главного окна */
        QMainWindow {{
            background-color: {COLOR_BACKGROUND};
            color: {COLOR_TEXT_MAIN};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
        }}

        /* Диалоговые окна */
        QDialog {{
            background-color: {COLOR_BACKGROUND};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}

        /* Кнопки управления */
        QPushButton {{
            background-color: {COLOR_PRIMARY};
            color: white;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            border: none;
        }}

        QPushButton:hover {{
            background-color: {COLOR_PRIMARY_HOVER};
        }}

        QPushButton:pressed {{
            background-color: {COLOR_PRIMARY_PRESSED};
        }}

        /* Кнопка удаления / деструктивные действия */
        QPushButton#deleteBtn {{
            background-color: {COLOR_DANGER};
        }}

        QPushButton#deleteBtn:hover {{
            background-color: {COLOR_DANGER_HOVER};
        }}

        /* Поля ввода и списки */
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
            background-color: {COLOR_CARD_BG};
            border: 1px solid {COLOR_BORDER};
            border-radius: 6px;
            padding: 6px 10px;
            color: {COLOR_TEXT_MAIN};
            selection-background-color: {COLOR_PRIMARY};
        }}

        QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
            border: 2px solid {COLOR_PRIMARY};
        }}

        /* Выпадающие списки */
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px;
            border-left-width: 0px;
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
        }}

        /* Таблицы */
        QTableWidget {{
            background-color: {COLOR_CARD_BG};
            gridline-color: #e2e8f0;
            border: 1px solid {COLOR_BORDER};
            border-radius: 8px;
            selection-background-color: #dbeafe;
            selection-color: {COLOR_TEXT_MAIN};
            alternate-background-color: {COLOR_ROW_ALT};
        }}

        /* Шапка таблицы */
        QHeaderView::section {{
            background-color: #e2e8f0;
            color: {COLOR_TEXT_MAIN};
            padding: 8px;
            font-weight: bold;
            border: none;
            border-right: 1px solid {COLOR_BORDER};
            border-bottom: 2px solid {COLOR_BORDER};
        }}

        /* Метки и текст */
        QLabel {{
            color: {COLOR_TEXT_MAIN};
            font-size: 13px;
        }}

        QLabel#totalLabel {{
            font-size: 16px;
            font-weight: bold;
            color: {COLOR_PRIMARY};
        }}
    """