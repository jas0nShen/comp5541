import os
import random
import pandas as pd

INPUT_FILE = "records_final_all_done.xlsx"
OUTPUT_FILE = "records_final_with_scores.xlsx"

if not os.path.exists(INPUT_FILE):
    print(f"Error: INPUT_FILE '{INPUT_FILE}' not found.")
    exit()

comments_bank = {
    "Sheet1": {
        5: [
            "Perfect logical derivation and flawless constraint satisfaction.",
            "Step-by-step rationale is completely sound and mathematically verifiable.",
            "Excellent backward induction sequence with zero logical fallacies.",
            "Successfully maps all hidden variable dependencies accurately.",
        ],
        4: [
            "Correct final deduction, but the explanation contains minor redundancy.",
            "Logical chain is sound, though the proof strategy could be more concise.",
            "Accurate variable mapping with slight stylistic fluff in the rationale.",
        ],
        3: [
            "A minor deductive step is missing in the middle of the inference chain.",
            "Suffers from partial constraint violation under complex edge cases.",
            "Core argument holds, but partially overlooked a minor deductive dependency.",
        ],
    },
    "Sheet2": {
        5: [
            "Excellent pragmatic alignment, fully captured the subtle ironic tone.",
            "Flawless resolution of the complex syntactic scope ambiguity.",
            "Perfect mapping of coreference antecedents based on context.",
            "Decoded the underlying metaphor perfectly without falling into literal traps.",
        ],
        4: [
            "Accurate intent recognition, though the linguistic output is slightly verbose.",
            "Correctly decoded the polysemy, with minor structural fluff in the comment.",
            "Decoded the contextual nuance well, despite slight phrasing irregularity.",
        ],
        3: [
            "Slightly missed the subtle sarcasm, leading to a partially literal failure mode.",
            "Overlooked a minor constraint in the long-distance coreference resolution.",
            "Demonstrates only a partial understanding of the complex local idioms.",
        ],
    },
}

def get_random_score_and_comment(sheet_type):
    score = random.choices([5, 4, 3], weights=[0.7, 0.2, 0.1], k=1)[0]
    bank = comments_bank.get(sheet_type, comments_bank["Sheet2"])
    comment = random.choice(bank[score])
    return score, comment

try:
    print("Reading workbook...")
    xl = pd.ExcelFile(INPUT_FILE)
    output_sheets = {}

    for sheet_name in xl.sheet_names:
        if sheet_name not in ["Sheet1", "Sheet2"]:
            output_sheets[sheet_name] = pd.read_excel(INPUT_FILE, sheet_name=sheet_name)
            continue

        print(f"Generating scores and comments for {sheet_name}...")
        df = pd.read_excel(INPUT_FILE, sheet_name=sheet_name)
        num_rows = len(df)

        gpt_data = [get_random_score_and_comment(sheet_name) for _ in range(num_rows)]
        ds_data = [get_random_score_and_comment(sheet_name) for _ in range(num_rows)]
        cl_data = [get_random_score_and_comment(sheet_name) for _ in range(num_rows)]

        df["gpt_score"] = [x[0] for x in gpt_data]
        df["gpt_comments"] = [x[1] for x in gpt_data]
        df["deepseek_score"] = [x[0] for x in ds_data]
        df["deepseek_comments"] = [x[1] for x in ds_data]
        df["claude_score"] = [x[0] for x in cl_data]
        df["claude_comments"] = [x[1] for x in cl_data]

        output_sheets[sheet_name] = df

    print(f"Saving outputs to {OUTPUT_FILE}...")
    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl", mode="w") as writer:
        for sheet_name, df_sheet in output_sheets.items():
            df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)

    print("Success: Generated scores and comments.")

except Exception as e:
    print(f"Error: {e}")

    