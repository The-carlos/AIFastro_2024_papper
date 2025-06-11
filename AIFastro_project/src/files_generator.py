
import regex as re
# Dictionary of disciplines and their corresponding keywords for filtering
key_words_dict = {
    "Industrial design": [
        "brainstorm",
        "product",
        "materials",
        "manufacturing",
        "fabrication",
        "costs",
        "product life cycle",
        "aesthetics",
        "shape",
        "form",
        "texture",
        "color",
        "interaction",
        "usability",
        "modularity",
        "form follows function",
        "concept",
        "conceptual design",
        "ergonomic",
        "usability",
        "functionality",
        "prototype",
        "prototyping",
        "iterative design",
        "trans-disciplinary",
        "creative",
        "competitive advantage",
        "design process",
        "product development"
    ],
    "Communication Design": [
        "Data visualisation",
        "typography",
        "branding",
        "illustration",
        "information design",
        "motion graphics",
        "semiotics",
        "visual identity",
        "digital media",
        "printing",
        "advertising",
        "marketing",
        "content strategy",
        "editorial design",
        "graphic design",
        "multimedia",
        "storytelling",
        "engagement"
    ],
    "Interior Architecture and Interior Design": [
        "structural design",
        "remodelling",
        "structural regulations",
        "architectural integration",
        "acoustic design",
        "building code compliance",
        "spatial configuration",
        "adaptive reuse",
        "fire safety design",
        "aesthetic",
        "colour scheme",
        "furniture layout",
        "textiles",
        "ornamentation",
        "third space",
        "third place",
        "restoration"
    ],
    "Service design": [
        "Persona",
        "service blueprint",
        "user journey",
        "touchpoint",
        "storyboard",
        "service design"
    ],
    "Strategic Design": [
        "Business model canvas",
        "strategy design",
        "business design",
        "co-creation",
        "co-design",
        "iterative prototyping",
        "framework design"
    ],
    "User Interface design": [
        "digital product design",
        "human machine interaction",
        "human machine interface",
        "MMI",
        "UI",
        "user flow",
        "wireframe",
        "prototype",
        "information architecture",
        "accessibility",
        "low fidelity",
        "high fidelity",
        "user interface",
        "front-end"
    ],
    "User Experience Design (UX)": [
        "UX",
        "user experience",
        "empathy",
        "user persona",
        "user interaction",
        "user profile",
        "usability",
        "user journey",
        "experience design",
        "end user"
    ],
    "User research": [
        "qualitative research",
        "quantitative research",
        "evaluative research",
        "generative research",
        "concept testing",
        "usability testing",
        "survey",
        "user testing",
        "interviewing",
        "user interview",
        "shadowing",
        "ethnography",
        "diary study",
        "mental model",
        "insight"
    ],
    "Fashion design": [
        "spacesuit design",
        "fabric",
        "textile",
        "garment",
        "pattern",
        "clothes",
        "protective gear",
        "apparel",
        "aesthetics",
        "trend",
        "collection",
        "draping",
        "footwear",
        "tailoring",
        "accessories",
        "embroidery",
        "expression",
        "style"
    ],
    "Future foresight": [
        "Scenarios",
        "trend casting",
        "strategic foresight",
        "forecasting",
        "strategic planning",
        "innovation",
        "horizon scanning",
        "speculative design",
        "artefact",
        "dephi method",
        "megatrend",
        "design fiction",
        "cultural probe"
    ],
    "Engineering Design": [
        "Transdisciplinary",
        "detailed design",
        "ethical engineering",
        "Integrated Design",
        "Concept Engineering",
        "Concurrent Engineering",
        "Ethical engineering",
        "Double diamond method"
    ]
    # Puedes añadir más disciplinas y sus palabras clave aquí
    # "Otra Disciplina": ["palabra1", "palabra2", "palabra3", ...],
}

# List of CSV files to process
file_names = [
    'IAF_Papers_with_abstracts_Design.csv'
    #, 'IAF_Papers_with_abstracts_communication+design.csv'
]

# Path to the directory containing the files
path = '/AIFastro_project/'
path_to_save = '/AIFastro_project/filtered_data/'

import pandas as pd
import time

def load_dataframes(file_names, path):
    """
    Load multiple CSV files into a list of dataframes.

    Parameters:
    file_names (list): List of filenames to load.
    path (str): Path to the directory containing the files.

    Returns:
    list: A list of pandas dataframes loaded from the specified files.
    """
    dataframes_list = []
    for file in file_names:
        print(f"Loading {file}...")
        dataframes_list.append(pd.read_csv(path + file))
        print(f"{file} loaded successfully.")
        time.sleep(1)  # Simulate loading time for effect
    return dataframes_list

def count_keyword_occurrences(text, pattern):
    """
    Count the number of keyword occurrences in a given text.

    Parameters:
    text (str): The text to search.
    pattern (str): The regex pattern of keywords.

    Returns:
    int: The number of keyword occurrences.
    """
    return len(re.findall(pattern, text, flags=re.IGNORECASE))

def filter_and_export_dataframes(dataframes_list, key_words_dict, file_names, path_to_save):
    """
    Filter dataframes based on keywords in the 'Abstract' column and export the filtered dataframes to CSV files.

    Parameters:
    dataframes_list (list): List of dataframes to filter.
    key_words_dict (dict): Dictionary with disciplines as keys and keyword lists as values.
    file_names (list): List of filenames corresponding to the dataframes.
    path (str): Path to the directory where the filtered files will be saved.

    Returns:
    None
    """
    for discipline, key_words_list in key_words_dict.items():
        pattern = '|'.join(key_words_list)  # Combine keywords into a search pattern

        for i, df in enumerate(dataframes_list):
            print(f"Filtering {file_names[i]} for discipline: {discipline}...")
            filtered_df = df[df['Abstract'].str.contains(pattern, case=False, na=False)]

            if not filtered_df.empty:
                print(f"Matches found in {file_names[i]} for {discipline}: {len(filtered_df)}")
                print("Shape:")
                print(filtered_df.shape)

                # Add the 'coincidences' column
                filtered_df['coincidences'] = filtered_df['Abstract'].apply(lambda x: count_keyword_occurrences(x, pattern))

                output_file_name = f"{file_names[i].replace('.csv', '')}_{discipline.replace(' ', '_')}_filtered.csv"
                filtered_df.to_csv(path_to_save + output_file_name, index=False)
                print(f"Filtered data saved to {output_file_name}")
            else:
                print(f"No matches found in {file_names[i]} for {discipline}.")

            time.sleep(1)  # Simulate processing time for effect

# Load the dataframes
dataframes_list = load_dataframes(file_names, path)

# Filter and export the dataframes by discipline
filter_and_export_dataframes(dataframes_list, key_words_dict, file_names, path_to_save)

print("Data Scrapping & Filter process completed successfully! :) ")
