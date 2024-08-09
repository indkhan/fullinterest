import time
import random
import os
import threading
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_random_paragraph():
    paragraphs = [
        "The sun slowly dipped below the horizon, painting the sky in vibrant hues of orange and pink. As twilight settled in, the city came alive with twinkling lights and the gentle hum of evening activities. People hurried home from work, while others ventured out to enjoy the cool evening air and the promise of nocturnal adventures.",
        "In the depths of the ancient forest, a hidden ecosystem thrived undisturbed by human interference. Towering trees reached towards the sky, their branches intertwining to create a lush canopy overhead. Beneath the verdant foliage, a myriad of creatures scurried about their daily routines, each playing a vital role in the delicate balance of nature.",
        "The bustling laboratory was a hive of activity as scientists worked tirelessly on their latest breakthrough. Intricate equipment hummed and beeped, while computer screens displayed complex data and simulations. Years of research had led to this moment, and the team was on the brink of a discovery that could revolutionize modern medicine and improve countless lives.",
        "As the spacecraft hurtled through the cosmos, the crew marveled at the breathtaking view of distant galaxies and nebulae. The vastness of space stretched out before them, a reminder of humanity's small place in the universe. Despite the inherent dangers of their mission, each member felt a sense of purpose and excitement at the prospect of expanding human knowledge and exploration.",
        "The old bookshop stood as a testament to the enduring power of literature in a world increasingly dominated by digital media. Dusty shelves lined the walls, packed with volumes ranging from ancient tomes to contemporary bestsellers. The musty scent of aged paper mingled with the aroma of freshly brewed coffee, creating an inviting atmosphere for bibliophiles and casual readers alike."
    ]
    return random.choice(paragraphs)

def calculate_wpm(start_time, end_time, typed_text):
    elapsed_time = end_time - start_time
    words = len(typed_text.split())
    wpm = (words / elapsed_time) * 60
    return round(wpm, 2)

def calculate_accuracy(original_text, typed_text):
    original_words = original_text.split()
    typed_words = typed_text.split()
    correct_words = sum(1 for orig, typed in zip(original_words, typed_words) if orig == typed)
    accuracy = (correct_words / len(original_words)) * 100
    return round(accuracy, 2)

def calculate_cpm(start_time, end_time, typed_text):
    elapsed_time = end_time - start_time
    characters = len(typed_text)
    cpm = (characters / elapsed_time) * 60
    return round(cpm, 2)

def display_text(text, user_input):
    words = text.split()
    user_words = user_input.split()
    display = ""
    for i, word in enumerate(words):
        if i < len(user_words):
            if word == user_words[i]:
                display += f"\033[92m{word}\033[0m "  # Green for correct words
            else:
                display += f"\033[91m{word}\033[0m "  # Red for incorrect words
        elif i == len(user_words):
            display += f"\033[1m{word}\033[0m "  # Bold for current word
        else:
            display += f"{word} "
    return display.strip()

def run_typing_test():
    total_tests = 0
    total_wpm = 0
    total_accuracy = 0
    total_cpm = 0

    while True:
        clear_screen()
        print("Welcome to the Advanced Typing Speed Test!")
        print("Type the following paragraph as quickly and accurately as you can.")
        print("The timer will start when you begin typing.")
        print("Press Enter without typing to see your results.\n")

        test_paragraph = get_random_paragraph()
        print(test_paragraph + "\n")

        input("Press Enter when you're ready to start...")
        clear_screen()

        user_input = ""
        start_time = None

        while True:
            clear_screen()
            print(display_text(test_paragraph, user_input))
            print("\n" + "-" * 50 + "\n")
            print(user_input)

            if start_time is None:
                start_time = time.time()

            char = sys.stdin.read(1)
            if char == '\n':
                break
            user_input += char

        end_time = time.time()

        if not user_input:
            print("No input detected. Test cancelled.")
            continue

        wpm = calculate_wpm(start_time, end_time, user_input)
        accuracy = calculate_accuracy(test_paragraph, user_input)
        cpm = calculate_cpm(start_time, end_time, user_input)

        total_tests += 1
        total_wpm += wpm
        total_accuracy += accuracy
        total_cpm += cpm

        clear_screen()
        print(f"Your results:")
        print(f"Words per minute (WPM): {wpm}")
        print(f"Characters per minute (CPM): {cpm}")
        print(f"Accuracy: {accuracy}%")

        if total_tests > 1:
            print(f"\nAverage results over {total_tests} tests:")
            print(f"Average WPM: {round(total_wpm / total_tests, 2)}")
            print(f"Average CPM: {round(total_cpm / total_tests, 2)}")
            print(f"Average Accuracy: {round(total_accuracy / total_tests, 2)}%")

        retry = input("\nWould you like to try again? (y/n): ").lower()
        if retry != 'y':
            break

    print("\nThank you for using the Advanced Typing Speed Test!")

if __name__ == "__main__":
    run_typing_test()
