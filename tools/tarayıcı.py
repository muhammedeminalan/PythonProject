from __future__ import annotations
import json, os, sys, re
from pathlib import Path
from typing import Optional
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QAction, QIcon, QKeySequence, QPalette, QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QToolBar, QLineEdit,
    QTabWidget, QFileDialog, QMessageBox, QStatusBar, QLabel
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import (
    QWebEngineProfile, QWebEngineDownloadRequest, QWebEnginePage
)


def normalize_url(text: str) -> QUrl:
    t = text.strip()
    if not t:
        return QUrl("https://duckduckgo.com")
    if re.match(r"^[a-zA-Z]+://", t):
        return QUrl(t)
    if re.match(r"^[\w\-\.]+\.[a-zA-Z]{2,}(/.*)?$", t):
        return QUrl(f"https://{t}")
    return QUrl(f"https://duckduckgo.com/?q={QUrl.toPercentEncoding(t).data().decode('utf-8')}")


class BrowserTab(QWidget):
    def __init__(self, url: Optional[str] = None, profile: Optional[QWebEngineProfile] = None, parent=None):
        super().__init__(parent)
        self.view = QWebEngineView(self)
        if profile:
            # Qt6: Özel sayfa ile yeni pencere isteklerini yakala
            page = BrowserPage(parent, profile, self.view)
            self.view.setPage(page)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.view)
        self._home = "https://duckduckgo.com"
        if url:
            self.navigate(url)

    def navigate(self, text: str):
        self.view.setUrl(normalize_url(text))

    def go_home(self):
        self.view.setUrl(QUrl(self._home))

    def set_home(self, url: str):
        self._home = url

    def back(self):
        self.view.back()

    def forward(self):
        self.view.forward()

    def reload(self):
        self.view.reload()

    def stop(self):
        self.view.stop()

    def zoom_in(self):
        self.view.setZoomFactor(self.view.zoomFactor() + 0.1)

    def zoom_out(self):
        self.view.setZoomFactor(self.view.zoomFactor() - 0.1)

    def reset_zoom(self):
        self.view.setZoomFactor(1.0)


class BookmarkBar(QToolBar):
    def __init__(self, store_path: Path, parent=None):
        super().__init__("Yer İmleri", parent)
        self.store_path = store_path
        self.setIconSize(QSize(16, 16))
        self.setMovable(False)
        self._bookmarks = []
        self.load()

    def load(self):
        self._bookmarks = []
        if self.store_path.exists():
            try:
                self._bookmarks = json.loads(self.store_path.read_text(encoding="utf-8"))
            except Exception:
                self._bookmarks = []
        self.refresh()

    def save(self):
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        self.store_path.write_text(json.dumps(self._bookmarks, ensure_ascii=False, indent=2), encoding="utf-8")

    def refresh(self):
        self.clear()
        for bm in self._bookmarks:
            act = QAction(bm.get("title") or bm.get("url"), self)
            act.setToolTip(bm.get("url"))
            act.triggered.connect(lambda _, u=bm.get("url"): self.parent().open_in_current_tab(u))
            self.addAction(act)
        self.addSeparator()
        add_act = QAction("☆ Ekle", self)
        add_act.setToolTip("Geçerli sayfayı yer imlerine ekle")
        add_act.triggered.connect(self.add_current_page)
        self.addAction(add_act)

    def add_current_page(self):
        mw: MainWindow = self.parent()
        if not isinstance(mw, MainWindow):
            return
        view = mw.current_view()
        if not view:
            return
        url = view.url().toString()
        title = view.title() or url
        self._bookmarks.append({"title": title, "url": url})
        self.save()
        self.refresh()


