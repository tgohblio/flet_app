import flet as ft
import falai

from falai import FalAI

ai_svc = FalAI()

def main(page: ft.Page):
    page.title = "Two-Tab Flet App"
    
    input_field = ft.TextField(label="Enter prompt")
    second_tab_text = ft.Text("Text from first tab will appear here")
    img = ft.Image(
                src=f"/blank-photo.jpg",
                width=512,
                height=512,
                fit=ft.ImageFit.CONTAIN
            )
    nsfw_switch = ft.Switch(label="NSFW On", value=True)

    def update_image(e):
        photos = ai_svc.gen_image(str(input_field.value), safety_on=nsfw_switch.value)
        img.src = photos[0]
        page.update()

    submit_button = ft.ElevatedButton("Send", on_click=update_image)

    tab1_content = ft.Column([
        img,
        ft.Text("Enter text below:"),
        input_field,
        submit_button,
        nsfw_switch
    ])

    tab2_content = ft.Column([
        ft.Text("Text from first tab:"),
        second_tab_text
    ])

    # Center the content on the page
    tab1_content.vertical_alignment = ft.MainAxisAlignment.CENTER
    tab1_content.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Input", content=tab1_content),
            ft.Tab(text="Display", content=tab2_content),
        ]
    )

    page.add(tabs)

ft.app(target=main, assets_dir="assets")