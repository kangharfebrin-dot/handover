# views/step1_checklist.py
import math
import flet as ft
from state import state
from views.common import create_mobile_header, create_info_card, create_info_banner

def ChecklistView(page: ft.Page):
    
    # State accordion: A terbuka, B & C tertutup secara default
    section_state = {
        "A": True,
        "B": False,
        "C": False
    }

    # Helper hitung checklist
    def get_mt_count_str():
        mt_baik = sum(1 for v in state.checklist_mt.values() if v)
        return f"{mt_baik}/{len(state.checklist_mt)} Terisi Baik"

    def get_amt_count_str():
        amt_baik = sum(1 for v in state.checklist_amt.values() if v)
        return f"{amt_baik}/{len(state.checklist_amt)} Siap"

    # Badges di header Accordion
    badge_mt_text = ft.Text(get_mt_count_str(), size=10, weight=ft.FontWeight.BOLD, color="#15803d")
    badge_mt = ft.Container(
        content=badge_mt_text,
        bgcolor="#dcfce7",
        border=ft.Border.all(1, "#bbf7d0"),
        border_radius=12,
        padding=ft.Padding.symmetric(horizontal=8, vertical=4)
    )

    badge_amt_text = ft.Text(get_amt_count_str(), size=10, weight=ft.FontWeight.BOLD, color="#15803d")
    badge_amt = ft.Container(
        content=badge_amt_text,
        bgcolor="#dcfce7",
        border=ft.Border.all(1, "#bbf7d0"),
        border_radius=12,
        padding=ft.Padding.symmetric(horizontal=8, vertical=4)
    )

    badge_c_text = ft.Text("Verifikasi", size=10, weight=ft.FontWeight.BOLD, color="#475569")
    badge_c = ft.Container(
        content=badge_c_text,
        bgcolor="#f1f5f9",
        border=ft.Border.all(1, "#e2e8f0"),
        border_radius=12,
        padding=ft.Padding.symmetric(horizontal=8, vertical=4)
    )

    def update_badge_c():
        if section_state["C"]:
            badge_c_text.value = "Aktif Diisi"
            badge_c_text.color = ft.Colors.WHITE
            badge_c.bgcolor = "#0d47a1"
            badge_c.border = None
            badge_c.border_radius = 4
        else:
            badge_c_text.value = "Verifikasi"
            badge_c_text.color = "#475569"
            badge_c.bgcolor = "#f1f5f9"
            badge_c.border = ft.Border.all(1, "#e2e8f0")
            badge_c.border_radius = 12

    def update_step_button():
        if section_state["C"]:
            submit_btn_text.value = "[ SIMPAN & SELESAIKAN HAND OVER ]"
            footer_text.value = "Langkah 2 dari 2: Verifikasi ODO Meter, Catatan & Selesai"
        else:
            submit_btn_text.value = "[ SIMPAN & LANJUTKAN HAND OVER ]"
            footer_text.value = "Langkah 1 dari 2: Alur Inspeksi & Hand Over MT"

    def auto_evaluate_checklist():
        ada_kerusakan = any(not v for v in state.checklist_mt.values()) or any(not v for v in state.checklist_amt.values())
        if ada_kerusakan and state.kategori_evaluasi == "Normal / Sesuai":
            state.kategori_evaluasi = "Minor (Catat)"
            update_kategori_ui()
        elif not ada_kerusakan and state.kategori_evaluasi not in ["Minor (Catat)", "Mayor (Stop)"]:
            state.kategori_evaluasi = "Normal / Sesuai"
            update_kategori_ui()

    def update_badges():
        badge_mt_text.value = get_mt_count_str()
        badge_amt_text.value = get_amt_count_str()
        auto_evaluate_checklist()
        page.update()

    def on_checklist_mt_change(e, item_name):
        state.checklist_mt[item_name] = (e.control.value == "Baik")
        update_badges()

    def on_checklist_amt_change(e, item_name):
        state.checklist_amt[item_name] = (e.control.value == "Baik")
        update_badges()

    def centang_semua_mt(e):
        for item_name in state.checklist_mt.keys():
            state.checklist_mt[item_name] = True
        build_mt_list()
        update_badges()

    def centang_semua_amt(e):
        for item_name in state.checklist_amt.keys():
            state.checklist_amt[item_name] = True
        build_amt_list()
        update_badges()

    # Kontrol list MT & AMT
    mt_list_column = ft.Column(spacing=6)
    amt_list_column = ft.Column(spacing=6)

    def build_mt_list():
        mt_list_column.controls.clear()
        for i, (item_name, is_baik) in enumerate(state.checklist_mt.items()):
            cg = ft.RadioGroup(
                content=ft.Row([
                    ft.Radio(value="Baik", label="Baik / Ada", active_color="#0284c7"),
                    ft.Radio(
                        value="Tidak", 
                        label="Tidak (Ada Kerusakan)", 
                        label_style=ft.TextStyle(color="#dc2626", size=12),
                        active_color="#dc2626"
                    )
                ], spacing=16),
                value="Baik" if is_baik else "Tidak",
                on_change=lambda e, name=item_name: on_checklist_mt_change(e, name)
            )
            mt_list_column.controls.append(
                ft.Column([
                    ft.Text(f"{i+1}. {item_name}", weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.BLACK),
                    cg,
                    ft.Divider(height=1, thickness=0.8, color="#f1f5f9")
                ], spacing=2)
            )

    def build_amt_list():
        amt_list_column.controls.clear()
        for i, (item_name, is_baik) in enumerate(state.checklist_amt.items()):
            cg = ft.RadioGroup(
                content=ft.Row([
                    ft.Radio(value="Baik", label="Baik / Ada", active_color="#0284c7"),
                    ft.Radio(
                        value="Tidak", 
                        label="Tidak (Ada Kerusakan)", 
                        label_style=ft.TextStyle(color="#dc2626", size=12),
                        active_color="#dc2626"
                    )
                ], spacing=16),
                value="Baik" if is_baik else "Tidak",
                on_change=lambda e, name=item_name: on_checklist_amt_change(e, name)
            )
            amt_list_column.controls.append(
                ft.Column([
                    ft.Text(f"{i+1}. {item_name}", weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.BLACK),
                    cg,
                    ft.Divider(height=1, thickness=0.8, color="#f1f5f9")
                ], spacing=2)
            )

    build_mt_list()
    build_amt_list()

    # Kontrol Accordion A
    body_a = ft.Container(
        padding=12,
        content=ft.Column([
            ft.Row([
                ft.Text("Kondisi 18 item kendaraan", size=11, color="#64748b"),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK, size=14, color=ft.Colors.WHITE),
                        ft.Text("Centang Semua Baik", size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                    ], spacing=4),
                    bgcolor="#00897b",
                    border_radius=6,
                    padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                    ink=True,
                    on_click=centang_semua_mt
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=4),
            mt_list_column
        ], spacing=6)
    )

    icon_a = ft.Icon(
        ft.Icons.KEYBOARD_ARROW_DOWN if section_state["A"] else ft.Icons.KEYBOARD_ARROW_RIGHT,
        color="#15803d",
        size=20
    )

    switcher_a = ft.AnimatedSwitcher(
        content=body_a if section_state["A"] else ft.Container(),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=250,
        reverse_duration=200,
        switch_in_curve=ft.AnimationCurve.EASE_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN
    )

    def toggle_a(e):
        section_state["A"] = not section_state["A"]
        icon_a.icon = ft.Icons.KEYBOARD_ARROW_DOWN if section_state["A"] else ft.Icons.KEYBOARD_ARROW_RIGHT
        switcher_a.content = body_a if section_state["A"] else ft.Container()
        update_step_button()
        page.update()

    card_a = ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#e2e8f0"),
        border_radius=8,
        content=ft.Column([
            ft.Container(
                padding=10,
                ink=True,
                on_click=toggle_a,
                content=ft.Row([
                    icon_a,
                    ft.Text("A. Perlengkapan Mobil Tangki (18 Item)", weight=ft.FontWeight.BOLD, color="#15803d", size=12, expand=True),
                    badge_mt
                ], spacing=6)
            ),
            switcher_a
        ], spacing=0)
    )

    # Kontrol Accordion B
    body_b = ft.Container(
        padding=12,
        content=ft.Column([
            ft.Row([
                ft.Text("Standar APD & Dokumen Personil", size=11, color="#64748b"),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK, size=14, color=ft.Colors.WHITE),
                        ft.Text("Centang Semua Siap", size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                    ], spacing=4),
                    bgcolor="#00897b",
                    border_radius=6,
                    padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                    ink=True,
                    on_click=centang_semua_amt
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=4),
            amt_list_column
        ], spacing=6)
    )

    icon_b = ft.Icon(
        ft.Icons.KEYBOARD_ARROW_DOWN if section_state["B"] else ft.Icons.KEYBOARD_ARROW_RIGHT,
        color="#15803d",
        size=20
    )

    switcher_b = ft.AnimatedSwitcher(
        content=body_b if section_state["B"] else ft.Container(),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=250,
        reverse_duration=200,
        switch_in_curve=ft.AnimationCurve.EASE_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN
    )

    def toggle_b(e):
        section_state["B"] = not section_state["B"]
        icon_b.icon = ft.Icons.KEYBOARD_ARROW_DOWN if section_state["B"] else ft.Icons.KEYBOARD_ARROW_RIGHT
        switcher_b.content = body_b if section_state["B"] else ft.Container()
        update_step_button()
        page.update()

    card_b = ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#e2e8f0"),
        border_radius=8,
        content=ft.Column([
            ft.Container(
                padding=10,
                ink=True,
                on_click=toggle_b,
                content=ft.Row([
                    icon_b,
                    ft.Text("B. Perlengkapan AMT (10 Item)", weight=ft.FontWeight.BOLD, color="#15803d", size=12, expand=True),
                    badge_amt
                ], spacing=6)
            ),
            switcher_b
        ], spacing=0)
    )

    # Kontrol Accordion C (ODO Meter, Evaluasi & Catatan)
    odo_awal_field = ft.TextField(
        value=state.odo_awal,
        text_size=12,
        suffix="km",
        dense=True,
        border_color="#cbd5e1",
        border_radius=6,
        content_padding=ft.Padding.symmetric(horizontal=10, vertical=8),
        on_change=lambda e: setattr(state, 'odo_awal', e.control.value)
    )

    odo_akhir_field = ft.TextField(
        value=state.odo_akhir,
        text_size=12,
        suffix="km",
        dense=True,
        border_color="#cbd5e1",
        border_radius=6,
        content_padding=ft.Padding.symmetric(horizontal=10, vertical=8),
        on_change=lambda e: setattr(state, 'odo_akhir', e.control.value)
    )

    catatan_field = ft.TextField(
        value=state.catatan,
        multiline=True,
        min_lines=3,
        max_lines=5,
        text_size=11,
        border_color="#cbd5e1",
        border_radius=6,
        content_padding=10,
        hint_text="Tuliskan catatan atau temuan kerusakan di sini...",
        on_change=lambda e: setattr(state, 'catatan', e.control.value)
    )

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

    body_c = ft.Container(
        padding=12,
        content=ft.Column([
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
            
            ft.Text("Kategori Evaluasi Temuan Alur:", weight=ft.FontWeight.BOLD, size=11, color=ft.Colors.BLACK),
            kategori_row,
            
            ft.Container(height=4),
            
            ft.Row([
                ft.Text("Catatan / Keterangan Temuan AMT:", weight=ft.FontWeight.BOLD, size=11, color=ft.Colors.BLACK),
                ft.Text("Opsional", size=10, color="#94a3b8")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            catatan_field,
            
            ft.Container(height=4),
            
            ft.Row([
                ft.Text("Tanda Tangan & Verifikasi Shift:", weight=ft.FontWeight.BOLD, size=11, color=ft.Colors.BLACK),
                ft.Text("3/3 Terverifikasi Lengkap", size=11, color="#15803d", weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            verif_row,
        ], spacing=8)
    )

    icon_c = ft.Icon(
        ft.Icons.KEYBOARD_ARROW_DOWN if section_state["C"] else ft.Icons.KEYBOARD_ARROW_RIGHT,
        color="#15803d",
        size=20
    )

    switcher_c = ft.AnimatedSwitcher(
        content=body_c if section_state["C"] else ft.Container(),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=250,
        reverse_duration=200,
        switch_in_curve=ft.AnimationCurve.EASE_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN
    )

    def toggle_c(e):
        section_state["C"] = not section_state["C"]
        icon_c.icon = ft.Icons.KEYBOARD_ARROW_DOWN if section_state["C"] else ft.Icons.KEYBOARD_ARROW_RIGHT
        switcher_c.content = body_c if section_state["C"] else ft.Container()
        update_badge_c()
        update_step_button()
        page.update()

    card_c = ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#e2e8f0"),
        border_radius=8,
        content=ft.Column([
            ft.Container(
                padding=10,
                ink=True,
                on_click=toggle_c,
                content=ft.Row([
                    icon_c,
                    ft.Text("C. ODO Meter & Catatan", weight=ft.FontWeight.BOLD, color="#15803d", size=12, expand=True),
                    badge_c
                ], spacing=6)
            ),
            switcher_c
        ], spacing=0)
    )

    # Handler tombol bawah:
    # Jika Section C belum dibuka -> buka Section C dan tutup A & B dengan animasi halus
    # Jika Section C sudah terbuka -> simpan & selesaikan
    async def on_action_button_click(e):
        state.odo_awal = odo_awal_field.value
        state.odo_akhir = odo_akhir_field.value
        state.catatan = catatan_field.value

        if not section_state["C"]:
            # Beralih ke Langkah 2: Buka C, tutup A & B
            section_state["A"] = False
            section_state["B"] = False
            section_state["C"] = True
            
            icon_a.icon = ft.Icons.KEYBOARD_ARROW_RIGHT
            switcher_a.content = ft.Container()
            
            icon_b.icon = ft.Icons.KEYBOARD_ARROW_RIGHT
            switcher_b.content = ft.Container()
            
            icon_c.icon = ft.Icons.KEYBOARD_ARROW_DOWN
            switcher_c.content = body_c
            
            update_badge_c()
            update_step_button()
            page.update()
        else:
            # Selesai: Berdasarkan flowchart
            # Jika Mayor -> /blocked
            # Jika Normal / Minor -> /success
            if "Mayor" in state.kategori_evaluasi:
                await page.push_route("/blocked")
            else:
                await page.push_route("/success")

    submit_btn_text = ft.Text(
        "[ SIMPAN & LANJUTKAN HAND OVER ]",
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
        size=13
    )

    submit_button = ft.Container(
        content=submit_btn_text,
        alignment=ft.Alignment.CENTER,
        bgcolor="#0284c7",
        border_radius=8,
        height=48,
        ink=True,
        on_click=on_action_button_click
    )

    footer_text = ft.Text(
        "Langkah 1 dari 2: Alur Inspeksi & Hand Over MT",
        size=11,
        color="#64748b",
        text_align=ft.TextAlign.CENTER
    )

    # Konten halaman utama
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
        create_mobile_header(page),
        scrollable_content
    ], spacing=0, expand=True)
