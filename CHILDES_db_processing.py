# Dake Peng, LING 275, Carleton College, WI 24
# A simple code to handle exports from the CHILDES database
# Usage: 
# 1. place your downloaded export file in the same folder as this code
# 2. replace the input_file_path variable and enter an appropriate graph title
# 3. run the code

#splits the input file into different groups
def filter_conversations(input_file_path):
    with open(input_file_path, 'r') as input_file:
        # Read all lines
        all_lines = input_file.readlines()
        
        child_lines = []
        mother_and_interviewer_lines = []
        grammar_lines = [[]]
        morphology_lines = [[]]
        line_number = 0
        
        for line in all_lines:
            tmp = line
            if "\t" in line:
                tmp = line.split("\t")[1]
            line_array = tmp.split(" ")
            
            if "%gra" in line:                        
                grammar_lines[line_number] = line_array
                continue
            
            if "%mor" in line:
                if "\n" in line_array[-1]:
                    line_array = line_array[0:-1]
                morphology_lines[line_number] = line_array
                continue
            
            if ("*CHI" in line) or ("*INV" in line) or ("*MOT" in line):
                line_number += 1
                grammar_lines.append([])
                morphology_lines.append([])
                line_array.insert(0, line_number)
                
            if "*CHI" in line:
                child_lines.append(line_array)
            elif "*INV" in line:
                mother_and_interviewer_lines.append(line_array)
            elif "*MOT" in line:
                mother_and_interviewer_lines.append(line_array)
                
    return (child_lines, mother_and_interviewer_lines, grammar_lines, morphology_lines)

#prints the total #words and #utterances of a target group;
#draws a frequency graph fot it.
def count_words(target, morphology_lines, graph_title):
    total_word_count = 0
    frequencies = []
    for line in target:
        line_number = line[0]
        grammar_line = morphology_lines[line_number]
        num_words_in_line = len(grammar_line);
        total_word_count+= num_words_in_line
        frequencies.append(num_words_in_line)
    graph_frequency(frequencies, graph_title)
    print("total word count: " + str(total_word_count))
    print("total utterances: " + str(len(target)))
    
def graph_frequency(data, graph_title): 
    import numpy as np
    import matplotlib.pyplot as plt
    from collections import Counter
    # Calculate mean and standard deviation
    mean_value = np.mean(data)
    std_dev = np.std(data)

    # Create a histogram
    plt.hist(data, bins=20, alpha=0.7, color='blue', edgecolor='black')

    # Add mean and std deviation lines
    plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_value:.2f}')
    plt.axvline(mean_value + std_dev, color='green', linestyle='dashed', linewidth=2, label=f'Std Dev: {std_dev:.2f}')
    plt.axvline(mean_value - std_dev, color='green', linestyle='dashed', linewidth=2)

    # Add labels and legend
    plt.xlabel('#words in utterance')
    plt.ylabel('Frequency')
    plt.legend()
    
    plt.title(graph_title)

    # Show the plot
    plt.show()
    
    
if __name__ == "__main__":    
    input_file_path = 'shem_020404.txt'  # Replace with your input file path
    (child_lines, mother_and_interviewer_lines, grammar_lines, morphology_lines) = filter_conversations(input_file_path)
    graph_title = "Frequency of Utterance Length (#words), Child" # Replace with your title
    count_words(child_lines, morphology_lines, graph_title)
    