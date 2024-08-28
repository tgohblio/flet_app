import flet as ft
from aimage import AImage


def main(page: ft.Page):
    """
    Main function to set up the Flet app page with a two-tab navigation bar.

    Args:
        page (ft.Page): The Flet page object.
    """
    page.title = "Two-Tab Flet App"
    page.scroll = ft.ScrollMode.ALWAYS

    # Define first tab content
    input_field = ft.TextField(
        label="Enter prompt here",
        hint_text="cat perching on a tree branch on a moonlit night",
    )
    img = ft.Image(
        src="blank-photo.jpg",
        width=512,
        height=512,
        fit=ft.ImageFit.CONTAIN
    )
    nsfw_switch = ft.Switch(label="NSFW On", value=True)

    def aiservice_changed(e):
        """
        Callback function to handle changes in the AI service selection.

        Args:
            e: The event object.
        """
        page.update()

    aiservice_radio_button = ft.RadioGroup(
        value=AImage.ai_services[0],
        content=ft.Row([
            ft.Radio(value=AImage.ai_services[0], label=AImage.ai_services[0]),
            ft.Radio(value=AImage.ai_services[1], label=AImage.ai_services[1]),
            ft.Radio(value=AImage.ai_services[2], label=AImage.ai_services[2])
        ]),
        on_change=aiservice_changed,
    )

    def model_changed(e):
        """
        Callback function to handle changes in the AI model selection.

        Args:
            e: The event object.
        """
        page.update()

    aimodel_radio_button = ft.RadioGroup(
        value=AImage.model[1],
        content=ft.Row([
            ft.Radio(value=AImage.model[0], label=AImage.model[0]),
            ft.Radio(value=AImage.model[1], label=AImage.model[1]),
            ft.Radio(value=AImage.model[2], label=AImage.model[2])
        ]),
        on_change=model_changed,
    )

    # Add a loading widget
    loading_widget = ft.ProgressRing(visible=False)

    # Use Overlay to stack the image and loading widget
    image_with_loading = ft.Stack([
            img,
            loading_widget
        ],
        alignment=ft.alignment.center
    )

    def create_image(e):
        """
        Callback function to generate an image based on the input prompt.

        Args:
            e: The event object.
        """
        loading_widget.visible = True
        page.update()

        ai_svc = AImage(aiservice_radio_button.value, aimodel_radio_button.value)
        if not input_field.value:
            input_field.value = input_field.hint_text
        output, format = ai_svc.gen_image(input_field.value, safety_on=nsfw_switch.value)
        if format == "base64":
            img.src_base64 = output
        else:
            # output is a file path
            img.src = output

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
        spacing=1,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Define second tab content
    second_tab_text = ft.Text("Text from first tab will appear here")

    tab2_content = ft.Column([
        ft.Text("Text from first tab:"),
        second_tab_text
    ])
    
    # Define navigation bar content
    def tab_changed(e):
        """
        Callback function to handle tab changes in the navigation bar.

        Args:
            e: The event object.
        """
        tab1_content.visible = True if e.control.selected_index == 0 else False
        tab2_content.visible = True if e.control.selected_index == 1 else False
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.DRAW, label="Create"),
            ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Commute"),
        ],
        selected_index=0,  # Set the default selected index here
        on_change=tab_changed
    )

    # setup default view on first tab i.e. draw
    tab2_content.visible = False
    tab1_content.visible = True
    page.add(ft.Column([tab1_content, tab2_content]))

ft.app(target=main, assets_dir="assets")
