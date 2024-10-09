import gradio as gr
from gradio_dataset import dataset
from gradio_modal_component import modal_component


# Initialize a three-column dataset for testing
def init_ds_three_col():
    ds = [
        [
            "Text 1",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 1",
        ],
        [
            "Text 2",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 2",
        ],
        [
            "Text 3",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 3",
        ],
        [
            "Text 4",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 4",
        ],
        [
            "Text 5",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
            "Description 5",
        ],
    ]
    return ds


# Initialize the global dataset
current_dataset = init_ds_three_col()


# Function to handle selection and actions
def get_selection(evt: gr.SelectData):
    """This will tranking envent and make any actions based on the event"""
    print("Selection Event Triggered")
    print(f"Row: {evt.index}")
    print(f"Value: {evt.value}")
    print(f"RowData: {evt.row_value}")

    global current_dataset

    # Check if it's a menu action
    if isinstance(evt.value, dict) and "menu_choice" in evt.value:
        menu_choice = evt.value["menu_choice"]

        if menu_choice == "View Profile":
            content = f"""
                # View Profile
                - You are viewing the profile number `{evt.index}`
                - Profile content:
                    - {evt.row_value}"""
            return gr.update(visible=True), content, current_dataset

        elif menu_choice == "Edit":
            content = f"""
                # Edit Profile
                - You are editing the profile number `{evt.index}`
                - Profile content:
                    - {evt.row_value}
            """
            return gr.update(visible=True), content, current_dataset

        elif menu_choice == "Delete":
            # Remove the row from the dataset
            current_dataset = [
                row for i, row in enumerate(current_dataset) if i != evt.index
            ]

            # Return updated dataset
            return (
                gr.update(visible=False),
                "",
                gr.update(value=current_dataset, samples=current_dataset),
            )

    # Default return
    return gr.update(visible=False), "", current_dataset


with gr.Blocks() as demo:
    # Modal component
    with modal_component(
        visible=False, width=500, height=300, bg_blur=0
    ) as profileModal:
        modal_text = gr.Markdown("")

    # Dataset component
    three_col_ds = dataset(
        components=[
            gr.Textbox(visible=False, interactive=True),
            gr.HTML(visible=False),
            gr.Textbox(visible=False, interactive=True),
        ],
        headers=[
            "Textbox",
            "Image",
            "Description",
        ],
        label="Three Columns Test",
        samples=current_dataset,
        menu_choices=["View Profile", "Edit", "Delete"],
        header_sort=True,
    )

    # Set up the select event
    three_col_ds.select(
        fn=get_selection, inputs=None, outputs=[profileModal, modal_text, three_col_ds]
    )

if __name__ == "__main__":
    demo.launch()
