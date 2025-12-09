#Professor assistant program
#Created by: Chaudhary Sanjana
#This program will help professor to creat exams from a question bank
import random
import os

def load_question_bank(file_path):
    """
    Reads the question bank file and returns a list of (question, answer) tuples.
    Each question is followed by its answer on the next line.
    
    Args:
        file_path (str): The path to the question bank file.

    Returns:
        list: A list of (question, answer) tuples, or None if the file is not found/readable.
    """
    qa_pairs = []
    try:
        # Using 'with' ensures the file is closed properly
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # Process lines in pairs (question followed by answer)
            for i in range(0, len(lines), 2):
                question = lines[i].strip()
                # Ensure there is a corresponding answer line
                if i + 1 < len(lines):
                    answer = lines[i+1].strip()
                    if question and answer: # Only add non-empty pairs
                        qa_pairs.append((question, answer))
        
        return qa_pairs

    except FileNotFoundError:
        print(f"\nERROR: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"\nAn unexpected error occurred while reading the file: {e}")
        return None

def create_exam(professor_name, qa_bank):
    """
    Asks the professor for exam details, randomly selects questions, and saves the exam.
    
    Args:
        professor_name (str): The name of the professor.
        qa_bank (list): The list of (question, answer) pairs from the bank.
    """
    
    # Check if the question bank is empty
    if not qa_bank:
        print("\nCannot create an exam. The question bank is empty or could not be loaded correctly.")
        return

    # 1. Get the desired number of questions
    while True:
        try:
            max_questions = len(qa_bank)
            print(f"\nThere are {max_questions} question-answer pairs available in the bank.")
            num_questions_str = input(f"How many question-answer pairs do you want to include in your exam (1 to {max_questions})? ")
            num_questions = int(num_questions_str)
            
            if 1 <= num_questions <= max_questions:
                break
            else:
                print(f"Please enter a number between 1 and {max_questions}.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # 2. Get the output file name
    while True:
        output_file = input("Where do you want to save your exam? ")
        if output_file.strip():
            break
        print("The output file name cannot be empty.")
        
    # 3. Randomly select questions
    # Use random.sample for selection without replacement
    selected_pairs = random.sample(qa_bank, num_questions)
    
    # 4. Save the exam to the output file
    try:
        # Using 'w' to write/overwrite the file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(f"--- Exam for Professor {professor_name} ---\n")
            outfile.write(f"--- Number of Questions: {num_questions} ---\n\n")
            
            for i, (question, answer) in enumerate(selected_pairs, 1):
                # Save the question
                outfile.write(f"Question {i}: {question}\n")
                # Save the answer (Optional: You might want to save answers to a separate 'key' file
                # but based on the prompt's focus on the pair, we'll keep it together for simplicity, 
                # or you can comment out the answer for a standard exam sheet)
                outfile.write(f"Answer {i}: {answer}\n") 
                outfile.write("-" * 30 + "\n")
                
        print(f"\nCongratulations Professor {professor_name}. Your exam is created and saved in {output_file}.")
        
    except IOError as e:
        print(f"\nERROR: Could not write to the file {output_file}. Details: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred during exam creation: {e}")


def professor_assistant():
    """
    The main execution function for the Professor Assistant program.
    """
    print("Welcome to professor assistant version 1.0.")
    
    # Get Professor's Name
    professor_name = input("Please Enter Your Name: ").strip()
    
    if not professor_name:
        print("Hello! Since you didn't enter a name, I'll call you Professor.")
        professor_name = "Professor"
    else:
        # Capitalize the first letter for a nice greeting if the user didn't
        professor_name = professor_name.title()

    print(f"Hello Professor {professor_name}, I am here to help you create exams from a question bank.")
    
    # Main loop for creating one or more exams
    while True:
        # Ask if they want to create an exam
        create_choice = input("Do you want me to help you create an exam (Yes to proceed | No to quit the program)? ").strip().lower()

        if create_choice in ['no', 'n']:
            print(f"Thank you professor {professor_name}. Have a good day!")
            break
        
        elif create_choice in ['yes', 'y']:
            # Get the Question Bank Path
            while True:
                question_bank_path = input("Please Enter the Path to the Question Bank. ").strip()
                if not question_bank_path:
                    print("Path cannot be empty. Please try again.")
                    continue
                    
                # Load the question bank
                qa_bank = load_question_bank(question_bank_path)
                
                if qa_bank is not None:
                    print("Yes, indeed the path you provided includes questions and answers.")
                    
                    # Proceed to create the exam
                    create_exam(professor_name, qa_bank)
                    break # Exit the question bank path loop and move to the 'another exam' question
                else:
                    # qa_bank is None, meaning an error occurred (e.g., File Not Found)
                    print("Please check the path and try again.")
            
            # Ask if they want to create another exam
            another_exam_choice = input("Do you want me to help you create another exam (Yes to proceed | No to quit the program)? ").strip().lower()
            
            if another_exam_choice in ['no', 'n']:
                print(f"Thank you professor {professor_name}. Have a good day!")
                break # Exit the main while loop
            
            # If 'yes' or any other input, the loop continues to the start.
            
        else:
            print("Invalid input. Please answer with 'Yes' or 'No'.")


if __name__ == "__main__":
    professor_assistant()