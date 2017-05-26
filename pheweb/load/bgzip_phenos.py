
from ..utils import get_phenolist
from ..file_utils import get_generated_path, convert_VariantFile_to_IndexedVariantFile
from .load_utils import get_num_procs, star_kwargs, exception_printer

import os
import multiprocessing


@exception_printer
@star_kwargs
def convert(src_filepath, out_filepath):
    print("{} -> {}".format(src_filepath, out_filepath))
    convert_VariantFile_to_IndexedVariantFile(src_filepath, out_filepath)

def get_conversions_to_do():
    phenocodes = [pheno['phenocode'] for pheno in get_phenolist()]
    for phenocode in phenocodes:
        src_filepath = get_generated_path('augmented_pheno', phenocode)
        out_filepath = get_generated_path('augmented_pheno_gz', '{}.gz'.format(phenocode))
        tbi_filepath = out_filepath + '.tbi'
        if not os.path.exists(out_filepath) or not os.path.exists(tbi_filepath) or \
           os.stat(src_filepath).st_mtime > min(os.stat(out_filepath).st_mtime, os.stat(tbi_filepath).st_mtime):
            yield {
                'src_filepath': src_filepath,
                'out_filepath': out_filepath,
            }

def run(argv):
    conversions_to_do = list(get_conversions_to_do())
    print('number of phenos to process:', len(conversions_to_do))
    with multiprocessing.Pool(get_num_procs()) as p:
        p.map(convert, conversions_to_do)
