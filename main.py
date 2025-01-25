from flet import *
import json

class MainApp:
    def __init__(self, page: Page):
        self.page = page
        self.text_field = TextField(label="Enter something", color="white")
        self.save_button = ElevatedButton(text="Save", on_click=self.save_to_json)
        self.read_button = ElevatedButton(text="Read", on_click=self.read_from_json)
        self.setup_ui()

    def setup_ui(self):
        self.page.add(
            SafeArea(
                content=Column([
                    Text("Hello from Flet", size=30, color="white"),
                    self.text_field,
                    self.save_button,
                    self.read_button
                ])
            )
        )

    def save_to_json(self, e):
        user_input = self.text_field.value
        data = {"user_input": user_input}
        with open("user_input.json", "w") as f:
            json.dump(data, f)
        self.page.add(Text("Data saved to user_input.json", color="green"))

    def read_from_json(self, e):
        try:
            with open("user_input.json", "r") as f:
                data = json.load(f)
            self.page.add(Text(f"Read from JSON: {data['user_input']}", color="blue"))
        except FileNotFoundError:
            self.page.add(Text("No JSON file found", color="red"))

def main(page: Page):
    MainApp(page)

app(main)
