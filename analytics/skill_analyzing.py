import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from gensim.models import Word2Vec
import re

# Function to preprocess skills
def preprocess_skills(requirements):
    """
    Split and clean skill requirements into individual skills.
    """
    return [re.sub(r"[^\w\s]", "", skill.strip()).lower() for skill in requirements.split(",") if skill.strip()]

# Process skills into a transactional format
def prepare_transactions(df, column):
    """
    Convert the skills in the 'requirement' column to transactional data for association rules.
    """
    df['skills_list'] = df[column].dropna().apply(preprocess_skills)
    transactions = df['skills_list'].tolist()
    return transactions

# Generate association rules using Apriori
def generate_association_rules(transactions, min_support=0.01, min_confidence=0.5):
    """
    Generate association rules from transactional data using the Apriori algorithm.
    """
    # Convert transactions into a one-hot-encoded DataFrame
    all_skills = set(skill for transaction in transactions for skill in transaction)
    encoded_data = pd.DataFrame([{skill: (skill in transaction) for skill in all_skills} for transaction in transactions])
    
    # Use Apriori to find frequent itemsets
    frequent_itemsets = apriori(encoded_data, min_support=min_support, use_colnames=True)
    
    # Generate association rules
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    return rules

# Train Word2Vec for skill embeddings
def train_word2vec(transactions):
    """
    Train a Word2Vec model on the list of skill transactions.
    """
    model = Word2Vec(sentences=transactions, vector_size=50, window=5, min_count=1, workers=4)
    return model

# Recommend related skills
def recommend_skills(rules, word2vec_model, input_skills):
    """
    Recommend skills based on association rules and Word2Vec similarity.
    """
    # Find associated skills via rules
    associated_skills = set()
    for skill in input_skills:
        matches = rules[rules['antecedents'].apply(lambda x: skill in x)]
        for consequent in matches['consequents']:
            associated_skills.update(consequent)
    
    # Find similar skills using Word2Vec
    similar_skills = set()
    for skill in input_skills:
        if skill in word2vec_model.wv:
            similar_skills.update([word for word, _ in word2vec_model.wv.most_similar(skill)])
    
    # Combine and return unique recommendations
    return list(associated_skills.union(similar_skills) - set(input_skills))

# # Example Workflow
# if __name__ == "__main__":
#     # Load sample data
#     data = {
#         "requirement": [
#             "Interpersonal Skills, English, Analyzing skills, Backend Developer",
#             "English, Strong Leadership Skills, Product Development",
#             "Backend Developer, Data Structures, Critical Thinking",
#             "Nosql, Data Modeling, Cloud Infrastructure, nodejs",
#             "English, Financial Literacy, Stakeholder Management"
#         ]
#     }
#     df = pd.DataFrame(data)
    
#     # Preprocess skills and prepare transactions

#     transactions = prepare_transactions(df, "requirement")
    
#     # Generate association rules
#     rules = generate_association_rules(transactions, min_support=0.2, min_confidence=0.6)
    
#     # Train Word2Vec model
#     word2vec_model = train_word2vec(transactions)
    
#     # Input skills
#     input_skills = ["english", "backend developer"]
    
#     # Recommend additional skills
#     recommendations = recommend_skills(rules, word2vec_model, input_skills)
#     print("Recommended skills:", recommendations)
