import openai
import os
import argparse
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import KEY
openai.api_key = KEY

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def format_prompt(version1, version2): # no need to give instruction in one go. <message + input>
    prompt = f"""
You are given two versions of text files, each containing a set of tuples that represent extracted relationships between entities. The format of each tuple is (key, value, relation, typeofkey, typeofvalue). Your task is to analyze these tuples and provide a comprehensive comparison of the two versions. Specifically, focus on the following points:

1. Identify Differences:
   - Highlight any differences between the tuples in the two versions. This includes changes in entities, relationships, or attributes.
   - Note any additions or deletions of tuples that represent new or removed information.

2. Evaluate Major Edits:
   - Determine significant changes that alter the meaning or context of the information. This could include changes in the nature of relationships (e.g., from "thing" to "event"), shifts in entity roles (e.g., from "person" to "group"), or any other critical edits.
   - Provide an explanation of the possible reasons behind these changes. For example, were they likely made to correct factual errors, update outdated information, or change the narrative focus?

3. Interpret the Versions Independently:
   - Analyze each version separately to understand the narrative or informational intent behind the tuples. What message or story does each version try to convey?
   - Discuss any implications or conclusions that can be drawn from each version. For instance, how does the information in each version shape the reader’s perception of events or entities involved?

4. Overall Summary:
   - Summarize the overall differences between the two versions, focusing on the impact of the edits. What do these changes suggest about the evolution of the content?
   - Mention any patterns or trends observed, such as shifts in focus, tone, or level of detail.

5. Additional Insights:
   - Highlight any other notable observations that may not directly relate to the differences but are important for understanding the context of the edits. This could include changes in consistency, clarity, or bias.

### Version 1 Tuples:
{version1}

### Version 2 Tuples:
{version2}

Provide your analysis in a structured and professional manner, using evidence from the tuples to support your conclusions.
    """
    return prompt

def extract_timestamp(file_path):
    """Extract timestamp from the file path."""
    return os.path.basename(file_path).split('_')[1].split('.')[0]

def save_result_to_file(content, file1_timestamp, file2_timestamp):
    """Save the content to a file with a name that includes the timestamps."""
    file_name = f"ResultV2.1_{file1_timestamp}_VS_{file2_timestamp}.txt"
    with open(file_name, 'w') as file:
        file.write(content)
    print(f"Result saved to {file_name}")


def generate_output_filename(file1_path, file2_path):
    # Extract the end numbers from the file paths
    file1_end = os.path.basename(file1_path).split('_')[-1].split('.')[0]
    file2_end = os.path.basename(file2_path).split('_')[-1].split('.')[0]

    # Generate the output file name
    output_filename = f"ResultV2_{file1_end}_VS_{file2_end}.txt"
    return output_filename

def analyze_versions(file1_path, file2_path):
    # Read the contents of the files
    version1 = read_file(file1_path)
    version2 = read_file(file2_path)

    # Format the prompt with the file contents
    prompt = format_prompt(version1, version2)

    # Prepare messages for ChatCompletion
    messages = [
        {"role": "system", "content": "You are a professional content analyst."},
        {"role": "user", "content": prompt}
    ]

    # Make the API request to OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Choose the model you want to use
        messages=messages,
        # max_tokens=1500,  # Adjust token limit as needed
        # temperature=0.5  # Adjust temperature for creativity level
    )

    # Extract the response from the API
    result = response.choices[0].message["content"].strip()

    # Generate the output file name
    output_filename = generate_output_filename(file1_path, file2_path)

    # Save the result to a text file
    with open(output_filename, 'w') as file:
        file.write(result)

    print(f"Result saved to {output_filename}")


def analyze_versions2(file1_path, file2_path):
    # Read the contents of the files
    with open(file1_path, 'r') as file:
        text_file_1 = file.read()

    with open(file2_path, 'r') as file:
        text_file_2 = file.read()

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
    7. Jaccard Index between two text files

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
        # max_tokens=1500,
        # temperature=0.7,
        # top_p=1.0,
        # frequency_penalty=0.0,
        # presence_penalty=0.0
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


# Example usage:

# Define the file paths
# file1_path = "/home/aura/gsoc/wbm_ai_kg/PageExtraction/channel/20240729191002/content_20240729191002.txt"
# file2_path = "/home/aura/gsoc/wbm_ai_kg/PageExtraction/channel/20240805015159/content_20240805015159.txt"

# analyze_versions(file1_path, file2_path)
# analyze_versions2(file1_path, file2_path)


def main():
    parser = argparse.ArgumentParser(description='Analyze differences between two text files using OpenAI API.')
    parser.add_argument('file1', type=str, help='Path to the first Tuple file')
    parser.add_argument('file2', type=str, help='Path to the second Tuple file')

    args = parser.parse_args()

    openai.api_key = KEY

    analyze_versions(args.file1, args.file2)

if __name__ == '__main__':
    main()