import gradio as gr
import requests

BASE_URL = "http://127.0.0.1:8000"  # Your FastAPI server base

# Call FastAPI Weather API
def weather_interface(city: str):
    try:
        resp = requests.get(f"{BASE_URL}/weather/{city}", timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        return f"❌ Error: {str(e)}"

    location = f"{data['location']['name']}, {data['location']['country']}"
    temp = f"{data['current']['temp_c']} °C"
    condition = data["current"]["condition"]["text"]
    humidity = f"{data['current']['humidity']}%"
    wind = f"{data['current']['wind_kph']} kph"
    
    return f"""
### 🌍 {location}
- 🌡 **Temperature:** {temp}  
- 🌤 **Condition:** {condition}  
- 💧 **Humidity:** {humidity}  
- 🌬 **Wind Speed:** {wind}  
"""

# Call FastAPI Password API
def password_interface(length: int):
    try:
        resp = requests.post(
            f"{BASE_URL}/generate-password",
            json={"length": length},
            timeout=10
        )
        resp.raise_for_status()
        return f"🔑 {resp.json()['password']}"
    except requests.exceptions.RequestException as e:
        return f"❌ Error: {str(e)}"

# Build Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🌦 Weather & 🔑 Password Generator  
        **Frontend powered by Gradio, Backend by FastAPI**  
        ---
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("## 🌍 Real-Time Weather")
                city_input = gr.Textbox(label="Enter City", placeholder="e.g. Islamabad")
                weather_button = gr.Button("Get Weather 🌦", variant="primary")
                weather_output = gr.Textbox(label="Weather Info", interactive=False, lines=6)
                weather_button.click(fn=weather_interface, inputs=city_input, outputs=weather_output)

        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("## 🔐 Password Generator")
                length_input = gr.Slider(minimum=6, maximum=32, value=12, step=1, label="Password Length")
                password_button = gr.Button("Generate Password 🔑", variant="primary")
                password_output = gr.Textbox(label="Generated Password", interactive=False)
                password_button.click(fn=password_interface, inputs=length_input, outputs=password_output)

# Run Gradio separately
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
