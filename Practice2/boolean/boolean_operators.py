class Button:
    def __init__(self):
        self.press_condition = False

    def buttonPress(self) -> str:
        self.press_condition = True
        return "you hold the button"

    def buttonRelease(self) -> str:
        self.press_condition = False
        return "button released"
    
    def currentCondition(self) -> bool:
        return self.press_condition
    
myButton = Button()

print(myButton.currentCondition())
print(myButton.buttonPress())
print(myButton.currentCondition())
print(myButton.buttonRelease())
print(myButton.currentCondition())