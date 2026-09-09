# views/step2_evaluation.py
import flet as ft
from state import state
from views.common import create_mobile_header, create_info_card, create_info_banner

def EvaluationView(page: ft.Page):
    
    # Menentukan Default Kategori Evaluasi berdasarkan checklist
    ada_kerusakan = any(not v for v in state.checklist_mt.values()) or any(not v for v in state.checklist_amt.values())
    if ada_kerusakan and state.kategori_evaluasi == "Normal / Sesuai":
        state.kategori_evaluasi = "Minor (Catat)"
    elif not ada_kerusakan and state.kategori_evaluasi not in ["Minor (Catat)", "Mayor (Stop)"]:
        state.kategori_evaluasi = "Normal / Sesuai"

    # Input ODO Awal & Akhir dengan on_change real-time
    odo_awal_field = ft.TextField(
        value=state.odo_awal,
        text_align=ft.TextAlign.LEFT,
        suffix="km",
        text_size=12,
        dense=True,
        border_color="#cbd5e1",
        border_radius=6,
        content_padding=ft.Padding.symmetric(horizontal=10, vertical=8),
        on_change=lambda e: setattr(state, 'odo_awal', e.control.value)
    )

    odo_akhir_field = ft.TextField(
        value=state.odo_akhir,
        text_align=ft.TextAlign.LEFT,
        suffix="km",
        text_size=12,
        dense=True,
        border_color="#cbd5e1",
        border_radius=6,
        content_padding=ft.Padding.symmetric(horizontal=10, vertical=8),
        on_change=lambda e: setattr(state, 'odo_akhir', e.control.value)
    )

    # Catatan input dengan on_change real-time
    catatan_field = ft.TextField(
        value=state.catatan,
        multiline=True,
        min_lines=3,
        max_lines=4,
        text_size=11,
        border_color="#cbd5e1",
        border_radius=6,
        content_padding=10,
        hint_text="Tuliskan catatan temuan di sini...",
        on_change=lambda e: setattr(state, 'catatan', e.control.value)
    )

    # Accordion A & B (Bisa diklik untuk kembali memeriksa checklist)
    async def go_to_step1(e):
        await page.push_route("/")

    card_a = ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#e2e8f0"),
        border_radius=8,
        padding=10,
        ink=True,
        on_click=go_to_step1,
        content=ft.Row([
            ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT, color="#15803d", size=20),
            ft.Text("A. Perlengkapan Mobil Tangki (18 Item)", weight=ft.FontWeight.BOLD, color="#15803d", size=12, expand=True),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK, size=12, color="#15803d"),
                    ft.Text("18/18 Siap", size=10, weight=ft.FontWeight.BOLD, color="#15803d")
                ], spacing=3),
                bgcolor="#dcfce7",
                border=ft.Border.all(1, "#bbf7d0"),
                border_radius=12,
                padding=ft.Padding.symmetric(horizontal=8, vertical=4)
            )
        ], spacing=6)
    )

    card_b = ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#e2e8f0"),
        border_radius=8,
        padding=10,
        ink=True,
        on_click=go_to_step1,
        content=ft.Row([
            ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT, color="#15803d", size=20),
            ft.Text("B. Perlengkapan AMT (10 Item)", weight=ft.FontWeight.BOLD, color="#15803d", size=12, expand=True),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK, size=12, color="#15803d"),
                    ft.Text("10/10 Siap", size=10, weight=ft.FontWeight.BOLD, color="#15803d")
                ], spacing=3),
                bgcolor="#dcfce7",
                border=ft.Border.all(1, "#bbf7d0"),
                border_radius=12,
                padding=ft.Padding.symmetric(horizontal=8, vertical=4)
            )
        ], spacing=6)
    )

    # 3 Kartu Kategori Evaluasi: Normal, Minor, Mayor
    def select_kategori(val):
        state.kategori_evaluasi = val
        update_kategori_ui()
        page.update()

    def make_kategori_card(title, subtitle, val, active_color, sub_color):
        is_sel = (state.kategori_evaluasi == val)
        if is_sel:
            radio_icon = ft.Container(
                width=16, height=16, border_radius=8,
                bgcolor=ft.Colors.WHITE,
                border=ft.Border.all(5, active_color)
            )
        else:
            radio_icon = ft.Container(
                width=16, height=16, border_radius=8,
                border=ft.Border.all(1.5, "#94a3b8")
            )

        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(2 if is_sel else 1, active_color if is_sel else "#cbd5e1"),
            border_radius=8,
            padding=ft.Padding.symmetric(horizontal=6, vertical=10),
            ink=True,
            on_click=lambda e, v=val: select_kategori(v),
            content=ft.Column([
                radio_icon,
                ft.Text(title, weight=ft.FontWeight.BOLD, size=11, text_align=ft.TextAlign.CENTER, color=ft.Colors.BLACK),
                ft.Text(subtitle, size=10, color=sub_color, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_500)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4)
        )

    kategori_row = ft.Row(spacing=8)

    def update_kategori_ui():
        kategori_row.controls = [
            make_kategori_card("Normal / Sesuai", "Siap Jalan", "Normal / Sesuai", "#16a34a", "#16a34a"),
            make_kategori_card("Minor (Catat)", "Lanjut Operasi", "Minor (Catat)", "#f59e0b", "#d97706"),
            make_kategori_card("Mayor (Stop)", "Maintenance", "Mayor (Stop)", "#dc2626", "#dc2626"),
        ]

    update_kategori_ui()

    # 3 Kartu Tanda Tangan & Verifikasi Shift
    def make_verif_card(title, name):
        return ft.Container(
            expand=True,
            bgcolor="#f8fafc",
            border=ft.Border.all(1, "#e2e8f0"),
            border_radius=8,
            padding=ft.Padding.symmetric(horizontal=6, vertical=8),
            content=ft.Column([
                ft.Text(title, weight=ft.FontWeight.BOLD, size=10, text_align=ft.TextAlign.CENTER, color="#1e293b"),
                ft.Text(name, size=9, color="#64748b", text_align=ft.TextAlign.CENTER),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK, size=11, color=ft.Colors.WHITE),
                        ft.Text("Terverifikasi", size=9, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=3),
                    bgcolor="#059669",
                    border_radius=10,
                    padding=ft.Padding.symmetric(horizontal=6, vertical=3)
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3)
        )

    verif_row = ft.Row([
        make_verif_card("Pengemudi AMT 1", "Budi Santoso"),
        make_verif_card("Pengawas AMT", "Hendra S. (Pws)"),
        make_verif_card("Petugas HSSE", "Rahmat D."),
    ], spacing=8)

    # Card C (Expanded)
    card_c = ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#e2e8f0"),
        border_radius=8,
        content=ft.Column([
            # Header C
            ft.Container(
                padding=10,
                content=ft.Row([
                    ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color="#15803d", size=20),
                    ft.Text("C. ODO Meter & Catatan", weight=ft.FontWeight.BOLD, color="#15803d", size=12, expand=True),
                    ft.Container(
                        content=ft.Text("Aktif Diisi", color=ft.Colors.WHITE, size=10, weight=ft.FontWeight.BOLD),
                        bgcolor="#0d47a1",
                        border_radius=4,
                        padding=ft.Padding.symmetric(horizontal=8, vertical=4)
                    )
                ], spacing=6)
            ),
            ft.Divider(height=1, thickness=0.8, color="#e2e8f0"),
            # Body C
            ft.Container(
                padding=12,
                content=ft.Column([
                    # Input ODO Awal & Akhir
                    ft.Row([
                        ft.Column([
                            ft.Text("Angka ODO Awal (KM)", weight=ft.FontWeight.BOLD, size=11, color=ft.Colors.BLACK),
                            odo_awal_field
                        ], expand=True, spacing=4),
                        ft.Column([
                            ft.Text("Angka ODO Akhir (KM)", weight=ft.FontWeight.BOLD, size=11, color=ft.Colors.BLACK),
                            odo_akhir_field
                        ], expand=True, spacing=4),
                    ], spacing=10),
                    
                    ft.Container(height=4),
                    
                    # Kategori Evaluasi
                    ft.Text("Kategori Evaluasi Temuan Alur:", weight=ft.FontWeight.BOLD, size=11, color=ft.Colors.BLACK),
                    kategori_row,
                    
                    ft.Container(height=4),
                    
                    # Catatan
                    ft.Row([
                        ft.Text("Catatan / Keterangan Temuan AMT:", weight=ft.FontWeight.BOLD, size=11, color=ft.Colors.BLACK),
                        ft.Text("Opsional", size=10, color="#94a3b8")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    catatan_field,
                    
                    ft.Container(height=4),
                    
                    # Tanda Tangan & Verifikasi
                    ft.Row([
                        ft.Text("Tanda Tangan & Verifikasi Shift:", weight=ft.FontWeight.BOLD, size=11, color=ft.Colors.BLACK),
                        ft.Text("3/3 Terverifikasi Lengkap", size=11, color="#15803d", weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    verif_row,
                ], spacing=8)
            )
        ], spacing=0)
    )

    async def on_submit(e):
        state.odo_awal = odo_awal_field.value
        state.odo_akhir = odo_akhir_field.value
        state.catatan = catatan_field.value
        
        # Berdasarkan flowchart:
        # Jika Mayor -> Blokir / Perbaikan
        # Jika Normal / Minor -> Selesai (Success)
        if "Mayor" in state.kategori_evaluasi:
            await page.push_route("/blocked")
        else:
            await page.push_route("/success")

    async def go_back(e):
        await page.push_route("/")

    submit_button = ft.Container(
        content=ft.Text("[ SIMPAN & SELESAIKAN HAND OVER ]", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=13),
        alignment=ft.Alignment.CENTER,
        bgcolor="#0284c7",
        border_radius=8,
        height=48,
        ink=True,
        on_click=on_submit
    )

    footer_text = ft.Text(
        "Langkah 2 dari 2: Verifikasi ODO Meter, Catatan & Selesai",
        size=11,
        color="#64748b",
        text_align=ft.TextAlign.CENTER
    )

    scrollable_content = ft.Container(
        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        expand=True,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            controls=[
                create_info_card(page),
                create_info_banner(),
                card_a,
                card_b,
                card_c,
                ft.Container(height=6),
                submit_button,
                footer_text,
                ft.Container(height=16)
            ]
        )
    )

    return ft.Column([
        create_mobile_header(page, on_back=go_back),
        scrollable_content
    ], spacing=0, expand=True)
