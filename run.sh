#!/bin/bash


. ./path.sh

set -e

stage=0


if [ $stage -le 0 ]; then
    # 训练1元N-gram语言模型，构建G.fst
    lmplz -o 1 --verbose_header --text text.txt --arpa text.arpa
    arpa2fst text.arpa G.fst
fi

if [ $stage -le 1 ]; then
#    构建L.fst, # 复合LG.fst
#    fstcompile --isymbols=phones.txt --osymbols=words.txt L.txt L.fst
#    fstcompose L.fst G.fst LG.fst
    mkfst.py --lexicon=lexicon.txt --word=words.txt --phone=phones.txt --G=G.fst --L=L.fst --LG=LG.fst
fi

if [ $stage -le 2 ]; then
#    测试解码
#    fstcomplie --isymbols=phones.txt --osymbols=phones.txt input.txt input.fst
#    fstcompose input.fst LG.fst result.fst
#    fstproject --project_output=true result.fst result.fsa
#    fstshortestpath --nshortest=1 --unique=true result.fsa short_result.fst
    decode.py --input='shenlanyuyinkecheng' --LG=LG.fst --word=words.txt --phone=phones.txt
    fstprint --isymbols=words.txt --osymbols=words.txt short_result.fst > short_result.txt
fi