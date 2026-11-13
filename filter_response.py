import argparse
import math


def low_pass(frequency, cutoff):
    return 1 / math.sqrt(1 + (frequency / cutoff) ** 4)


def high_pass(frequency, cutoff):
    return 0 if frequency == 0 else low_pass(cutoff, frequency)


def bands(frequency, low_cutoff=300, high_cutoff=3000):
    if not all(map(math.isfinite, (frequency, low_cutoff, high_cutoff))):
        raise ValueError("frequencies must be finite")
    if frequency < 0 or not 0 < low_cutoff < high_cutoff:
        raise ValueError("expected a nonnegative frequency and ordered positive cutoffs")
    return (
        low_pass(frequency, low_cutoff),
        high_pass(frequency, low_cutoff) * low_pass(frequency, high_cutoff),
        high_pass(frequency, high_cutoff),
    )


def decibels(gain):
    return 20 * math.log10(gain) if gain > 0 else -math.inf


def check():
    assert math.isclose(low_pass(300, 300), 1 / math.sqrt(2))
    assert math.isclose(high_pass(300, 300), 1 / math.sqrt(2))
    assert bands(0) == (1, 0, 0)
    for band, frequency in enumerate((80, 1000, 8000)):
        gains = bands(frequency)
        assert gains[band] == max(gains)
    print("Filter-response checks passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the response of three audio filter paths.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("frequencies", type=float, nargs="*", default=[80, 1000, 8000])
    args = parser.parse_args()
    if args.check:
        check()
    else:
        print(f"{'Hz':>10} {'Bass dB':>10} {'Mid dB':>10} {'Treble dB':>10}")
        for frequency in args.frequencies:
            print(f"{frequency:10.1f}" + "".join(f"{decibels(gain):10.2f}" for gain in bands(frequency)))
