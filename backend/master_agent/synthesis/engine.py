import json
import uuid

from backend.common.llm.inference import llm_structured
from backend.common.schemas.canonical_result import CanonicalResult, SynthesisOutput
from backend.common.schemas.worker_outputs import ClinicalTrialsOutputs, MarketIntelligenceOutputs

def run_synthesis(
        job_id: uuid.UUID,
        molecule: str,
        ct_outputs: ClinicalTrialsOutputs,
        market_outputs: MarketIntelligenceOutputs
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

You are also given the market and competitor intelligence data:
{market_outputs.model_dump_json(indent=2)}

Your output MUST strictly follow the SynthesisOutput schema.
Do NOT output the raw trials list. Just the analysis.

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

6. **Assess Risks**:
   - Provide a detailed Risk Assessment paragraph

7. **Provide an overall confidence score** (0 to 1) reflecting:
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
Return exactly ONE dictionary matching the SynthesisOutput schema.
No markdown. No text. No code fences.

Begin.
"""
    
    # 1. Get Analysis from LLM
    analysis: SynthesisOutput = llm_structured(
        prompt=prompt,
        schema=SynthesisOutput,
        job_id=job_id,
        stage="synthesis"
    )

    # 2. Construct Full Canonical Result (Data + Analysis)
    canonical_result = CanonicalResult(
        molecule=molecule,
        trial_summary=analysis.trial_summary,
        trials=ct_outputs.trials, # Pass through raw data without LLM touch
        key_findings=analysis.key_findings,
        suggested_follow_up=analysis.suggested_follow_up,
        data_completeness_score=analysis.data_completeness_score,
        confidence_overall=analysis.confidence_overall,
        swot_analysis=analysis.swot_analysis,
        risk_assessment=analysis.risk_assessment,
        market_data=market_outputs.model_dump()
    )

    return canonical_result