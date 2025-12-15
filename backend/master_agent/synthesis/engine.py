import json
import uuid

from backend.common.llm.inference import llm_structured
from backend.common.schemas.canonical_result import CanonicalResult
from backend.common.schemas.worker_outputs import ClinicalTrialsOutputs

def run_synthesis(
        job_id: uuid.UUID,
        molecule: str,
        ct_outputs: ClinicalTrialsOutputs
) -> CanonicalResult:
    # take raw clinical trial output, produce structured CanonicalResult

    trials_json = json.dumps([t.model_dump() for t in ct_outputs.trials], indent=2)

    prompt = f"""
You are a biomedical evidence synthesis engine with expertise in clinical trial
interpretation, drug development, and risk/benefit evaluation.

Your job is to analyze and synthesize clinical trial evidence for the molecule:

    Molecule: {molecule}

You are given the normalized clinical trial dataset (JSON list):
{trials_json}

Your output MUST strictly follow the CanonicalResult schema.

-------------------------
TASKS YOU MUST COMPLETE:
-------------------------

1. **Summarize the overall trial landscape**, including:
   - trial phases represented
   - statuses (Completed, Recruiting, Terminated, Withdrawn)
   - conditions and therapeutic focus areas
   - geographical distribution
   - sponsor patterns

2. **Extract evidence-based key findings**, such as:
   - efficacy signals
   - safety observations
   - patterns across trials
   - contradictory or inconclusive evidence

3. **Identify trends or anomalies**, e.g.:
   - early stoppage or terminations
   - missing results
   - unusual phase transitions
   - clustering in certain regions or conditions

4. **Assess data completeness**, considering:
   - missing fields
   - incomplete results
   - trial dropouts
   - limited sample size

   Output a score between **0 and 1** for `data_completeness_score`.

5. **Suggest follow-up research actions**, such as:
   - recommended next-phase trials
   - populations that need more data
   - endpoints requiring deeper investigation

6. **Provide an overall confidence score** (0 to 1) reflecting:
   - quality of evidence
   - consistency across trials
   - robustness of results

--------------------------------------------
RULES FOR THE OUTPUT:
--------------------------------------------

Return ONLY ONE JSON OBJECT.
Do NOT wrap the result in a list or array.
Do NOT return an array.
Do NOT return multiple objects.
Return exactly ONE dictionary matching the CanonicalResult schema.
No markdown. No text. No code fences.

Begin.
"""
    
    canonical_result = llm_structured(
        prompt=prompt,
        schema=CanonicalResult,
        job_id=job_id,
        stage="synthesis"
    )

    return canonical_result