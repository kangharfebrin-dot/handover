# views/common.py
import flet as ft
from state import state

def create_mobile_header(page: ft.Page, on_back=None):
    """
    Membuat header atas dengan gradien biru ke hijau, status bar ponsel,
    tombol kembali, judul 'Hand Over', dan ikon pencarian.
    """
    return ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.Alignment.CENTER_LEFT,
            end=ft.Alignment.CENTER_RIGHT,
            colors=["#38bdf8", "#4ade80", "#86efac"]
        ),
        padding=ft.Padding.only(left=16, right=16, top=8, bottom=10),
        content=ft.Column([
            # Status Bar Ponsel (02:03, wifi, battery)
            ft.Row([
                ft.Text("02:03", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                ft.Row([
                    ft.Icon(ft.Icons.NETWORK_CELL, size=13, color=ft.Colors.BLACK),
                    ft.Icon(ft.Icons.WIFI, size=13, color=ft.Colors.BLACK),
                    ft.Icon(ft.Icons.BATTERY_FULL, size=15, color=ft.Colors.BLACK),
                ], spacing=3)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            # Nav Bar (Kembali, Judul, Cari)
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.BLUE_900,
                    icon_size=22,
                    on_click=on_back,
                    tooltip="Kembali"
                ),
                ft.Text("Hand Over", size=17, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                ft.IconButton(
                    icon=ft.Icons.SEARCH,
                    icon_color=ft.Colors.BLUE_900,
                    icon_size=22,
                    tooltip="Cari"
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], spacing=2)
    )

def create_info_card(page: ft.Page, on_reset=None):
    """
    Card informasi No Polisi MT (bisa diketik bebas & reset), Shift (dropdown interaktif),
    dan Status Alur Checklist.
    """
    def on_no_polisi_change(e):
        state.no_polisi = e.control.value

    def on_shift_change(e):
        state.shift = e.control.value

    # Input No Polisi (Bisa diisi sendiri oleh pengguna)
    no_polisi_input = ft.TextField(
        value=state.no_polisi,
        text_size=12,
        text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
        dense=True,
        border_color="#cbd5e1",
        border_radius=6,
        content_padding=ft.Padding.symmetric(horizontal=10, vertical=6),
        expand=True,
        hint_text="Contoh: R 9356 BM",
        on_change=on_no_polisi_change
    )

    def on_reset_click(e):
        state.no_polisi = "R 9356 BM"
        no_polisi_input.value = "R 9356 BM"
        if on_reset:
            on_reset(e)
        page.update()

    reset_btn = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.REFRESH, size=13, color="#475569"),
            ft.Text("Reset", size=11, color="#475569", weight=ft.FontWeight.W_500)
        ], spacing=4),
        border=ft.Border.all(1, "#cbd5e1"),
        border_radius=6,
        padding=ft.Padding.symmetric(horizontal=8, vertical=6),
        ink=True,
        on_click=on_reset_click
    )

    # Dropdown Shift (Bisa milih sendiri oleh pengguna)
    shift_dropdown = ft.Dropdown(
        value=state.shift,
        options=[
            ft.dropdown.Option("Shift 1 - 04:30 WIB"),
            ft.dropdown.Option("Shift 2 - 12:30 WIB"),
            ft.dropdown.Option("Shift 3 - 20:30 WIB"),
        ],
        dense=True,
        text_size=12,
        border_color="#cbd5e1",
        border_radius=6,
        content_padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        expand=True,
        on_select=on_shift_change
    )

    status_pill = ft.Container(
        content=ft.Row([
            ft.Container(width=7, height=7, border_radius=4, bgcolor="#16a34a"),
            ft.Text("Siap Operasi (Normal)", color="#15803d", size=11, weight=ft.FontWeight.BOLD)
        ], spacing=6),
        bgcolor="#dcfce7",
        border=ft.Border.all(1, "#bbf7d0"),
        border_radius=14,
        padding=ft.Padding.symmetric(horizontal=10, vertical=4)
    )

    return ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#e2e8f0"),
        border_radius=10,
        padding=12,
        content=ft.Column([
            ft.Row([
                ft.Text("No Polisi MT", weight=ft.FontWeight.BOLD, size=12, width=85),
                ft.Text(":", size=12, weight=ft.FontWeight.BOLD),
                no_polisi_input,
                reset_btn
            ], spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row([
                ft.Text("Shift", weight=ft.FontWeight.BOLD, size=12, width=85),
                ft.Text(":", size=12, weight=ft.FontWeight.BOLD),
                shift_dropdown
            ], spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row([
                ft.Text("Status Alur Checklist:", size=11, color="#64748b"),
                status_pill
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], spacing=10)
    )

def create_info_banner():
    """
    Banner biru 'Silakan centang kondisi item di bawah ini:'
    """
    return ft.Container(
        bgcolor="#0d47a1",
        border_radius=6,
        padding=ft.Padding.symmetric(horizontal=12, vertical=8),
        content=ft.Row([
            ft.Icon(ft.Icons.INFO, color=ft.Colors.WHITE, size=16),
            ft.Text("Silakan centang kondisi item di bawah ini:", color=ft.Colors.WHITE, size=11, weight=ft.FontWeight.W_500)
        ], spacing=8)
    )
