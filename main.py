import flet as ft

from aimage import AImage

# instantiate AImage object with default text-to-image model
service_name = AImage.ai_services[0]
model_name = "DEV"
ai_svc = AImage(service_name, model_name)


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

    def aiservice_radiogroup_changed(e):
        ai_svc(aiservice_radio_button.value, model_name)
        page.update()

    aiservice_radio_button = ft.RadioGroup(
        value=service_name,
        content=ft.Row(
            [
                ft.Radio(
                    value=AImage.ai_services[0], label=AImage.modeai_servicesl[0]),
                ft.Radio(
                    value=AImage.ai_services[1], label=AImage.ai_services[1]),
                ft.Radio(
                    value=AImage.ai_services[2], label=AImage.ai_services[2]),
            ]
        ),
        on_change=aiservice_radiogroup_changed,
    )

    def modelgroup_changed(e):
        ai_svc(service_name, aimodel_radio_button.value)
        page.update()

    aimodel_radio_button = ft.RadioGroup(
        value=model_name,
        content=ft.Row(
            [
                ft.Radio(
                    value=AImage.model[0], label=AImage.model[0]),
                ft.Radio(
                    value=AImage.model[1], label=AImage.model[1]),
                ft.Radio(
                    value=AImage.model[2], label=AImage.model[2]),
            ]
        ),
        on_change=modelgroup_changed,
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
        aiservice_radio_button,
        model_radio_button,
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
