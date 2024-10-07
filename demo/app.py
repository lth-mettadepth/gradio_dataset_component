import gradio as gr
import pandas as pd

# Create sample data
data = {
    'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown'],
    'Age': [28, 34, 42, 25],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston'],
    'Occupation': ['Engineer', 'Designer', 'Teacher', 'Developer']
}

# Convert to DataFrame
df = pd.DataFrame(data)

def show_dataset():
    # Create and return the dataset component
    dataset = gr.Dataset(
        components=[gr.Textbox(label="Name"),
                   gr.Number(label="Age"),
                   gr.Textbox(label="City"),
                   gr.Textbox(label="Occupation")],
        samples=[[row['Name'], row['Age'], row['City'], row['Occupation']]
                for _, row in df.iterrows()],
        label="Employee Database"
    )
    return dataset

# Create the interface
with gr.Blocks() as demo:
    gr.Markdown("## Employee Database Demo")
    show_dataset()

# Launch the interface
if __name__ == "__main__":
    demo.launch()