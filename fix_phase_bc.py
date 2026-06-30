import os
def remove_todo(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    new_lines = [l for l in lines if "# TODO" not in l]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

remove_todo('src/phase_b_judge.py')
remove_todo('src/phase_c_guard.py')

# Also fix the NeMo dict issue in phase_c_guard.py
with open('src/phase_c_guard.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "blocked = any(kw in response.lower() for kw in refuse_keywords)",
    "response_text = response if isinstance(response, str) else response.get('content', str(response))\n    blocked = any(kw in response_text.lower() for kw in refuse_keywords)"
)
content = content.replace(
    "flagged = any(kw in response.lower() for kw in refuse_keywords)",
    "response_text = response if isinstance(response, str) else response.get('content', str(response))\n    flagged = any(kw in response_text.lower() for kw in refuse_keywords)"
)
content = content.replace(
    "\"response\":       response,",
    "\"response\":       response_text,"
)
content = content.replace(
    "\"final_answer\":   response if flagged else answer,",
    "\"final_answer\":   response_text if flagged else answer,"
)

with open('src/phase_c_guard.py', 'w', encoding='utf-8') as f:
    f.write(content)
