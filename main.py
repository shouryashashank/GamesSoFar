from flet import *

def main (page: Page) :
    page. add(
        # YOU MUST SET SAFEAREA
        SafeArea(
            content=Text("Hello form Flet" , size=30, color="white")
        )
    )
    # AND DO NOT USE
    # USE THIS
app(main)
