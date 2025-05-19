import os
import time
import pandas as pd
from tqdm import tqdm
import wandb

from openai import OpenAI
from src.prompt_variants import PROMPT_VARIANTS
from src.config import OPENAI_API_KEY, MODEL_NAME
from src.eval import evaluate_response

client = OpenAI(api_key=OPENAI_API_KEY)

def run_experiment(input_csv, output_dir, max_samples=100):
    df = pd.read_csv(input_csv).sample(n=max_samples, random_state=42)

    for variant_name, prompt_template in PROMPT_VARIANTS.items():
        print(f"\n🚀 Running Prompt Variant: {variant_name}")
        wandb.init(project="chatbot-prompt-eval", name=variant_name, config={"prompt": prompt_template}, reinit=True)

        results = []

        for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Evaluating {variant_name}"):
            prompt = prompt_template.format(customer_query=row['customer_query'])

            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=300
                )
                bot_response = response.choices[0].message.content.strip()
                scores = evaluate_response(row['customer_query'], bot_response)
                
                record = {
                    "variant": variant_name,
                    "customer_query": row['customer_query'],
                    "prompt_used": prompt,
                    "bot_response": bot_response,
                    **scores
                }

                wandb.log(scores)
                results.append(record)
                time.sleep(1)
            except Exception as e:
                print(f"❌ Failed on {variant_name}: {e}")

        # Save variant results
        variant_df = pd.DataFrame(results)
        variant_df.to_csv(os.path.join(output_dir, f"{variant_name}_results.csv"), index=False)

        wandb.finish()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input CSV with 'customer_query'")
    parser.add_argument("--output_dir", required=True, help="Folder to store evaluation CSVs")
    parser.add_argument("--samples", type=int, default=100, help="Samples to evaluate per variant")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    run_experiment(args.input, args.output_dir, args.samples)
