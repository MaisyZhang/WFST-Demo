import argparse
import openfst_python as fst


def load_symbols(symfile):
    syms = dict()
    with open(symfile, 'r') as rp:
        for l in rp.readlines():
            items = l.strip().split(' ')
            syms[items[0]] = int(items[1])
        return syms


def make_fst(word_sym, phone_sym, pydict_file):
    with open(pydict_file, 'r') as rp:
        f = fst.Fst()
        start = f.add_state()
        end = f.add_state()
        f.set_start(start)
        f.add_arc(start, fst.Arc(phone_sym['<eps>'], word_sym['<s>'], fst.Weight(f.weight_type(), 0.0), start))  # 自转
        f.add_arc(end, fst.Arc(phone_sym['<eps>'], word_sym['</s>'], fst.Weight(f.weight_type(), 0.0), end))  # 自转
        f.add_arc(end, fst.Arc(phone_sym['<eps>'], word_sym['<eps>'], fst.Weight(f.weight_type(), 0.0), start))  # 1 --> 0
        f.set_final(end, fst.Weight(f.weight_type(), 0.0))
        for l in rp.readlines():
            items = l.strip().split(' ')
            prev_state = start
            ilabel = phone_sym['<eps>']
            olabel = word_sym['<eps>']
            for i in range(len(items[0])):
                n = f.add_state()
                pych = items[0][i]
                chch = items[1]
                ilabel = phone_sym[pych]
                if (i == 0):
                    olabel = word_sym[chch]
                else:
                    olabel = word_sym['<eps>']
                f.add_arc(prev_state, fst.Arc(ilabel, olabel, fst.Weight(f.weight_type(), 0.0), n))
                prev_state = n
            # connect the last state with end node
            f.add_arc(prev_state, fst.Arc(phone_sym['<eps>'], olabel, fst.Weight(f.weight_type(), 0.0), end))
        return f


def main():
    parser=argparse.ArgumentParser("")
    parser.add_argument("--lexicon", type=str)
    parser.add_argument("--word", type=str)
    parser.add_argument("--phone", type=str)
    parser.add_argument("--G", type=str)
    parser.add_argument("--L", type=str)
    parser.add_argument("--LG", type=str)
    args = parser.parse_args()

    word_sym = load_symbols(args.word)
    phone_sym = load_symbols(args.phone)

    l = make_fst(word_sym, phone_sym, args.lexicon)
    l.write(args.L)
    g = fst.Fst.read(args.G)
    lg = fst.compose(l, g)
    lg.write(args.LG)

if __name__ == "__main__":
    main()