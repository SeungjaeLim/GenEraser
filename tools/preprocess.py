import pandas as pd

# Load the TSV file
input_file = "./data/unsmile_train_v1.0.tsv"  # Replace with your input file path
output_file = "./content.csv"  # Replace with your desired output file path
# Read the TSV file
df = pd.read_csv(input_file, delimiter='\t')

# Define a function to generate the "혐오내용설명" column
def generate_hate_description(row):
    hate_categories = ["여성/가족", "남성", "성소수자", "인종/국적", "연령", "지역", "종교", "기타 혐오", "악플/욕설"]
    description = []
    
    for category in hate_categories:
        if row[category] == 1:
            description.append(category)
    
    if description:
        return f"{', '.join(description)} 혐오 표현입니다."
    else:
        return "혐오 표현이 아닙니다."

# Apply the function to create the "혐오내용설명" column
df['혐오내용설명'] = df.apply(generate_hate_description, axis=1)

# Select the columns and reorder them as required
df_new = df[['문장', '혐오내용설명', 'clean']]

# Save the new dataframe to a TSV file
df_new.to_csv(output_file, index=False)

print(f"New file created: {output_file}")