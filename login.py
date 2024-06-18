from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from random import randint
from firebase import firebase

# Firebase initialization
firebase = firebase.FirebaseApplication('https://auth-794be-default-rtdb.firebaseio.com/', None)

class AnimatedButton(Button):
    def on_press(self):
        anim = Animation(size=(self.width + 10, self.height + 10), duration=0.1) + Animation(size=(self.width, self.height), duration=0.1)
        anim.start(self)
        return super().on_press()

class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint=(None, None), width=dp(300), height=dp(400))
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
        self.email_input = TextInput(hint_text="Email", multiline=False, size_hint_y=None, height=dp(40))
        self.email_input.font_size = dp(14)
        self.layout.add_widget(self.email_input)
        
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, size_hint_y=None, height=dp(40))
        self.password_input.font_size = dp(14)
        self.layout.add_widget(self.password_input)

        self.captcha = self.generate_captcha()
        self.captcha_label = Label(text=self.captcha[0], color=(1, 1, 1, 1), size_hint_y=None, height=dp(30))
        self.captcha_label.font_size = dp(14)
        self.layout.add_widget(self.captcha_label)
        
        self.captcha_input = TextInput(hint_text="Captcha Answer", multiline=False, size_hint_y=None, height=dp(40))
        self.captcha_input.font_size = dp(14)
        self.layout.add_widget(self.captcha_input)
        
        self.login_button = AnimatedButton(text="Login", background_color=(0.2, 0.6, 0.86, 1), size_hint_y=None, height=dp(50))
        self.login_button.bind(on_press=self.authenticate_user)
        self.layout.add_widget(self.login_button)

        self.register_button = AnimatedButton(text="Register", background_color=(0.2, 0.6, 0.86, 1), size_hint_y=None, height=dp(50))
        self.register_button.bind(on_press=self.go_to_register)
        self.layout.add_widget(self.register_button)
        
        self.message = Label(text="", color=(1, 1, 1, 1), size_hint_y=None, height=dp(30))
        self.message.font_size = dp(14)
        self.layout.add_widget(self.message)
        
        self.add_widget(self.layout)
        self.set_background_color()

    def generate_captcha(self):
        num1 = randint(1, 9)
        num2 = randint(1, 9)
        question = f"Solve: {num1} + {num2}"
        answer = str(num1 + num2)
        return (question, answer)

    def authenticate_user(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        captcha_answer = self.captcha_input.text

        if captcha_answer != self.captcha[1]:
            self.message.text = "Incorrect CAPTCHA"
            return
        
        result = firebase.get('auth-794be-default-rtdb/Users', '')

        for user_id, user_info in result.items():
            if user_info['Email'] == email and user_info['Password'] == password:
                self.manager.current = 'hello'
                return
        self.message.text = "Invalid email or password"

    def go_to_register(self, instance):
        self.manager.current = 'register'

    def set_background_color(self):
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class RegisterScreen(Screen):

    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint=(None, None), width=dp(300), height=dp(400))
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
        self.email_input = TextInput(hint_text="Email", multiline=False, size_hint_y=None, height=dp(40))
        self.email_input.font_size = dp(14)
        self.layout.add_widget(self.email_input)
        
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, size_hint_y=None, height=dp(40))
        self.password_input.font_size = dp(14)
        self.layout.add_widget(self.password_input)

        self.captcha = self.generate_captcha()
        self.captcha_label = Label(text=self.captcha[0], color=(1, 1, 1, 1), size_hint_y=None, height=dp(30))
        self.captcha_label.font_size = dp(14)
        self.layout.add_widget(self.captcha_label)
        
        self.captcha_input = TextInput(hint_text="Captcha Answer", multiline=False, size_hint_y=None, height=dp(40))
        self.captcha_input.font_size = dp(14)
        self.layout.add_widget(self.captcha_input)
        
        self.register_button = AnimatedButton(text="Register", background_color=(0.2, 0.6, 0.86, 1), size_hint_y=None, height=dp(50))
        self.register_button.bind(on_press=self.register_user)
        self.layout.add_widget(self.register_button)
        
        self.back_to_login_button = AnimatedButton(text="Back to Login", background_color=(0.2, 0.6, 0.86, 1), size_hint_y=None, height=dp(50))
        self.back_to_login_button.bind(on_press=self.go_to_login)
        self.layout.add_widget(self.back_to_login_button)
        
        self.message = Label(text="", color=(1, 1, 1, 1), size_hint_y=None, height=dp(30))
        self.message.font_size = dp(14)
        self.layout.add_widget(self.message)
        
        self.add_widget(self.layout)
        self.set_background_color()

    def generate_captcha(self):
        num1 = randint(1, 9)
        num2 = randint(1, 9)
        question = f"Solve: {num1} + {num2}"
        answer = str(num1 + num2)
        return (question, answer)

    def register_user(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        captcha_answer = self.captcha_input.text

        if captcha_answer != self.captcha[1]:
            self.message.text = "Incorrect CAPTCHA"
            return
        
        if '@' not in email or '.' not in email:
            self.message.text = "Invalid email format"
            return

        if len(password) < 6:
            self.message.text = "Password must be at least 6 characters"
            return

        data = {'Email': email, 'Password': password}
        firebase.post('auth-794be-default-rtdb/Users', data)
        self.manager.current = 'login'

    def go_to_login(self, instance):
        self.manager.current = 'login'

    def set_background_color(self):
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class HelloWorldScreen(Screen):

    def __init__(self, **kwargs):
        super(HelloWorldScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint=(None, None), width=dp(300), height=dp(400))
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
        self.label = Label(text="Hello World", color=(1, 1, 1, 1), size_hint_y=None, height=dp(40))
        self.label.font_size = dp(18)
        self.layout.add_widget(self.label)
        
        self.logout_button = AnimatedButton(text="Logout", background_color=(0.2, 0.6, 0.86, 1), size_hint_y=None, height=dp(50))
        self.logout_button.bind(on_press=self.logout_user)
        self.layout.add_widget(self.logout_button)
        
        self.add_widget(self.layout)
        self.set_background_color()

    def logout_user(self, instance):
        self.manager.current = 'login'

    def set_background_color(self):
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class MyApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(HelloWorldScreen(name='hello'))
        return sm

if __name__ == '__main__':
    MyApp().run()
