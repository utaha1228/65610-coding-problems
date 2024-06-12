# 6.5610 coding problems

## Pset 1
* Challenge files: `gen.py`, `data.txt`, `ciphertext.txt`, `hint.pdf`. They are compressed to `pset1.zip`.
* Secret file: `secret.txt`
* run `python3 sol.py` to recover the secret text

## Pset 2
* Challenge files: `encrypt.py`. `gen.py` can be public after removing the random seed.
* `sol.py` is the solution file.
* Run `sage recover_secret.sage` to recover the secret `s`, which is a solution to the bonus challenge.
* `pset2/autograder` contains the files for the Piazza auto grader.
  * It is insecure because students can run malicious code in `enc()`.
  * The grader forgot to check that `r` is non-deterministic.

## Pset 3
* Challenge files: `output.txt`. `gen_public.py`. `gen.py` is similar to `gen_public.py` except that it explicitly chooses the random seed.
* Run `sage sol.sage` to recover the secret `s`.

## Pset 4
* Modify `prover.sage` so that it passes the verifier check.
* `run.sh` performs the check by importing prover code to verifier.
