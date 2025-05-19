import os
from generator import generate_dataset
from config import OUTPUT_FILE, NUM_SAMPLES

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df = generate_dataset(NUM_SAMPLES)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Saved {len(df)} examples to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
