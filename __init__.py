from vasisualy.skills.vas_skill.vas_skill import Skill  # Импорт родительского класса навыков
import os
import random
from . import animals_descs

animals = animals_descs.animals
animal_naming = ("Оно", "Животное", "Это животное", "Моё животное")


class GuessTheAnimal(Skill):

    def temp_dir(self):
        tmp = super(GuessTheAnimal, self).get_temp_dir()
        return tmp
    
    def first_run(self, user_message):
        # Вызывается при активации триггера, затем навык перехватывает ввод пользователя.
        if super(GuessTheAnimal, self)._is_triggered(user_message, super(GuessTheAnimal, self)._get_triggers()):
            animals_keys = []

            for i in animals.keys():
                animals_keys.append(i)
            animal = random.choice(animals_keys)

            with open(f"{self.temp_dir()}/.animal", 'w') as f:
                f.write(animal)

            descriptions = animals[animal].split("/")
            first_description = random.choice(descriptions)
            descriptions.remove(first_description)
            second_description = random.choice(descriptions)
            descriptions.remove(second_description)

            with open(f"{self.temp_dir()}/.descriptions", 'w') as f:
                for description in descriptions:
                    f.write(description + "\n")

            toSpeak = f"Я загадал какое-то животное, тебе нужно отгадать его по моему описанию. {random.choice(animal_naming)} {first_description} и {second_description}. Если тебе нужна подсказка - скажи \"подсказка\"."

            super(GuessTheAnimal, self).run_loop()  # Активация цикла навыка.

            return toSpeak
        else:
            return ''

    def main(self, user_message):
        # Вызывается, когда навык активирован и существует файл блокировки, перехватывает
        # все сообщения, введённые пользователем.
        with open(f"{self.temp_dir()}/.animal", 'r') as f:
            animal = f.read()

        if super(GuessTheAnimal, self)._is_triggered_to_exit(user_message, super(GuessTheAnimal, self)._get_exit_triggers()):
            toSpeak = "Завершение работы навыка..."

            super(GuessTheAnimal, self).exit_loop()  # Завершение цикла.

            return toSpeak

        elif ("подсказка" in user_message) or ("Подсказка" in user_message):
            with open(f"{self.temp_dir()}/.descriptions", 'r') as f:
                descriptions = []
                lines = f.read()

                if lines:
                    lines = lines.split("\n")
                    for line in lines:
                        if line: descriptions.append(line)

            s_description = random.choice(descriptions) if len(descriptions) else None
            toSpeak = f"{random.choice(animal_naming)} {s_description}." if s_description else "Подсказок больше нет!"
            if s_description: descriptions.remove(s_description)

            with open(f"{self.temp_dir()}/.descriptions", 'w') as f:
                for description in descriptions:
                    f.write(description + '\n')

            return toSpeak

        elif animal in user_message.lower():
            toSpeak = "Поздравляю, я загадал именно это животное!"

            super(GuessTheAnimal, self).exit_loop()  # Завершение цикла.

            # Удаление временных файлов.
            os.remove(f"{self.temp_dir()}/.animal")
            os.remove(f"{self.temp_dir()}/.descriptions")
            return toSpeak

        else:
            toSpeak = random.choice(("Не правильно я загадал другое животное.", "Нет.", "Неправильно.", "Я загадал не это."))
            return toSpeak

def main(user_message):
    skill = GuessTheAnimal("guess_the_animal", user_message, loop=True)  # Вывод сообщения, переданного навыком, пользователю.
    return skill.first_run(user_message)

def loop(user_message):
    skill = GuessTheAnimal("guess_the_animal", user_message, loop=True)
    return skill.main(user_message)
