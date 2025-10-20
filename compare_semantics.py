# import google.generativeai as genai
import numpy as np
import os

# Set the environment variable before importing TensorFlow
# #You may see slightly different numerical results due to floating-point round-off errors from different computation orders. 
# To turn them off
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# disable warning - he name tf.losses.sparse_softmax_cross_entropy is deprecated. 
# Please use tf.compat.v1.losses.sparse_softmax_cross_entropy instead.
# This method does not work for the mentioned warning because 
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppresses INFO, WARNING, and ERROR logs

from sentence_transformers import SentenceTransformer, losses
import keyboard
import threading
import torch

# Set your API key here or via environment variable
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load a pre-trained model (free and local)
#model_name = 'all-MiniLM-L6-v2'
model_name = 'all-mpnet-base-v2'
model = SentenceTransformer(model_name)
loss = losses.MultipleNegativesRankingLoss(model)

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

def compare_semantics(str1, str2):
    print(f"Input strings: str1='{str1}', str2='{str2}'")
    try:
        # result = genai.embed_content(model="models/embedding-001", content=[str1, str2], task_type="SEMANTIC_SIMILARITY")
        # print(f"API result keys: {result.keys()}")
        # vec1, vec2 = np.array(result['embedding'][0]), np.array(result['embedding'][1])
        embeddings = model.encode([str1, str2])
        vec1, vec2 = np.array(embeddings[0]), np.array(embeddings[1])
        print(f"Vec1 shape: {vec1.shape}, Vec2 shape: {vec2.shape}")
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        print(f"Similarity: {similarity}")
        return similarity
    except Exception as e:
        print(f"Error in compare_semantics: {e}")
        return None


# Shared flag to signal exit
exit_flag = False

def monitor_ctrl_x():
    global exit_flag
    while True:
        if keyboard.is_pressed('ctrl+x'):
            #print("\nCTRL + X detected. Breaking loop...")
            exit_flag = True
            break

def main():

    # Start the monitoring thread
    threading.Thread(target=monitor_ctrl_x, daemon=True).start()
    # prints the name of the loaded model
    print(f"Model name: {model_name}") 
    print(f"Model device: {model.device}") 

    while True:
        print("Provide 2 strings for semantic comparison")
        str1 = input("First string: ")
        str2 = input("Second string: ")
        result = compare_semantics(str1, str2)
        if result is not None:
            print(f"The strings are {result * 100:.2f} % similar")
        else:
            print("Failed to compute similarity")
        
        if exit_flag:
            print("CTRL + X detected. Exiting...")
            break

if __name__ == "__main__":
    main()