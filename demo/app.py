import gradio as gr
from gradio_dataset import dataset
from gradio_modal_component import modal_component


def init_ds_two_col():
    ds = [
        [
            "Text 1",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
        ],
        [
            "Text 2",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
        ],
        [
            "Text 3",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
        ],
        [
            "Text 4",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
        ],
        [
            "Text 5",
            "<img src='https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1u64v34tov7a3tdqitrz.png' width='100px' height='100px'>",
        ],
    ]
    return ds


def init_ds_one_col():
    ds = [["Text 1"], ["Text 2"], ["Text 3"], ["Text 4"], ["Text 5"]]
    return ds


# Function to handle selection
def get_selection(evt: gr.SelectData):
    print("Selection Event Triggered")
    print(f"Row: {evt.index}")
    print(f"Value: {evt.value}")
    print(f"RowData: {evt.row_value}")

    # Check the action taken and display the modal accordingly
    if isinstance(evt.value, dict):
        if evt.value["menu_choice"] == "View Profile":
            # Display the modal with the selected value
            content = f"""
                # View Profile
                - You are viewing the profile number `{evt.index}`
                - Profile content:
                    -  {evt.row_value}"""
            return gr.update(visible=True), content
        if evt.value["menu_choice"] == "Edit":
            # Display the modal with the selected value
            return gr.update(visible=True), f"Edit clicked on: {evt.row_value}"

    # Return to hide the modal
    return gr.update(visible=False), ""


with gr.Blocks() as demo:
    # Modal that shows the content dynamically based on user selection
    with modal_component(
        visible=False, width=500, height=300, bg_blur=0
    ) as profileModal:
        modal_text = gr.Markdown(f"")

    # Define the dataset
    two_col_ds = dataset(
        components=[
            gr.Textbox(visible=False, interactive=True),
            gr.HTML(visible=False),
        ],
        headers=["Textbox", "Image"],
        label="Two Columns Test",
        samples=init_ds_two_col(),
        menu_choices=["View Profile", "Edit", "Delete"],
    )

    # Set the select event to update modal visibility and content
    two_col_ds.select(fn=get_selection, inputs=None, outputs=[profileModal, modal_text])

if __name__ == "__main__":
    demo.launch()
