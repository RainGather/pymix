import fire
from hashlib import sha1
from pathlib import Path

def mix(f, protect_lines, mix_lines, vname, chr_fn_prefix='c', ord_fn_prefix='o'):
    protect_code = f'''
# ====================
from hashlib import sha1
from pathlib import Path
with Path(__file__).open('r', encoding=\'utf-8\') as fr:
    c = fr.read().split('\\n')
{vname} = ''.join([sha1(l.encode('utf-8')).hexdigest()[:5] for l in c])

for i in range(10):
    exec(\'{chr_fn_prefix}\' + str(i) + \'=chr\')
    exec(\'{ord_fn_prefix}\' + str(i) + \'=ord\')
for i in range(97, 105):
    exec(\'{chr_fn_prefix}\' + chr(i) + \'=chr\')
    exec(\'{ord_fn_prefix}\' + chr(i) + \'=ord\')
# ====================
'''
    if not isinstance(f, Path):
        f = Path(f)
    with f.open('r', encoding='utf-8') as fr:
        code = fr.read().split('\n')
    if not isinstance(protect_lines, list):
        protect_lines = list(range(1, int(protect_lines + 1)))
    protect_lines = [int(l) - 1 for l in protect_lines]
    mix_lines = [int(l) - 1 for l in mix_lines]
    hashstr = ''.join([sha1(line.encode('utf-8')).hexdigest()[:5] for line in code])
    i = 0
    li = 0
    for lineno in mix_lines:
        line = code[lineno]
        space_count = 0
        for c in line:
            if c == ' ':
                space_count += 1
            else:
                break
        mixline = ' ' * space_count + 'exec(f\''
        for c in line.strip():
            mix_c = f'{chr_fn_prefix}{hashstr[i]}({ord_fn_prefix}{hashstr[i]}({vname}[{i}]) + {ord(c) - ord(hashstr[i])})'
            # mix_c = f'chr(ord(\"{hashstr[i]}\") + {ord(c) - ord(hashstr[i])})'
            mix_c = '{' + mix_c + '}'
            mixline += mix_c
            i += 1
            if i % 5 == 0:
                li += 1
                if li >= len(protect_lines):
                    li -= len(protect_lines)
                i = protect_lines[li]
        mixline += '\')'
        code[lineno] = mixline
    code = code[:max(protect_lines) + 1] + protect_code.split('\n') + code[max(protect_lines) + 1:]
    with f.with_name(f.stem + '_mixed' + f.suffix).open('w', encoding='utf-8') as fw:
        fw.write('\n'.join(code))
    print(hashstr)

if __name__ == '__main__':
    # mix('npdraw.py', [2, 3, 4, 5, 6], [86, 88], 'v')
    fire.Fire()