class BrowserPage(QWebEnginePage):
    def __init__(self, main_window: QMainWindow, profile: QWebEngineProfile, parent=None):
        super().__init__(profile, parent)
        self._main_window = main_window

    def createWindow(self, _type):
        # Yeni pencere isteğini yeni sekme olarak aç
        if hasattr(self._main_window, "add_tab"):
            new_tab = self._main_window.add_tab()
            return new_tab.view.page()
        return super().createWindow(_type)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Py Tarayıcı")
        self.resize(1200, 800)
        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.downloadRequested.connect(self.on_download_requested)
        self.tabs = QTabWidget(self)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.setCentralWidget(self.tabs)
        self.nav = QToolBar("Gezinme", self)
        self.nav.setMovable(False)
        self.addToolBar(self.nav)
        self.act_back = QAction("←", self, triggered=self.go_back)
        self.act_forward = QAction("→", self, triggered=self.go_forward)
        self.act_reload = QAction("⟳", self, triggered=self.reload_page)
        self.act_stop = QAction("⨯", self, triggered=self.stop_load)
        self.act_home = QAction("⌂", self, triggered=self.go_home)
        self.act_new_tab = QAction("+", self, triggered=lambda: self.add_tab("https://duckduckgo.com"))
        self.act_close_tab = QAction("×", self, triggered=self.close_current_tab)
        for a in (self.act_back, self.act_forward, self.act_reload, self.act_stop, self.act_home):
            self.nav.addAction(a)
        self.addr = QLineEdit(self)
        self.addr.returnPressed.connect(self.on_address_enter)
        self.addr.setPlaceholderText("URL veya arama...")
        self.nav.addWidget(self.addr)
        self.nav.addAction(self.act_new_tab)
        self.nav.addAction(self.act_close_tab)
        store = Path.home() / ".pybrowser" / "bookmarks.json"
        self.bookmarks = BookmarkBar(store, parent=self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.bookmarks)
        self.status = QStatusBar(self)
        self.setStatusBar(self.status)
        self.progress_lbl = QLabel("")
        self.status.addPermanentWidget(self.progress_lbl)
        self.act_new_tab.setShortcut(QKeySequence("Ctrl+T"))
        self.act_close_tab.setShortcut(QKeySequence("Ctrl+W"))
        self.addr.setClearButtonEnabled(True)
        self.dark_mode = False
        theme_act = QAction("🌓 Tema", self, triggered=self.toggle_theme)
        self.nav.addAction(theme_act)
        self.add_tab("https://duckduckgo.com")

    def current_tab(self) -> Optional[BrowserTab]:
        w = self.tabs.currentWidget()
        return w if isinstance(w, BrowserTab) else None

    def current_view(self) -> Optional[QWebEngineView]:
        tab = self.current_tab()
        return tab.view if tab else None

    def set_tab_title(self, idx: int, title: str):
        self.tabs.setTabText(idx, (title or "Yeni Sekme")[:30])

    def add_tab(self, url: Optional[str] = None) -> BrowserTab:
        tab = BrowserTab(url, profile=self.profile, parent=self)
        idx = self.tabs.addTab(tab, "Yükleniyor...")
        self.tabs.setCurrentIndex(idx)
        v = tab.view
        v.titleChanged.connect(lambda t, i=idx: self.set_tab_title(self.tabs.indexOf(tab), t))
        v.urlChanged.connect(lambda u: self.addr.setText(u.toString()))
        v.loadProgress.connect(lambda p: self.progress_lbl.setText(f"%{p}"))
        v.loadFinished.connect(lambda ok: self.progress_lbl.setText("" if ok else "Yükleme hatası"))
        return tab

    def close_tab(self, index: int):
        if self.tabs.count() == 1:
            self.close()
            return
        self.tabs.removeTab(index)

    def close_current_tab(self):
        idx = self.tabs.currentIndex()
        if idx >= 0:
            self.close_tab(idx)

    def on_address_enter(self):
        text = self.addr.text()
        self.open_in_current_tab(text)

    def open_in_current_tab(self, text: str):
        tab = self.current_tab()
        if tab:
            tab.navigate(text)

    def go_back(self):
        v = self.current_view()
        if v: v.back()

    def go_forward(self):
        v = self.current_view()
        if v: v.forward()

    def reload_page(self):
        v = self.current_view()
        if v: v.reload()

    def stop_load(self):
        v = self.current_view()
        if v: v.stop()

    def go_home(self):
        tab = self.current_tab()
        if tab: tab.go_home()

    def on_tab_changed(self, idx: int):
        v = self.current_view()
        if not v:
            return
        self.addr.setText(v.url().toString())
        self.set_tab_title(idx, v.title())

    def on_download_requested(self, req: QWebEngineDownloadRequest):
        suggested = req.suggestedFileName() or "indirilen_dosya"
        path, _ = QFileDialog.getSaveFileName(self, "Kaydet", str(Path.home() / "Downloads" / suggested))
        if not path:
            req.cancel()
            return
        req.setDownloadFileName(os.path.basename(path))
        req.setDownloadDirectory(os.path.dirname(path))
        req.accept()
        self.status.showMessage(f"İndiriliyor: {os.path.basename(path)}", 5000)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        pal = QPalette()
        if self.dark_mode:
            pal.setColor(QPalette.Window, QColor(30, 30, 30))
            pal.setColor(QPalette.WindowText, Qt.white)
            pal.setColor(QPalette.Base, QColor(20, 20, 20))
            pal.setColor(QPalette.Text, Qt.white)
            pal.setColor(QPalette.Button, QColor(45, 45, 45))
            pal.setColor(QPalette.ButtonText, Qt.white)
            pal.setColor(QPalette.Highlight, QColor(64, 128, 255))
            pal.setColor(QPalette.HighlightedText, Qt.white)
        QApplication.instance().setPalette(pal)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Py Tarayıcı")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
