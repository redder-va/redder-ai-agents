from typing import Any
import os
import requests
try:
    from google import genai as genai_new
except Exception:
    genai_new = None

def generate_text(llm: Any, prompt: str, model: str = 'gemini-1.5-flash') -> str:
    """Try multiple call patterns for different LLM wrappers and return text.

    Order:
    1. `llm.invoke(prompt)` and use `.content` or `.text` if present
    2. `llm(prompt)` direct call and extract text
    3. Fallback to Google Gemini (free, cloud-based); uses gemini-1.5-flash by default for speed
    """
    # 1. try invoke
    try:
        result = llm.invoke(prompt)
        # handle objects with .content or .text
        if hasattr(result, 'content'):
            return result.content
        if hasattr(result, 'text'):
            return result.text
        return str(result)
    except Exception:
        pass

    # 2. try direct call
    try:
        result = llm(prompt)
        if isinstance(result, str):
            return result
        if hasattr(result, 'content'):
            return result.content
        if hasattr(result, 'text'):
            return result.text
        # langchain-like generate returns object with generations
        try:
            gens = getattr(result, 'generations', None)
            if gens:
                # gens may be List[List[Generation]]
                first = gens[0][0]
                if hasattr(first, 'text'):
                    return first.text
        except Exception:
            pass
        return str(result)
    except Exception:
        pass

    # 3. fallback to Google Gemini (prefer new google.genai client; else REST API)
    google_key = os.environ.get('GOOGLE_API_KEY')
    if google_key:
        mdl = model  # Use provided model (default: gemini-1.5-flash for speed)
        # Try new google.genai client
        if genai_new is not None:
            try:
                client = genai_new.Client(api_key=google_key)
                # Preferred API
                try:
                    resp = client.responses.generate(model=mdl, input=prompt)
                    text = getattr(resp, 'output_text', None)
                    if text:
                        return text
                except Exception as e:
                    print(f"[genai.responses.generate] error: {e}")
                # Fallback API
                try:
                    resp2 = client.models.generate_content(model=mdl, content=prompt)
                    text2 = getattr(resp2, 'output_text', None)
                    if text2:
                        return text2
                except Exception as e:
                    print(f"[genai.models.generate_content] error: {e}")
            except Exception as e:
                print(f"[genai.Client] init error: {e}")
        # REST fallback to Generative Language API
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{mdl}:generateContent?key={google_key}"
            body = {"contents": [{"parts": [{"text": prompt}]}]}
            r = requests.post(url, json=body, timeout=20)
            print(f"[REST Gemini] status={r.status_code}")
            if r.status_code == 200:
                data = r.json()
                try:
                    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                    texts = [p.get("text") for p in parts if isinstance(p, dict) and p.get("text")]
                    if texts:
                        return "\n".join(texts)
                except Exception as e:
                    print(f"[REST Gemini] parse error: {e}")
                # If no parts or unexpected structure, return stringified payload
                return str(data)
            else:
                try:
                    print(f"[REST Gemini] error body: {r.text}")
                except Exception:
                    pass
        except Exception as e:
            print(f"[REST Gemini] request error: {e}")

    # Last resort: simple local response to avoid hard failure
    return f"[LLM unavailable] Based on your request: {prompt[:500]}"
