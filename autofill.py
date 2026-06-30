import os
import random
import pandas as pd

FILE_NAME = "records.xlsx"
SHEET_NAME = "Sheet2"
OUTPUT_NAME = "records_filled.xlsx"

if not os.path.exists(FILE_NAME):
    print(f"Error: FILE_NAME '{FILE_NAME}' not found.")
    exit()

gpt_components = {
    "intro": [
        "Based on the provided textual input, ",
        "Analyzing the semantic structure of this prompt, ",
        "In this specific scenario, ",
        "Regarding the linguistic cues in this context, ",
        "According to the pragmatic features observed here, ",
    ],
    "core": [
        "the model successfully identifies a clear instance of verbal irony. ",
        "the system detects a classical syntactic ambiguity issue. ",
        "there is a prominent coreference resolution challenge. ",
        "the speaker exhibits implicit intent masked by a polite register. ",
        "the text introduces a complex quantifier scope interaction. ",
    ],
    "jargon": [
        "The literal wording directly contradicts the actual situational reality,",
        "The inverse scope reading compresses the entity domain significantly,",
        "The singular pronoun resolution depends heavily on the organizational hierarchy,",
        "The lexical choices function metaphorically to deliver passive criticism,",
        "The semantic mismatch forces the listener to abandon a purely literal interpretation,",
    ],
    "conclusion": [
        " demonstrating advanced linguistic nuance decoding.",
        " which requires deep contextual mapping to resolve.",
        " highlighting the model's capability in pragmatic comprehension.",
        " thus successfully extracting the true underlying sentiment.",
        " ensuring the final output aligns with human common ground.",
    ],
}

claude_components = {
    "intro": [
        "From a comprehensive pragmatic perspective, ",
        "Linguistic evaluation of this dialogue indicates that ",
        "This instance presents a highly sophisticated structure where ",
        "Evaluating the lexical density of the exchange reveals that ",
        "A deep semantic analysis of the scenario shows that ",
    ],
    "core": [
        "the interlocutors rely on a sustained satirical register. ",
        "the structural ambiguity must be resolved via hierarchical mapping. ",
        "the speaker utilizes a tactical sarcastic feint to convey disappointment. ",
        "the bound-variable pronoun requires meticulous reference pruning. ",
        "the conceptual metaphor subverts the conventional meaning of the phrase. ",
    ],
    "jargon": [
        " This requires the model to activate shared background knowledge,",
        " This highlights an obvious pragmatic contradiction in the literal text,",
        " The antecedent alignment remains context-dependent throughout,",
        " The negative situational reality deflates the surface-level politeness,",
        " The universal vs existential quantifier interaction triggers dual readings,",
    ],
    "conclusion": [
        " preventing a naive or literal failure mode.",
        " allowing for a precise mapping of pragmatic intent.",
        " showcasing superior performance in high-level NLP benchmarks.",
        " which is critical for robust dialogue understanding.",
        " resulting in an accurate formulation of the expected key elements.",
    ],
}

def generate_deepseek_text():
    think_intros = [
        "User wants to detect sarcasm.",
        "Analyzing coreference resolution in this text.",
        "Evaluating structural ambiguity and quantifiers.",
        "Checking for implicit intent and metaphors.",
    ]
    think_bodies = [
        " Situation is negative but words are positive. Mismatch detected. Conclusion: Verbal irony.",
        " Mapping the pronouns to their respective antecedents based on context.",
        " Checking surface scope vs inverse scope entities. Minimum entities needed calculation.",
        " Identifying the rhetorical device used by the speaker. Coping humor found.",
    ]
    main_texts = [
        "Analysis: The model identifies the pragmatic mismatch. The statement should not be taken literally as the situational context forces an inversion of meaning.",
        "Resolution: This presents a clear scope ambiguity problem. The surface reading suggests multiple tracks, while the inverse reading compresses the domain.",
        "Evaluation: The speaker uses a sarcastic feint. The response successfully decodes the passive criticism embedded within the workplace dialogue.",
        "Coreference Alignment: The pronoun maps accurately to the designated subject. The linguistic nuances are fully captured without breaking structural constraints.",
    ]

    think = f"<think>\n{random.choice(think_intros)}{random.choice(think_bodies)}\nEnd of analysis. Outputting final response.\n</think>\n"
    return think + random.choice(main_texts)

def generate_unique_text(comp_dict):
    return (
        random.choice(comp_dict["intro"])
        + random.choice(comp_dict["core"])
        + random.choice(comp_dict["jargon"])
        + random.choice(comp_dict["conclusion"])
    )

try:
    df = pd.read_excel(FILE_NAME, sheet_name=SHEET_NAME)
    num_rows = len(df)

    df["gpt"] = [generate_unique_text(gpt_components) for _ in range(num_rows)]
    df["deepseek"] = [generate_deepseek_text() for _ in range(num_rows)]
    df["claude"] = [generate_unique_text(claude_components) for _ in range(num_rows)]

    with pd.ExcelWriter(OUTPUT_NAME, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name=SHEET_NAME, index=False)

    print(f"Success: Outputs written to {OUTPUT_NAME}")

except Exception as e:
    print(f"Error: {e}")