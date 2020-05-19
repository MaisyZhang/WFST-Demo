import argparse
import openfst_python as fst


def load_symbols(symfile):
    syms = dict()
    labels = []
    with open(symfile, 'r') as rp:
        for l in rp.readlines():
            items = l.strip().split(' ')
            syms[items[0]] = int(items[1])
            labels.append(items[0])
        return syms, labels


def make_input_fst(query, pysym):
    f = fst.Fst()
    start = f.add_state()
    end = f.add_state()
    f.set_start(start)
    f.set_final(end, fst.Weight(f.weight_type(), 0.0))
    prev_state = start
    for ch in query:
        n = f.add_state()
        label = pysym[ch]
        f.add_arc(prev_state, fst.Arc(label, label, fst.Weight(f.weight_type(), 0.0), n))
        prev_state = n
    f.add_arc(prev_state, fst.Arc(pysym['<eps>'], pysym['<eps>'], fst.Weight(f.weight_type(), 0.0), end))
    f.write('input.fst')
    return f


def load_LG_fst(model_path):
    LG = fst.Fst.read(model_path)
    return LG


def decode(input_fst, model):
    res = fst.compose(input_fst, model)
    res = fst.shortestpath(res)
    return res


def get_result(resfst, word_labels):
    res = ""
    if resfst.num_states() <= 0:
        return res

    s = resfst.start()
    while (resfst.num_arcs(s) != 0):
        arc = resfst.arcs(s).value()
        if (arc.olabel != 0):
            res += word_labels[arc.olabel]
            res += " "
        s = arc.nextstate
    return res


def decode_one_query(model, input, word_sym, word_labels):
    f = make_input_fst(input, word_sym)
    res = decode(f, model)
    res.write('short_result.fst')
    output = get_result(res, word_labels)
    print(output)


def main():
    parser=argparse.ArgumentParser("")
    parser.add_argument("--input", type=str)
    parser.add_argument("--LG", type=str)
    parser.add_argument("--word", type=str)
    parser.add_argument("--phone", type=str)
    args = parser.parse_args()

    word_sym, word_labels = load_symbols(args.word)
    phone_sym, _ = load_symbols(args.phone)

    LG = load_LG_fst(args.LG)
    decode_one_query(LG, args.input, word_sym, word_labels)


if __name__ == "__main__":
    main()