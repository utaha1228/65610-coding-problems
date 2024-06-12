#!/usr/bin/env bash

sage --preparse prover.sage
mv prover.sage.py prover.py
sage verifier.sage
