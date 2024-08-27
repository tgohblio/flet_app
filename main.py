import flet as ft

from aimage import AImage


def main(page: ft.Page):
    page.title = "Two-Tab Flet App"

    input_field = ft.TextField(
        label="Enter prompt",
        hint_text="cat perching on a tree branch on a moonlit night",
    )
    second_tab_text = ft.Text("Text from first tab will appear here")
    img = ft.Image(
        src="blank-photo.jpg",
        width=512,
        height=512,
        fit=ft.ImageFit.CONTAIN
    )
    nsfw_switch = ft.Switch(label="NSFW On", value=True)

    def aiservice_radiogroup_changed(e):
        page.update()

    aiservice_radio_button = ft.RadioGroup(
        value=AImage.ai_services[0],
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
        on_change=aiservice_radiogroup_changed,
    )

    def modelgroup_changed(e):
        page.update()

    aimodel_radio_button = ft.RadioGroup(
        value=AImage.model[1],
        content=ft.Row(
            [
                ft.Radio(
                    value=AImage.model[0], label=AImage.model[0]),
                ft.Radio(
                    value=AImage.model[1], label=AImage.model[1]),
                ft.Radio(
                    value=AImage.model[2], label=AImage.model[2]),
                ft.Radio(
                    value=AImage.model[3], label=AImage.model[3]),
            ]
        ),
        on_change=modelgroup_changed,
    )

    # Add a loading widget
    loading_widget = ft.ProgressRing(visible=False)

    # Use Overlay to stack the image and loading widget
    image_with_loading = ft.Stack(
        [
            img,
            loading_widget
        ],
        alignment=ft.alignment.center
    )

    def create_image(e):
        loading_widget.visible = True
        page.update()

        ai_svc = AImage(aiservice_radio_button.value, aimodel_radio_button.value)
        if not input_field.value:
            input_field.value = input_field.hint_text
        photos = ai_svc.gen_image(input_field.value, safety_on=nsfw_switch.value)
        img.src = photos[0]

        loading_widget.visible = False
        page.update()

    submit_button = ft.ElevatedButton("Send", on_click=create_image)

    tab1_content = ft.Column([
            image_with_loading,
            ft.Text("Enter text below:"),
            input_field,
            aiservice_radio_button,
            aimodel_radio_button,
            submit_button,
            nsfw_switch
        ],
    )

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
