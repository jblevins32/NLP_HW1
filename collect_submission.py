# Credits: https://github.com/fastai/course-v3/tree/master/nbs/dl2͏︆͏󠄃͏󠄌͏󠄍͏︅͏︀͏︋͏︋͏󠄅͏︈͏︍

import os
import sys
import re
import json


def is_export(cell):
    if cell['cell_type'] != 'code': return False
    src = cell['source']
    if len(src) == 0 or len(src[0]) < 7: return False
    return re.match(r'^\s*#\s*export\s*$', src[0], re.IGNORECASE) is not None


def removeTestLines(cellText):
    matchList = [re.search("^\s*tests", cell) for cell in cellText]  # If any spaces are in front
    linesToRemoveIdx = [matchList.index(i) for i in matchList if i is not None]
    linesToRem = [cellText[i] for i in linesToRemoveIdx]
    for i in linesToRem:
        cellText.remove(i)
    return cellText


def notebook2scriptSingle(fname, destination):
    "Finds cells starting with `#export` and puts them into a new module"
    fname_out = 'submission.py'
    main_dic = json.load(open(fname, 'r', encoding="utf-8"))
    code_cells = [c for c in main_dic['cells'] if is_export(c)]

    module = f'''
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###͏︆͏󠄃͏󠄌͏󠄍͏︅͏︀͏︋͏︋͏󠄅͏︈͏︍
#################################################
# file to edit: {fname}͏︆͏󠄃͏󠄌͏󠄍͏︅͏︀͏︋͏︋͏󠄅͏︈͏︍

'''
    # module += "from utils import plot_gradient_descent\n"
    for cell in code_cells:
        text = removeTestLines(cell['source'])
        module += ''.join(text[1:]) + '\n\n'

    # remove trailing spaces͏︆͏󠄃͏󠄌͏󠄍͏︅͏︀͏︋͏︋͏󠄅͏︈͏︍
    module = re.sub(r' +$', '', module, flags=re.MULTILINE)
    output_path = os.path.join(destination, fname_out)
    open(output_path, 'w', encoding='utf-8').write(module[:-2])
    print(f"Converted {fname} to {output_path}")
    # copy individual files of model_weights directory to submission folder
    os.system(f"cp -r model_weights/* {destination}")
    


LATE_POLICY = \
    """Late Policy:

      \"I have read the late policy for CS 4650/7650.\"
    """

HONOR_PLEDGE = \
    """Honor Pledge:

      \"I have read the Collaboration and Academic Honesty policy for CS 4650/7650.
      I certify that I have or will use outside references only in accordance with
      this policy, that I have or will cite any such references via code comments,
      and that I have not or will not copy any portion of my submission from another
      past or current student.\"\n
    """


def require_pledges():
    print(LATE_POLICY)
    ans = input("Please type 'yes' to agree and continue>")
    assert ans.lower() == "yes", "Late policy not accepted"
    print("\n")

    print(HONOR_PLEDGE)
    ans = input("Please type 'yes' to agree and continue>")
    assert ans.lower() == "yes", "Honor pledge not accepted"
    print("\n")


if __name__ == '__main__':
    require_pledges()
    folder_location = 'submission'
    os.makedirs(folder_location, exist_ok=True)
    notebook2scriptSingle('CS4650_7650_hw1_release_su2025.ipynb', folder_location)
