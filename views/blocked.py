# views/blocked.py
import flet as ft
from state import state

def BlockedView(page: ft.Page):
    
    async def on_back_eval(e):
        await page.push_route("/step2")

    async def on_restart(e):
        state.reset()
        await page.push_route("/")

    summary_card = ft.Container(
        bgcolor="#fff5f5",
        border=ft.Border.all(1, "#fecaca"),
        border_radius=12,
        padding=16,
        content=ft.Column([
            ft.Row([
                ft.Text("No Polisi MT", color="#64748b", size=12),
                ft.Text(state.no_polisi, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, size=12)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Row([
                ft.Text("Status Evaluasi", color="#64748b", size=12),
                ft.Container(
                    content=ft.Row([
                        ft.Container(width=6, height=6, border_radius=3, bgcolor="#dc2626"),
                        ft.Text("Mayor (Stop / Maintenance)", color="#b91c1c", size=11, weight=ft.FontWeight.BOLD)
                    ], spacing=5),
                    bgcolor="#fee2e2",
                    border_radius=12,
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Divider(height=16, thickness=0.8, color="#fecaca"),
            
            ft.Column([
                ft.Text("Catatan Temuan Kerusakan:", color="#64748b", size=11, weight=ft.FontWeight.BOLD),
                ft.Text(
                    state.catatan if state.catatan else "Ada temuan kategori mayor pada checklist perlengkapan kendaraan / personil.",
                    color="#991b1b",
                    size=12
                )
            ], spacing=4)
        ], spacing=10)
    )

    btn_eval = ft.Container(
        content=ft.Text("Kembali ke Evaluasi & Catatan ➔", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=13),
        alignment=ft.Alignment.CENTER,
        bgcolor="#0284c7",
        border_radius=8,
        height=48,
        ink=True,
        on_click=on_back_eval
    )

    btn_restart = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.BUILD_OUTLINED, size=15, color="#1e293b"),
            ft.Text("Perbaikan Selesai: Ulangi Checklist", color="#1e293b", weight=ft.FontWeight.BOLD, size=12)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=6),
        alignment=ft.Alignment.CENTER,
        bgcolor="#f8fafc",
        border=ft.Border.all(1, "#cbd5e1"),
        border_radius=8,
        height=48,
        ink=True,
        on_click=on_restart
    )

    card_container = ft.Container(
        width=380,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#fecaca"),
        border_radius=16,
        padding=24,
        content=ft.Column([
            ft.Container(height=10),
            
            # Warning Icon
            ft.Container(
                width=76, height=76, border_radius=38,
                bgcolor="#fee2e2",
                alignment=ft.Alignment.CENTER,
                content=ft.Icon(ft.Icons.REPORT_PROBLEM_ROUNDED, color="#dc2626", size=40)
            ),
            
            ft.Container(height=6),
            
            # Pill
            ft.Container(
                content=ft.Text("PROSES DIBLOKIR", color="#dc2626", weight=ft.FontWeight.BOLD, size=10),
                bgcolor="#fee2e2",
                border_radius=12,
                padding=ft.Padding.symmetric(horizontal=12, vertical=4)
            ),
            
            ft.Container(height=4),
            
            ft.Text("Kondisi Mayor: Kendaraan Perlu Perbaikan!", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color="#991b1b"),
            
            ft.Text("Sesuai standar operasional, temuan kategori Mayor wajib masuk bengkel (Maintenance) sebelum dioperasikan.", size=12, color="#64748b", text_align=ft.TextAlign.CENTER),
            
            ft.Container(height=12),
            
            summary_card,
            
            ft.Container(height=16),
            
            btn_eval,
            
            ft.Container(height=6),
            
            btn_restart
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
