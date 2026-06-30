import os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    in_todo = False
    for line in lines:
        if "# TODO: Implement" in line:
            in_todo = True
            new_lines.append(line)
            if "cohen_kappa(" in "".join(new_lines[-15:]):
                new_lines.append("    from sklearn.metrics import cohen_kappa_score\n")
                new_lines.append("    return cohen_kappa_score(human_labels, judge_labels)\n")
                in_todo = False # We handle it manually
            continue
            
        if in_todo:
            if line.strip().startswith("# "):
                idx = line.find("# ")
                if idx != -1:
                    new_lines.append(line[:idx] + line[idx+2:])
            elif line.strip().startswith("return"):
                in_todo = False
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

for f in ['src/phase_a_ragas.py', 'src/phase_b_judge.py', 'src/phase_c_guard.py']:
    fix_file(f)
