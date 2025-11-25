class System:
    def __init__(self):
        self.history = []

    def greating_message(self):
        message_1 = "Привет! Ты попал в подземелье. Я твой персональный помощник. Я помогу тебе из него выбраться. Для начала изучим команды передвижения. Чтобы двинуться в направление вправо, влево, вверх или вниз, напиши мне об этом чат!"
        print(message_1)
        return message_1
    
    def answer(self, from_model):
        if from_model[0] == 'movement':
            if from_model[1] == 'вниз':
                return ['movement', 'down']
            if from_model[1] == 'вверх':
                return ['movement', 'up']
            if from_model[1] == 'влево':
                return ['movement', 'left']
            if from_model[1] == 'вправо':
                return ['movement', 'right']
