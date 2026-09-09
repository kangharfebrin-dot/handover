# main.py
import flet as ft
from views.step1_checklist import ChecklistView
from views.step2_evaluation import EvaluationView
from views.step3_success import SuccessView
from views.blocked import BlockedView

def main(page: ft.Page):
    page.title = "Hand Over App - Pertamina iAMT"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = "#f1f5f9"
    
    # Ukuran jendela desktop mensimulasikan layar perangkat mobile (smartphone)
    page.window.width = 420
    page.window.height = 860
    page.window.resizable = True

    def route_change(e=None):
        page.views.clear()
        
        # Penentuan tampilan berdasarkan rute halaman
        if page.route == "/step2":
            view_content = EvaluationView(page)
        elif page.route == "/success":
            view_content = SuccessView(page)
        elif page.route == "/blocked":
            view_content = BlockedView(page)
        else: # "/"
            view_content = ChecklistView(page)
            
        page.views.append(
            ft.View(
                route=page.route,
                controls=[view_content],
                padding=0,
                bgcolor="#f8fafc"
            )
        )
        page.update()

    async def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Inisialisasi dan render tampilan rute awal
    route_change(None)

if __name__ == "__main__":
    ft.run(main)
