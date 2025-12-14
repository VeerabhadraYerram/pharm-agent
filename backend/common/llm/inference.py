import json
import os
import re
import uuid
import uuid6
from typing import Type, TypeVar

from groq import Groq
from pydantic import BaseModel, ValidationError

from backend.database import SessionLocal
from backend.master_agent.models.llm_call import LLMCall

class LLMResponseFormatError(Exception): pass
class LLMServiceError(Exception): pass


client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# generic type for schema
T = TypeVar("T", bound=BaseModel)

def _extract_json_block(text: str) -> str:
    # extract json from code blocks / raw test
    # 1. direct parse
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass

    # obj regex
    obj_match = re.search(r"\{[\s\S]*\}", text)
    if obj_match:
        candidate = obj_match.group(0)
        try:
            json.loads(candidate)
            return candidate
        except Exception:
            pass

    # arr regex
    arr_match = re.search(r"\[[\s\S]*\]", text)
    if arr_match:
        candidate = arr_match.group(0)
        try:
            json.loads(candidate)
            return candidate
        except Exception:
            pass

    raise LLMResponseFormatError(f"Could not extract JSON from LLM output. Partial Output: {text[:200]}...")

def _log_llm_call(
        db,
        *,
        job_id: uuid.UUID,
        stage: str,
        model: str,
        prompt: str,
        response: str,
        prompt_tokens: int,
        completion_tokens: int
):
    call = LLMCall(
        id = uuid6.uuid7(),
        job_id = job_id,
        stage = stage,
        model = model,
        prompt = prompt,
        response = response,
        prompt_tokens = prompt_tokens,
        response_tokens = completion_tokens
    )

    db.add(call)
    db.commit()

def llm_structured(
        *,
        prompt: str,
        schema: Type[T],
        job_id: uuid.UUID,
        stage: str,
        max_retries: int = 3,
) -> T:
    # structured llm caller
    # inject schema definition, enforce json, log history, handle retries.

    db = SessionLocal()

    schema_json = json.dumps(schema.model_json_schema(), indent=2)
    instructions = (
        "You are a strict JSON generator.\n"
        "Return ONLY valid JSON (json) with NO text before or after.\n"
        "Your JSON MUST follow this schema:\n"
        f"{schema_json}\n"
        "If you cannot satisfy the schema, return an empty JSON object {}."
    )
    input_text = f"Task:\n{prompt}\nReturn ONLY JSON."

    try:        
        for attempt in range(max_retries):
            try:
                # api call
                resp = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": instructions},
                        {"role": "user", "content": input_text}
                    ],
                    temperature=0,
                    response_format={"type": "json_object"}
                )

                raw_text = resp.choices[0].message.content

                # extract json
                json_text = _extract_json_block(raw_text)
                parsed = json.loads(json_text)

                # validate
                validated = schema.model_validate(parsed)

                usage = resp.usage
                prompt_tokens = usage.prompt_tokens if usage else 0
                completion_tokens = usage.completion_tokens if usage else 0

                # log success
                _log_llm_call(
                    db,
                    job_id=job_id,
                    stage=stage,
                    model=MODEL_NAME,
                    prompt=input_text,
                    response=json_text,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens
                )

                return validated
                       
            except (ValidationError, json.JSONDecodeError, LLMResponseFormatError) as e:
                print(f"[LLM] JSON validation failed ({attempt+1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise LLMResponseFormatError(f"Failed to get valid JSON: {e}")

            except Exception as e:
                # Actual API/network problems
                print(f"[LLM] API Error ({attempt+1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise LLMServiceError(f"GROQ API failed: {e}")
                
    finally:
        db.close()