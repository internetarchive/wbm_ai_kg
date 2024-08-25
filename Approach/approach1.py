import openai
import os
import argparse
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import KEY
openai.api_key = KEY

def extract_timestamp(file_path):
    file_name = os.path.basename(file_path)
    try:
        return file_name.split('_')[1].split('.')[0]
    except IndexError:
        print(f"Error: The filename '{file_name}' does not match the expected format.")
        return None


def save_result_to_file(content, file1_timestamp, file2_timestamp):
    """Save the content to a file with a name that includes the timestamps."""
    file_name = f"ResultV1_{file1_timestamp}_VS_{file2_timestamp}.txt"
    with open(file_name, 'w') as file:
        file.write(content)
    print(f"Result saved to {file_name}")

def analyze_text_differences(file1_path, file2_path):
    # Read the contents of the files
    with open(file1_path, 'r') as file:
        text_file_1 = file.read()

    with open(file2_path, 'r') as file:
        text_file_2 = file.read()

    # Extract the timestamps from the file paths
    file1_timestamp = extract_timestamp(file1_path)
    file2_timestamp = extract_timestamp(file2_path)

    if file1_timestamp is None or file2_timestamp is None:
        print("Error: Unable to extract timestamps from one or both file paths.")
        return

    # Example content for the initial and updated text files
    example_text_file_1_a = """\
    This is the original content of the website.
    It contains some initial information.
    """

    example_text_file_2_a = """\
    This is the updated content of the website.
    It contains some additional information and some modifications.
    """

    example_text_file_1_b = """\
    Breaking News: Major Earthquake Hits City

    A major earthquake with a magnitude of 7.8 has struck the city, causing significant damage to buildings and infrastructure. Early reports indicate that several buildings have collapsed, and there are numerous injuries. Emergency services are responding to the scene, and people are advised to stay away from affected areas.

    Initial estimates suggest that the earthquake struck at 10:45 AM local time, and aftershocks are expected. The city’s mayor has declared a state of emergency and urged citizens to remain calm and follow official instructions.
    """

    example_text_file_2_b = """\
    Breaking News: Major Earthquake Hits City, Casualties Reported

    A devastating earthquake with a magnitude of 7.8 has struck the city, causing extensive damage to buildings and infrastructure. Updated reports confirm that multiple buildings have collapsed, and there are numerous casualties, including fatalities. Emergency services are working tirelessly to rescue those trapped under the rubble.

    The earthquake struck at 10:45 AM local time, followed by several powerful aftershocks. The city’s mayor has declared a state of emergency, urging citizens to remain calm and follow official instructions. The national government has also mobilized additional resources to aid in the rescue and relief efforts.
    """

    # Example structure of the desired output
    example_output_a = {
        "introduction": "This report analyzes the differences between two versions of website content from different timestamps.",
        "summary_of_changes": "The updated version includes additional information and modifications to the existing content.",
        "significance_of_changes": "The changes are significant, as they add new details and modify existing information.",
        "detailed_analysis": {
            "additions": [
                "Added: 'It contains some additional information.'"
            ],
            "modifications": [
                "Original: 'It contains some initial information.'",
                "Updated: 'It contains some additional information and some modifications.'"
            ],
            "deletions": []
        },
        "reasons_for_changes": "The changes might have been made to provide more comprehensive information and to update the content.",
        "impact_on_user_perception": "The updates could improve user understanding and provide more relevant information."
    }

    example_output_b = {
        "introduction": "This report analyzes the differences between two versions of a news article reporting on a major earthquake in a city.",
        "summary_of_changes": "The updated version includes additional information about casualties and the involvement of the national government in rescue efforts.",
        "significance_of_changes": "The changes are significant, as they provide more detailed information on the impact of the earthquake and the ongoing rescue operations.",
        "detailed_analysis": {
            "additions": [
                "Added: 'Updated reports confirm that multiple buildings have collapsed, and there are numerous casualties, including fatalities.'",
                "Added: 'The national government has also mobilized additional resources to aid in the rescue and relief efforts.'"
            ],
            "modifications": [
                "Original: 'Early reports indicate that several buildings have collapsed, and there are numerous injuries.'",
                "Updated: 'Updated reports confirm that multiple buildings have collapsed, and there are numerous casualties, including fatalities.'"
            ],
            "deletions": []
        },
        "reasons_for_changes": "The changes might have been made to provide more comprehensive and updated information as more details became available.",
        "impact_on_user_perception": "The updates could significantly impact user perception by highlighting the severity of the earthquake and the scale of the response efforts."
    }

    # Create the prompt for the API
    prompt = f"""
    Analyze the differences between the two texts extracted from different timestamps of the same website.

    Text File 1:
    {text_file_1}

    Text File 2:
    {text_file_2}

    Provide a detailed analysis report including:
    1. Introduction
    2. Summary of Changes
    3. Significance of Changes
    4. Detailed Analysis
    5. Possible Reasons for Changes
    6. Impact on User Perception

    Example 1:
    Text File 1:
    {example_text_file_1_a}

    Text File 2:
    {example_text_file_2_a}

    Example Output:
    Introduction: {example_output_a['introduction']}
    Summary of Changes: {example_output_a['summary_of_changes']}
    Significance of Changes: {example_output_a['significance_of_changes']}
    Detailed Analysis:
        Additions: {example_output_a['detailed_analysis']['additions']}
        Modifications: {example_output_a['detailed_analysis']['modifications']}
        Deletions: {example_output_a['detailed_analysis']['deletions']}
    Possible Reasons for Changes: {example_output_a['reasons_for_changes']}
    Impact on User Perception: {example_output_a['impact_on_user_perception']}

    Example 2:
    Text File 1:
    {example_text_file_1_b}

    Text File 2:
    {example_text_file_2_b}

    Example Output:
    Introduction: {example_output_b['introduction']}
    Summary of Changes: {example_output_b['summary_of_changes']}
    Significance of Changes: {example_output_b['significance_of_changes']}
    Detailed Analysis:
        Additions: {example_output_b['detailed_analysis']['additions']}
        Modifications: {example_output_b['detailed_analysis']['modifications']}
        Deletions: {example_output_b['detailed_analysis']['deletions']}
    Possible Reasons for Changes: {example_output_b['reasons_for_changes']}
    Impact on User Perception: {example_output_b['impact_on_user_perception']}
    """

    # Make the API request to OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Extract the timestamps from the file paths
    file1_timestamp = extract_timestamp(file1_path)
    file2_timestamp = extract_timestamp(file2_path)

    # Print the analysis report and save to a file
    if response:
        result_content = response['choices'][0]['message']['content'].strip()
        print("Analysis Report:")
        print(result_content)
        save_result_to_file(result_content, file1_timestamp, file2_timestamp)
    else:
        print("Request failed.")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Analyze text differences between two files.")
    parser.add_argument("file1", help="Path to the first text file")
    parser.add_argument("file2", help="Path to the second text file")
    args = parser.parse_args()



    analyze_text_differences(args.file1, args.file2)

if __name__ == "__main__":
    main()
