# Compare Semantics

## Description

This script computes the semantic similarity between two input strings using sentence embeddings. It leverages a pre-trained transformer model to encode strings into vectors and calculates cosine similarity, providing a percentage match. The script is designed for interactive use, allowing users to input strings repeatedly until manually exited.

## Installation

Ensure dependencies are installed: `pip install sentence-transformers numpy keyboard`.

## Usage

1. Execute: `python compare_semantics.py`.
2. Follow prompts to enter strings; press Ctrl+X to exit.

## Dependencies

- `sentence_transformers`: For loading the 'all-MiniLM-L6-v2' model and encoding strings.
- `numpy`: For array operations and similarity calculation.
- `keyboard`: For detecting key presses (Ctrl+X).
- `threading`: For running the exit monitor in a daemon thread.
- `os`: For setting environment variables (TF_ENABLE_ONEDNN_OPTS to suppress warnings).

## How It Works

- **Core Operation**: Encodes two strings into embeddings via the SentenceTransformer model, computes cosine similarity (dot product normalized by vector norms), and returns a similarity score between 0 and 1.
- **Interactive Loop**: Runs in a continuous loop prompting for two strings, displaying the similarity as a percentage (e.g., "85.42% similar"), and handling errors gracefully.
- **Exit Mechanism**: Monitors for Ctrl+X key press in a background thread to allow graceful termination.
- **Error Handling**: Catches exceptions during embedding or computation, printing errors and returning None.

## Key Functions

- `compare_semantics(str1, str2)`: Main function that encodes inputs, computes similarity, and returns the score. Prints debug info (inputs, vector shapes, similarity).
- `monitor_ctrl_x()`: Threaded function that sets a global exit flag on Ctrl+X detection.
- `main()`: Entry point that starts the monitoring thread and runs the input loop.

No classes; uses global variables like `exit_flag` for thread communication.

## Input/Output

- **Input**: Two strings provided interactively via `input()` prompts ("First string:" and "Second string:").
- **Output**:
  - Debug prints: Input strings, vector shapes, similarity value.
  - Result: Similarity as a percentage (e.g., "The strings are 85.42% similar") or "Failed to compute similarity" on error.
  - Exit message: "CTRL + X detected. Exiting..." on termination.

## Command-Line Arguments/Parameters

- None. The script does not accept CLI arguments; all input is handled interactively.