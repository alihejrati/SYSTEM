from os import system
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
    '--args',
    type=str,
    default=''
)

opt, unknown = parser.parse_known_args()

arglist = opt.args.split(':')

for arg in arglist:
    parser.add_argument(
        f'--{arg}',
        type=str,
        default=''
    )

opt, unknown = parser.parse_known_args()
opt = vars(opt)

for key, value in opt.items():
    K = f'K_ARG_{key}'.upper()
    V = str(value).strip()
    print(f'export {K}="{V}"')
    # system(f'export {K}="{V}"')
