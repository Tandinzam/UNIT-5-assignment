
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class HelloApp(App):
    def build(self):
        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=10
        )

        self.label = Label(text="Welcome to Kivy!")

        button = Button(text="Click Me")
        button.bind(on_press=self.show_message)

        layout.add_widget(self.label)
        layout.add_widget(button)

        return layout

    def show_message(self, instance):
        self.label.text = "Hello! Button Clicked."

HelloApp().run()
