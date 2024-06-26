import os
import openai
import argparse
from tqdm import tqdm
from config import KEY
openai.api_key = KEY

def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def chunk_text(text, chunk_size=1000):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def save_chunks_to_folder(chunks, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    chunk_paths = []
    for i, chunk in enumerate(chunks):
        chunk_path = os.path.join(folder_path, f'chunk_{i+1}.txt')
        with open(chunk_path, 'w') as file:
            file.write(chunk)
        chunk_paths.append(chunk_path)
    
    return chunk_paths

def generate_tuples_from_chunk(chunk):
    prompt = f"""
    You are an advanced text extraction model designed to identify and extract key-value-relation tuples from a given text. Your task is to read the provided text and identify the relationships between entities mentioned in the text. For each relationship, you will create a tuple in the format (subject, predicate, object) where:

    - Subject: The main entity involved in the relationship.
    - Predicate: The type of relationship or action connecting the subject and object.
    - Object: The secondary entity or value that is related to the subject.

    While extracting the tuples, follow these guidelines:

    1. Identify Entities: Recognize all significant entities in the text such as people, organizations, locations, dates, products, and any other notable items.
    2. Determine Relationships: Understand the relationships or actions that connect these entities. Look for verbs, prepositions, and conjunctions that signify relationships.
    3. Extract Attributes: Identify attributes related to entities, such as dates, quantities, and descriptive terms.
    4. Formulate Tuples: Create tuples in the format (subject, predicate, object) for each identified relationship or attribute. Ensure that each tuple accurately represents the information in the text.
    5. Handle Multiple Relationships: If an entity has multiple relationships or attributes, create separate tuples for each one.
    6. Contextual Understanding: Use contextual understanding to ensure that the relationships are meaningful and correctly interpreted.

    Examples:

    1. Example 1:
       - Text: "The capital of France is Paris. The population of Japan is 126.3 million."
       - Tuples: 
         - ("France", "capital", "Paris")
         - ("Japan", "population", "126.3 million")

    2. Example 2:
       - Text: "Barack Obama was born in Honolulu. He served as the 44th President of the United States."
       - Tuples:
         - ("Barack Obama", "born in", "Honolulu")
         - ("Barack Obama", "served as", "44th President of the United States")

    3. Example 3:
       - Text: "Microsoft was founded by Bill Gates and Paul Allen. It is headquartered in Redmond, Washington."
       - Tuples:
         - ("Microsoft", "founded by", "Bill Gates")
         - ("Microsoft", "founded by", "Paul Allen")
         - ("Microsoft", "headquartered in", "Redmond")
         - ("Redmond", "located in", "Washington")

    Task:

    Please provide the text from which you need key-value-relation tuples to be extracted. Follow the guidelines and examples above to accurately identify and extract the tuples.

    Text:
    {chunk}

    Tuples:
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a text extraction model."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7,
    )

    output = response['choices'][0]['message']['content'].strip()
    return output

def main(file_path, output_folder, output_file, chunk_size=1000):
    text = read_text_from_file(file_path)
    chunks = chunk_text(text, chunk_size)
    chunk_paths = save_chunks_to_folder(chunks, output_folder)
    
    all_tuples = []
    for chunk_path in tqdm(chunk_paths, desc="Processing chunks"):
        with open(chunk_path, 'r') as file:
            chunk = file.read()
        tuples = generate_tuples_from_chunk(chunk)
        all_tuples.append(tuples)
    
    with open(output_file, 'w') as file:
        for idx, t in enumerate(all_tuples):
            file.write(f"Tuples from chunk {idx+1}:\n")
            file.write(f"{t}\n\n")
    
    return all_tuples

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate key-value-relation tuples from a text file.")
    parser.add_argument("file_path", type=str, help="Path to the input text file.")
    parser.add_argument("output_folder", type=str, help="Folder to save the text chunks.")
    parser.add_argument("output_file", type=str, help="File to save the generated tuples.")
    parser.add_argument("--chunk_size", type=int, default=2000, help="Size of each text chunk.")
    
    args = parser.parse_args()
    
    tuples = main(args.file_path, args.output_folder, args.output_file, args.chunk_size)
    for idx, t in enumerate(tuples):
        print(f"Tuples from chunk {idx+1}:")
        print(t)
        print()
