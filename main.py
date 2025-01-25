from flet import *
import json

def main(page: Page):
    def save_to_json(e):
        user_input = text_field.value
        data = {"user_input": user_input}
        with open("user_input.json", "w") as f:
            json.dump(data, f)
        page.add(Text("Data saved to user_input.json", color="green"))

    def read_from_json(e):
        try:
            with open("user_input.json", "r") as f:
                data = json.load(f)
            page.add(Text(f"Read from JSON: {data['user_input']}", color="blue"))
        except FileNotFoundError:
            page.add(Text("No JSON file found", color="red"))

    text_field = TextField(label="Enter something",  color="white")
    save_button = ElevatedButton(text="Save", on_click=save_to_json)
    read_button = ElevatedButton(text="Read", on_click=read_from_json)

    page.add(
        SafeArea(
            content=Column([
                Text("Hello from Flet", size=30, color="white"),
                text_field,
                save_button,
                read_button
            ])
        )
    )

app(main)
