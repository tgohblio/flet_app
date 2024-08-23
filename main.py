import flet as ft

from aimage import AImage

# instantiate AImage object with default text-to-image model
default_service = AImage.ai_services[0]
ai_svc = AImage(default_service)


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

    def radiogroup_changed(e):
        ai_svc(radio_button.value)
        page.update()

    radio_button = ft.RadioGroup(
        value=default_service,
        content=ft.Row(
            [
                ft.Radio(
                    value=AImage.ai_services[0], label=AImage.ai_services[0]),
                ft.Radio(
                    value=AImage.ai_services[1], label=AImage.ai_services[1]),
                ft.Radio(
                    value=AImage.ai_services[2], label=AImage.ai_services[2]),
            ]
        ),
        on_change=radiogroup_changed,
    )

    def create_image(e):
        global ai_svc
        photos = ai_svc.gen_image(
            input_field.value, safety_on=nsfw_switch.value)
        img.src = photos[0]
        page.update()

    submit_button = ft.ElevatedButton("Send", on_click=create_image)

    tab1_content = ft.Column([
        img,
        ft.Text("Enter text below:"),
        input_field,
        radio_button,
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
