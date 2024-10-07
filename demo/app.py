
import gradio as gr
from gradio_dataset import dataset


import gradio as gr
import pandas as pd
# Create sample data with image paths
data = {
    'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown'],
    'Age': [28, 34, 42, 25],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston'],
    'Occupation': ['Engineer', 'Designer', 'Teacher', 'Developer'],
    'Image': [
        '/api/placeholder/150/150',  # Using placeholder images for demo
        '/api/placeholder/150/150',
        '/api/placeholder/150/150',
        '/api/placeholder/150/150'
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

def handle_menu_action(evt: gr.EventData):
    """Handle menu actions for the dataset"""
    index = evt.value["index"]
    choice = evt.value["menu_choice"]

    employee = df.iloc[index]

    if choice == "View Profile":
        return {
            view_modal: True,
            profile_name: employee['Name'],
            profile_details: f"""
Age: {employee['Age']}
City: {employee['City']}
Occupation: {employee['Occupation']}
            """,
            profile_image: employee['Image']
        }
    return {
        view_modal: False,
        profile_name: "",
        profile_details: "",
        profile_image: None
    }

def show_dataset():
    # Create and return the dataset component
    return dataset(
        components=[
            gr.Textbox(label="Name"),
            gr.Number(label="Age"),
            gr.Textbox(label="City"),
            gr.Textbox(label="Occupation"),
            gr.Image(label="Profile", visible=False)  # Hidden component to store image data
        ],
        samples=[
            [row['Name'], row['Age'], row['City'], row['Occupation'], row['Image']]
            for _, row in df.iterrows()
        ],
        menu_icon="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.1/icons/three-dots-vertical.svg",
        menu_choices=["View Profile", "Edit", "Delete"],
        label="Employee Database"
    )

# Create the interface
with gr.Blocks() as demo:
    gr.Markdown("## Employee Database Demo")

    # Create the dataset component
    dataset = show_dataset()

    # Create the profile view modal
    with gr.Group(visible=False) as view_modal:
        with gr.Column():
            gr.Markdown("## Employee Profile")
            profile_image = gr.Image(label="Profile Picture", interactive=False)
            profile_name = gr.Markdown("### Name")
            profile_details = gr.Markdown("Details")
            close_btn = gr.Button("Close")

    # Handle events
    dataset.select(
        handle_menu_action,
        outputs=[view_modal, profile_name, profile_details, profile_image]
    )

    close_btn.click(
        lambda: {
            view_modal: False,
            profile_name: "",
            profile_details: "",
            profile_image: None
        },
        outputs=[view_modal, profile_name, profile_details, profile_image]
    )

# Launch the interface
if __name__ == "__main__":
    demo.launch()