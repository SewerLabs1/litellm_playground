import streamlit as st
import threading
import requests

# Function to get model outputs
def get_model_output_thread(prompt, model_name, outputs, idx):
    url = "https://api.together.xyz/inference" 
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer cad84f39be62a8e36fdd846152dbb18abddef0aefcd921e82e287b4c228ac3e1"
    }
    data = {
        "model": model_name,
        "messages": [
            {
                "content": prompt,
                "role": "user"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
  
    output = response_data['choices'][0]['message']['content']
    outputs[idx] = output

# Streamlit app
def main():
    st.title("DittoLLM Playground")
    st.subheader("Powered LiteLLM")

    # Sidebar for user input
    st.header("User Input")
    prompt = st.text_area("Enter your prompt here:")
    submit_button = st.button("Submit")
    
    # Main content area to display model outputs
    st.header("Model Outputs")
    
    # List of models to test
    model_names = ["togethercomputer/CodeLlama-34b-Instruct", "mistralai/Mistral-7B-Instruct-v0.1", "Phind/Phind-CodeLlama-34B-v2"]  # Add your model names here
    
    cols = st.columns(len(model_names))  # Create columns
    outputs = [""] * len(model_names)  # Initialize outputs list with empty strings

    threads = []

    if submit_button and prompt:
        for idx, model_name in enumerate(model_names):
            thread = threading.Thread(target=get_model_output_thread, args=(prompt, model_name, outputs, idx))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    # Display text areas and fill with outputs if available
    for idx, model_name in enumerate(model_names):
        with cols[idx]:
            st.text_area(label=f"{model_name}", value=outputs[idx], height=300, key=f"output_{model_name}_{idx}")  # Use a unique key

if __name__ == "__main__":
    main()
