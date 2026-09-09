# views/step3_success.py
import flet as ft
from state import state

def SuccessView(page: ft.Page):
    
    mt_baik = sum(1 for v in state.checklist_mt.values() if v)
    amt_baik = sum(1 for v in state.checklist_amt.values() if v)
    
    status_label = "Laik Operasi (Normal)" if state.kategori_evaluasi == "Normal / Sesuai" else f"Catatan: {state.kategori_evaluasi}"
    status_dot_color = "#16a34a" if state.kategori_evaluasi == "Normal / Sesuai" else "#f59e0b"
    status_bg_color = "#dcfce7" if state.kategori_evaluasi == "Normal / Sesuai" else "#fef3c7"
    status_text_color = "#15803d" if state.kategori_evaluasi == "Normal / Sesuai" else "#b45309"

    async def on_next(e):
        state.reset()
        await page.push_route("/")

    summary_card = ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#e2e8f0"),
        border_radius=12,
        padding=16,
        content=ft.Column([
            ft.Row([
                ft.Text("No Polisi", color="#64748b", size=12),
                ft.Text(state.no_polisi, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, size=12)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Row([
                ft.Text("Shift", color="#64748b", size=12),
                ft.Text(state.shift, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, size=12)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Row([
                ft.Text("Status", color="#64748b", size=12),
                ft.Container(
                    content=ft.Row([
                        ft.Container(width=6, height=6, border_radius=3, bgcolor=status_dot_color),
                        ft.Text(status_label, color=status_text_color, size=11, weight=ft.FontWeight.BOLD)
                    ], spacing=5),
                    bgcolor=status_bg_color,
                    border_radius=12,
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Divider(height=16, thickness=0.8, color="#f1f5f9"),
            
            ft.Row([
                ft.Text("Checklist Kendaraan", color="#64748b", size=12),
                ft.Text(f"{mt_baik}/{len(state.checklist_mt)} Baik", weight=ft.FontWeight.BOLD, color="#15803d", size=12)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Row([
                ft.Text("Perlengkapan AMT", color="#64748b", size=12),
                ft.Text(f"{amt_baik}/{len(state.checklist_amt)} Lengkap", weight=ft.FontWeight.BOLD, color="#15803d", size=12)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Row([
                ft.Text("ODO Meter", color="#64748b", size=12),
                ft.Text(f"{state.odo_akhir or state.odo_awal} km", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, size=12)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ], spacing=10)
    )

    btn_next = ft.Container(
        content=ft.Text("Lanjut ke Ringkasan Perjalanan ➔", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=13),
        alignment=ft.Alignment.CENTER,
        bgcolor="#0284c7",
        border_radius=8,
        height=48,
        ink=True,
        on_click=on_next
    )

    btn_pdf = ft.Container(
        content=ft.Row([
            ft.Text("📄", size=14),
            ft.Text("Cetak / Unduh Bukti PDF", color="#1e293b", weight=ft.FontWeight.BOLD, size=12)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
        alignment=ft.Alignment.CENTER,
        bgcolor="#f8fafc",
        border=ft.Border.all(1, "#cbd5e1"),
        border_radius=8,
        height=48,
        ink=True
    )

    card_container = ft.Container(
        width=380,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#e2e8f0"),
        border_radius=16,
        padding=24,
        content=ft.Column([
            ft.Container(height=10),
            
            # Checkmark Icon besar
            ft.Container(
                width=76, height=76, border_radius=38,
                bgcolor="#dcfce7",
                alignment=ft.Alignment.CENTER,
                content=ft.Icon(ft.Icons.CHECK, color="#15803d", size=40)
            ),
            
            ft.Container(height=6),
            
            # Pill Verifikasi Sukses
            ft.Container(
                content=ft.Text("VERIFIKASI SUKSES", color="#15803d", weight=ft.FontWeight.BOLD, size=10),
                bgcolor="#dcfce7",
                border_radius=12,
                padding=ft.Padding.symmetric(horizontal=12, vertical=4)
            ),
            
            ft.Container(height=4),
            
            ft.Text("Inspeksi & Hand Over Berhasil Disimpan!", size=17, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=ft.Colors.BLACK),
            
            ft.Text("Seluruh alur pemeriksaan telah tervalidasi dalam sistem digital iAMT.", size=12, color="#64748b", text_align=ft.TextAlign.CENTER),
            
            ft.Container(height=12),
            
            summary_card,
            
            ft.Container(height=16),
            
            btn_next,
            
            ft.Container(height=6),
            
            btn_pdf
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4)
    )

    return ft.Container(
        bgcolor="#f8fafc",
        expand=True,
        alignment=ft.Alignment.CENTER,
        padding=16,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                card_container
            ]
        )
    )
